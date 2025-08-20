import tkinter as tk
from login_window import LoginWindow
from pc2_receiver import PC2Application

def main():
    """Main function to choose which PC to run"""
    choice_root = tk.Tk()
    choice_root.title("Choose PC")
    choice_root.geometry("300x150")
    choice_root.configure(bg='lightgray')
    
    tk.Label(choice_root, text="Select which PC to run:", 
             font=("Arial", 12), bg='lightgray').pack(pady=20)
    
    def run_pc1():   
        choice_root.destroy()
        login_window = LoginWindow()
        login_window.root.mainloop()
    
    def run_pc2():
        choice_root.destroy()
        pc2_app = PC2Application()
        pc2_app.run()
    
    pc1_btn = tk.Button(choice_root, text="PC1 (Timer + Login)", command=run_pc1,
                       bg='green', fg='white', font=("Arial", 10, "bold"), width=20)
    pc1_btn.pack(pady=5)
    
    pc2_btn = tk.Button(choice_root, text="PC2 (Receiver)", command=run_pc2,
                       bg='blue', fg='white', font=("Arial", 10, "bold"), width=20)
    pc2_btn.pack(pady=5)
    
    choice_root.mainloop()

if __name__ == "__main__":
    main()