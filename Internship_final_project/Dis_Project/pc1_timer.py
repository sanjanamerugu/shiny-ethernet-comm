import tkinter as tk
from tkinter import ttk, filedialog
import threading
import time
import socket
import json
from datetime import datetime
from network_utils import NetworkManager

class TimerApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PC1")
        self.root.geometry("400x400")
        self.root.configure(bg='cyan')

        # Timer variables
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.is_running = False
        self.timer_thread = None

        # Network manager
        self.network_manager = NetworkManager()

        # Communication data
        self.comm_data = {
            'send_id': 'PC1',
            'receive_id': 'PC2',
            'hours': 0,
            'minutes': 0,
            'seconds': 0,
            'total_size': 0,
            'status': 'stopped'
        }

        self.create_widgets()
        self.setup_network()

    def create_widgets(self):
        timer_frame = tk.Frame(self.root, bg='cyan')
        timer_frame.pack(pady=20)

        self.hours_label = tk.Label(timer_frame, text="00", font=("Arial", 24, "bold"), bg='black', fg='red', width=4)
        self.hours_label.grid(row=0, column=0, padx=5)
        tk.Label(timer_frame, text="Hours", bg='cyan', fg='orange').grid(row=1, column=0)

        self.minutes_label = tk.Label(timer_frame, text="00", font=("Arial", 24, "bold"), bg='black', fg='red', width=4)
        self.minutes_label.grid(row=0, column=1, padx=5)
        tk.Label(timer_frame, text="Minutes", bg='cyan', fg='orange').grid(row=1, column=1)

        self.seconds_label = tk.Label(timer_frame, text="00", font=("Arial", 24, "bold"), bg='black', fg='red', width=4)
        self.seconds_label.grid(row=0, column=2, padx=5)
        tk.Label(timer_frame, text="Seconds", bg='cyan', fg='orange').grid(row=1, column=2)

        button_frame = tk.Frame(self.root, bg='cyan')
        button_frame.pack(pady=10)

        self.start_btn = tk.Button(button_frame, text="START", command=self.start_timer, bg='green', fg='white', width=8)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = tk.Button(button_frame, text="STOP", command=self.stop_timer, bg='red', fg='white', width=8)
        self.stop_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = tk.Button(button_frame, text="RESET", command=self.reset_timer, bg='blue', fg='white', width=8)
        self.reset_btn.grid(row=0, column=2, padx=5)

        self.send_image_btn = tk.Button(self.root, text="Send Image", command=self.send_image_to_pc2, bg='orange', fg='black')
        self.send_image_btn.pack(pady=5)

        network_frame = tk.LabelFrame(self.root, text="Network Settings", bg='cyan')
        network_frame.pack(pady=10, padx=20, fill='x')

        tk.Label(network_frame, text="Server Port:", bg='cyan').grid(row=0, column=0, sticky='w')
        self.server_port_var = tk.StringVar(value="12345")
        tk.Entry(network_frame, textvariable=self.server_port_var, width=10).grid(row=0, column=1)

        tk.Label(network_frame, text="Client IP:", bg='cyan').grid(row=1, column=0, sticky='w')
        self.client_ip_var = tk.StringVar(value="127.0.0.1")
        tk.Entry(network_frame, textvariable=self.client_ip_var, width=15).grid(row=1, column=1)

        tk.Label(network_frame, text="Client Port:", bg='cyan').grid(row=2, column=0, sticky='w')
        self.client_port_var = tk.StringVar(value="12346")
        tk.Entry(network_frame, textvariable=self.client_port_var, width=10).grid(row=2, column=1)

        tk.Label(network_frame, text="Image Port:", bg='cyan').grid(row=3, column=0, sticky='w')
        self.image_port_var = tk.StringVar(value="12347")
        tk.Entry(network_frame, textvariable=self.image_port_var, width=10).grid(row=3, column=1)

        self.status_label = tk.Label(self.root, text="Status: Ready", bg='cyan')
        self.status_label.pack(pady=5)

    def setup_network(self):
        self.network_manager.start_server(int(self.server_port_var.get()), self.handle_received_data)

    def handle_received_data(self, data):
        self.update_status(f"Received from PC2: {data.get('status', 'No status')}")

    def send_data_to_pc2(self):
        self.comm_data.update({
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds,
            'status': 'running' if self.is_running else 'stopped',
            'timestamp': datetime.now().isoformat()
        })
        data_json = json.dumps(self.comm_data)
        byte_data = data_json.encode()
        self.comm_data['total_size'] = len(byte_data)
        print(f"Sending {len(byte_data)} bytes: {data_json}")
        success = self.network_manager.send_data(
            self.client_ip_var.get(),
            int(self.client_port_var.get()),
            self.comm_data
        )
        if not success:
            self.update_status("Failed to send data to PC2")

    def send_image_to_pc2(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            success = self.network_manager.send_image(
                self.client_ip_var.get(),
                int(self.image_port_var.get()),
                file_path
            )
            if success:
                self.update_status("Image sent to PC2")
            else:
                self.update_status("Failed to send image")

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
            self.update_status("Timer started")

    def stop_timer(self):
        self.is_running = False
        self.update_status("Timer stopped")

    def reset_timer(self):
        self.is_running = False
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.update_display()
        self.update_status("Timer reset")

    def run_timer(self):
        while self.is_running:
            start_time = time.time()
            self.seconds += 1
            if self.seconds >= 60:
                self.seconds = 0
                self.minutes += 1
                if self.minutes >= 60:
                    self.minutes = 0
                    self.hours += 1
                    if self.hours >= 24:
                        self.hours = 0
            self.update_display()
            for _ in range(10):
                self.send_data_to_pc2()
                time.sleep(0.1)
            elapsed = time.time() - start_time
            remaining = max(0, 1 - elapsed)
            time.sleep(remaining)

    def update_display(self):
        self.hours_label.config(text=f"{self.hours:02d}")
        self.minutes_label.config(text=f"{self.minutes:02d}")
        self.seconds_label.config(text=f"{self.seconds:02d}")

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.is_running = False
        self.network_manager.stop_server()
        self.root.destroy()

if __name__ == "__main__":
    app = TimerApplication()
    app.run()
