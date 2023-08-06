import sys
import tty
import termios
import os
import time
import fcntl
try:
    from . import term
except ImportError:
    import term
try:
    from .ctrl import *
except ImportError:
    from ctrl import *
import sys
class NoBufReader:
    def __init__(self,file):
        self.fileno=file.fileno
        self.encoding=file.encoding
        self.fd=self.fileno()
        self.file=file
    def read(self,size):
        return self.file.read(size)

def _getkey_nonblocking(tout=0.1,catch=False):
    char=''
    buffer=buf(NoBufReader(sys.stdin),catch)
    e=False
    for _ in range(round(tout/0.0001)):
        a=next(buffer)
        if a:
            if not e:
                e=True
            char+=a
        else:
            if e:
                break
        try:    
            time.sleep(0.0001)
        except KeyboardInterrupt:
            if not catch:
                raise
            if not e:
                e=True
            char+='\x03'
            
    return char

def _getkey_blocking(tout=0.01,catch=False):
    char=''
    buffer=buf(NoBufReader(sys.stdin),catch)
    entering=False
    for c in buffer:
        if not c:
            if entering:
                break
        else:
            if not entering:
                entering=True
            char+=c
        try:
            time.sleep(0.0001)
        except KeyboardInterrupt:
            if not catch:
                raise
            if not entering:
                entering=True
            char+='\x03'
    return char
            

def _getkey(blocking=True,tout=0.1,catch=False):
    if blocking:
        return _getkey_blocking(tout,catch)
    else:
        return _getkey_nonblocking(tout,catch)
def getkey(blocking=True,tout=0.1,catch=False):
    try:
        return parse_key(_getkey(blocking,tout,catch))
    finally:
        term.buffering.on()
def buf(file,catch=False):
    fcntl.fcntl(file, fcntl.F_SETFL, os.O_NONBLOCK)

    with term.Buffering(file):
        res=''
        while True:
            try:
                a=file.read(1)
            except KeyboardInterrupt:
                if not catch:
                    raise
                a='\x03'
            yield a
