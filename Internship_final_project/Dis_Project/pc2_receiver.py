import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import json
import socket
import os
from datetime import datetime
from network_utils import NetworkManager

class PC2Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PC2")
        self.root.geometry("500x500")
        self.root.configure(bg='cyan')

        # Timer variables
        self.received_hours = 0
        self.received_minutes = 0
        self.received_seconds = 0

        # Network manager
        self.network_manager = NetworkManager()

        self.create_widgets()
        self.setup_network()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="PC2 - Timer Receiver", font=("Arial", 16, "bold"), bg='cyan')
        title_label.pack(pady=10)

        # Timer display
        timer_frame = tk.Frame(self.root, bg='cyan')
        timer_frame.pack(pady=10)

        self.hours_label = tk.Label(timer_frame, text="00", font=("Arial", 24, "bold"), bg='black', fg='red', width=4)
        self.hours_label.grid(row=0, column=0, padx=5)
        tk.Label(timer_frame, text="Hours", bg='cyan', fg='orange').grid(row=1, column=0)

        self.minutes_label = tk.Label(timer_frame, text="00", font=("Arial", 24, "bold"), bg='black', fg='red', width=4)
        self.minutes_label.grid(row=0, column=1, padx=5)
        tk.Label(timer_frame, text="Minutes", bg='cyan', fg='orange').grid(row=1, column=1)

        self.seconds_label = tk.Label(timer_frame, text="00", font=("Arial", 24, "bold"), bg='black', fg='red', width=4)
        self.seconds_label.grid(row=0, column=2, padx=5)
        tk.Label(timer_frame, text="Seconds", bg='cyan', fg='orange').grid(row=1, column=2)

        # Image display
        self.image_label = tk.Label(self.root, bg='cyan')
        self.image_label.pack(pady=10)

        # Status
        self.status_label = tk.Label(self.root, text="Status: Waiting for PC1 connection", bg='cyan', font=("Arial", 10))
        self.status_label.pack(pady=10)

        # Data Info
        info_frame = tk.LabelFrame(self.root, text="Received Data", bg='cyan')
        info_frame.pack(pady=10, padx=20, fill='both', expand=True)

        self.info_text = tk.Text(info_frame, height=8, width=55)
        scrollbar = tk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)

        self.info_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def setup_network(self):
        self.network_manager.start_server(12346, self.handle_received_data)
        self.image_server_thread = threading.Thread(
            target=self.image_receiver_thread, args=(), daemon=True)
        self.image_server_thread.start()
        self.update_status("Listening for PC1 on ports 12346 (timer) and 12347 (image)")

    def handle_received_data(self, received_data):
        try:
            self.received_hours = received_data.get('hours', 0)
            self.received_minutes = received_data.get('minutes', 0)
            self.received_seconds = received_data.get('seconds', 0)
            self.update_display()
            self.update_status(f"Received data from {received_data.get('send_id', 'PC1')}")

            log_entry = (f"[{datetime.now().strftime('%H:%M:%S')}] "
                         f"From: {received_data.get('send_id', 'Unknown')}, "
                         f"Timer: {self.received_hours:02d}:{self.received_minutes:02d}:{self.received_seconds:02d}, "
                         f"Status: {received_data.get('status', 'Unknown')}\n")
            self.log_data(log_entry)

            # Optional: Acknowledge to PC1
            ack_data = {
                'send_id': 'PC2',
                'receive_id': 'PC1',
                'status': 'received',
                'timestamp': datetime.now().isoformat()
            }
            self.network_manager.send_data('127.0.0.1', 12345, ack_data)

        except Exception as e:
            self.update_status(f"Data handling error: {str(e)}")

    def image_receiver_thread(self):
        image_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        image_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        image_socket.bind(('', 12347))
        image_socket.listen(1)
        while True:
            conn, addr = image_socket.accept()
            self.network_manager.client_socket = conn
            image_path = "received/received_image.jpg"
            if self.network_manager.receive_image(image_path):
                self.display_image(image_path)
            conn.close()

    def display_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
            self.update_status("Image received and displayed")
        except Exception as e:
            self.update_status(f"Error displaying image: {str(e)}")

    def update_display(self):
        self.root.after(0, lambda: [
            self.hours_label.config(text=f"{self.received_hours:02d}"),
            self.minutes_label.config(text=f"{self.received_minutes:02d}"),
            self.seconds_label.config(text=f"{self.received_seconds:02d}")
        ])

    def update_status(self, message):
        self.root.after(0, lambda: self.status_label.config(text=f"Status: {message}"))

    def log_data(self, message):
        self.root.after(0, lambda: [
            self.info_text.insert(tk.END, message),
            self.info_text.see(tk.END)
        ])

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.network_manager.stop_server()
        self.root.destroy()

if __name__ == "__main__":
    app = PC2Application()
    app.run()
