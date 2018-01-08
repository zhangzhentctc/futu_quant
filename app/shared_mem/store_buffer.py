import mmap
import contextlib
import time
import os
import threading
import random
import json

FILE_DFT_NAME = "./tick_store_buff.dat"
FILE_DFT_SIZE = 1024 * 32

RET_ERR = -1
RET_OK = 0

class store_buffer:
    def __init__(self, buffer_size = FILE_DFT_SIZE):
        self.buffer_size = buffer_size
        self.mutex_lock = threading.Lock()

    def initialize(self):
        try:
            self.f_handler = open(FILE_DFT_NAME, "w")
        except:
            print("Buffer File Creation Fail")
            return RET_ERR

        try:
            self.f_handler.write('\x00' * self.buffer_size)
        except:
            print("Buffer Reset Fail")
            return RET_ERR

        self.f_handler.close()

        try:
            self.f_handler = open(FILE_DFT_NAME, "r+")
        except:
            print("Buffer File Opening Fail")
            return RET_ERR

        return RET_OK

    def open_mmap(self):
        try:
            self.mmap = mmap.mmap(self.f_handler.fileno(), self.buffer_size, access=mmap.ACCESS_WRITE)
        except:
            print("MMap Fail")
            return RET_ERR

    def close_mmap(self):
        self.mmap.close()

    def buffer_read(self):
        self.mmap.seek(0)
        s = self.mmap.read(self.buffer_size).decode().replace('\x00', '')
        return RET_OK, s

    def buffer_reset(self):
        self.mmap.seek(0)
        blank = "\0" * self.buffer_size
        self.mmap.write(blank.encode())
        return RET_OK

    def buffer_write(self, str):
        self.mmap.seek(0)
        try:
            self.mmap.write(str.encode())
        except:
            print("buffer is full!")
        self.mmap.flush()

