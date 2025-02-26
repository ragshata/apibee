import socket


port_range = [22,  # SSH
              23,  # Telnet
              88,  # Web Proxy
              500,  # L2TP VPN
              1194,  # Open VPN
              8080,  # Web Proxy
              3389,  # Remote Desktop
              1701,  # L2TP VPN
              1723,  # PPTP VPN
              5000,  # VPN
              9000,  # Proxy
              9001,  # Proxy
              3128,  # Proxy
              1080,  # Proxy
              8123,  # Proxy
              5500,  # VNC
              5900,  # VNC
              5901,  # VNC
              5800,  # VNC
              5801,  # VNC
]


def check_ports(target):
    for port in port_range:
        TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPsock.settimeout(0.4)
        try:
            TCPsock.connect((target, port))
            TCPsock.close()
            # print(f'Port {port} open')
            return True
        except Exception as e:
            # print(f'Port {port} close')
            # print(e)
            pass
    return False


