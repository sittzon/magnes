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
    #Clock
    #Clocked 1.789773Mhz for NTSC (System 21.47727Mhz / 12) and 
    #1.773447Mhz for PAL (System 26.601171Mhz / 15)
    clockHertz = 1.773447*1000000 #PAL
    
    def __init__(self):
        #Memory - 2kB
        self.ramSize = 2*1024
        self.ram = [0]*self.ramSize
        self.ram[2] = 2
        
        #Registers
        self.regA = 0 #Accumulator register, 8 bit
        self.regX = 0 #Index register 1, 8 bit
        self.regY = 0 #Index register 2, 8 bit
        self.regS = 0 #Stack pointer, 8 bit
        self.regP = 0 #Processor status flag bits, Negative(O)VerflowBinaryIZC
        self.PC = 0 #Program counter, 16 bit
        
        # OPcodes
        self.ops = {
            0 : self.opCode0,
            1 : self.opCode1,
            2 : self.opCode2,
            3 : self.opCode3,
            4 : self.opCode4,
            5 : self.opCode5,
            6 : self.opCode6,
            7 : self.opCode7,
            8 : self.opCode8,
            9 : self.opCode9
        }

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
    
    def opCode1(self):
        print("OPcode 1")
        
    def opCode2(self):
        print("OPcode 2")
        
    def opCode3(self):
        print("OPcode 3")
        
    def opCode4(self):
        print("OPcode 4")
        
    def opCode5(self):
        print("OPcode 5")
        
    def opCode6(self):
        print("OPcode 6")
        
    def opCode7(self):
        print("OPcode 7")
        
    def opCode8(self):
        print("OPcode 8")
        
    def opCode9(self):
        print("OPcode 9")

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

    
