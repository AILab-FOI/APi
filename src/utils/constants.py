import re

NIE = "Sorry, it is planned, I promise ;-)"
TMP_FOLDER = "/tmp/APi/"

file_re = re.compile(r"FILE (.*)")
http_re = re.compile(r"HTTP (.*)")
ws_re = re.compile(r"WS (.*)")
netcat_re = re.compile(r"NETCAT (.*)[:]([0-9]+)(?:[:](udp))?")

delimiter_re = re.compile(r"DELIMITER (.*)")
time_re = re.compile(r"TIME ([0-9.]+)")
size_re = re.compile(r"SIZE ([0-9]+)")
regex_re = re.compile(r"REGEX .*")

var_re = re.compile(r"[?][a-zA-Z][a-zA-Z0-9_-]*")
