import queue

from socket import *

import select
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

server = socket()
server.connect(("INSERT SERVER IP", 2401))

def ask_for_name():
    def on_pressed_enter_chat():
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("No Name", "Please enter your name!")
            return

        window.destroy()

        enter_chat(name)

    window = tk.Tk()
    window.title("Lazy Text App")
    window.geometry("300x150")
    window.resizable(False, False)

    enter_name_label = tk.Label(window, text="Enter your name:", font=("Arial", 12))
    enter_name_label.pack(pady=20)

    name_entry = tk.Entry(window, font=("Arial", 12))
    name_entry.pack(pady=5)
    name_entry.focus()

    submit_button = tk.Button(window, text="Enter Chat", font=("Arial", 12), command=on_pressed_enter_chat)
    submit_button.pack(pady=10)

    window.mainloop()

def enter_chat(self_name):
    window = tk.Tk()
    window.title("Lazy Text App")
    window.geometry("600x400")
    window.resizable(True, True)

    chat_area = scrolledtext.ScrolledText(window, state="disabled", font=("Arial", 12))
    chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def print_message(username, msg):
        chat_area.config(state="normal")
        
        if username == self_name:
            chat_area.insert(tk.END, "- " + username + "(You)\n")
        else:
            chat_area.insert(tk.END, "- " + username + "\n")

        chat_area.insert(tk.END, msg + "\n\n")
        chat_area.config(state="disabled")
        chat_area.see(tk.END)

    def update():
        should_read, _, _ = select.select([server], [], [], 0.0)
        if should_read:
            server_message = server.recv(1001).decode()
            server_message_parts = server_message.split("\"")

            username = server_message_parts[0]
            msg = server_message_parts[2]

            print_message(username, msg)

        window.after(100, update)

    window.after(100, update)

    entry_frame = tk.Frame(window)
    entry_frame.pack(fill=tk.X, padx=10, pady=5)

    msg_entry = tk.Entry(entry_frame, font=("Arial", 12))
    msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def on_pressed_send():
        msg = msg_entry.get().strip()
        msg_entry.delete(0, tk.END)

        server_msg = f"\"{self_name}\",\"{msg}\""
        server.send(server_msg.encode())

    send_btn = tk.Button(entry_frame, text="Send", command=on_pressed_send)
    send_btn.pack(side=tk.LEFT, padx=5)

    window.mainloop()

ask_for_name()