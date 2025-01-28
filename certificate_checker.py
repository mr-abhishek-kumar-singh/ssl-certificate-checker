import ssl
import socket
from datetime import datetime

def check_certificate(hostname, port):
    """
    Checks the SSL/TLS certificate of a given hostname and port.

    Args:
        hostname (str): The domain or IP address of the server.
        port (int): The port number (e.g., 443 for HTTPS).

    Returns:
        None
    """
    try:
        context = ssl.create_default_context()  # Generates a default SSL context
        with socket.create_connection((hostname, port)) as sock:  # Connects to the host and port
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:  # Wraps connection with SSL context
                cert = ssock.getpeercert()  # Retrieves the SSL certificate
                expiry = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")  # Extracts expiration date
                
                print(f"Certificate for {hostname} expires on: {expiry}")
                if expiry < datetime.now():
                    print("[!] Certificate has expired!")
                else:
                    print("[+] Certificate is valid.")
    except Exception as e:
        print(f"Error: Unable to check certificate for {hostname}:{port}. {e}")

# Get user input for hostname and port
hostname = input("Enter the hostname (e.g., google.com): ")
try:
    port = int(input("Enter the port (default: 443): ") or 443)
    check_certificate(hostname, port)
except ValueError:
    print("Error: Port must be a valid integer.")
