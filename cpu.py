class CpuR2A03:
  def __init__(self):
    #Clock
    #Clocked 1.789773Mhz for NTSC (System 21.47727Mhz / 12) and
    #1.773447Mhz for PAL (System 26.601171Mhz / 15)
    clockHertz = 1.773447*1000000 #PAL

    #Memory - 2kB
    self.ramSize = 2*1024
    self.ram = [0]*self.ramSize
    self.ram[2] = 0x01
    self.ram[5] = 0xa9
    self.ram[6] = 0xff

    #Registers
    self.regA = 0 #Accumulator register, 8 bit
    self.regX = 0 #Index register 1, 8 bit
    self.regY = 0 #Index register 2, 8 bit
    self.regS = 0 #Stack pointer, 8 bit
    #bit ->   7                           0
    #       +---+---+---+---+---+---+---+---+
    #       | N | V |   | B | D | I | Z | C |  <-- flag, 0/1 = reset/set
    #       +---+---+---+---+---+---+---+---+
    #(N)egative, O(V)erflow, (B)inary, (D)ecimal, (I)nterrupt, (Z)ero, (C)arry
    self.regP = 0 #Processor status flag bits
    self.PC = 0 #Program counter, 16 bit
        
    # OPcodes
    self.ops = {
      '0x00' : self.BRK,
      '0x01' : self.ORA,
      '0x05' : self.ORA,
      '0x06' : self.ASL,
      '0x08' : self.PHP,
      '0x09' : self.ORA,
      '0x0a' : self.ASL,
      '0x0d' : self.ORA,
      '0x0e' : self.ASL,
      '0x10' : self.BPL,
      '0x15' : self.ORA,
      '0x16' : self.ASL,
      '0x18' : self.CLC,
      '0x19' : self.ORA,
      '0x1d' : self.ORA,
      '0x1e' : self.ASL,
      '0x20' : self.JSR,
      '0x21' : self.AND,
      '0x24' : self.BIT,
      '0x25' : self.AND,
      '0x26' : self.ROL,
      '0x28' : self.PLP,
      '0x29' : self.AND,
      '0x2a' : self.ROL,
      '0x2c' : self.BIT,
      '0x2d' : self.AND,
      '0x2e' : self.ROL,
      '0x30' : self.BMI,
      '0x31' : self.AND,
      '0x35' : self.AND,
      '0x36' : self.ROL,
      '0x38' : self.SEC,
      '0x39' : self.AND,
      '0x3d' : self.AND,
      '0x3e' : self.ROL,
      '0x40' : self.RTI,
      '0x41' : self.EOR,
      '0x45' : self.EOR,
      '0x46' : self.LSR,
      '0x48' : self.PHA,
      '0x49' : self.EOR,
      '0x4a' : self.LSR,
      '0x4c' : self.JMP,
      '0x4d' : self.EOR,
      '0x4e' : self.LSR,
      '0x50' : self.BVC,
      '0x55' : self.EOR,
      '0x56' : self.LSR,
      '0x58' : self.CLI,
      '0x58' : self.EOR,
      '0x5d' : self.EOR,
      '0x5e' : self.LSR,
      '0x60' : self.RTS,
      '0x61' : self.ADC,
      '0x65' : self.ADC,
      '0x66' : self.ROR,
      '0x68' : self.PLA,
      '0x69' : self.ADC,
      '0x6a' : self.ROR,
      '0x6c' : self.JMP,
      '0x6d' : self.ADC,
      '0x6e' : self.ROR,
      '0x70' : self.BVS,
      '0x71' : self.ADC,
      '0x75' : self.ADC,
      '0x76' : self.ROR,
      '0x78' : self.SEI,
      '0x79' : self.ADC,
      '0x7d' : self.ADC,
      '0x7e' : self.ROR,
      '0x81' : self.STA,
      '0x85' : self.STA,
      '0x86' : self.STX,
      '0x88' : self.DEY,
      '0x8a' : self.TXA,
      '0x8c' : self.STY,
      '0x8d' : self.STA,
      '0x8e' : self.STX,
      '0x90' : self.BCC,
      '0x91' : self.STA,
      '0x94' : self.STY,
      '0x95' : self.STA,
      '0x96' : self.STX,
      '0x98' : self.TYA,
      '0x99' : self.STA,
      '0x9a' : self.TXS,
      '0x9c' : self.STA,
      '0xa0' : self.LDY,
      '0xa1' : self.LDA,
      '0xa2' : self.LDX,
      '0xa4' : self.LDY,
      '0xa5' : self.LDA,
      '0xa6' : self.LDX,
      '0xa8' : self.TAY,
      '0xa9' : self.LDA,
      '0xaa' : self.TAX,
    }
    
  def load(self, filename):
    print("Loading " + filename + " ...")
    tempRam = [0]*self.ramSize
    f = open(filename, 'rb')
    try:
      byte = f.read(1)
      for i in range(0,64):#while byte != "":
        #Do something with byte
        print("0x%(byte)s" % {"byte":byte.encode("hex")}),
        #self.ram[i] = int(byte.encode("hex"), 16)
        tempRam[i] = int(byte.encode("hex"), 16)
        byte = f.read(1)
    finally:
      f.close()
    print("")
      
    #Verify 'NES'
    if tempRam[0] != 0x4e and tempRam[0] != 0x45 and tempRam[0] != 0x53:
      print("Not a 'NES' file! Loading incorrect")
    else :
      print("Identified 'NES' file")
    #self.ram = tempRam
      
    print("Loading complete.")

  def run(self):
    i = 0
    while (i < 16):
      #Fetch opcode
      self.currentOP = self.ram[self.PC]
      #self.mode = 0
      #self.operand = 0

      #Execute Opcode
      mnemonic = self.ops[format(self.currentOP, '#04x')].__name__
      print("%(pc)08d:%(op)02x %(mnem)s" % {"pc":self.PC, "op":self.currentOP, "mnem":mnemonic}),
      self.printRegisters()
      self.opcode = format(self.currentOP, '#04x')
      self.ops[self.opcode]()

      #Increase Program Counter
      self.PC += 1
      if (self.PC > self.ramSize):
        self.PC = 0
      i += 1
        
  def printRegisters(self):
    print('(PC:%(pc)2x, regA:%(ra)2x, regX:%(rx)2x, regY:%(ry)2x, regS:%(rs)2x, regP:%(rp)2x' %\
          {"pc":self.PC, "ra":self.regA, "rx":self.regX, "ry":self.regY, "rs":self.regS, "rp":self.regP})

  #BRK (BReaK)
  #Affects Flags: B
  #Mode: Implied
  def BRK(self):
    self.PC += 1;
    self.regP |= 0x10

  #ORA (Or Memory With Accumulator)
  #Affects Flags: S Z
  #Performs logical OR on operand and accumulator, stores result in accumulator
  def ORA(self):
    pass
    #Operand |= ACCUMULATOR        // OR the two values together.
    #SET_NEGATIVE(Operand);        // Clears the Negative Flag if the Operand is $#00-7F, otherwise sets it.
    #SET_ZERO(Operand);            // Sets the Zero Flag if the Operand is $#00, otherwise clears it.
    #self.regP = self.regP & 
    #ACCUMULATOR = Operand;        // Stores the Operand in the Accumulator Register.
    #self.regA =

  def ASL(self):
    pass

  def BPL(self):
    pass

  def PHP(self):
    pass

  #Jump to subroutine
  def JMP(self):
    pass

  def JSR(self):
    pass

  def AND(self):
    pass

  def BIT(self):
    pass

  def ROL(self):
    pass

  def SEC(self):
    pass

  def EOR(self):
    pass

  def PLP(self):
    pass

  def BMI(self):
    pass

  def LSR(self):
    pass

  def PHA(self):
    pass

  def BVC(self):
    pass
  
  def CLI(self):
    pass
  
  def ADC(self):
    pass
  
  def ROR(self):
    pass
  
  def PLA(self):
    pass
  
  def BVS(self):
    pass
  
  def SEI(self):
    pass
  
  def STY(self):
    pass
  
  def STX(self):
    pass
  
  def DEY(self):
    pass
  
  def TXA(self):
    pass
  
  def BCC(self):
    pass
  
  def TYA(self):
    pass
  
  def TXS(self):
    pass
  
  def TXY(self):
    pass
  
  def LDY(self):
    pass
  
  def LDX(self):
    pass
  
  def TAY(self):
    pass
  
  def TAX(self):
    pass
  
  #Clear carry flag
  def CLC(self):
    pass

  #Return to calling subroutine
  def RTS(self):
    pass

  def RTI(self):
    pass

  #Store accumulator into memory location (operand)
  def STA(self):
    pass

  #LDA (LoaD Accumulator)
  #Affects Flags: S Z
  def LDA(self):
    if self.opcode == '0xa1': #Indirect, x
      pass
    elif self.opcode == '0xa5': #Zero page
      pass
    elif self.opcode == '0xa9': #Immediatate
      self.PC += 1
      operand = self.ram[self.PC]
      if operand > 0x7f : #Negative
        pass
        #self.regP |= 0x70
      self.regA = operand
    elif self.opcode == '0xad': #Absolute
      pass
    elif self.opcode == '0xb1': #Indirect, Y
      pass
    elif self.opcode == '0xb5': #Zero page, X
      pass
    elif self.opcode == '0xb9': #Absolute, Y
      pass
    elif self.opcode == '0xbd': #Absolute, X
      pass
    pass

