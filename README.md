# 🖧 Ethernet Communication Between Two PCs

This project demonstrates **real-time Ethernet communication** between two computers (PC1 and PC2) using **Python, Tkinter, and socket programming**. The core functionality is a synchronized **timer system with GUI controls**, where one PC can control and mirror the timer running on the other.

---

## 🚀 Features

* 🔑 **Login System** – Secure login before accessing the timer.
* ⏱ **GUI Timer** – Start, Stop, and Reset functions with hour–minute–second tracking.
* 🖥 **PC1 (Controller)** – Runs the main timer and sends updates to PC2.
* 💻 **PC2 (Receiver)** – Mirrors PC1’s timer and can send commands back.
* 🌐 **Ethernet Communication** – Data exchange using IP addresses and ports.
* 📡 **Bidirectional Communication** – PC2 can also control PC1’s timer remotely.
* 🖼 **Image Transmission** – Option to send images between PCs.

---

## 🛠 Tech Stack

* **Language:** Python 3
* **GUI:** Tkinter
* **Networking:** Socket Programming (TCP)
* **Threading:** For real-time updates
* **Libraries Used:**

  * `socket`
  * `threading`
  * `tkinter`
  * `json`
  * `PIL` (for image handling)

---

## 📂 Project Structure

```
├── main.py              # Entry point – select PC1 or PC2
├── login_window.py      # Secure login window for PC1
├── pc1_timer.py         # Timer application for PC1 (controller)
├── pc2_receiver.py      # Receiver application for PC2
├── network_utils.py     # Networking functions (send/receive data)
├── received/            # Stores received images
└── README.md            # Project documentation
```

---

## ⚙️ How It Works

1. **Run `main.py`** → Choose PC1 (Timer) or PC2 (Receiver).
2. **PC1 Login** → Authenticate using username/password.
3. **Timer Control** → Start, stop, or reset timer from PC1.
4. **Data Sync** → Timer updates are sent to PC2 in real-time.
5. **PC2 Control** → Can send back Start/Stop/Reset commands to PC1.
6. **Image Transfer** → Optional image exchange feature.

---

## 🔗 Communication Protocol

**PC1 → PC2**

* Sender ID, Receiver ID
* Hours, Minutes, Seconds
* Timer Status (Running/Stopped)
* Timestamp

**PC2 → PC1**

* Sender ID, Receiver ID
* Acknowledgement (Received)
* Control Commands (Start/Stop/Reset)
* Timestamp

---

## 📸 Output Preview

* GUI-based **login window**
* Timer interface with Start/Stop/Reset
* Real-time mirrored timer on PC2
* Image transfer display

---

## 📘 References

* [Python Socket Programming – Real Python](https://realpython.com/python-sockets/)
* [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
* [Threading in Python](https://realpython.com/intro-to-python-threading/)

---

## ✅ Conclusion

This project highlights how to:

* Build **GUI-based interactive applications**.
* Use **socket programming for inter-PC communication**.
* Implement **real-time synchronization** across systems.
* Gain practical skills in **networking, threading, and GUI development**.

