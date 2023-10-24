import time
import os
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DataForwarder:
    def __init__(self, server_url):
        self.server_url = server_url

    def forward_data(self, data):
        headers = {'Content-Type': 'application/json'}  # Set the Content-Type to indicate JSON data
        response = requests.post(self.server_url, json=data, headers=headers)  # Send data as JSON
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
                combined_data =  new_data  # Append new data to existing data
                data = {
                    'log_data': combined_data,
                    'file_name': os.path.basename(event.src_path)  # Include the filename in the data
                    
                }
                self.data_forwarder.forward_data(data)



if __name__ == "__main__":
    server_url = "http://127.0.0.1:8000/forwarder-data/"  
    data_forwarder = DataForwarder(server_url)

    path = "C:\\Users\\ashhe\\Desktop\\log-monitor"

    event_handler = FileHandler(data_forwarder)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
