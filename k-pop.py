#!/usr/bin/env python3

import requests
import argparse
from hashlib import sha1
from time import sleep

parser = argparse.ArgumentParser(description='HaveIBeenPwned K-Anonymity Mass Checker')
parser.add_argument('--pass-file',help="Path to file containing passwords",dest='pass_path')
#parser.add_argument('--user-pass',help="Path to file containig 'username:password' to check")
args = parser.parse_args()

with open(args.pass_path) as passfile:
    password_list = passfile.read().splitlines()

password_list = sorted(set(password_list))

for password in password_list:
    if len(password) < 1:
        continue
    hash = ((sha1(password.encode('utf-8'))).hexdigest()).upper()

    url = ("https://api.pwnedpasswords.com/range/" + hash[0:5])
    response = ((requests.get(url)).text).split("\r\n")

    for line in response:

        if len(line) > 1:
            line_hash = line.split(":")[0]
            line_count = line.split(":")[1]
            if line_hash.rstrip() == hash.rstrip()[5:]:
                print ("Password '" + password + "' has been owned " + line_count + " times.")
				continue
    # Rate limit
    sleep(1.5)
