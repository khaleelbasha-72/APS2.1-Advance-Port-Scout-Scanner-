import socket
import subprocess
import signal
import sys
import requests
from concurrent.futures import ThreadPoolExecutor

from rich.console import Console
from rich.table import Table
from scapy.all import ARP, Ether, srp

console = Console()

GREEN="\033[92m"
RESET="\033[0m"

results=[]

# ---------------- CTRL+C ----------------

def ctrl_handler(sig,frame):
    console.print("\nScan stopped safely\n")
    sys.exit(0)

signal.signal(signal.SIGINT,ctrl_handler)

# ---------------- BANNER ----------------

def banner():

    console.print("""
 █████╗ ██████╗ ███████╗
██╔══██╗██╔══██╗██╔════╝
███████║██████╔╝███████╗
██╔══██║██╔═══╝ ╚════██║
██║  ██║██║     ███████║
╚═╝  ╚═╝╚═╝     ╚══════╝

APS - Advanced Port Scout
by Khaleel basha
""")

# ---------------- BAR ----------------

def bar():
    console.print("═"*80)

# ---------------- PORT DATABASE ----------------

port_db={

21:("FTP","File Transfer Protocol","ftp TARGET"),
22:("SSH","Secure Shell","ssh user@TARGET"),
23:("Telnet","Remote terminal protocol","telnet TARGET"),
25:("SMTP","Simple Mail Transfer Protocol","smtp TARGET"),
53:("DNS","Domain Name System","nslookup google.com TARGET"),
80:("HTTP","HyperText Transfer Protocol","http://TARGET"),
110:("POP3","Post Office Protocol","pop3 TARGET"),
139:("NetBIOS","Windows file sharing","net use \\\\TARGET"),
143:("IMAP","Internet Message Access Protocol","imap TARGET"),
443:("HTTPS","Secure Web Protocol","https://TARGET"),
445:("SMB","Server Message Block","smbclient //TARGET/share"),
3306:("MySQL","Database Service","mysql -h TARGET -u root"),
3389:("RDP","Remote Desktop","rdesktop TARGET")

}

# ---------------- SERVICE DETECTION ----------------

def detect_service(port):

    if port in port_db:
        return port_db[port][0]

    return "Unknown"

# ---------------- OS DETECTION ----------------

def detect_os(ip):

    try:

        output=subprocess.check_output(["ping","-c","1",ip]).decode()

        for line in output.split("\n"):

            if "ttl=" in line:

                ttl=int(line.split("ttl=")[1].split(" ")[0])

                if ttl<=64:
                    return "Linux / Unix"

                elif ttl<=128:
                    return "Windows"

        return "Unknown"

    except:

        return "Unknown"

# ---------------- VERSION DETECTION ----------------

def detect_version(ip,port):

    try:

        s=socket.socket()
        s.settimeout(2)

        s.connect((ip,port))

        if port in [80,8080]:
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")

        banner=s.recv(1024).decode(errors="ignore")

        if banner:
            return banner.split("\n")[0]

    except:
        pass

    return "Version not detected"

# ---------------- CVE LOOKUP ----------------

def cve_lookup(service):

    try:

        url=f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={service}"

        r=requests.get(url,timeout=5)

        data=r.json()

        vulns=data.get("vulnerabilities",[])

        return vulns[:2]

    except:

        return []

# ---------------- PORT OUTPUT ----------------

def show_port(ip,port,version,vulns):

    bar()

    service=detect_service(port)

    if port in port_db:
        name,full,connect=port_db[port]
    else:
        name,full,connect=("Unknown","Unknown Service","manual")

    connect_cmd=connect.replace("TARGET",ip)

    console.print(f"\nPORT: {port}")
    console.print(f"STATUS: {GREEN}OPEN{RESET}\n")

    console.print(f"SERVICE: {name}")
    console.print(f"FULL FORM: {full}\n")

    console.print("HOW TO CONNECT:")
    console.print(connect_cmd)

    console.print("\nVERSION:")
    console.print(version)

    console.print("\nVULNERABILITY INFORMATION:")

    if not vulns:
        console.print("No vulnerabilities found")

    for v in vulns:

        cve=v["cve"]["id"]

        desc=v["cve"]["descriptions"][0]["value"]

        console.print(f"\nCVE: {cve}")
        console.print(f"Description: {desc[:200]}...")

        console.print("Exploit-DB:")
        console.print(f"https://www.exploit-db.com/search?cve={cve}")

    bar()

# ---------------- TCP SCAN ----------------

def scan_tcp(ip,port):

    try:

        s=socket.socket()
        s.settimeout(1)

        result=s.connect_ex((ip,port))

        if result==0:

            version=detect_version(ip,port)

            service=detect_service(port)

            vulns=cve_lookup(service)

            show_port(ip,port,version,vulns)

            results.append((port,service,"OPEN"))

        s.close()

    except:
        pass

# ---------------- UDP SCAN ----------------

def scan_udp(ip,port):

    try:

        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

        s.settimeout(1)

        s.sendto(b"test",(ip,port))

        data,addr=s.recvfrom(1024)

        console.print(f"[UDP OPEN] {port}")

        results.append((port,"UDP service","OPEN"))

    except:
        pass

# ---------------- THREAD SCAN ----------------

def threaded_tcp(ip,start,end):

    with ThreadPoolExecutor(max_workers=400) as executor:

        for port in range(start,end+1):

            executor.submit(scan_tcp,ip,port)

def threaded_udp(ip,start,end):

    with ThreadPoolExecutor(max_workers=300) as executor:

        for port in range(start,end+1):

            executor.submit(scan_udp,ip,port)

# ---------------- FULL SCAN ----------------

def full_tcp_udp(ip):

    console.print("\nRunning full TCP + UDP scan\n")

    threaded_tcp(ip,1,65535)

    threaded_udp(ip,1,65535)

# ---------------- ARP SCAN ----------------

def arp_scan(network):

    console.print("\nRunning ARP Scan\n")

    packet=Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network)

    result=srp(packet,timeout=2,verbose=0)[0]

    for sent,received in result:

        console.print(f"Host Alive → IP: {received.psrc} | MAC: {received.hwsrc}")

# ---------------- SCRIPT SCAN ----------------

def script_scan(ip):

    console.print("\nRunning Script Scan (-sc)\n")

    subprocess.call(["nmap","-sC",ip])

# ---------------- IDS DETECTION ----------------

def ids_detection(ip):

    console.print("\nRunning IDS Detection\n")

    subprocess.call(["nmap","-A",ip])

# ---------------- HTML REPORT ----------------

def save_report(ip):

    html="<html><body><h1>APS Scan Report</h1>"

    html+=f"<h2>Target: {ip}</h2>"

    html+="<table border=1><tr><th>Port</th><th>Service</th><th>Status</th></tr>"

    for r in results:

        html+=f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"

    html+="</table></body></html>"

    f=open("aps_report.html","w")

    f.write(html)

    f.close()

    console.print("\nReport saved → aps_report.html")

# ---------------- RESULTS TABLE ----------------

def show_results():

    table=Table(title="APS Scan Results")

    table.add_column("Port")
    table.add_column("Service")
    table.add_column("Status")

    for r in results:

        table.add_row(str(r[0]),r[1],r[2])

    console.print(table)

# ---------------- MENU ----------------

def menu():

    console.print("""

1 ARP Scan
2 ICMP Ping
3 TCP Scan (range)
4 UDP Scan (range)
5 TCP + UDP Full Scan
6 Aggressive Scan
7 Script Scan (-sc)
8 IDS Detection
9 OS Detection
0 Exit

""")

# ---------------- MAIN ----------------

def main():

    banner()

    while True:

        menu()

        choice=input("Select option or type back: ")

        if choice=="0":
            break

        if choice=="back":
            continue

        if choice=="1":

            network=input("Network (192.168.1.0/24): ")

            arp_scan(network)

        else:

            ip=input("Target IP: ")

            console.print("Detected OS:",detect_os(ip))

            if choice=="2":

                subprocess.call(["ping","-c","2",ip])

            if choice=="3":

                start=int(input("Start port: "))
                end=int(input("End port: "))

                threaded_tcp(ip,start,end)

            if choice=="4":

                start=int(input("Start UDP port: "))
                end=int(input("End UDP port: "))

                threaded_udp(ip,start,end)

            if choice=="5":

                full_tcp_udp(ip)

            if choice=="6":

                threaded_tcp(ip,1,1000)

            if choice=="7":

                script_scan(ip)

            if choice=="8":

                ids_detection(ip)

            if choice=="9":

                console.print("Detected OS:",detect_os(ip))

        show_results()

        save_report(ip)

if __name__=="__main__":
    main()
