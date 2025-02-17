# SFTP Client - Python GUI

This is a simple SFTP (SSH File Transfer Protocol) client application built using Python and Tkinter for the graphical user interface and Paramiko for SFTP functionality.

## Features

*   **Graphical User Interface (GUI):** Easy-to-use interface for SFTP operations.
*   **SFTP Support:** Securely connect to SFTP servers on port 22 (default).
*   **Verbose Connection Output:** Displays detailed messages during the connection process to help with debugging.
*   **Show Password Feature:** Option to temporarily reveal the password entered for verification (use with caution!).
*   **Browse Local File:**  Button to open a file dialog for selecting local files to upload or download.
*   **Upload Files:** Upload files from your local machine to the SFTP server.
*   **Download Files:** Download files from the SFTP server to your local machine.
*   **List Files:** View a list of files and directories on the remote SFTP server.
*   **Disconnect:** Safely disconnect from the SFTP server.
*   **Error Handling:** Basic error messages displayed in the output text area.

## Prerequisites

*   **Python 3.6 or later:**  Required for f-string syntax.
*   **Paramiko library:**  Install Paramiko using pip:
    ```bash
    pip install paramiko
    ```
    or
    ```bash
    pip3 install paramiko
    ```

## How to Run the GUI Client

1.  **Save the Python code:** Save the provided Python code as `stfpclient.py`.
2.  **Install Paramiko:** If you haven't already, install Paramiko: `pip install paramiko` or `pip3 install paramiko`.
3.  **Run from the command line:** Open a terminal or command prompt and navigate to the directory where you saved `stfpclient.py`. Execute the script using:
    ```bash
    python3 stfpclient.py
    ```
4.  **Enter SFTP Details:** The GUI window will appear. Enter the following information:
    *   **SFTP Host:** The hostname or IP address of the SFTP server.
    *   **Port:** The SFTP port (default is 22).
    *   **Username:** Your SFTP username.
    *   **Password:** Your SFTP password.
5.  **Connect:** Click the "Connect" button. Observe the output text area for connection messages.
6.  **Perform Operations:**
    *   **Browse Local File:** Click "Browse" to select a local file.
    *   **Enter Remote File Path:** Specify the remote file path for uploads or downloads.
    *   **Upload:** Click "Upload" to upload the selected local file to the specified remote path.
    *   **Download:** Click "Download" to download the specified remote file to the selected local path (local file path entry is used for download destination as well).
    *   **List Files:** Click "List Files" to see the file listing of the current remote directory (initially the server's default directory).
7.  **Disconnect:** Click "Disconnect" to close the SFTP connection.
8.  **Quit:** Click "Quit" to exit the application.

## Security Warning

**Important Security Notes:**

*   **`paramiko.AutoAddPolicy()`:**  This client uses `paramiko.AutoAddPolicy()` for simplicity, which automatically adds new host keys. **This is insecure for production environments.** In real-world applications, you should implement proper host key verification to prevent man-in-the-middle attacks.
*   **"Show Password" Feature:** The "Show Password" checkbox is included for debugging and convenience in **controlled, non-sensitive environments only.**  Displaying passwords in plain text on the screen is a significant security risk and should be avoided in production or when handling sensitive credentials.  Do not use this feature in untrusted environments or for sensitive accounts. Consider removing this feature for better security in general use.
*   **Password Security:** This script takes passwords as direct input in the GUI. For improved security, consider using SSH key-based authentication instead of passwords, or implement more secure password handling practices.

**Use this SFTP client responsibly and understand the security implications, especially when dealing with sensitive data or production systems.**
