import cpu
import ppu

class Main:
    def __init__(self):
        self.ppu = ppu.PpuR2C02()
        self.cpu = cpu.CpuR2A03()

    def start(self, filename):
        self.cpu.load(filename)
        self.cpu.powerUp()
        self.cpu.run()

mainInstance = Main()
mainInstance.start('tests/nestest.nes')
