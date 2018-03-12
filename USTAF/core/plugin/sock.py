import socket, time
import traceback

class SOCK(object):
    def __init__(self, address, port, timeout=10):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print address,port
        self.sock.connect((address, port))
        time.sleep(1)
        self.timeout = timeout

    def communicate(self, cmd):
        self.sock.send(cmd)
        s = ''
        try:
            self.sock.settimeout(self.timeout)
            frag = self.sock.recv(1024)
            s = frag
            while len(frag) > 0:
                frag = self.sock.recv(1024)
                s += frag
        except socket.timeout:
            print(traceback.format_exc())
            return '-2'

        return s

    def finish(self):
        self.sock.close()

if __name__ == '__main__':
    s = SOCK('10.239.140.27', 52587,1)
    rc = s.communicate('PIT_Linux_IVI_MAGNA_001')
    print rc
