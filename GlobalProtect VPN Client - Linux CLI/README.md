## GlobalProtect VPN Client - Linux CLI

This guide provides a simple way to connect to GlobalProtect VPN on Linux using the command-line interface (CLI).

**Connecting to the VPN:**

Use the following command to initiate the connection:

```bash
sudo openconnect --protocol=gp <IP Address/Domain>
```

Replace `<IP Address/Domain>` with the actual IP address or domain name of your GlobalProtect server.

**Handling SSL Certificate Verification Issues:**

If you encounter issues verifying the SSL certificate, the CLI will display a message similar to:

```
To trust this server in future, perhaps add this to your command line: --servercert pin-sha256:********************************************
```

In such cases, use the suggested command, including the provided `pin-sha256` value:

```bash
sudo openconnect --protocol=gp <IP Address/Domain> --servercert pin-sha256:********************************************
```

**Authentication:**

After running the `openconnect` command, you will be prompted for your login credentials:

```
Enter login credentials
Username: ********
Password: ********
```

Enter your username and password to authenticate.

**Successful Connection:**

Upon successful authentication, the connection will be established.

**Reference:**

For further information and potential troubleshooting, see this issue on the OpenConnect GitLab repository: [https://gitlab.com/openconnect/openconnect/-/issues/491](https://gitlab.com/openconnect/openconnect/-/issues/491)
