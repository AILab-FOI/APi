#!/usr/bin/env python3
from yaml import load
import warnings
from helpers import *
from errors import *

from uuid import uuid4
import requests
# When using HTTPS with insecure servers this has to be uncommented
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class APiRegistrationService:
    '''
    Registration service which generates unique agent names
    and registers them on XMPP server(s) according to rules
    given in config file.
    '''
    # open cfg file

    def __init__(self, holonname):
        self.name = holonname
        try:
            fh = open(holonname + '.cfg')
        except IOError as e:
            err = 'Missing holon configuration file or permission issue.\n' + \
                str(e)
            raise APiIOError(err)
        self.services = []
        self._load(fh)
        self.next = lambda: cycle(self.services).__next__()
        self.MAX_RETRIES = 4

    # read yml file and setup class
    def _load(self, fh):
        try:
            self.descriptor = load(fh.read(), Loader)
        except Exception as e:
            err = 'Holon configuration file cannot be loaded.\n' + str(e)
            raise APiHolonConfigurationError(err)
        try:
            self.services = self.descriptor['registration-services']
        except Exception as e:
            err = 'Holon configuration file has invalid format.\n' + str(e)
            raise APiHolonConfigurationError(err)
        if not self.services:
            err = 'Holon configuration file does not list any services.'
            raise APiHolonConfigurationError(err)
        try:
            self.min_port = int(self.descriptor['port-range']['min'])
            self.max_port = int(self.descriptor['port-range']['max'])
        except Exception as e:
            err = 'Holon configuration file has invalid format.\n' + str(e)
            raise APiHolonConfigurationError(err)

    # create services from self.services

    def register(self, name):
        username = '%s_%s_%s' % (self.name, name, str(uuid4().hex))
        password = str(uuid4().hex)
        host = 'host.docker.internal' # specifying docker socket to access prosody

        return ('%s@%s' % (username, host), password)

    # TODO: uncomment once for production ready PoC
    """
    def register(self, name):
        server = self.next()
        # APi-test_holonko1_1640719515a8481c9dfa818fd2836955
        username = '%s_%s_%s' % (self.name, name, str(uuid4().hex))
        password = str(uuid4().hex)
        # send request to FOI XMPP server to create users

        host = server.split(':')[0]

        url = "https://%s/register/%s/%s" % (server, username, password)
        try:
            response = requests.get(url, verify=False)
        except requests.exceptions.ConnectionError as e:
            warnings.warn(
                'Falling back to registering over insecure HTTP instead of HTTPS', APiHTTPSWarning)
            url = "http://%s/register/%s/%s" % (server, username, password)
            response = requests.get(url, verify=False)

        
        if response.status_code == 200:
            result = response.content.decode('utf-8')
            # user succesfuly registered
            if result == 'OK':
                return ('%s@%s' % (username, host), password)
            else:
                # retry to register XMP user 4x
                for i in range(self.MAX_RETRIES):
                    response = requests.get(url, verify=False)
                    result = response.content.decode('utf-8')
                    if result == 'OK':
                        return ('%s@%s' % (username, host), password)
                raise XMPPRegisterException('Cannot register agent "%s" after %d retries, giving up. Error from server: %s' % (
                    username, self.MAX_RETRIES, result))
        else:
            raise XMPPRegisterException(
                'Error while communicating with server at "%s"' % server)
    """
