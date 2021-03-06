from threading import Thread, Lock

import cpu
import ppu
import sys

class Main:
  def __init__(self, filename):
    ramSize = 65*1024 #2kB CPU internal RAM, 64kB adressable
    self.memory = [0]*ramSize
    writeLock = Lock()
    readLock = Lock()

    self.cpu = cpu.CpuR2A03(self.memory, writeLock, readLock)
    self.cpu.load(filename)
    self.ppu = ppu.PpuR2C02(self.memory, writeLock, readLock)

  def start(self):
    
    #for i in range(0, 200):
    #  self.cpu.run() #Run 1 cpu cycle
    #  self.ppu.run() #Run 3 ppu cycles = 1 cpu cycles

    self.cpu.start() #Start cpu thread
    self.ppu.start() #Start ppu thread
    self.cpu.join()
    self.ppu.join()


if len(sys.argv) == 2:
  mainInstance = Main(str(sys.argv[1]))
else:
  mainInstance = Main('tests/nestest.nes')
mainInstance.start()
