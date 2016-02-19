class CpuR2A03:
  def __init__(self):
    #Clock
    #Clocked 1.789773Mhz for NTSC (System 21.47727Mhz / 12) and
    #1.773447Mhz for PAL (System 26.601171Mhz / 15)
    clockHertz = 1.773447*1000000 #PAL

    self.ramSize = 64*1024 #2kB CPU internal RAM, 64kB adressable
    self.ram = [0]*self.ramSize

    #self.ram[5] = 0xa5
    #self.ram[6] = 0x03
    #self.ram[7] = 0xa9
    #self.ram[8] = 0x30
    #self.ram[9] = 0xa2
    #self.ram[10] = 0xab
    #self.ram[11] = 0xac
    #self.ram[12] = 0xab
    #self.ram[13] = 0xcd
    #self.ram[0xcdab] = 0xef
        
    # OPcodes
    self.ops = {
      '0x00' : self.BRK,
      '0x01' : self.ORA_INDX,
      '0x05' : self.ORA_ZP,
      '0x06' : self.ASL,
      '0x08' : self.PHP,
      '0x09' : self.ORA_IMM,
      '0x0a' : self.ASL,
      '0x0d' : self.ORA_ABS,
      '0x0e' : self.ASL,
      '0x10' : self.BPL,
      '0x11' : self.ORA_INDY,
      '0x15' : self.ORA_ZPX,
      '0x16' : self.ASL,
      '0x18' : self.CLC,
      '0x19' : self.ORA_ABSY,
      '0x1d' : self.ORA_ABSX,
      '0x1e' : self.ASL,
      '0x20' : self.JSR,
      '0x21' : self.AND_INDX,
      '0x24' : self.BIT,
      '0x25' : self.AND_ZP,
      '0x26' : self.ROL,
      '0x28' : self.PLP,
      '0x29' : self.AND_IMM,
      '0x2a' : self.ROL,
      '0x2c' : self.BIT,
      '0x2d' : self.AND_ABS,
      '0x2e' : self.ROL,
      '0x30' : self.BMI,
      '0x31' : self.AND_INDY,
      '0x35' : self.AND_ZPX,
      '0x36' : self.ROL,
      '0x38' : self.SEC,
      '0x39' : self.AND_ABSY,
      '0x3d' : self.AND_ABSX,
      '0x3e' : self.ROL,
      '0x40' : self.RTI,
      '0x41' : self.EOR_INDX,
      '0x45' : self.EOR_ZP,
      '0x46' : self.LSR,
      '0x48' : self.PHA,
      '0x49' : self.EOR_IMM,
      '0x4a' : self.LSR,
      '0x4c' : self.JMP_ABS,
      '0x4d' : self.EOR_ABS,
      '0x4e' : self.LSR,
      '0x50' : self.BVC,
      '0x51' : self.EOR_INDY,
      '0x55' : self.EOR_ZPX,
      '0x56' : self.LSR,
      '0x58' : self.CLI,
      '0x59' : self.EOR_ABSY,
      '0x5d' : self.EOR_ABSX,
      '0x5e' : self.LSR,
      '0x60' : self.RTS,
      '0x61' : self.ADC,
      '0x65' : self.ADC,
      '0x66' : self.ROR,
      '0x68' : self.PLA,
      '0x69' : self.ADC,
      '0x6a' : self.ROR,
      '0x6c' : self.JMP_IND,
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
      '0x84' : self.STY,
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
      '0xa0' : self.LDY_IMM,
      '0xa1' : self.LDA_INDX,
      '0xa2' : self.LDX_IMM,
      '0xa4' : self.LDY_ZP,
      '0xa5' : self.LDA_ZP,
      '0xa6' : self.LDX_ZP,
      '0xa8' : self.TAY,
      '0xa9' : self.LDA_IMM,
      '0xaa' : self.TAX,
      '0xac' : self.LDY_ABS,
      '0xad' : self.LDA_ABS,
      '0xae' : self.LDX_ABS,
      '0xb0' : self.BCS,
      '0xb1' : self.LDA_INDY,
      '0xb4' : self.LDY_ZPX,
      '0xb5' : self.LDA_ZPX,
      '0xb6' : self.LDX_ZPY,
      '0xb8' : self.CLV,
      '0xb9' : self.LDA_ABSY,
      '0xba' : self.TSX,
      '0xbc' : self.LDY_ABSX,
      '0xbd' : self.LDA_ABSX,
      '0xbe' : self.LDX_ABSY,
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

  #----------------------------------------------------------------------
  # CPU MAIN LOGIC
  #----------------------------------------------------------------------

  def printRegisters(self):
    print('(regA:%(ra)02x, regX:%(rx)02x, regY:%(ry)02x, regS:%(rs)02x, regP:%(rp)02x' %\
          {"ra":self.regA, "rx":self.regX, "ry":self.regY, "rs":self.regS, "rp":self.regP})

  def load(self, filename):
    print("Loading " + filename + " ...")
    tempRam = [0]*self.ramSize
    f = open(filename, 'rb')
    try:
      byte = f.read(1)
      i = 0
      while byte != "":#for i in range(0,64):
        #Do something with byte
        if (i < 128): #Print only first bytes
          print("0x%(byte)s" % {"byte":byte.encode("hex")}),
        tempRam[i] = int(byte.encode("hex"), 16)
        byte = f.read(1)
        i += 1
    finally:
      f.close()
      
    #Verify 'NES' + MS-DOS end-of-file
    if (tempRam[0] != 0x4e) or (tempRam[1] != 0x45) or (tempRam[2] != 0x53) or (tempRam[3] != 0x1a):
      print("String 'NES' not found. Aborting loading.")
    else:
      self.loadNES(tempRam)
      
    print("Loading complete.")


  def loadNES(self, tempLoadedRam):
    self.nrOf16kbPrgRomBanks = tempLoadedRam[4]
    self.nrOf8kbChrRomBanks = tempLoadedRam[5] #0 means CHR RAM (AKA VRAM)
    self.romControlByte1 = tempLoadedRam[6]
    self.romControlByte2 = tempLoadedRam[7]
    self.nrOf8kbPrgRamBanks = tempLoadedRam[8]

    isZero = True
    for i in range(9,16):
      if tempLoadedRam[i] != 0x00:
        isZero = False
    if isZero == False:
      print("Required format not correct")

    #self.isPal = False
    #if tempLoadedRam[9] == 0x01:
    #  self.isPal = True

    #if self.isPal == False:
      #print("isPal: " + str(self.isPal) + ", " + str(tempLoadedRam[8]))
      #print("NTSC cartridge not currently supported. Aborting loading.")
      #return

    #Transfer rom data to CPU memory
    if self.romControlByte1 & 0x02 == 0x00: #Trainer not present
      for i in range(0,60*1024-16):
        self.ram[i] = tempLoadedRam[i+16]
    else:
      print("512 byte trainer present")
      for i in range(0,64*1024-16-512):
      	self.ram[i] = tempLoadedRam[i+16+512]

  def powerUp(self):
    #Start-up state
    self.ram[0x4015] = 0x00 #All sound disabled
    self.ram[0x4017] = 0x00 #Frame IRQ enabled
    for i in range(0, 16):
      self.ram[0x4000 + i] = 0x00

    #Registers
    self.regA = 0 #Accumulator register, 8 bit
    self.regX = 0 #Index register 1, 8 bit
    self.regY = 0 #Index register 2, 8 bit
    self.regS = 0xfd #Stack pointer, 8 bit, offset from $0100, wraps around on overflow
    self.regP = 0 #Processor status flag bits, 8 bit
    self.PC = 0 #Program counter, 16 bit

  def run(self):
    i = 0
    while (i < 20):
      #Fetch opcode, print
      self.currentOpcode = self.ram[self.PC]
      print("%(pc)04x:%(op)02x" % {"pc":self.PC, "op":self.currentOpcode}),

      #Execute instruction
      self.ops[format(self.currentOpcode, '#04x')]()

      #Print registers
      self.printRegisters()
      i += 1

  def reset(self):
    #A,X,Y not affected
    self.regS -= 0x03 #S decremented by 3
    self.setInterrupt() #Interrupt flag is set
    #Internal memory unchanged
    #APU mode in $4017 unchanged
    self.ram[0x4015] = 0x00 #All sound disabled

  #----------------------------------------------------------------------
  # ADRESSING MODES
  #----------------------------------------------------------------------

  def printSpacesBeforeOpcode(self):
    print("     "),

  def getTwoBytes(self, adress):
    low = self.ram[adress]
    high = self.ram[adress + 1] << 8
    return high + low

  def pushStack(self, value):
    self.ram[self.regS] = value
    self.regS += 1

  def popStack(self):
    self.regS -= 1
    return self.ram[self.regS + 1];

  def getImpliedOperand(self):
    self.PC += 1

  def getAccumulatorOperand(self):
    self.PC += 1

  def getImmediateOperand(self):
    operand = self.ram[self.PC + 1]
    print("#$" + format(operand, "02x") + " "),
    self.PC += 2
    return operand

  def getZeroPageOperand(self):
    adress = self.ram[self.PC + 1]
    if adress > 0xff:
      adress -= 0xff
    operand = self.ram[adress]
    print("$" + format(adress, "02x") + "  "),
    self.PC += 2
    return operand

  def getZeroPageXOperand(self, adress):
    adressZeroPage = self.ram[self.ram[self.PC +1]]
    adress = adressZeroPage + self.regX
    if adress > 0xff:
      adress -= 0xff
    operand = self.ram[adress]
    print("$" + format(adress, "02x") + "  "),
    self.PC += 2
    return operand

  def getZeroPageYOperand(self, adress):
    adressZeroPage = self.ram[self.ram[self.PC + 1]]
    adress = adressZeroPage + self.regY
    if adress > 0xff:
      adress -= 0xff
    operand = self.ram[adress]
    print("$" + format(adress, "02x") + "  "),
    self.PC += 2
    return operand

  def getAbsoluteOperand(self):
    adress = self.getTwoBytes(self.PC + 1)
    operand = self.ram[adress]
    print("$" + format(adress, "04x")),
    self.PC += 3
    return operand

  def getAbsoluteXOperand(self):
    adress = self.getTwoBytes(self.PC + 1)
    adress += self.regX
    operand = self.ram[adress]
    print("$" + format(adress, "04x") + ".X"),
    self.PC += 3
    return operand

  def getAbsoluteYOperand(self):
    adress = self.getTwoBytes(self.PC + 1)
    adress += self.regY
    operand = self.ram[adress]
    print("$" + format(adress, "04x") + ".Y"),
    self.PC += 3
    return operand

  def getIndirectOperand(self):
    adress1 = self.getTwoBytes(self.PC + 1)
    adress2 = self.getTwoBytes(adress1)
    operand = self.ram[adress2]
    print("($" + format(adress1, "04x") + ")"),
    self.PC += 3
    return operand

  #AKA Indexed Indirect or pre-indexed
  def getIndirectXOperand(self):
    adress1 = self.ram[self.PC + 1]
    adress2 = adress1 + self.regX
    adress3 = self.getTwoBytes(adress2)
    operand = self.ram[adress3]
    print("($" + format(adress1, "02x") + ",X)"),
    self.PC += 2
    return operand


  #AKA Indirect Indexed or post-indexed
  def getIndirectYOperand(self):
    adress1 = self.ram[self.PC + 1]
    adress2 = self.getTwoBytes(adress1)
    adress3 = adress2 + self.regY
    operand = self.ram[adress3]
    print("($" + format(adress1, "02x") + ",Y)"),
    self.PC += 2
    return operand

  def getRelativeOperand(self):
    operand = self.ram[self.PC + 2]
    #if condition:
    if (operand & 0x80 != 0x00): #Negative adress
      operand = ~operand + 1 #Bitwise flip and add 1 -> two-complement
      self.PC -= operand
    else:
      self.PC += operand
    print("$RELATIVENOTIMPLEMENTED" + format(operand, "02x")),
    self.PC += 2
   	
  #----------------------------------------------------------------------
  # PROCESSOR STATUS FLAGS
  #----------------------------------------------------------------------
  #bit ->   7                           0
  #       +---+---+---+---+---+---+---+---+
  #       | N | V |   | B | D | I | Z | C |  <-- flag, 0/1 = reset/set
  #       +---+---+---+---+---+---+---+---+
  #(N)egative, O(V)erflow, (B)inary, (D)ecimal, (I)nterrupt, (Z)ero, (C)arry
  def isNegative(self):
    if (self.regP & 0x80):
      return True
    else:
      return False
  def setNegative(self):
    self.regP |= 0x80
  def setNegativeIfNegative(self, operand):
    if operand & 0x80 != 0x00: #MSB is set when zero in two-complement
      self.setNegative()
    else:
      self.clearNegative()
  def clearNegative(self):
    self.regP &= 0x7f
  def isOverflow(self):
    if (self.regP & 0x40):
      return True
    else:
      return False
  def setOverflow(self):
    self.regP |= 0x40
  def clearOverflow(self):
    self.regP &= 0xbf
  def isBinary(self):
    if (self.regP & 0x10):
      return True
    else:
      return False
  def setBinary(self):
    self.regP |= 0x10
  def clearBinary(self):
    self.regP &= 0xef
  def isDecimal(self):
    if (self.regP & 0x08):
      return True
    else:
      return False
  def setDecimal(self):
    self.regP |= 0x08
  def clearDecimal(self):
    self.regP &= 0xf7
  def isInterrupt(self):
    if (self.regP & 0x40):
      return True
    else:
      return False
  def setInterrupt(self):
    self.regP |= 0x04
  def clearInterrupt(self):
    self.regP &= 0xfb
  def isZero(self):
    if (self.regP & 0x02):
      return True
    else:
      return False
  def setZero(self):
    self.regP |= 0x02
  def setZeroIfZero(self, operand):
    if operand == 0x00:
      self.setZero()
    else:
      self.clearZero()
  def clearZero(self):
    self.regP &= 0xfd
  def isCarry(self):
    if (self.regP & 0x01):
      return True
    else:
      return False
  def setCarry(self):
    self.regP |= 0x01
  def clearCarry(self):
    self.regP &= 0xfe

  #----------------------------------------------------------------------
  # OPCODE IMPLEMENTATION
  #----------------------------------------------------------------------

  def BRK(self):
    self.printSpacesBeforeOpcode()
    print("BRK"),
    self.getImpliedOperand()

  def ORA_IMM(self):
    self.ORA(self.getImmediateOperand())

  def ORA_ZP(self):
    self.ORA(self.getZeroPageOperand())

  def ORA_ZPX(self):
    self.ORA(self.getZeroPageXOperand())

  def ORA_ABS(self):
    self.ORA(self.getAbsoluteOperand())

  def ORA_ABSX(self):
    self.ORA(self.getAbsoluteXOperand())

  def ORA_ABSY(self):
    self.ORA(self.getAbsoluteYOperand())

  def ORA_INDX(self):
    self.ORA(self.getIndirectXOperand())

  def ORA_INDY(self):
    self.ORA(self.getIndirectYOperand())

  def ORA(self, operand):
    print("ORA"),
    self.regA = operand | self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)

  def ASL(self):
    pass

  def BPL(self):
    pass

  def PHP(self):
    pass

  def JMP_ABS(self):
    self.JMP(self.getAbsoluteOperand())

  def JMP_IND(self):
    self.JMP(self.getIndirectOperand())

  def JMP(self, operand):
    print("JMP"),
    #Push PC,A,P
    self.pushStack(self.PC)
    self.pushStack(self.regA)
    self.pushStack(self.regP)
    self.PC = operand

  def JSR(self):
    pass

  def AND_IMM(self):
    self.AND(self.getImmediateOperand())

  def AND_ZP(self):
    self.AND(self.getZeroPageOperand())

  def AND_ZPX(self):
    self.AND(self.getZeroPageXOperand())

  def AND_ABS(self):
    self.AND(self.getAbsoluteOperand())

  def AND_ABSX(self):
    self.AND(self.getAbsoluteXOperand())

  def AND_ABSY(self):
    self.AND(self.getAbsoluteYOperand())

  def AND_INDX(self):
    self.AND(self.getIndirectXOperand())

  def AND_INDY(self):
    self.AND(self.getIndirectYOperand())

  def AND(self, operand):
    print("AND"),
    self.regA = operand & self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)

  def BIT(self):
    pass

  def ROL(self):
    self.printSpacesBeforeOpcode()
    print("ROL"),
    self.getImpliedOperand()
    tempCarry = self.isCarry()
    if self.regA & 0x70 != 0x00: #MSB set
      self.setCarry()
    self.regA <<= 1
    self.regA += tempCarry

  def SEC(self):
    self.printSpacesBeforeOpcode()
    print("SEC"),
    self.getImpliedOperand()
    self.setCarry()

  def EOR_IMM(self):
    self.EOR(self.getImmediateOperand())

  def EOR_ZP(self):
    self.EOR(self.getZeroPageOperand())

  def EOR_ZPX(self):
    self.EOR(self.getZeroPageXOperand())

  def EOR_ABS(self):
    self.EOR(self.getAbsoluteOperand())

  def EOR_ABSX(self):
    self.EOR(self.getAbsoluteXOperand())

  def EOR_ABSY(self):
    self.EOR(self.getAbsoluteYOperand())

  def EOR_INDX(self):
    self.EOR(self.getIndirectXOperand())

  def EOR_INDY(self):
    self.EOR(self.getIndirectYOperand())

  def EOR(self, operand):
    print("EOR"),
    self.regA = operand ^ self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)

  def PLP(self):
    pass

  def BMI(self):
    pass

  def LSR(self):
    self.printSpacesBeforeOpcode()
    print("LSR"),
    self.getImpliedOperand()
    if self.regA & 0x01 != 0x00: #LSB set
      self.setCarry()
    self.regA >>= 1

  def PHA(self):
    pass

  def BVC(self):
    pass
  
  def CLI(self):
    self.printSpacesBeforeOpcode()
    print("CLI"),
    self.getImpliedOperand()
    self.clearInterrupt()
  
  def ADC(self):
    pass
  
  def ROR(self):
    self.printSpacesBeforeOpcode()
    print("ROR"),
    self.getImpliedOperand()
    tempCarry = self.isCarry()
    if self.regA & 0x01 != 0x00: #LSB set
      self.setCarry()
    self.regA >>= 1
    self.regA += tempCarry << 8
  
  def PLA(self):
    pass
  
  def BVS(self):
    pass
  
  def SEI(self):
    self.printSpacesBeforeOpcode()
    print("SEI"),
    self.getImpliedOperand()
    self.setInterrupt()
  
  def STY(self):
    pass
  
  def STX(self):
    pass
  
  def DEY(self):
    pass

  def BCC(self):
    pass
  
  def TXA(self):
    self.printSpacesBeforeOpcode()
    print("TXA"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regX)
    self.setZeroIfZero(self.regX)
    self.regA = self.regX
  
  def TYA(self):
    self.printSpacesBeforeOpcode()
    print("TYA"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regY)
    self.setZeroIfZero(self.regY)
    self.regA = self.regY
  
  def TXS(self):
    self.printSpacesBeforeOpcode()
    print("TXS"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regX)
    self.setZeroIfZero(self.regX)
    self.regS = self.regX

  def TAY(self):
    self.printSpacesBeforeOpcode()
    print("TAY"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.regY = self.regA
  
  def TAX(self):
    self.printSpacesBeforeOpcode()
    print("TAX"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.regX = self.regA

  def LDY_ZP(self):
    self.LDY(self.getZeroPageOperand())
  
  def LDY_IMM(self):
    self.LDY(self.getImmediateOperand())

  def LDY_ABS(self):
    self.LDY(self.getAbsoluteOperand())

  def LDY_ZPX(self):
    self.LDY(self.getZeroPageXOperand())

  def LDY_ABSX(self):
    self.LDY(self.getAbsoluteXOperand())

  def LDY(self, operand):
    print("LDY"),
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regY = operand

  def LDX_ZP(self):
    self.LDX(self.getZeroPageOperand())

  def LDX_IMM(self):
    self.LDX(self.getImmediateOperand())

  def LDX_ABS(self):
    self.LDX(self.getAbsoluteOperand())

  def LDX_ZPY(self):
    self.LDX(self.getZeroPageYOperand())

  def LDX_ABSY(self):
    self.LDX(self.getAbsoluteYOperand())

  def LDX(self, operand):
    print("LDX"),
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regX = operand
  
  def CLC(self):
    self.printSpacesBeforeOpcode()
    print("CLC"),
    self.getImpliedOperand()
    self.clearCarry()

  def RTS(self):
    print("RTS"),
    #Pop reverse order JMP
    self.regP = self.popStack()
    self.regA = self.popStack()
    self.regPC = self.popStack()
    self.getImpliedOperand()

  def RTI(self):
    pass

  def STA(self):
    pass

  def LDA_INDX(self):
    self.LDA(self.getIndirectXOperand())

  def LDA_ZP(self):
    self.LDA(self.getZeroPageOperand())

  def LDA_IMM(self):
    self.LDA(self.getImmediateOperand())

  def LDA_ABS(self):
    self.LDA(self.getAbsoluteOperand())

  def LDA_INDY(self):
    self.LDA(self.getIndirectYOperand())

  def LDA_ZPX(self):
    self.LDA(self.getZeroPageXOperand())

  def LDA_ABSY(self):
    self.LDA(self.getAbsoluteYOperand())

  def LDA_ABSX(self):
    self.LDA(self.getAbsoluteXOperand())

  def LDA(self, operand):
    print("LDA"),
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regA = operand

  def BCS(self):
    pass
  
  def CLV(self):
    self.printSpacesBeforeOpcode()    
    print("CLV"),
    self.getImpliedOperand()
    self.clearOverflow()
  
  def TSX(self):
    self.printSpacesBeforeOpcode()
    print("TSX"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regS)
    self.setZeroIfZero(self.regS)
    self.regX = self.regS
  
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
    self.printSpacesBeforeOpcode()    
    print("CLD"),
    self.getImpliedOperand()
    self.clearDecimal()
  
  def CPX(self):
    pass
  
  def SBC(self):
    pass
  
  def INC(self):
    pass
  
  def INX(self):
    pass
  
  def NOP(self):
    self.printSpacesBeforeOpcode()
    print("NOP"),
    self.getImpliedOperand()
  
  def BEQ(self):
    pass
  
  def SED(self):
    self.printSpacesBeforeOpcode()    
    print("SED"),
    self.getImpliedOperand()
    self.setDecimal()