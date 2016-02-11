class CpuR2A03:
  #Clock
  #Clocked 1.789773Mhz for NTSC (System 21.47727Mhz / 12) and 
  #1.773447Mhz for PAL (System 26.601171Mhz / 15)
  clockHertz = 1.773447*1000000 #PAL
    
  def __init__(self):
    #Memory - 2kB
    self.ramSize = 2*1024
    self.ram = [0]*self.ramSize
    self.ram[2] = 16
      
    #Registers
    self.regA = 0 #Accumulator register, 8 bit
    self.regX = 0 #Index register 1, 8 bit
    self.regY = 0 #Index register 2, 8 bit
    self.regS = 0 #Stack pointer, 8 bit
    self.regP = 0 #Processor status flag bits, (N)egative,(O)Verflow,(B)inary,I,(Z)ero,(C)arry
    self.PC = 0 #Program counter, 16 bit
        
    # OPcodes
    self.ops = {
      0 : self.BRK,
      1 : self.ORA,
      2 : self.opCode2,
      3 : self.opCode3,
      4 : self.opCode4,
      5 : self.opCode5,
      6 : self.opCode6,
      7 : self.opCode7,
      8 : self.opCode8,
      9 : self.opCode9
    }
    
  def load(self, filename):
    print("Loading " + filename + " ...")
    print("Loading complete.")

  def run(self):
    i = 0
    while (i < 10):
      #Fetch opcode
      currentRam = self.ram[self.PC]
      self.currentOP = (currentRam & 240) >> 4 #1111 0000 = 240
          
      #Execute Opcode
      self.ops[int(self.currentOP)]()

      #Increase Program Counter
      self.PC += 1
      i += 1
      if (self.PC > self.ramSize):
        self.PC = 0
        
  def printRegisters(self):
    print("PC:" + str(self.PC) + ", regA:" + str(self.regA) + ", regX:" + str(self.regX)+ ", regY:" + str(self.regY)+ ", regS:" + str(self.regS)+ ", regP:" + str(self.regP) + ", RAM: " + str(self.ram[self.PC]))
    
  #BRK (BReaK)
  #Affects Flags: B
  #Mode: Implied
  #HEX: 0x00
  def BRK(self):
    print("0x00:BRK"),
    self.printRegisters()

  #ORA (Or Memory With Accumulator)
  #Affects Flags: S Z
  #Performs logical OR on operand and accumulator, stores result in accumulator
  #Mode: Indirect
  def ORA(self):
    print("0x01:ORA"),
    self.printRegisters()
    #Operand |= ACCUMULATOR        // OR the two values together.
    #SET_NEGATIVE(Operand);        // Clears the Negative Flag if the Operand is $#00-7F, otherwise sets it.
    #SET_ZERO(Operand);            // Sets the Zero Flag if the Operand is $#00, otherwise clears it.
    #self.regP = self.regP & 
    #ACCUMULATOR = Operand;        // Stores the Operand in the Accumulator Register.
    #self.regA = 
        
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
