import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import os
import threading
import paramiko  # Import paramiko for SFTP

class FTPGUIClient:
    def __init__(self, master):
        self.master = master
        master.title("SFTP Client - Python")  # Changed title to SFTP Client

        # FTP Server Details Frame (Still using "FTP" in frame name for UI consistency, but it's SFTP now)
        self.server_frame = tk.Frame(master)
        self.server_frame.pack(pady=10)

        tk.Label(self.server_frame, text="SFTP Host:").grid(row=0, column=0, sticky="e") # Changed label to SFTP Host
        self.host_entry = tk.Entry(self.server_frame, width=30)
        self.host_entry.grid(row=0, column=1)

        tk.Label(self.server_frame, text="Port:").grid(row=0, column=2, padx=5, sticky="e")
        self.port_entry = tk.Entry(self.server_frame, width=5)
        self.port_entry.grid(row=0, column=3)
        self.port_entry.insert(0, "22") # Default SFTP port is 22

        tk.Label(self.server_frame, text="Username:").grid(row=1, column=0, sticky="e")
        self.user_entry = tk.Entry(self.server_frame, width=30)
        self.user_entry.grid(row=1, column=1)

        tk.Label(self.server_frame, text="Password:").grid(row=1, column=2, padx=5, sticky="e")
        self.password_entry = tk.Entry(self.server_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=3)

        self.show_password_var = tk.BooleanVar()
        self.show_password_check = tk.Checkbutton(self.server_frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility)
        self.show_password_check.grid(row=2, column=3, sticky="e", padx=5)

        # File Paths Frame
        self.file_frame = tk.Frame(master)
        self.file_frame.pack(pady=5)

        tk.Label(self.file_frame, text="Local File:").grid(row=0, column=0, sticky="e")
        self.local_file_entry = tk.Entry(self.file_frame, width=40)
        self.local_file_entry.grid(row=0, column=1)
        self.browse_button = tk.Button(self.file_frame, text="Browse", command=self.browse_local_file)
        self.browse_button.grid(row=0, column=2, padx=5)

        tk.Label(self.file_frame, text="Remote File:").grid(row=1, column=0, sticky="e")
        self.remote_file_entry = tk.Entry(self.file_frame, width=40)
        self.remote_file_entry.grid(row=1, column=1)

        # Buttons Frame
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        self.connect_button = tk.Button(self.button_frame, text="Connect", command=self.connect_ftp) # Button text still "Connect" but now for SFTP
        self.connect_button.grid(row=0, column=0, padx=5)

        self.upload_button = tk.Button(self.button_frame, text="Upload", command=self.upload_file, state=tk.DISABLED)
        self.upload_button.grid(row=0, column=1, padx=5)

        self.download_button = tk.Button(self.button_frame, text="Download", command=self.download_file, state=tk.DISABLED)
        self.download_button.grid(row=0, column=2, padx=5)

        self.list_button = tk.Button(self.button_frame, text="List Files", command=self.list_files, state=tk.DISABLED)
        self.list_button.grid(row=0, column=3, padx=5)

        self.quit_button = tk.Button(self.button_frame, text="Quit", command=master.quit)
        self.quit_button.grid(row=0, column=4, padx=5)

        # Output Text Area
        self.output_text = scrolledtext.ScrolledText(master, height=10, width=80)
        self.output_text.pack(pady=10, padx=10)
        self.output_text.config(state=tk.DISABLED) # Make it read-only

        self.ftp_session = None # Now this will store paramiko SFTP client or None
        self.ssh_client = None # Store SSH client object
        self.connected = False

    def browse_local_file(self):
        filename = filedialog.askopenfilename()
        self.local_file_entry.delete(0, tk.END)
        self.local_file_entry.insert(0, filename)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def connect_ftp(self): # Still using "connect_ftp" function name for UI button consistency, but it's SFTP connect now
        host = self.host_entry.get()
        port_str = self.port_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()

        if not host or not user or not password:
            self.update_output("Error: Please fill in Host, Username, and Password.")
            return

        try:
            port = int(port_str) if port_str else 22 # Default SFTP port
        except ValueError:
            self.update_output("Error: Invalid port number.")
            return

        # Run connection in a thread to prevent GUI freeze
        threading.Thread(target=self._connect_ftp_thread, args=(host, port, user, password)).start()

    def _connect_ftp_thread(self, host, port, user, password):
        try:
            self.ssh_client = paramiko.SSHClient() # Create SSH client object
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # WARNING: Insecure for production - auto-adds host key
            self.update_output(f"Connecting to SFTP server {host}:{port}...") # Updated output message
            self.ssh_client.connect(hostname=host, port=port, username=user, password=password) # SSH connect
            self.update_output(f"SSH connection to {host}:{port} established.") # Updated output message
            self.update_output(f"Opening SFTP channel...") # Added output message
            self.ftp_session = self.ssh_client.open_sftp() # Open SFTP channel
            self.update_output(f"SFTP channel opened successfully.") # Added output message
            self.update_output(f"SFTP Server connected.") # Updated output message
            self.connected = True
            self.enable_buttons()
        except Exception as e:
            self.update_output(f"SFTP Connection failed: {e}") # Updated output message
            self.update_output(f"Error details: {e}") # Added error details
            self.connected = False
            self.disable_buttons()
            if self.ssh_client: # Close SSH client if connection failed
                self.ssh_client.close()
                self.ssh_client = None
            self.ftp_session = None # Ensure ftp_session is None on failure

    def upload_file(self):
        if not self.connected:
            self.update_output("Error: Not connected to SFTP server.") # Updated error message
            return

        local_file_path = self.local_file_entry.get()
        remote_file_path = self.remote_file_entry.get()

        if not local_file_path or not remote_file_path:
            self.update_output("Error: Please specify both local and remote file paths.")
            return

        if not os.path.exists(local_file_path):
            self.update_output("Error: Local file path does not exist.")
            return

        # Run upload in a thread
        threading.Thread(target=self._upload_file_thread, args=(local_file_path, remote_file_path)).start()

    def _upload_file_thread(self, local_file_path, remote_file_path):
        try:
            self.update_output(f"Uploading '{local_file_path}' to '{remote_file_path}'...") # Added output message
            self.ftp_session.put(local_file_path, remote_file_path) # Using sftp.put for SFTP upload
            self.update_output(f"File '{local_file_path}' uploaded to '{remote_file_path}' successfully.") # Updated output message
        except Exception as e:
            self.update_output(f"SFTP Upload failed: {e}") # Updated error message

    def download_file(self):
        if not self.connected:
            self.update_output("Error: Not connected to SFTP server.") # Updated error message
            return

        remote_file_path = self.remote_file_entry.get()
        local_file_path = self.local_file_entry.get() # Using local file entry also for download destination

        if not remote_file_path or not local_file_path:
            self.update_output("Error: Please specify both remote and local file paths.")
            return

        # Run download in a thread
        threading.Thread(target=self._download_file_thread, args=(remote_file_path, local_file_path)).start()

    def _download_file_thread(self, remote_file_path, local_file_path):
        try:
            self.update_output(f"Downloading '{remote_file_path}' to '{local_file_path}'...") # Added output message
            self.ftp_session.get(remote_file_path, local_file_path) # Using sftp.get for SFTP download
            self.update_output(f"File '{remote_file_path}' downloaded to '{local_file_path}' successfully.") # Updated output message
        except Exception as e:
            self.update_output(f"SFTP Download failed: {e}") # Updated error message

    def list_files(self):
        if not self.connected:
            self.update_output("Error: Not connected to SFTP server.") # Updated error message
            return

        # Run file listing in a thread
        threading.Thread(target=self._list_files_thread).start()

    def _list_files_thread(self):
        try:
            self.update_output("Fetching file list from SFTP server...") # Added output message
            files = self.ftp_session.listdir() # Using sftp.listdir for SFTP file listing
            output = "File listing:\n" + "\n".join(files)
            self.update_output(output)
            self.update_output("File list fetched successfully.") # Added output message
        except Exception as e:
            self.update_output(f"Error listing files on SFTP server: {e}") # Updated error message

    def update_output(self, message):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)

    def enable_buttons(self):
        self.upload_button.config(state=tk.NORMAL)
        self.download_button.config(state=tk.NORMAL)
        self.list_button.config(state=tk.NORMAL)
        self.connect_button.config(text="Disconnect", command=self.disconnect_ftp)

    def disable_buttons(self):
        self.upload_button.config(state=tk.DISABLED)
        self.download_button.config(state=tk.DISABLED)
        self.list_button.config(state=tk.DISABLED)
        self.connect_button.config(text="Connect", command=self.connect_ftp)

    def disconnect_ftp(self):
        if self.ftp_session:
            try:
                self.ftp_session.close() # Close SFTP session
                self.update_output("SFTP channel closed.") # Updated output message
            except Exception as e:
                self.update_output(f"Error during SFTP channel close: {e}") # Updated output message
            self.ftp_session = None # Set SFTP session to None

        if self.ssh_client: # Close SSH connection
            try:
                self.ssh_client.close()
                self.update_output("Disconnected from SFTP server.") # Updated output message
            except Exception as e:
                self.update_output(f"Error during disconnection from SFTP server: {e}") # Updated output message
            self.ssh_client = None # Set SSH client to None

        self.connected = False
        self.disable_buttons()
        self.connect_button.config(text="Connect", command=self.connect_ftp)


if __name__ == "__main__":
    root = tk.Tk()
    gui = FTPGUIClient(root)
    root.mainloop()
