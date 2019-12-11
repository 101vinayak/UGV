import sys,tty,termios
class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        if k== ('\x1b[A' and '\x1b[D'):
                print "up"
        elif k=='\x1b[B':
                print "down"
        elif k=='\x1b[C':
                print "right"
        elif k=='\x1b[D':
                print "left"
        else:
                return 0

def main():
        while(True):
                if get() == 0: break

if __name__=='__main__':
        main()
