import requests

# When using HTTPS with insecure servers this has to be uncommented
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import asyncio
import aiofiles
import aiohttp


import websockets
import nclib


import os

from time import sleep
from uuid import uuid4
import subprocess as sp
import shlex
import psutil
from threading import Thread
from copy import deepcopy
from src.agents.base.base_talking_agent import APiTalkingAgent
from src.utils.errors import (
    APiCommunicationError,
    APiAgentDefinitionError,
    APiCallbackException,
)
from src.utils.constants import (
    NIE,
    http_re,
    ws_re,
    file_re,
    time_re,
    size_re,
    delimiter_re,
    regex_re,
    netcat_re,
)
from src.utils.logger import setup_logger

logger = setup_logger("agent")


class APiBaseWrapperAgent(APiTalkingAgent):
    """
    Base wrapper agent implementing all input/output mappings (e.g. STDIN/STDOUT/STDERR,
    file, HTTP, WebSocket, Netcat). Not to be instanced by itself, but should be
    used for inheritance.

    The wrapper agent objective is to provide various communication interfaces
    to the underlying agent.
    """

    def __init__(self, name, password, token):
        global logger
        logger = setup_logger("agent " + name)

        super().__init__(name, password, token)
        self.output_channel_servers = {}
        self.input_channel_servers = {}

    # TODO: Sort methods / coroutines by type and write documentation
    async def read_stdout(self, stdout):
        """
        Coroutine reading STDOUT and calling callback method.
        stdout - STDOUT file handle
        """
        # while True and self.input_ended == False: # might need to verify if this is helpful or not
        while True:
            buf = await stdout.readline()
            if not buf:
                break

            if self.output_type == "STDOUT" and buf:
                await self.output_callback(buf.decode())
        await self.output_callback(
            self.output_delimiter
        )  # TODO: End of output? Verify this

    async def read_stderr(self, stderr):
        """
        Coroutine reading STDERR and calling callback method.
        stderr - STDERR file handle
        """
        # while True and self.input_ended == False: # might need to verify if this is helpful or not
        while True:
            buf = await stderr.readline()

            if not buf:
                break

            if self.output_type == "STDERR":
                await self.output_callback(buf.decode())

    async def read_file(self, file_path):
        """
        Coroutine reading file and calling callback method.
        file_path - file path to be read from
        """
        while not self.all_setup():
            await asyncio.sleep(0.1)
        file_empty = True
        # while file_empty and self.input_ended == False: # might need to verify if this is helpful or not
        while file_empty:
            async with aiofiles.open(file_path, mode="r") as f:
                async for line in f:
                    await self.output_callback(line)
                    file_empty = False
            await asyncio.sleep(0.1)

    async def read_url(self, url):
        """
        Coroutine reading URL and calling callback method.
        url - URL to be read from
        """
        not_available = True
        # while not_available and self.input_ended == False: # might need to verify if this is helpful or not
        while not_available:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        result = await resp.text()
                        if self.output_delimiter:
                            res = [i for i in result.split(self.output_delimiter) if i]
                        else:
                            res = [result]
                        for r in res:
                            await self.output_callback(r)
                not_available = False
            except Exception as e:
                logger.error(f"Error reading url: {e}")
                await asyncio.sleep(0.2)

    async def read_ws(self, url):
        """
        Coroutine reading WebSocket and calling callback method.
        url - WS URL to be read from
        """
        error = True
        not_timeout = True
        # while error and self.input_ended == False: # might need to verify if this is helpful or not
        while error:
            try:
                async with websockets.connect(url) as websocket:
                    not_timeout = True
                    while not_timeout:
                        try:
                            resp = await asyncio.wait_for(websocket.recv(), timeout=0.1)
                            logger.debug(f"Just read: {resp}")
                            if self.output_delimiter:
                                res = [
                                    i for i in resp.split(self.output_delimiter) if i
                                ]
                            else:
                                res = [resp]
                            for r in res:
                                await self.output_callback(r)
                        except asyncio.TimeoutError:
                            not_timeout = False
                    error = False
            except Exception as e:
                try:
                    assert e.errno == 111
                except Exception as e:
                    logger.error(f"Error reading ws: {e}")
                    error = False

                await asyncio.sleep(0.2)

    async def read_nc(self, host, port, udp=False):
        """
        Method reading from NETCAT socket and calling callback method.
        host - host
        port - port
        udp=False - should NETCAT use UDP (if false, default is TCP)
        """
        not_available = True
        # while not_available and self.input_ended == False: # might need to verify if this is helpful or not
        while not_available:
            try:
                ncclient = nclib.Netcat((host, port), udp=udp, raise_eof=True)
                not_available = False
            except Exception as e:
                logger.error(f"Error creating nc client: {e}")
                sleep(0.2)

        error = False
        while not error:
            try:
                result = ncclient.recv_until(self.output_delimiter, timeout=0.2)
                sleep(0.5)
                if result:
                    result = result.decode()
                    if self.output_delimiter:
                        res = [i for i in result.split(self.output_delimiter) if i]
                    else:
                        res = [result]
                    for r in res:
                        await self.output_callback(r)
                elif self.input_ended:
                    raise Exception("Done")
            except Exception as e:
                logger.error(f"Error reading nc: {e}")
                error = True

    async def write_stdin(self, stdin):
        """
        Coroutine writing to STDIN
        stdin - STDIN file handle
        """
        send = True
        # while send and self.input_ended == False: # might need to verify if this is helpful or not
        while send:
            if not self.BUFFER:
                await asyncio.sleep(0.1)
            else:
                i = self.BUFFER.pop(0)
                if i == self.input_end:
                    send = False
                else:
                    buf = f"{i}\n".encode()

                    try:
                        stdin.write(buf)
                        await stdin.drain()
                        await asyncio.sleep(0.1)
                    except ConnectionResetError as e:
                        logger.error(f"Error writing stdin: {e}")
                        self.service_quit("STDIN connection reset, quitting!")
                        break
        stdin.close()

    def input_file(self, data):
        """
        File input method
        data - data to be written to file
        """
        if self.input_file_written:
            err = 'Agent %s cannot write multiple times to input file "%s".' % (
                self.name,
                self.input_file_path,
            )
            raise APiCommunicationError(err)
        if self.input_value_type == "BINARY":
            data = data.encode("utf-8")
        fh = open(self.input_file_path, "w")
        fh.write(data)
        fh.close()
        self.input_file_written = True
        # TODO: This needs to be synchronized with
        # processes reading the file (i.e. the process
        # should not start until the file has been
        # written. Also the service should not stop
        # until the process has read the file.
        self.service_quit("Input file written, quitting!")

    async def input_file_run(self, cmd):
        """
        File to STDOUT/STDERR coroutine
        cmd - command to be started as service
        """
        while not self.all_setup():
            await asyncio.sleep(0.1)

        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        await asyncio.gather(
            self.read_stderr(proc.stderr), self.read_stdout(proc.stdout)
        )

    def input_stdin(self, data):
        """
        STDIN input method
        data - data to be written to STDIN
        """
        logger.debug(f"Just got: {data}")
        if self.input_value_type == "BINARY":
            data = data.encode("utf-8")

        if self.input_delimiter:
            inp = [i for i in data.split(self.input_delimiter) if i]
        else:
            inp = [data]

        logger.debug(f"Inp is now: {inp}")
        self.BUFFER.extend(inp)
        logger.debug(f"Buffer is now: {self.BUFFER}")

        if data == self.input_end:
            self.service_quit("Got end delimiter on STDIN, quitting!")

    async def input_stdin_run(self, cmd):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        await asyncio.gather(
            self.read_stderr(proc.stderr),
            self.read_stdout(proc.stdout),
            self.write_stdin(proc.stdin),
        )

    async def input_stdinfile_run(self, cmd, file_path):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(cmd, stdin=asyncio.subprocess.PIPE)

        await asyncio.gather(self.write_stdin(proc.stdin), self.read_file(file_path))

    async def input_stdinhttp_run(self, cmd, url):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
        )

        await asyncio.gather(self.write_stdin(proc.stdin), self.read_url(url))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_stdinws_run(self, cmd, url):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
        )

        await asyncio.gather(self.write_stdin(proc.stdin), self.read_ws(url))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_stdinnc_run(self, cmd, host, port, udp):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
        )

        await asyncio.gather(self.write_stdin(proc.stdin))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_filefile_run(self, cmd, file_path):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        await asyncio.create_subprocess_shell(cmd, stdin=asyncio.subprocess.PIPE)

        await asyncio.gather(self.read_file(file_path))

    async def input_filehttp_run(self, cmd, file_path, url):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
        )

        await asyncio.gather(self.read_url(url))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_filews_run(self, cmd, file_path, url):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
        )

        await asyncio.gather(self.read_ws(url))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_filenc_run(self, cmd, file_path):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
        )
        while not self.input_file_written:
            await asyncio.sleep(0.1)
        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_httpstdout_run(self, cmd):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd, stderr=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE
        )

        await asyncio.gather(
            self.read_stderr(proc.stderr), self.read_stdout(proc.stdout)
        )

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_httphttp_run(self, cmd, url):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL
        )

        await asyncio.gather(self.read_url(url))

        while not self.input_ended:
            sleep(0.1)

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_httpfile_run(self, cmd, file_path):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(cmd)

        await asyncio.gather(self.read_file(file_path))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_httpws_run(self, cmd, url):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(cmd)

        await asyncio.gather(self.read_ws(url))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_httpnc_run(self, cmd):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
        )

        while not self.input_ended:
            sleep(0.1)

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_http(self, data, callback=False):
        if self.input_value_type == "BINARY":
            data = data.encode("utf-8")
        if self.input_delimiter:
            inp = [i for i in data.split(self.input_delimiter) if i != ""]
        else:
            inp = [data]
        for d in inp:
            url = self.http_url + d
            error = True
            while error:
                try:
                    response = requests.get(url, verify=False)
                    result = response.content.decode("utf-8")
                    if callback:
                        if self.output_delimiter:
                            out = [i for i in result.split(self.output_delimiter) if i]
                        else:
                            out = [result]
                        for i in out:
                            await self.output_callback(i)
                    error = False
                except Exception as e:
                    logger.error(f"Error input_http: {e}")
                    sleep(0.2)
            if d == self.input_end:
                self.service_quit("Received end delimiter, shutting down HTTP server!")
                return

    async def input_wsstdout_run(self, cmd):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd, stderr=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE
        )

        await asyncio.gather(
            self.read_stderr(proc.stderr), self.read_stdout(proc.stdout)
        )

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_wsfile_run(self, cmd, file_path):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(cmd)

        await asyncio.gather(self.read_file(file_path))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_wshttp_run(self, cmd, url):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
        )

        await asyncio.gather(self.read_url(url))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_wsws_run(self, cmd, url):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL
        )

        while not self.input_ended:
            sleep(0.1)

        await asyncio.gather(self.read_ws(url))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_wsnc_run(self, cmd):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
        )

        while not self.input_ended:
            sleep(0.1)

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    def input_ws(self, data, callback=False):
        if self.input_value_type == "BINARY":
            data = data.encode("utf-8")
        if self.input_delimiter:
            inp = [i for i in data.split(self.input_delimiter) if i != ""]
        else:
            inp = [data]
        for i in inp:
            try:
                loop = asyncio.get_event_loop()
            except Exception as e:
                logger.error(f"Error getting event loop: {e}")
                loop = asyncio.new_event_loop()
            loop.run_until_complete(self.ws(i, callback))
            if i == self.input_end:
                self.service_quit(
                    "Received end delimiter, shutting down WebSocket server!"
                )
                return

    async def ws(self, msg, callback=False):
        error = True
        while error:
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    await websocket.send(msg)
                    resp = await websocket.recv()
                    if callback:
                        if self.output_delimiter:
                            resp = [i for i in resp.split(self.output_delimiter) if i]
                        else:
                            resp = [resp]
                        for i in resp:
                            await self.output_callback(i)
                    error = False
            except Exception as e:
                logger.error(f"Error ws: {e}")
                sleep(0.2)

    async def input_ncstdout_run(self, cmd):
        while not self.all_setup():
            await asyncio.sleep(0.1)

        proc = await asyncio.create_subprocess_shell(
            cmd, stderr=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE
        )

        await asyncio.gather(
            self.read_stderr(proc.stderr), self.read_stdout(proc.stdout)
        )

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_ncfile_run(self, cmd, file_path):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(cmd)

        await asyncio.gather(self.read_file(file_path))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_nchttp_run(self, cmd, url):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
        )

        await asyncio.gather(self.read_url(url))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_ncws_run(self, cmd, url):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(cmd)

        await asyncio.gather(self.read_ws(url))

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_ncnc_run(self, cmd):
        while not self.all_setup():
            await asyncio.sleep(0.1)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.DEVNULL,
        )

        while not self.input_ended:
            sleep(0.1)

        try:
            pid = proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
        except Exception as e:
            logger.error(f"Error killing process: {e}")
            pass

    async def input_nc(self, data, callback=False):
        if self.input_value_type == "BINARY":
            data = data.encode("utf-8")
        if data == self.input_end:
            self.nc_client.close()
            self.service_quit("Got end delimiter, quitting NETCAT!")
            return None
        if self.input_delimiter:
            inp = [i for i in data.split(self.input_delimiter) if i != ""]
        else:
            inp = [data]
        sleep(0.1)
        for i in inp:
            try:
                self.nc_client.sendline(i.encode("utf-8"))
                if callback:
                    result = self.nc_client.read(timeout=1).decode("utf-8")
                    if result:
                        if self.output_delimiter:
                            result = [
                                j for j in result.split(self.output_delimiter) if j
                            ]
                        else:
                            result = [result]
                        for j in result:
                            await self.output_callback(j)

            except Exception as e:
                logger.error(f"Error input_nc: {e}")
                self.nc_client.close()
                self.service_quit("NETCAT process ended, quitting!")
                return None

    def output_callback(self, data):
        err = "Trying to call output_callback directly from APiBaseAgent. This method should be overriden!"
        raise APiCallbackException(err)

    def service_start(self):
        """
        Start main thread dealing with service input/output.
        """
        service_quit_thread = Thread(
            target=asyncio.run, args=(self.service_quit_run(),)
        )
        service_quit_thread.start()

        try:
            if self.stdinout_thread:
                self.stdinout_thread.start()
            if self.stdinfile_thread:
                self.stdinfile_thread.start()
            if self.stdinhttp_thread:
                self.stdinhttp_thread.start()
            if self.stdinws_thread:
                self.stdinws_thread.start()
            if self.stdinnc_thread:
                self.stdinnc_thread.start()
            if self.stdinncrec_thread:
                self.stdinncrec_thread.start()
            if self.filestdout_thread:
                self.filestdout_thread.start()
            if self.filefile_thread:
                self.filefile_thread.start()
            if self.filehttp_thread:
                self.filehttp_thread.start()
            if self.filews_thread:
                self.filews_thread.start()
            if self.filenc_thread:
                self.filenc_thread.start()
            if self.filencrec_thread:
                self.filencrec_thread.start()
            if self.nc_output_thread:
                self.nc_output_thread.start()
            if self.httpstdout_thread:
                self.httpstdout_thread.start()
            if self.httpfile_thread:
                self.httpfile_thread.start()
            if self.httphttp_thread:
                self.httphttp_thread.start()
            if self.httpws_thread:
                self.httpws_thread.start()
            if self.httpnc_thread:
                self.httpnc_thread.start()
            if self.httpncrec_thread:
                self.httpncrec_thread.start()
            if self.wsstdout_thread:
                self.wsstdout_thread.start()
            if self.wsfile_thread:
                self.wsfile_thread.start()
            if self.wshttp_thread:
                self.wshttp_thread.start()
            if self.wsws_thread:
                self.wsws_thread.start()
            if self.wsnc_thread:
                self.wsnc_thread.start()
            if self.wsncrec_thread:
                self.wsncrec_thread.start()
            if self.ncstdout_thread:
                self.ncstdout_thread.start()
            if self.ncfile_thread:
                self.ncfile_thread.start()
            if self.nchttp_thread:
                self.nchttp_thread.start()
            if self.ncws_thread:
                self.ncws_thread.start()
            if self.ncnc_thread:
                self.ncnc_thread.start()
            if self.ncncrec_thread:
                self.ncncrec_thread.start()
        except Exception as e:
            logger.error(f"Error starting threads: {e}")
            pass

    def service_quit(self, msg=""):
        """
        Service quitting and clean up method. Joins all threads and
        kills all running processes (services).

        msg - optional message (more or less for debug purposes)
        """

        self.say(msg)  # firstly need to clean up and finish all threads
        self.input_ended = True

    async def service_quit_run(self):
        while not self.input_ended:
            await asyncio.sleep(0.1)

        try:
            if self.stdinout_thread:
                self.stdinout_thread.join()
            if self.stdinfile_thread:
                self.stdinfile_thread.join()
            if self.stdinhttp_thread:
                self.stdinhttp_thread.join()
            if self.stdinws_thread:
                self.stdinws_thread.join()
            if self.stdinnc_thread:
                self.stdinnc_thread.join()
            if self.stdinncrec_thread:
                self.stdinncrec_thread.join()
            if self.filestdout_thread:
                self.filestdout_thread.join()
            if self.filefile_thread:
                self.filefile_thread.join()
            if self.filehttp_thread:
                self.filehttp_thread.join()
            if self.filews_thread:
                self.filews_thread.join()
            if self.filenc_thread:
                self.filenc_thread.join()
            if self.filencrec_thread:
                self.filencrec_thread.join()
            if self.nc_output_thread:
                self.nc_output_thread.join()
            if self.httpstdout_thread:
                self.httpstdout_thread.join()
            if self.httpfile_thread:
                self.httpfile_thread.join()
            if self.httphttp_thread:
                self.httphttp_thread.join()
            if self.httpws_thread:
                self.httpws_thread.join()
            if self.httpnc_thread:
                self.httpnc_thread.join()
            if self.httpncrec_thread:
                self.httpncrec_thread.join()
            if self.wsstdout_thread:
                self.wsstdout_thread.join()
            if self.wsfile_thread:
                self.wsfile_thread.join()
            if self.wshttp_thread:
                self.wshttp_thread.join()
            if self.wsws_thread:
                self.wsws_thread.join()
            if self.wsnc_thread:
                self.wsnc_thread.join()
            if self.wsncrec_thread:
                self.wsncrec_thread.join()
            if self.ncstdout_thread:
                self.ncstdout_thread.join()
            if self.ncfile_thread:
                self.ncfile_thread.join()
            if self.nchttp_thread:
                self.nchttp_thread.join()
            if self.ncws_thread:
                self.ncws_thread.join()
            if self.ncnc_thread:
                self.ncnc_thread.join()
            if self.ncncrec_thread:
                self.ncncrec_thread.join()
        except Exception as e:
            logger.error(f"Error joining threads: {e}")
            pass

        if self.http_proc:
            self.http_proc.terminate()

        if self.ws_proc:
            self.ws_proc.terminate()

        if self.nc_proc:
            # Total overkill ;-)
            pid = self.nc_proc.pid
            pr = psutil.Process(pid)
            for proc in pr.children(recursive=True):
                proc.kill()
            pr.kill()
            self.nc_proc.terminate()
            os.system("kill -9 %d" % pid)

        self.nc_output_thread_flag = False
        # TODO: Send message to holon that agent has finished
        metadata = deepcopy(self.inform_msg_template)
        metadata["reply-with"] = str(uuid4().hex)
        metadata["status"] = "finished"
        metadata["error-message"] = "null"

        await self.schedule_message(self.holon, metadata=metadata)

    def process_descriptor(self):
        """
        Agent descriptor processor (the heart of the agent). Processes
        the agent description (as loaded with self._load) and connects
        inputs to outputs for various types of communication channels
        (STDIN/STDOUT/STDERR, files, HTTP, WebSocket, Netcat). It also
        starts the defined services (subprocesses) and needed threads
        and/or coroutines to handle and connect inputs to outputs.
        The basic rule is that the START value from the agent description
        file (.ad) is started as a subprocess (the microservice), input
        is written to the input as specified by the agent description
        file and output is read from the output also specified in the
        same file. The output threads / coroutines call the output_callback
        method to handle to output in a desired manner (i.e. forward it
        to a given output channel of the agent).
        """
        if self.input_data_type == "ONEVALUE":
            pass
        elif self.input_data_type == "STREAM":
            if self.input_cutoff[:4] == "TIME":
                time = float(time_re.findall(self.input_cutoff)[0])
                raise NotImplementedError(NIE)
            elif self.input_cutoff[:4] == "SIZE":
                size = int(size_re.findall(self.input_cutoff)[0])
                raise NotImplementedError(NIE)
            elif self.input_cutoff[:9] == "DELIMITER":
                self.input_delimiter = delimiter_re.findall(self.input_cutoff)[0]
                if self.input_delimiter == "NEWLINE":
                    self.input_delimiter = "\n"
            elif self.input_cutoff[:5] == "REGEX":
                regex = int(regex_re.findall(self.input_cutoff)[0])
                raise NotImplementedError(NIE)
            else:
                err = 'Invalid input cutoff "%s"\n' % self.input_cutoff
                raise APiAgentDefinitionError(err)

            if self.input_end == "NEWLINE":
                self.input_end = "\n"
        else:
            err = 'Invalid input data type "%s"\n' % self.input_data_type
            raise APiAgentDefinitionError(err)

        # I hate to do this the way down there, i.e. writing the same more
        # or less twice with different attributes, but I am not going into
        # AspectOP just for the sake of a few lines of duplicate code :P
        if self.output_data_type == "ONEVALUE":
            pass
        elif self.output_data_type == "STREAM":
            if self.output_cutoff[:4] == "TIME":
                # time = float(time_re.findall(self.output_cutoff)[0])
                raise NotImplementedError(NIE)
            elif self.output_cutoff[:4] == "SIZE":
                # size = int(size_re.findall(self.output_cutoff)[0])
                raise NotImplementedError(NIE)
            elif self.output_cutoff[:9] == "DELIMITER":
                self.output_delimiter = delimiter_re.findall(self.output_cutoff)[0]
                if self.output_delimiter == "NEWLINE":
                    self.output_delimiter = "\n"
            elif self.output_cutoff[:5] == "REGEX":
                # regex = int(regex_re.findall(self.output_cutoff)[0])
                raise NotImplementedError(NIE)
            else:
                err = 'Invalid output cutoff "%s"\n' % self.output_cutoff
                raise APiAgentDefinitionError(err)

            if self.output_end == "NEWLINE":
                self.output_end = "\n"
        else:
            err = 'Invalid output data type "%s"\n' % self.output_data_type
            raise APiAgentDefinitionError(err)

        if self.input_type == "STDIN" and self.output_type in ("STDOUT", "STDERR"):
            self.input = self.input_stdin

            self.BUFFER = []
            self.stdinout_thread = Thread(
                target=asyncio.run, args=(self.input_stdin_run(self.cmd),)
            )
            # self.stdinout_thread.start()
        elif self.input_type == "STDIN" and self.output_type[:4] == "FILE":
            fl = file_re.findall(self.output_type)[0]
            self.output_file_path = fl

            self.input = self.input_stdin

            self.BUFFER = []

            self.stdinfile_thread = Thread(
                target=asyncio.run, args=(self.input_stdinfile_run(self.cmd, fl),)
            )
            # self.stdinfile_thread.start()
        elif self.input_type == "STDIN" and self.output_type[:4] == "HTTP":
            url = http_re.findall(self.output_type)[0]
            self.output_url = url
            self.input = self.input_stdin
            self.BUFFER = []

            self.stdinhttp_thread = Thread(
                target=asyncio.run, args=(self.input_stdinhttp_run(self.cmd, url),)
            )
            # self.stdinhttp_thread.start()

        elif self.input_type == "STDIN" and self.output_type[:2] == "WS":
            url = ws_re.findall(self.output_type)[0]
            self.output_url = url
            self.input = self.input_stdin
            self.BUFFER = []

            self.stdinws_thread = Thread(
                target=asyncio.run, args=(self.input_stdinws_run(self.cmd, url),)
            )
            # self.stdinws_thread.start()

        elif self.input_type == "STDIN" and self.output_type[:6] == "NETCAT":
            host, port, udp = netcat_re.findall(self.output_type)[0]
            self.nc_host = host
            self.nc_port = int(port)
            self.nc_udp = udp != ""
            self.input = self.input_stdin
            self.BUFFER = []

            self.stdinnc_thread = Thread(
                target=asyncio.run,
                args=(
                    self.input_stdinnc_run(
                        self.cmd, self.nc_host, self.nc_port, self.nc_udp
                    ),
                ),
            )
            # self.stdinnc_thread.start()
            self.stdinncrec_thread = Thread(
                target=self.read_nc, args=(self.nc_host, self.nc_port, self.nc_udp)
            )
            # self.stdinncrec_thread.start()

        elif self.input_type[:4] == "FILE" and self.output_type in ("STDOUT", "STDERR"):
            fl = file_re.findall(self.input_type)[0]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            self.filestdout_thread = Thread(
                target=asyncio.run, args=(self.input_file_run(self.cmd),)
            )
            # self.filestdout_thread.start()
        elif self.input_type[:4] == "FILE" and self.output_type[:4] == "FILE":
            infl = file_re.findall(self.input_type)[0]
            outfl = file_re.findall(self.output_type)[0]
            self.input_file_path = infl
            self.output_file_path = outfl
            self.input_file_written = False
            self.input = self.input_file
            self.filefile_thread = Thread(
                target=asyncio.run,
                args=(self.input_filefile_run(self.cmd, self.output_file_path),),
            )
            # self.filefile_thread.start()
        elif self.input_type[:4] == "FILE" and self.output_type[:4] == "HTTP":
            fl = file_re.findall(self.input_type)[0]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            url = http_re.findall(self.output_type)[0]
            self.output_url = url
            self.filehttp_thread = Thread(
                target=asyncio.run,
                args=(
                    self.input_filehttp_run(
                        self.cmd, self.input_file_path, self.output_url
                    ),
                ),
            )
            # self.filehttp_thread.start()

        elif self.input_type[:4] == "FILE" and self.output_type[:2] == "WS":
            fl = file_re.findall(self.input_type)[0]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            url = ws_re.findall(self.output_type)[0]
            self.output_url = url
            self.filews_thread = Thread(
                target=asyncio.run,
                args=(
                    self.input_filews_run(
                        self.cmd, self.input_file_path, self.output_url
                    ),
                ),
            )
            # self.filews_thread.start()

        elif self.input_type[:4] == "FILE" and self.output_type[:6] == "NETCAT":
            fl = file_re.findall(self.input_type)[0]
            self.input_file_path = fl
            self.input_file_written = False
            self.input = self.input_file
            host, port, udp = netcat_re.findall(self.output_type)[0]
            self.nc_host = host
            self.nc_port = int(port)
            self.nc_udp = udp != ""

            self.filenc_thread = Thread(
                target=asyncio.run,
                args=(self.input_filenc_run(self.cmd, self.input_file_path),),
            )
            # self.filenc_thread.start()
            self.filencrec_thread = Thread(
                target=self.read_nc, args=(self.nc_host, self.nc_port, self.nc_udp)
            )
            # self.filencrec_thread.start()

        elif self.input_type[:4] == "HTTP" and self.output_type in ("STDOUT", "STDERR"):
            url = http_re.findall(self.input_type)[0]
            self.http_url = url
            self.input = self.input_http
            self.httpstdout_thread = Thread(
                target=asyncio.run, args=(self.input_httpstdout_run(self.cmd),)
            )
            # self.httpstdout_thread.start()

        elif self.input_type[:4] == "HTTP" and self.output_type[:4] == "FILE":
            url = http_re.findall(self.input_type)[0]
            self.http_url = url
            self.input = self.input_http
            fl = file_re.findall(self.output_type)[0]
            self.output_file_path = fl

            self.httpfile_thread = Thread(
                target=asyncio.run,
                args=(self.input_httpfile_run(self.cmd, self.output_file_path),),
            )
            # self.httpfile_thread.start()

        elif self.input_type[:4] == "HTTP" and self.output_type[:4] == "HTTP":
            url = http_re.findall(self.input_type)[0]
            self.http_url = url
            url = http_re.findall(self.output_type)[0]
            self.http_url_output = url
            if self.http_url == self.http_url_output:
                cmd = shlex.split(self.cmd + " > /dev/null 2>&1 &")
                self.http_proc = sp.Popen(cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
                self.input = lambda data: self.input_http(data, callback=True)
            else:
                self.input = self.input_http
                self.httphttp_thread = Thread(
                    target=asyncio.run,
                    args=(self.input_httphttp_run(self.cmd, self.http_url_output),),
                )
                # self.httphttp_thread.start()

        elif self.input_type[:4] == "HTTP" and self.output_type[:2] == "WS":
            url = http_re.findall(self.input_type)[0]
            self.http_url = url
            url = ws_re.findall(self.output_type)[0]
            self.ws_output_url = url
            self.input = self.input_http

            self.httpws_thread = Thread(
                target=asyncio.run,
                args=(self.input_httpws_run(self.cmd, self.ws_output_url),),
            )
            # self.httpws_thread.start()

        elif self.input_type[:4] == "HTTP" and self.output_type[:6] == "NETCAT":
            url = http_re.findall(self.input_type)[0]
            self.http_url = url
            host, port, udp = netcat_re.findall(self.output_type)[0]
            self.nc_host = host
            self.nc_port = int(port)
            self.nc_udp = udp != ""
            self.input = self.input_http

            self.httpnc_thread = Thread(
                target=asyncio.run, args=(self.input_httpnc_run(self.cmd),)
            )
            # self.httpnc_thread.start()
            self.httpncrec_thread = Thread(
                target=self.read_nc, args=(self.nc_host, self.nc_port, self.nc_udp)
            )
            # self.httpncrec_thread.start()

        elif self.input_type[:2] == "WS" and self.output_type in ("STDOUT", "STDERR"):
            url = ws_re.findall(self.input_type)[0]
            self.ws_url = url
            self.input = self.input_ws

            self.wsstdout_thread = Thread(
                target=asyncio.run, args=(self.input_wsstdout_run(self.cmd),)
            )
            # self.wsstdout_thread.start()

        elif self.input_type[:2] == "WS" and self.output_type[:4] == "FILE":
            url = ws_re.findall(self.input_type)[0]
            self.ws_url = url
            self.input = self.input_ws
            fl = file_re.findall(self.output_type)[0]
            self.output_file_path = fl

            self.wsfile_thread = Thread(
                target=asyncio.run,
                args=(self.input_wsfile_run(self.cmd, self.output_file_path),),
            )
            # self.wsfile_thread.start()

        elif self.input_type[:2] == "WS" and self.output_type[:4] == "HTTP":
            url = ws_re.findall(self.input_type)[0]
            self.ws_url = url
            self.input = self.input_ws
            url = http_re.findall(self.output_type)[0]
            self.output_url = url

            self.wshttp_thread = Thread(
                target=asyncio.run,
                args=(self.input_wshttp_run(self.cmd, self.output_url),),
            )
            # self.wshttp_thread.start()

        elif self.input_type[:2] == "WS" and self.output_type[:2] == "WS":
            url = ws_re.findall(self.input_type)[0]
            self.ws_url = url
            self.input = self.input_ws
            url = ws_re.findall(self.output_type)[0]
            self.ws_output_url = url
            if self.ws_url == self.ws_output_url:
                cmd = shlex.split(self.cmd + " > /dev/null 2>&1 &")
                self.ws_proc = sp.Popen(cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
                self.input = lambda data: self.input_ws(data, callback=True)
            else:
                self.input = self.input_ws
                self.wsws_thread = Thread(
                    target=asyncio.run,
                    args=(self.input_wsws_run(self.cmd, self.ws_output_url),),
                )
                # self.wsws_thread.start()

        elif self.input_type[:2] == "WS" and self.output_type[:6] == "NETCAT":
            url = ws_re.findall(self.input_type)[0]
            self.ws_url = url
            self.input = self.input_ws
            host, port, udp = netcat_re.findall(self.output_type)[0]
            self.nc_host = host
            self.nc_port = int(port)
            self.nc_udp = udp != ""

            self.wsnc_thread = Thread(
                target=asyncio.run, args=(self.input_wsnc_run(self.cmd),)
            )
            # self.wsnc_thread.start()
            self.wsncrec_thread = Thread(
                target=self.read_nc, args=(self.nc_host, self.nc_port, self.nc_udp)
            )
            # self.wsncrec_thread.start()

        elif self.input_type[:6] == "NETCAT" and self.output_type in (
            "STDOUT",
            "STDERR",
        ):
            host, port, udp = netcat_re.findall(self.input_type)[0]
            self.nc_host = host
            self.nc_port = int(port)
            self.nc_udp = udp != ""
            self.input = self.input_nc

            self.ncstdout_thread = Thread(
                target=asyncio.run, args=(self.input_ncstdout_run(self.cmd),)
            )
            # self.ncstdout_thread.start()

            error = True
            while error:
                try:
                    self.nc_client = nclib.Netcat(
                        (self.nc_host, self.nc_port), udp=self.nc_udp
                    )
                    error = False
                except Exception as e:
                    logger.error(f"Error creating nc client: {e}")
                    sleep(0.1)

        elif self.input_type[:6] == "NETCAT" and self.output_type[:4] == "FILE":
            host, port, udp = netcat_re.findall(self.input_type)[0]
            self.nc_host = host
            self.nc_port = int(port)
            self.nc_udp = udp != ""
            fl = file_re.findall(self.output_type)[0]
            self.output_file_path = fl
            self.input = self.input_nc

            self.ncfile_thread = Thread(
                target=asyncio.run,
                args=(self.input_ncfile_run(self.cmd, self.output_file_path),),
            )
            # self.ncfile_thread.start()
            # TODO: find out why only the first output is processed, i.e.
            # ncat writes to the file and closes it seemingly after each
            # input making it possible for read_file() to read it and end
            # prematurely. See if this can be avoided.

            error = True
            while error:
                try:
                    self.nc_client = nclib.Netcat(
                        (self.nc_host, self.nc_port), udp=self.nc_udp
                    )
                    error = False
                except Exception as e:
                    logger.error(f"Error creating nc client: {e}")
                    sleep(0.1)

        elif self.input_type[:6] == "NETCAT" and self.output_type[:4] == "HTTP":
            host, port, udp = netcat_re.findall(self.input_type)[0]
            self.nc_host = host
            self.nc_port = int(port)
            self.nc_udp = udp != ""
            self.input = self.input_nc
            url = http_re.findall(self.output_type)[0]
            self.output_url = url

            self.nchttp_thread = Thread(
                target=asyncio.run,
                args=(self.input_nchttp_run(self.cmd, self.output_url),),
            )
            # self.nchttp_thread.start()

            error = True
            while error:
                try:
                    self.nc_client = nclib.Netcat(
                        (self.nc_host, self.nc_port), udp=self.nc_udp
                    )
                    error = False
                except Exception as e:
                    logger.error(f"Error creating nc client: {e}")
                    sleep(0.1)

        elif self.input_type[:6] == "NETCAT" and self.output_type[:2] == "WS":
            host, port, udp = netcat_re.findall(self.input_type)[0]
            self.nc_host = host
            self.nc_port = int(port)
            self.nc_udp = udp != ""
            self.input = self.input_nc
            url = ws_re.findall(self.output_type)[0]
            self.ws_output_url = url

            self.ncws_thread = Thread(
                target=asyncio.run,
                args=(self.input_ncws_run(self.cmd, self.ws_output_url),),
            )
            # self.ncws_thread.start()

            error = True
            while error:
                try:
                    self.nc_client = nclib.Netcat(
                        (self.nc_host, self.nc_port), udp=self.nc_udp
                    )
                    error = False
                except Exception as e:
                    logger.error(f"Error creating nc client: {e}")
                    sleep(0.1)

        elif self.input_type[:6] == "NETCAT" and self.output_type[:6] == "NETCAT":
            host, port, udp = netcat_re.findall(self.input_type)[0]
            self.nc_host = host
            self.nc_port = int(port)
            self.nc_udp = udp != ""

            ohost, oport, oudp = netcat_re.findall(self.output_type)[0]
            self.nc_host_output = ohost
            self.nc_port_output = int(oport)
            self.nc_udp_output = oudp != ""

            if (host, port, udp) == (ohost, oport, oudp):
                self.nc_proc = sp.Popen(
                    shlex.split(self.cmd), stdout=sp.PIPE, stderr=sp.DEVNULL
                )
                sleep(0.1)
                self.input = lambda data: self.input_nc(data, callback=True)

                error = True
                while error:
                    try:
                        self.nc_client = nclib.Netcat(
                            (self.nc_host, self.nc_port), udp=self.nc_udp
                        )
                        error = False
                    except Exception as e:
                        logger.error(f"Error creating nc client: {e}")
                        sleep(0.1)

            else:
                self.input = self.input_nc
                self.ncnc_thread = Thread(
                    target=asyncio.run, args=(self.input_ncnc_run(self.cmd),)
                )
                # self.ncnc_thread.start()

                error = True
                while error:
                    try:
                        self.nc_client = nclib.Netcat(
                            (self.nc_host, self.nc_port), udp=self.nc_udp
                        )

                        error = False
                    except Exception as e:
                        logger.error(f"Error creating nc client: {e}")
                        sleep(0.1)

                self.ncncrec_thread = Thread(
                    target=self.read_nc,
                    args=(self.nc_host_output, self.nc_port_output, self.nc_udp_output),
                )
                # self.ncncrec_thread.start()

        else:
            err = 'Invalid input type "%s"\n' % self.input_type
            raise APiAgentDefinitionError(err)

        if self.input_value_type not in ["STRING", "BINARY"]:
            err = 'Invalid input value type "%s"\n' % self.input_value_type
            raise APiAgentDefinitionError(err)
