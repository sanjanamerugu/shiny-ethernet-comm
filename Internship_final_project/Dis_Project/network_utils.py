import socket
import threading
import json
import os

class NetworkManager:
    def __init__(self):
        self.server_socket = None
        self.is_server_running = False
        self.server_thread = None
        self.data_handler = None
        self.client_socket = None  # Needed for image transfer receive

    def start_server(self, port, data_handler):
        """Start server to listen for incoming JSON data"""
        self.data_handler = data_handler
        self.server_thread = threading.Thread(target=self._run_server, args=(port,), daemon=True)
        self.server_thread.start()

    def _run_server(self, port):
        """Internal server loop for JSON data"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', port))
            self.server_socket.listen(5)
            self.is_server_running = True

            while self.is_server_running:
                try:
                    client_socket, address = self.server_socket.accept()
                    threading.Thread(target=self._handle_client, args=(client_socket,), daemon=True).start()
                except socket.error:
                    break

        except Exception as e:
            print(f"Server error: {str(e)}")

    def _handle_client(self, client_socket):
        """Handle individual client connections for JSON"""
        try:
            data = client_socket.recv(1024).decode()
            if data and self.data_handler:
                received_data = json.loads(data)
                self.data_handler(received_data)
        except Exception as e:
            print(f"Client handling error: {str(e)}")
        finally:
            client_socket.close()

    def send_data(self, host, port, data):
        """Send JSON data to specified host and port"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            client_socket.connect((host, port))

            data_json = json.dumps(data)
            client_socket.send(data_json.encode())
            client_socket.close()
            return True

        except Exception as e:
            print(f"Send error: {str(e)}")
            return False

    def stop_server(self):
        """Stop the JSON data server"""
        self.is_server_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass

    # ─────────────────────────────────────────────
    #              IMAGE TRANSFER SUPPORT
    # ─────────────────────────────────────────────

    def send_image(self, host, port, image_path):
        """Send an image file to a client"""
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()

            # Open a new connection
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            # Send length first (8 bytes)
            client_socket.sendall(len(image_data).to_bytes(8, 'big'))
            # Send image data
            client_socket.sendall(image_data)
            client_socket.close()

            print("Image sent successfully.")
            return True
        except Exception as e:
            print(f"Image send error: {str(e)}")
            return False

    def receive_image(self, save_path):
        """Receive image from connected socket and save to disk"""
        try:
            # First, receive the 8-byte length
            image_size = int.from_bytes(self.client_socket.recv(8), 'big')

            # Now receive the image content
            received_data = b''
            while len(received_data) < image_size:
                chunk = self.client_socket.recv(4096)
                if not chunk:
                    break
                received_data += chunk

            # Save the image
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(received_data)

            print(f"Image saved to {save_path}")
            return True
        except Exception as e:
            print(f"Image receive error: {str(e)}")
            return False
