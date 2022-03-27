#!/usr/bin/env python

import subprocess
import optparse
import re
from termcolor import colored

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error(colored("[-] Please specify an interface, use --help for more info.", 'red'))
    elif not options.new_mac:
        parser.error(colored("[-] Please specify a new MAC, use --help for more info", 'red'))
    return options

def change_mac(interface, new_mac):
    print(colored("[+] Changing MAC address for " + interface + " to " + new_mac, 'blue'))
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[?]Could not read MAC address. Please try again.")

options = get_arguments()
current_mac = get_current_mac(options.interface)
print(colored("Current MAC = " + str(current_mac), 'yellow'))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
        print(colored("[+] MAC address was successfully changed to " + current_mac, 'green'))
else:
    print(colored("[x] Sorry, the MAC address change was unsuccessful.", 'red'))








