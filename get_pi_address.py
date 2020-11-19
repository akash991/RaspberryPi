import subprocess
import os

def get_ip_and_mac_of_devices_connected_to_interface(interfaceAddress):
    cmd = "arp -a -N {}".format(interfaceAddress)
    output = subprocess.check_output(cmd).decode("ascii").split("\n")
    ip_mac = {}
    for entry in output[3:]:
        content = entry.strip(" \r").split(" ")
        for _ in content[1:]:
            if _ != "":
                ip_mac[content[0]] = _
                break
    return ip_mac

def get_wlan_ip():
    cmd = "ipconfig"
    output = subprocess.check_output(cmd).decode("ascii")
    result = {}
    data = [a.strip("\r ") for a in output.split("\n") if a!='\r'][1:]
    for i in data:
        if 'adapter' in i.lower():
            adapter = i
            result[adapter] = {}
            continue
        else:
             _ = i.split(" : ")
             if len(_) < 2:
                 continue
             result[adapter][_[0].strip(". ").lower()] = _[1].strip(" ")
    for key, val in result.items():
        if "wi-fi" in key.lower():
            return val["ipv4 address"]

def get_ip_from_mac(ip_mac_table, mac_address):
    for k, v in ip_mac_table.items():
        if v == mac_address:
            return k


if __name__ == "__main__":
    wifiInterfaceAddress = get_wlan_ip()
    ip_mac_dict = get_ip_and_mac_of_devices_connected_to_interface(wifiInterfaceAddress)
    pi_mac_address = os.getenv("PI-MAC-ADDRESS")
    pi_ip_address = get_ip_from_mac(ip_mac_dict, pi_mac_address)
    print("Ip of the PI board is: {}".format(pi_ip_address))