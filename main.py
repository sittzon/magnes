__author__ = 'Sittzon'
#To change this template use Tools | Templates.
#

class PpuR2C02:

    #Constants
    #xRes = 256 
    #yRes = 240 #224 for NTSC
    def __init__(self):
        self.spriteArray = []

class CpuR2A03:
	
    #Opcodes
    
    #mnenmonics
    
    #Memory - 2kB
    #ramSize = 2*1024
    #ram = [0]*ramSize
    
    #Program counter
    #PC = 0
    
    #Clock
    #Clocked 1.789773Mhz for NTSC (System 21.47727Mhz / 12) and 
    #1.773447Mhz for PAL (System 26.601171Mhz / 15)
    clockHertz = 1.773447*1000000 #PAL
    
    def __init__(self):
        self.PC = 0
        self.ramSize = 2*1024
        self.ram = [0]*self.ramSize
        
        # Setup opcodes
        self.ops = {
            0 : self.opCode0
        }
        pass

    def run(self):
        i = 0
        while (i < 10):
            #Fetch opcode
            self.currentOP = self.ram[self.PC]
            
            #Execute Opcode
            #print("Ram: ".join(str(self.currentOP)))
            self.ops[int(self.currentOP)]()
            
            #Increase Program Counter
            self.PC += 1
            i += 1
            if (self.PC > self.ramSize):
                self.PC = 0

    def opCode0(self):
        print("OPcode 0")

class Main:
    def __init__(self):
        print("Init PPU...")
        self.ppu = PpuR2C02()
        print("Init CPU...")
        self.cpu = CpuR2A03()

    def start(self, filename):
        print("Starting " + filename)
        self.cpu.run()

mainInstance = Main()
mainInstance.start('something.nes')

    
