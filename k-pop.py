#!/usr/bin/env python3

import requests
import argparse
from hashlib import sha1
from time import sleep
import getpass

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser(description='HaveIBeenPwned K-Anonymity Mass Checker')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--pass-file', help="Path to file containing passwords", dest='pass_path')
group.add_argument('-p', '--pass', help="Use to enter password via prompt", dest='single_pass', action='store_true')
parser.add_argument('--show', help="Enable to show plaintext password in view", dest='show_pass', action='store_true')
parser.add_argument('-u', '--user', help="Enable to delimit file by 'username:password'", dest='userdelim', action='store_true')
args = parser.parse_args()


if args.single_pass is False:
    with open(args.pass_path) as passfile:
        password_list = passfile.read().splitlines()

    password_list = sorted(set(password_list))

else:
    password_list = []

if args.single_pass:
    password_list.append(getpass.getpass('Password:'))

for password in password_list:
    if len(password) < 1:
        continue

    if args.userdelim:
        password = password.split(":",1)[1]

    pwdhash = ((sha1(password.encode('utf-8'))).hexdigest()).upper()

    url = ("https://api.pwnedpasswords.com/range/" + pwdhash[0:5])

    if len(password_list) > 1:
        # API Rate limit
        sleep(1.51)

    response = requests.get(url).text.split("\r\n")

    owned = False

    for line in response:

        if len(line) > 1:
            line_hash = line.split(":")[0]
            line_count = line.split(":")[1]
            if line_hash.rstrip() == pwdhash.rstrip()[5:]:
                if args.show_pass:
                    print (bcolors.FAIL + "[!]" + bcolors.ENDC + " Password '" + password + "' has been owned " + bcolors.FAIL + line_count + bcolors.ENDC + " times." + bcolors.ENDC)
                else:
                    print (bcolors.FAIL + "[!]" + bcolors.ENDC + " Password has been owned " + bcolors.FAIL + line_count + bcolors.ENDC + " times."  + bcolors.ENDC)

                owned = True

                #continue
                break

    if owned is False:
        if args.show_pass:
            print (bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Password '" + bcolors.ENDC + password + "' has not been owned." + bcolors.ENDC)
        else:
            print (bcolors.OKGREEN + "[+]" + bcolors.ENDC + " Password has not been owned!")


print ("")