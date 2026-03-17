# 🚀 APS - Advanced Port Scout

Advanced Port Scout (APS) is a powerful Python-based network scanning tool designed for **port scanning, service detection, OS fingerprinting, and vulnerability lookup**.

It combines speed ⚡, automation 🤖, and useful insights 📊 into one CLI tool.

---

## 📌 Features

* 🔍 TCP Port Scanning (custom range)
* 📡 UDP Port Scanning
* ⚡ Multi-threaded fast scanning
* 🧠 Service Detection (common ports)
* 🖥️ OS Detection (TTL-based)
* 🧾 Version Detection (banner grabbing)
* 🛡️ CVE Vulnerability Lookup (via NVD API)
* 🌐 ARP Network Scanning
* 🔧 Nmap Script Scan (`-sC`)
* 🛠️ IDS / Aggressive Scan (`-A`)
* 📊 Rich CLI Output (tables using rich)
* 📄 HTML Report Generation

---

## 🛠️ Requirements

* Python 3.x
* Linux (Recommended: Kali Linux)

### Install dependencies:

```bash
pip install scapy rich requests
```

---

## 🚀 Installation

```bash
git clone https://github.com/yourusername/APS-Advanced-Port-Scout.git
cd APS-Advanced-Port-Scout
python main.py
```

---

## 🧪 Usage

Run the tool:

```bash
python main.py
```

You will see a menu like:

```
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
```

---

## 📖 Example

### 🔹 TCP Scan

```
Select option: 3
Target IP: 192.168.1.1
Start port: 1
End port: 100
```

---

### 🔹 ARP Scan

```
Select option: 1
Network: 192.168.1.0/24
```

---

## 📊 Output

* Displays:

  * Open Ports
  * Service Name
  * Version Info
  * CVE Vulnerabilities

* Generates HTML report:

```
aps_report.html
```

---

## ⚠️ Important Notes

* Run with root privileges for full functionality:

```bash
sudo python main.py
```

* Some features depend on:

  * `nmap` installed
  * Network permissions

Install nmap:

```bash
sudo apt install nmap
```

---

## 🔐 Legal Disclaimer

This tool is created for **educational and ethical testing purposes only**.

❌ Do NOT use on networks without permission
✅ Use only on your own systems or authorized environments

---

## 👨‍💻 Author

**Khaleel Basha**

---

## ⭐ Support

If you like this project:

* ⭐ Star the repository
* 🍴 Fork it
* 🛠️ Contribute improvements

---

## 🔥 Future Improvements

* Web UI Dashboard
* Login system
* Export to PDF
* Live scan progress bar
* AI-based vulnerability suggestions

---

## 📬 Contact

For suggestions or issues, open a GitHub issue.

---

# 💡 Happy Hacking (Ethically) 🚀
