from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def connect_and_check_ports(ip_or_dns, username, password):
    # Define connection parameters
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip_or_dns,
        'username': username,
        'password': password,
    }

    try:
        # Attempt connection via Telnet
        connection = ConnectHandler(**device)
        print("Telnet connection successful")
    except (NetMikoTimeoutException, NetMikoAuthenticationException):
        print("Telnet connection failed, trying SSH")
        device['device_type'] = 'cisco_ios'
        
        try:
            # Attempt connection via SSH
            connection = ConnectHandler(**device)
            print("SSH connection successful")
        except (NetMikoTimeoutException, NetMikoAuthenticationException):
            print("Connection failed for both Telnet and SSH")
            return None

    # Run command to check the status of the ports
    output = connection.send_command("show interface status")
    connection.disconnect()
    
    # Count how many ports are up, excluding portchannel interfaces
    active_ports = sum(1 for line in output.splitlines() if "connected" in line.lower() and not line.lower().startswith("po"))

    return active_ports

if __name__ == "__main__":
    # Get IP address, username, and password from the user
    ip_or_dns = input("Enter the device IP or DNS: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # If the user did not provide a username or password, use defaults
    if not username:
        username = 'nmtg'
    if not password:
        password = 'NRSFHn31'

    active_ports = connect_and_check_ports(ip_or_dns, username, password)
    
    if active_ports is not None:
        print(f"Found {active_ports} active ports on the device.")
    else:
        print("Failed to connect to the device.")
