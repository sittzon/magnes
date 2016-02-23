import threading
import cpu

class PpuR2C02 (threading.Thread):
  def __init__(self, memory, writeLock, readLock):
    threading.Thread.__init__(self)
    self.sharedMemory = memory
    self.writeLock = writeLock
    self.readLock = readLock

  def run(self):
    self.readLock.acquire()
    print("Entering ppu thread")
    print("PPU: Ram at 0xc000:" + str(format(self.sharedMemory[0xc000], "02x")))
    print("Exiting ppu thread")
    self.readLock.release()
