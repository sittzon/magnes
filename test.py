import cpu
import ppu

class Main:
    def __init__(self, filename):
        self.ppu = ppu.PpuR2C02()
        self.cpu = cpu.CpuR2A03(filename)

    def start(self):
        self.cpu.start() #Start cpu thread
        self.ppu.start() #Start ppu thread

mainInstance = Main('tests/nestest.nes')
mainInstance.start()
