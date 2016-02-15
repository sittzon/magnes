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
    self.ram[3] = 0x06
    self.ram[5] = 0xa5
    self.ram[6] = 0x03
    self.ram[7] = 0xa9
    self.ram[8] = 0xab

    #Registers
    self.regA = 0 #Accumulator register, 8 bit
    self.regX = 0 #Index register 1, 8 bit
    self.regY = 0 #Index register 2, 8 bit
    self.regS = 0 #Stack pointer, 8 bit
    self.regP = 0 #Processor status flag bits, 8 bit
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
      '0xac' : self.LDY,
      '0xad' : self.LDA,
      '0xae' : self.LDX,
      '0xb0' : self.BCS,
      '0xb1' : self.LDA,
      '0xb4' : self.LDY,
      '0xb5' : self.LDA,
      '0xb6' : self.LDX,
      '0xb8' : self.CLV,
      '0xb9' : self.LDA,
      '0xba' : self.TSX,
      '0xbc' : self.LDY,
      '0xbd' : self.LDA,
      '0xbe' : self.LDX,
      '0xc0' : self.CPY,
      '0xc1' : self.CMP,
      '0xc4' : self.CPY,
      '0xc5' : self.CMP,
      '0xc6' : self.DEC,
      '0xc8' : self.INY,
      '0xc9' : self.CMP,
      '0xca' : self.DEX,
      '0xcc' : self.CPY,
      '0xcd' : self.CMP,
      '0xce' : self.DEC,
      '0xd0' : self.BNE,
      '0xd1' : self.CMP,
      '0xd5' : self.CMP,
      '0xd6' : self.DEC,
      '0xd8' : self.CLD,
      '0xd9' : self.CMP,
      '0xdd' : self.CMP,
      '0xde' : self.DEC,
      '0xd0' : self.CPX,
      '0xde' : self.DEC,
      '0xe0' : self.CPX,
      '0xe1' : self.SBC,
      '0xe4' : self.CPX,
      '0xe5' : self.SBC,
      '0xe6' : self.INC,
      '0xe8' : self.INX,
      '0xe9' : self.SBC,
      '0xea' : self.NOP,
      '0xec' : self.CPX,
      '0xed' : self.SBC,
      '0xee' : self.INC,
      '0xf0' : self.BEQ,
      '0xf1' : self.SBC,
      '0xf5' : self.SBC,
      '0xf6' : self.INC,
      '0xf8' : self.SED,
      '0xf9' : self.SBC,
      '0xfd' : self.SBC,
      '0xfe' : self.INC
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
        tempRam[i] = int(byte.encode("hex"), 16)
        byte = f.read(1)
    finally:
      f.close()
    print("")
      
    #Verify 'NES'
    if tempRam[0] != 0x4e and tempRam[0] != 0x45 and tempRam[0] != 0x53:
      print("Not a 'NES' file! Loading incorrect")
    else:
      print("Identified 'NES' file")
      #for i in tempRam:
      #  self.ram[i] = tempRam[i+16]
      
    print("Loading complete.")

  def run(self):
    i = 0
    while (i < 16):
      #Fetch opcode, print current opcode
      self.currentOpcode = self.ram[self.PC]
      print("%(pc)08d:%(op)02x" % {"pc":self.PC, "op":self.currentOpcode}),

      #Execute Opcode
      self.ops[format(self.currentOpcode, '#04x')]()

      ##Print mnemonice and registers
      mnemonic = self.ops[format(self.currentOpcode, '#04x')].__name__
      print("     %(mnem)s" % {"mnem":mnemonic}),
      self.printRegisters()

      #Increase Program Counter
      self.PC += 1
      if (self.PC > self.ramSize):
        self.PC = 0
      i += 1
        
  def printRegisters(self):
    print('(PC:%(pc)04x, regA:%(ra)02x, regX:%(rx)02x, regY:%(ry)02x, regS:%(rs)02x, regP:%(rp)02x' %\
          {"pc":self.PC, "ra":self.regA, "rx":self.regX, "ry":self.regY, "rs":self.regS, "rp":self.regP})

  def getImmediateOperand(self):
    operand = self.ram[self.PC]
    print("#$" + format(operand, "02x")),
    return operand

  def getZeroPageOperand(self):
    adress = self.ram[self.PC]
    operand = self.ram[adress]
    print("$" + format(adress, "02x")),
    return operand

  def getZeroPageXOperand(self, adress):
    pass

  def getAbsoluteOperand(self, adress):
    pass

  def getAbsoluteXOperand(self, adress):
    pass

  def getAbsoluteYOperand(self, adress):
    pass

  def getIndirectXOperand(self, adress):
    pass

  def getIndirectYOperand(self, adress):
    pass

  #bit ->   7                           0
  #       +---+---+---+---+---+---+---+---+
  #       | N | V |   | B | D | I | Z | C |  <-- flag, 0/1 = reset/set
  #       +---+---+---+---+---+---+---+---+
  #(N)egative, O(V)erflow, (B)inary, (D)ecimal, (I)nterrupt, (Z)ero, (C)arry
  def setNegativeFlag(self):
    self.regP |= 0x80
  def clearNegativeFlag(self):
    self.regP &= 0x7f
  def setOverflowFlag(self):
    self.regP |= 0x40
  def clearOverflowFlag(self):
    self.regP &= 0xbf
  def setBinaryFlag(self):
    self.regP |= 0x10
  def clearBinaryFlag(self):
    self.regP &= 0xef
  def setDecimalFlag(self):
    self.regP |= 0x08
  def clearDecimalFlag(self):
    self.regP &= 0xf7
  def setInterruptFlag(self):
    self.regP |= 0x04
  def clearInterruptFlag(self):
    self.regP &= 0xfb
  def setZeroFlag(self):
    self.regP |= 0x02
  def clearZeroFlag(self):
    self.regP &= 0xfc
  def setCarryFlag(self):
    self.regP |= 0x01
  def clearCarryFlag(self):
    self.regP &= 0xfe

  def BRK(self):
    self.setBinaryFlag()

  def ORA(self):
    pass

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
    self.regP &= 0xfe

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
    self.PC += 1
    if self.currentOpcode == 0xa1: #Indirect, x
      self.regA = self.getIndirectXOperand()
    elif self.currentOpcode == 0xa5: #Zero page
      self.regA = self.getZeroPageOperand()
    elif self.currentOpcode == 0xa9: #Immediate
      self.regA = self.getImmediateOperand()
    elif self.currentOpcode == 0xad: #Absolute
      self.regA = self.getAbsoluteOperand()
    elif self.currentOpcode == 0xb1: #Indirect, Y
      self.regA = self.getIndirectYOperand()
    elif self.currentOpcode == 0xb5: #Zero page, X
      self.regA = self.getZeroPageXOperand()
    elif self.currentOpcode == 0xb9: #Absolute, Y
      self.regA = self.getAbsoluteYOperand()
    elif self.currentOpcode == 0xbd: #Absolute, X
      self.regA = self.getAbsoluteXOperand()

    #Check if operand is negative
    if self.regA > 0x7f:
      self.setNegativeFlag()
    else:
      self.clearNegativeFlag()

    #Check if operand is zero
    if self.regA == 0x00:
      self.setZeroFlag()
    else:
      self.clearZeroFlag()

  def BCS(self):
    pass
  
  def CLV(self):
    pass
  
  def TSX(self):
    pass
  
  def CPY(self):
    pass
  
  def CMP(self):
    pass
  
  def DEC(self):
    pass
  
  def INY(self):
    pass
  
  def DEX(self):
    pass
  
  def BNE(self):
    pass
  
  def CLD(self):
    pass
  
  def CPX(self):
    pass
  
  def SBC(self):
    pass
  
  def INC(self):
    pass
  
  def INX(self):
    pass
  
  def NOP(self):
    pass
  
  def BEQ(self):
    pass
  
  def SED(self):
    pass