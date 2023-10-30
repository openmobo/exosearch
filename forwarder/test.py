import tkinter as tk
from tkinter import Entry
from tkinter import ttk
import jwt
import time
import os
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import socket

# Check if the user is already logged in
logged_in = False

STATIC_TOKEN = os.environ.get('STATIC_TOKEN')
email_file = "user_email.txt"

# Create global variables for email_entry and password_entry
email_entry = None
password_entry = None

class DataForwarder:
    def __init__(self, server_url):
        self.server_url = server_url

    def forward_data(self, data):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {STATIC_TOKEN}'  
        }
        response = requests.post(self.server_url, json=data, headers=headers)
        if response.status_code == 201:
            print("Data forwarded successfully")
        else:
            print(f"Error forwarding data. Status code: {response.status_code}")

class FileHandler(FileSystemEventHandler):
    def __init__(self, data_forwarder):
        self.data_forwarder = data_forwarder

    def on_modified(self, event):
        if not event.is_directory and event.event_type == 'modified':
            with open(event.src_path, 'r') as file:
                new_data = file.read()
                new_data1 = new_data
                print(new_data1)
                combined_data = new_data  # Append new data to existing data

                host = socket.gethostname()  # Get the host name
                print("host: " + host)

                email = get_user_email()  # Read email from the file
                data = {
                    'log_data': combined_data,
                    'file_name': os.path.basename(event.src_path),
                    "host": host,
                    "isForwarder": True,
                    "email": email  
                }
                self.data_forwarder.forward_data(data)

def save_user_email(email):
    with open(email_file, 'w') as file:
        file.write(email)

def get_user_email():
    if os.path.exists(email_file):
        with open(email_file, 'r') as file:
            return file.read()
    return ""

def submit_data():
    global logged_in

    email = email_entry.get()
    password = password_entry.get()

    dataLogin = {
        'email': email,
        'password': password,
    }

    if not logged_in:
        headers = {'Content-Type': 'application/json'}
        urlLogin = "http://127.0.0.1:8000/login"
        
        response1 = requests.post(urlLogin, json=dataLogin, headers=headers)

        if response1.status_code == 200:
            print("Login Data submitted successfully")

            save_user_email(email)  # Save the email to the file

            token = response1.cookies.get('jwt')

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            print(token)
            if token:
                try:
                    decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
                    print("Decoded Token:", decoded_token)
                except jwt.ExpiredSignatureError:
                    print("JWT token has expired.")
                except jwt.DecodeError:
                    print("JWT token decode error.")
        else:
            print(f"Error submitting data. Status code: {response1.status_code}")

def open_window_if_no_email():
    if not os.path.exists(email_file) or os.path.getsize(email_file) == 0:
        open_window()
    else:
        print("Email found in the file. Not opening the window")

def open_window():
    # Create a window
    window = tk.Tk()
    window.title("User Input and Data Forwarding")

    global email_entry, password_entry  # Make email_entry and password_entry global

    style = ttk.Style()
    style.configure("TButton", padding=5, font=("Helvetica", 12))
    style.configure("TLabel", padding=5, font=("Helvetica", 12))

    email_label = ttk.Label(window, text="Email:")
    email_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    email_entry = Entry(window)
    email_entry.grid(row=1, column=1, padx=10, pady=5)

    password_label = ttk.Label(window, text="Password:")
    password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    password_entry = Entry(window, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    submit_button = ttk.Button(window, text="Submit User Data", command=submit_data)
    submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    server_url = "http://127.0.0.1:8000/forwarder-data/"
    data_forwarder = DataForwarder(server_url)

    path = "C:\\Users\\ashhe\\Desktop\\log-monitor"

    event_handler = FileHandler(data_forwarder)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    open_window_if_no_email()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
