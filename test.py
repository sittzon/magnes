import cpu
import ppu

class Main:
    def __init__(self):
        print("Init PPU...")
        self.ppu = ppu.PpuR2C02()
        print("Init CPU...")
        self.cpu = cpu.CpuR2A03()

    def start(self, filename):
        print("Starting " + filename)
        self.cpu.run()

mainInstance = Main()
mainInstance.start('something.nes')
