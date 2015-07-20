import socket
import struct

class SSDP:
    SSDP_ADDR = "239.255.255.250"
    SSDP_PORT = 1900

    def __init__(self, web_addr, web_port):
        self.web_addr = web_addr
        self.web_port = web_port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        mreq = struct.pack("=4sl", socket.inet_aton(self.SSDP_ADDR), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        sock.bind(("", self.SSDP_PORT))

        while True:
            data, addr = sock.recvfrom(1024)

            ssdp_response = "HTTP/1.1 200 OK\r\n" + \
                            "CACHE-CONTROL: max-age=86400\r\n" + \
                            "EXT:\r\n" + \
                            "LOCATION: http://%s:%d/setup.xml\r\n" % (self.web_addr, self.web_port) + \
                            "OPT: \"http://schemas.upnp.org/upnp/1/0/\"; ns=01\r\n" + \
                            "01-NLS: 776c1cbc-790a-425f-a890-a761ec57513c\r\n" + \
                            "ST: urn:schemas-upnp-org:device:basic:1\r\n" + \
                            "USN: uuid:Socket-1_0-00000000000001::urn:Belkin:device:**\r\n" + \
                            "\r\n"

            sock_responder = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock_responder.sendto(ssdp_response, addr)
