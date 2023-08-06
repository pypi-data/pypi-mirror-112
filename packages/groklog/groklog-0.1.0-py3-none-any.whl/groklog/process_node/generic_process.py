import fcntl
import itertools
import os
import re
import shlex
import subprocess
import unicodedata
from threading import RLock, Thread
from time import sleep

from .base import ProcessNode


class GenericProcessIO(ProcessNode):
    def __init__(self, name: str, command: str):
        super().__init__(name=name, command=command)

        self._process = subprocess.Popen(
            shlex.split(self.command),
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        # Set stdout to be nonblocking
        fd = self._process.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        # Lock while processes are piping data in
        self._input_lock = RLock()

        self._running = True
        self._extraction_thread = Thread(
            name=f"Thread({self})", daemon=True, target=self._background
        )
        self._extraction_thread.start()

    def write(self, data: bytes):
        """Input data from an upstream process"""
        if not self._running:
            return

        with self._input_lock:
            self._process.stdin.write(data)
            self._process.stdin.flush()

    def _background(self):
        # control_chars = bytes(''.join(map(chr, itertools.chain(range(0x00,0x20), range(0x7f,0xa0)))).encode("utf-8"))
        # control_char_re = re.compile(b'[%s]' % re.escape(control_chars))

        control_chars = bytes(b"".join([b"0x03", b"0x04", b"0x018", b"0x00"]))
        control_char_re = re.compile(b"[%s]" % re.escape(b"\x03"))

        while self._running:
            self._onboard_new_subscribers()

            # Read in a non-blocking fashion up to a certain number of characters.
            data_bytes = self._process.stdout.read1(self._READ_MAX_BYTES)

            if len(data_bytes) == 0:
                # Prevent a busyloop where there's no data in stdout.
                sleep(0.1)
                continue

            # data_bytes = data_bytes.replace(bytes(0x03), b'')
            # data_bytes = data_bytes.replace(bytes(0x04), b'')
            # data_bytes = data_bytes.replace(bytes(0x018), b'')
            # data_bytes = control_char_re.sub(b'', data_bytes)
            # data_bytes = bytes(c for c in data_bytes if c == 3)
            data_bytes = data_bytes.replace(b"\x03", b"")
            self._record_and_publish(data_bytes)
