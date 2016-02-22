class CpuR2A03:
  def __init__(self):
    #Clock
    #Clocked 1.789773Mhz for NTSC (System 21.47727Mhz / 12) and
    #1.773447Mhz for PAL (System 26.601171Mhz / 15)
    clockHertz = 1.773447*1000000 #PAL

    self.ramSize = 64*1024 #2kB CPU internal RAM, 64kB adressable
    self.ram = [0]*self.ramSize
    self.stackOffset = 0x0100

    self.ram[5] = 0xa9
    self.ram[6] = 0x8f
    self.ram[7] = 0xa9
    self.ram[8] = 0x30
    self.ram[9] = 0xa2
    self.ram[10] = 0xab
    self.ram[11] = 0xac
    self.ram[12] = 0xab
    self.ram[13] = 0xcd
    self.ram[0xcdab] = 0xef
        
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
      '0x24' : self.BIT_ZP,
      '0x25' : self.AND_ZP,
      '0x26' : self.ROL,
      '0x28' : self.PLP,
      '0x29' : self.AND_IMM,
      '0x2a' : self.ROL,
      '0x2c' : self.BIT_ABS,
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
      '0x61' : self.ADC_INDX,
      '0x65' : self.ADC_ZP,
      '0x66' : self.ROR,
      '0x68' : self.PLA,
      '0x69' : self.ADC_IMM,
      '0x6a' : self.ROR,
      '0x6c' : self.JMP_IND,
      '0x6d' : self.ADC_ABS,
      '0x6e' : self.ROR,
      '0x70' : self.BVS,
      '0x71' : self.ADC_INDY,
      '0x75' : self.ADC_ZPX,
      '0x76' : self.ROR,
      '0x78' : self.SEI,
      '0x79' : self.ADC_ABSY,
      '0x7d' : self.ADC_ABSX,
      '0x7e' : self.ROR,
      '0x81' : self.STA_INDX,
      '0x84' : self.STY_ZP,
      '0x85' : self.STA_ZP,
      '0x86' : self.STX_ZP,
      '0x88' : self.DEY,
      '0x8a' : self.TXA,
      '0x8c' : self.STY_ABS,
      '0x8d' : self.STA_ABS,
      '0x8e' : self.STX_ABS,
      '0x90' : self.BCC,
      '0x91' : self.STA_INDY,
      '0x94' : self.STY_ZPX,
      '0x95' : self.STA_ZPX,
      '0x96' : self.STX_ZPY,
      '0x98' : self.TYA,
      '0x99' : self.STA_ABSY,
      '0x9a' : self.TXS,
      '0x9d' : self.STA_ABSX,
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
      '0xc0' : self.CPY_IMM,
      '0xc1' : self.CMP_INDX,
      '0xc4' : self.CPY_ZP,
      '0xc5' : self.CMP_ZP,
      '0xc6' : self.DEC_ZP,
      '0xc8' : self.INY,
      '0xc9' : self.CMP_IMM,
      '0xca' : self.DEX,
      '0xcc' : self.CPY_ABS,
      '0xcd' : self.CMP_ABS,
      '0xce' : self.DEC_ABS,
      '0xd0' : self.BNE,
      '0xd1' : self.CMP_INDY,
      '0xd5' : self.CMP_ZPX,
      '0xd6' : self.DEC_ZPX,
      '0xd8' : self.CLD,
      '0xd9' : self.CMP_ABSY,
      '0xdd' : self.CMP_ABSX,
      '0xde' : self.DEC_ABSX,
      '0xe0' : self.CPX_IMM,
      '0xe1' : self.SBC_INDX,
      '0xe4' : self.CPX_ZP,
      '0xe5' : self.SBC_ZP,
      '0xe6' : self.INC_ZP,
      '0xe8' : self.INX,
      '0xe9' : self.SBC_IMM,
      '0xea' : self.NOP,
      '0xec' : self.CPX_ABS,
      '0xed' : self.SBC_ABS,
      '0xee' : self.INC_ABS,
      '0xf0' : self.BEQ,
      '0xf1' : self.SBC_INDY,
      '0xf5' : self.SBC_ZPX,
      '0xf6' : self.INC_ZPX,
      '0xf8' : self.SED,
      '0xf9' : self.SBC_ABSY,
      '0xfd' : self.SBC_ABSX,
      '0xfe' : self.INC_ABSX
      }

  #----------------------------------------------------------------------
  # CPU MAIN LOGIC
  #----------------------------------------------------------------------

  def printRegisters(self):
    print('A:%(ra)02x, X:%(rx)02x, Y:%(ry)02x, S:%(rs)02x, P:%(rp)02x' %\
          {"ra":self.currentRegA, "rx":self.currentRegX, "ry":self.currentRegY, "rs":self.currentRegS, "rp":self.currentRegP})

  def load(self, filename):
    print("Loading " + filename + " ...")
    #Load bytes from file
    tempRam = [0]*self.ramSize
    f = open(filename, 'rb')
    try:
      byte = f.read(1)
      i = 0
      while byte != "":
        tempRam[i] = int(byte.encode("hex"), 16)
        byte = f.read(1)
        i += 1
    finally:
      f.close()
      
    #Verify 'NES' + MS-DOS end-of-file
    if (tempRam[0] != 0x4e) or (tempRam[1] != 0x45) or (tempRam[2] != 0x53) or (tempRam[3] != 0x1a):
      print("String 'NES' not found. Aborting loading.")
      return
    
    self.nrOf16kbPrgRomBanks = tempRam[4]
    self.nrOf8kbChrRomBanks = tempRam[5] #0 means CHR RAM (AKA VRAM)
    self.romControlByte1 = tempRam[6]
    self.romControlByte2 = tempRam[7]
    self.nrOf8kbPrgRamBanks = tempRam[8]

    print(str(self.nrOf16kbPrgRomBanks) + " 16kbPrgRomBank(s) detected")
    print(str(self.nrOf8kbChrRomBanks) + " 8kbChrRomBank(s) detected")
    print(str(self.nrOf8kbPrgRamBanks) + " 8kbPrgRomBank(s) detected")

    allZero = True
    for i in range(9,16):
      if tempRam[i] != 0x00:
        allZero = False
    if allZero == False:
      print("Required format (zeros at [0x0009-0x000f]) not correct")
      return

    #self.isPal = False
    #if tempRam[9] == 0x01:
    #  self.isPal = True

    #if self.isPal == False:
      #print("isPal: " + str(self.isPal) + ", " + str(tempRam[8]))
      #print("NTSC cartridge not currently supported. Aborting loading.")
      #return

    self.offsetTrainer = 0
    if self.romControlByte1 & 0x02 != 0x00: #Trainer present
      print("Trainer detected")
      self.offsetTrainer = 512

    #Transfer rom data to CPU memory (only 1 or 2 banks ATM)
    offsetPrg = 16
    offset16kb = 16*1024
    if self.nrOf16kbPrgRomBanks == 1:
        self.ram[0x8000:0x8000+offset16kb] = tempRam[offsetPrg+self.offsetTrainer:offset16kb-offsetPrg-self.offsetTrainer]
        self.ram[0xc000:0xc000+offset16kb] = tempRam[offsetPrg+self.offsetTrainer:offset16kb-offsetPrg-self.offsetTrainer]
    elif self.nrOf16kbPrgRomBanks == 2:
        self.ram[0x8000:0x8000+offset16kb] = tempRam[offsetPrg+self.offsetTrainer:offset16kb-offsetPrg-self.offsetTrainer]
        self.ram[0xc000:0xc000+offset16kb] = tempRam[offsetPrg+self.offsetTrainer+offset16kb:2*offset16kb-offsetPrg-self.offsetTrainer]

    print("Loading complete.")
    
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
    self.PC = 0xc000 #Program counter, 16 bit (0xc000 start of prg-rom)

  def run(self):
    i = 0
    while (i < 256):
      #Fetch opcode, print
      self.currentOpcode = self.ram[self.PC]
      print("%(pc)04x:%(op)02x" % {"pc":self.PC, "op":self.currentOpcode}),
      #Save current registers for output
      self.currentRegA = self.regA
      self.currentRegX = self.regX
      self.currentRegY = self.regY
      self.currentRegS = self.regS
      self.currentRegP = self.regP

      #Execute instruction
      self.ops[format(self.currentOpcode, '#04x')]()

      #Print registers
      self.printRegisters()
      #i += 1

  def reset(self):
    #A,X,Y not affected
    self.regS -= 0x03 #S decremented by 3
    self.setInterrupt() #Interrupt flag is set
    #Internal memory unchanged
    #APU mode in $4017 unchanged
    self.ram[0x4015] = 0x00 #All sound disabled

  #----------------------------------------------------------------------
  # HELPER FUNCTIONS
  #----------------------------------------------------------------------

  def pushStack(self, value):
    self.writeByte(self.regS + self.stackOffset, value)
    self.regS -= 1
    self.regS = self.regS % 0xff

  def popStack(self):
    self.regS += 1
    self.regS = self.regS % 0xff
    returnValue = self.readByte(self.regS + self.stackOffset)
    return returnValue;

  def zeroPageWrapping(self, adress):
    return adress % 0xff

  #Mirror memory if write to certain adresses
  def writeByte(self, adress, value):
    if adress <= 0x00ff or (0x0800 <= adress <= 0x08ff) or (0x1000 <= adress <= 0x10ff) or (0x1800 < adress <= 0x18ff): #Zero page
      self.ram[adress] = value
      self.ram[adress + 0x0800] = value
      self.ram[adress + 0x1000] = value
      self.ram[adress + 0x1800] = value
      #print("$" + str(format(adress, "02x"))),
    else:
      self.ram[adress] = value

  def writeWord(self, adress, value):
    self.ram[adress] = value >> 8
    self.ram[adress + 1] = value & 0x00ff

  def readByte(self, adress):
    return self.ram[adress]

  def readWord(self, adress):
    low = self.ram[adress]
    high = self.ram[adress + 1] << 8
    return high + low

  #----------------------------------------------------------------------
  # ADRESSING MODES
  #----------------------------------------------------------------------

  def getImpliedOperand(self):
    self.PC += 1
    print("       "),

  def getAccumulatorOperand(self):
    self.PC += 1
    print("A      "),

  def getImmediateOperand(self):
    operand = self.readByte(self.PC + 1)
    print("#$" + format(operand, "02x") + "   "),
    self.PC += 2
    return operand

  def getZeroPageAdress(self):
    adressZeroPage = self.readByte(self.PC + 1)
    adress = self.zeroPageWrapping(adressZeroPage)
    self.PC += 2
    return adress

  def getZeroPageOperand(self):
    adress = self.getZeroPageAdress()
    operand = self.readByte(adress)
    print("$" + format(adress, "02x") + "    "),
    return operand

  def getZeroPageXAdress(self):
    adressZeroPage = self.readByte(self.readByte(self.PC +1)) + self.regX
    adress = self.zeroPageWrapping(adressZeroPage)
    self.PC += 2
    return adress

  def getZeroPageXOperand(self):
    adress = self.getZeroPageXAdress()
    operand = self.readByte(adress)
    print("$" + format(adress, "02x") + ",X  "),
    return operand

  def getZeroPageYAdress(self):
    adressZeroPage = self.readByte(self.readByte(self.PC +1)) + self.regY
    adress = self.zeroPageWrapping(adressZeroPage)
    self.PC += 2
    return adress

  def getZeroPageYOperand(self):
    adress = self.getZeroPageYAdress()
    operand = self.readByte(adress)
    print("$" + format(adress, "02x") + ",Y  "),
    return operand

  def getAbsoluteAdress(self):
    adress = self.readWord(self.PC + 1)
    self.PC += 3
    return adress

  def getAbsoluteOperand(self):
    adress = self.getAbsoluteAdress()
    operand = self.readByte(adress)
    print("$" + format(adress, "04x") + "  "),
    return operand

  def getAbsoluteXAdress(self):
    adress = self.readWord(self.PC + 1) + self.regX
    self.PC += 3
    return adress

  def getAbsoluteXOperand(self):
    adress = self.getAbsoluteXAdress()
    operand = self.readByte(adress)
    print("$" + format(adress, "04x") + ",X"),
    return operand

  def getAbsoluteYOperand(self):
    adress = self.readWord(self.PC + 1) + self.regY
    operand = self.readByte(adress)
    print("$" + format(adress, "04x") + ",Y"),
    self.PC += 3
    return operand

  def getIndirectOperand(self):
    adress1 = self.readWord(self.PC + 1)
    adress2 = self.readWord(adress1)
    operand = self.readByte(adress2)
    print("($" + format(adress1, "04x") + ")"),
    self.PC += 3
    return operand

  #AKA Indexed Indirect or pre-indexed
  def getIndirectXOperand(self):
    adress1 = self.readByte(self.PC + 1) + self.regX
    adress2 = self.readWord(adress1)
    operand = self.readByte(adress2)
    print("($" + format(adress1, "02x") + ",X)"),
    self.PC += 2
    return operand

  #AKA Indirect Indexed or post-indexed
  def getIndirectYOperand(self):
    adress1 = self.readByte(self.PC + 1)
    adress2 = self.readWord(adress1)
    adress3 = adress2 + self.regY
    operand = self.readByte(adress3)
    print("($" + format(adress1, "02x") + "),Y"),
    self.PC += 2
    return operand

  def getRelativeOperand(self):
    operand = self.readByte(self.PC + 1)
    if (operand & 0x80): #Negative adress
      operand = ~operand + 1 #Bitwise flip and add 1 -> two-complement
      result = self.PC - operand + 2
    else:
      result = self.PC + operand + 2
    print("$" + format(result, "04x") + "  "),
    return result
   	
  #----------------------------------------------------------------------
  # PROCESSOR STATUS FLAGS
  #----------------------------------------------------------------------
  #bit ->   7                           0
  #       +---+---+---+---+---+---+---+---+
  #       | N | V |   | B | D | I | Z | C |  <-- flag, 0/1 = reset/set
  #       +---+---+---+---+---+---+---+---+
  #(N)egative, O(V)erflow, (B)inary, (D)ecimal, (I)nterrupt, (Z)ero, (C)arry

  def clearAllFlags(self):
    self.regP & 0x00

  def isNegativeFlagSet(self):
    if (self.regP & 0x80):
      return True
    else:
      return False
  def setNegative(self):
    self.regP |= 0x80
  def setNegativeIfNegative(self, operand):
    if operand & 0x80: #MSB is set when zero in two-complement
      self.setNegative()
    else:
      self.clearNegative()
  def clearNegative(self):
    self.regP &= 0x7f
  def isOverflowFlagSet(self):
    if (self.regP & 0x40):
      return True
    else:
      return False
  def setOverflow(self):
    self.regP |= 0x40
  def clearOverflow(self):
    self.regP &= 0xbf
  def isBreakFlagSet(self):
    if (self.regP & 0x10):
      return True
    else:
      return False
  def setBreak(self):
    self.regP |= 0x10
  def clearBreak(self):
    self.regP &= 0xef
  def isDecimalFlagSet(self):
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

  def setZero(self):
    self.regP |= 0x02
  def getZero(self):
    return (self.regP & 0x02) >> 1
  def setZeroIfZero(self, operand):
    if operand == 0x00:
      self.setZero()
    else:
      self.clearZero()
  def clearZero(self):
    self.regP &= 0xfd

  def setCarry(self):
    self.regP |= 0x01
  def getCarry(self):
    return self.regP & 0x01
  def clearCarry(self):
    self.regP &= 0xfe

  #----------------------------------------------------------------------
  # OPCODE IMPLEMENTATION
  #----------------------------------------------------------------------

  def BRK(self):
    print("BRK"),
    self.setBreak()
    self.getImpliedOperand()

  def NOP(self):
    print("NOP"),
    self.getImpliedOperand()

  def ORA_IMM(self):
    print("ORA"),
    self.ORA(self.getImmediateOperand())

  def ORA_ZP(self):
    print("ORA"),
    self.ORA(self.getZeroPageOperand())

  def ORA_ZPX(self):
    print("ORA"),
    self.ORA(self.getZeroPageXOperand())

  def ORA_ABS(self):
    print("ORA"),
    self.ORA(self.getAbsoluteOperand())

  def ORA_ABSX(self):
    print("ORA"),
    self.ORA(self.getAbsoluteXOperand())

  def ORA_ABSY(self):
    print("ORA"),
    self.ORA(self.getAbsoluteYOperand())

  def ORA_INDX(self):
    print("ORA"),
    self.ORA(self.getIndirectXOperand())

  def ORA_INDY(self):
    print("ORA"),
    self.ORA(self.getIndirectYOperand())

  def ORA(self, operand):
    self.clearAllFlags()
    self.regA = operand | self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)

  def AND_IMM(self):
    print("AND"),
    self.AND(self.getImmediateOperand())

  def AND_ZP(self):
    print("AND"),
    self.AND(self.getZeroPageOperand())

  def AND_ZPX(self):
    print("AND"),
    self.AND(self.getZeroPageXOperand())

  def AND_ABS(self):
    print("AND"),
    self.AND(self.getAbsoluteOperand())

  def AND_ABSX(self):
    print("AND"),
    self.AND(self.getAbsoluteXOperand())

  def AND_ABSY(self):
    print("AND"),
    self.AND(self.getAbsoluteYOperand())

  def AND_INDX(self):
    print("AND"),
    self.AND(self.getIndirectXOperand())

  def AND_INDY(self):
    print("AND"),
    self.AND(self.getIndirectYOperand())

  def AND(self, operand):
    self.regA = operand & self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)

  def EOR_IMM(self):
    print("EOR"),
    self.EOR(self.getImmediateOperand())

  def EOR_ZP(self):
    print("EOR"),
    self.EOR(self.getZeroPageOperand())

  def EOR_ZPX(self):
    print("EOR"),
    self.EOR(self.getZeroPageXOperand())

  def EOR_ABS(self):
    print("EOR"),
    self.EOR(self.getAbsoluteOperand())

  def EOR_ABSX(self):
    print("EOR"),
    self.EOR(self.getAbsoluteXOperand())

  def EOR_ABSY(self):
    print("EOR"),
    self.EOR(self.getAbsoluteYOperand())

  def EOR_INDX(self):
    print("EOR"),
    self.EOR(self.getIndirectXOperand())

  def EOR_INDY(self):
    print("EOR"),
    self.EOR(self.getIndirectYOperand())

  def EOR(self, operand):
    self.clearAllFlags()
    self.regA = operand ^ self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
  
  def ADC_IMM(self):
    print("ADC"),
    self.ADC(self.getImmediateOperand())
  
  def ADC_ZP(self):
    print("ADC"),
    self.ADC(self.getZeroPageOperand())
  
  def ADC_ZPX(self):
    print("ADC"),
    self.ADC(self.getZeroPageXOperand)
  
  def ADC_ABS(self):
    print("ADC"),
    self.ADC(self.getAbsoluteOperand)
  
  def ADC_ABSX(self):
    print("ADC"),
    self.ADC(self.getAbsoluteXOperand)
  
  def ADC_ABSY(self):
    print("ADC"),
    self.ADC(self.getAbsoluteYOperand)
  
  def ADC_INDX(self):
    print("ADC"),
    self.ADC(self.getIndirectXOperand)
  
  def ADC_INDY(self):
    print("ADC"),
    self.ADC(self.getIndirectYOperand)
  
  def ADC(self, operand):
    self.clearAllFlags()
    if self.regA + operand + self.getCarry() > 0xff:
      self.setOverflow()
    self.regA += operand + self.getCarry()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)

  def SBC_IMM(self):
    print("SBC"),
    self.SBC(self.getImmediateOperand())

  def SBC_ZP(self):
    print("SBC"),
    self.SBC(self.getZeroPageOperand())

  def SBC_ZPX(self):
    print("SBC"),
    self.SBC(self.getZeroPageXOperand())

  def SBC_ABS(self):
    print("SBC"),
    self.SBC(self.getAbsoluteOperand())

  def SBC_ABSX(self):
    print("SBC"),
    self.SBC(self.getAbsoluteXOperand())

  def SBC_ABSY(self):
    print("SBC"),
    self.SBC(self.getAbsoluteYOperand())

  def SBC_INDX(self):
    print("SBC"),
    self.SBC(self.getIndirectXOperand())

  def SBC_INDY(self):
    print("SBC"),
    self.SBC(self.getIndirectYOperand())

  def SBC(self, operand):
    self.clearAllFlags()
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    if self.regA - operand - self.getCarry() > 0xff:
      self.setOverflow()
    self.regA -= operand + self.getCarry()

  #Hack implementation!
  def JMP_ABS(self):
    print("JMP"),
    adress = self.readWord(self.PC + 1)
    print("$" + format(adress, "04x") + "  "),
    self.PC += 3
    self.JMP(adress)

  def JMP_IND(self):
    print("JMP"),
    self.JMP(self.getIndirectOperand())

  def JMP(self, operand):
    self.PC = operand

  #Hack implementation!
  def JSR(self):
    print("JSR"),
    adress = self.readWord(self.PC + 1)
    print("$" + format(adress, "04x") + "  "),
    self.PC += 2
    self.pushStack(self.PC >> 8)
    self.pushStack(self.PC & 0x00ff)
    self.PC = adress

  def RTS(self):
    print("RTS"),
    #Pop reverse order JSR
    self.PC = self.popStack()
    self.PC += self.popStack() << 8
    self.getImpliedOperand()
 
  def RTI(self):
    print("RTI"),
    self.PC = self.popStack() << 8
    self.PC += self.popStack()

  def BMI(self):
    print("BMI"),
    result = self.getRelativeOperand()
    if self.isNegativeFlagSet():
      self.PC = result
    else:
      self.PC += 2

  def BVC(self):
    print("BVC"),
    result = self.getRelativeOperand()
    if self.isOverflowFlagSet() == False:
      self.PC = result
    else:
      self.PC += 2

  def BCC(self):
    print("BCC"),
    result = self.getRelativeOperand()
    if self.getCarry() == 0x00:
      self.PC = result
    else:
      self.PC += 2
  
  def BVS(self):
    print("BVS"),
    result = self.getRelativeOperand()
    if self.isOverflowFlagSet():
      self.PC = result
    else:
      self.PC += 2

  def BCS(self):
    print("BCS"),
    result = self.getRelativeOperand()
    if self.getCarry() == 0x01:
      self.PC = result
    else:
      self.PC += 2

  def BPL(self):
    print("BPL"),
    result = self.getRelativeOperand()
    if self.isNegativeFlagSet() == False:
      self.PC = result
    else:
      self.PC += 2
  
  def BEQ(self):
    print("BEQ"),
    adress = self.getRelativeOperand()
    if self.getZero() == 0x01:
      self.PC = adress
    else:
      self.PC += 2
  
  def BNE(self):
    print("BNE"),
    adress = self.getRelativeOperand()
    if self.getZero() == 0x00:
      self.PC = adress
    else:
      self.PC += 2

  def BIT_ZP(self):
    print("BIT"),
    self.BIT(self.getZeroPageOperand())

  def BIT_ABS(self):
    print("BIT"),
    self.BIT(self.getAbsoluteOperand())

  def BIT(self, operand):
    result = self.regA & operand
    self.setZeroIfZero(result)
    self.setNegativeIfNegative(result)
    if (result | 0x70) >> 7:
      self.setOverflow()
    else:
      self.clearOverflow()

  def ROL(self):
    print("ROL"),
    self.clearAllFlags()
    self.getImpliedOperand()
    tempCarry = self.getCarry()
    if self.regA & 0x70 != 0x00: #MSB set
      self.setCarry()
    self.regA <<= 1
    self.regA += tempCarry

  def LSR(self):
    print("LSR"),
    self.clearAllFlags()
    self.getImpliedOperand()
    if self.regA & 0x01 != 0x00: #LSB set
      self.setCarry()
    self.regA >>= 1

  def ASL(self):
    print("ASL"),
    self.clearAllFlags()
    self.getImpliedOperand()
    if self.regA & 0x70 != 0x00: #MSB set
      self.setCarry()
    self.regA <<= 1
  
  def ROR(self):
    print("ROR"),
    self.clearAllFlags()
    self.getImpliedOperand()
    tempCarry = self.getCarry()
    if self.regA & 0x01 != 0x00: #LSB set
      self.setCarry()
    self.regA >>= 1
    self.regA += tempCarry << 8

  def PHP(self):
    print("PHP"),
    self.getImpliedOperand()
    self.pushStack(self.regP)

  def PHA(self):
    print("PHA"),
    self.getImpliedOperand()
    self.pushStack(self.regA)

  def PLP(self):
    print("PLP"),
    self.getImpliedOperand()
    self.regP = self.popStack()
  
  def PLA(self):
    print("PLA"),
    self.getImpliedOperand()
    self.regA = self.popStack()

  def SEC(self):
    print("SEC"),
    self.getImpliedOperand()
    self.setCarry()
  
  def SEI(self):
    print("SEI"),
    self.getImpliedOperand()
    self.setInterrupt()
  
  def SED(self):  
    print("SED"),
    self.getImpliedOperand()
    self.setDecimal()
  
  def CLD(self):  
    print("CLD"),
    self.getImpliedOperand()
    self.clearDecimal()
  
  def CLV(self):
    print("CLV"),
    self.getImpliedOperand()
    self.clearOverflow()
  
  def CLC(self):
    print("CLC"),
    self.getImpliedOperand()
    self.clearCarry()
  
  def CLI(self):
    print("CLI"),
    self.getImpliedOperand()
    self.clearInterrupt()

  def STA_ZP(self):
    print("STA"),
    adress = self.getZeroPageAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STA(adress)

  def STA_ZPX(self):
    print("STA"),
    adress = self.getZeroPageXAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STA(adress)

  def STA_ABS(self):
    print("STA"),
    adress = self.getAbsoluteAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STA(adress)

  def STA_ABSX(self):
    print("STA"),
    adress = self.getAbsoluteXAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STA(adress)

  def STA_ABSY(self):
    print("STA"),
    adress = self.getAbsoluteYAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STA(adress)

  def STA_INDX(self):
    print("STA"),
    adress = self.getIndirectXAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STA(adress)

  def STA_INDY(self):
    print("STA"),
    adress = self.getIndirectYAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STA(adress)

  def STA(self, adress):
    self.writeByte(adress, self.regA)
  
  def STY_ZP(self):
    print("STY"),
    adress = self.getZeroPageAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STY(adress)
  
  def STY_ZPX(self):
    print("STY"),
    adress = self.getZeroPageXAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STY(adress)
  
  def STY_ABS(self):
    print("STY"),
    adress = self.getAbsoluteAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STY(adress)
  
  def STY(self, adress):
    self.writeByte(adress, self.regY)
  
  def STX_ZP(self):
    print("STX"),
    adress = self.getZeroPageAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STX(adress)
  
  def STX_ZPY(self):
    print("STX"),
    adress = self.getZeroPageYAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STX(adress)
  
  def STX_ABS(self):
    print("STX"),
    adress = self.getAbsoluteAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STX(adress)
  
  def STX(self, adress):
    self.writeByte(adress, self.regX)
  
  def TXA(self):
    print("TXA"),
    self.clearAllFlags()
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regX)
    self.setZeroIfZero(self.regX)
    self.regA = self.regX
  
  def TYA(self):
    print("TYA"),
    self.clearAllFlags()
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regY)
    self.setZeroIfZero(self.regY)
    self.regA = self.regY
  
  def TSX(self):
    print("TSX"),
    self.clearAllFlags()
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regS)
    self.setZeroIfZero(self.regS)
    self.regX = self.regS
  
  def TXS(self):
    print("TXS"),
    self.clearAllFlags()
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regX)
    self.setZeroIfZero(self.regX)
    self.regS = self.regX

  def TAY(self):
    print("TAY"),
    self.clearAllFlags()
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.regY = self.regA
  
  def TAX(self):
    print("TAX"),
    self.clearAllFlags()
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.regX = self.regA

  def LDY_ZP(self):
    print("LDY"),
    self.LDY(self.getZeroPageOperand())
  
  def LDY_IMM(self):
    print("LDY"),
    self.LDY(self.getImmediateOperand())

  def LDY_ABS(self):
    print("LDY"),
    self.LDY(self.getAbsoluteOperand())

  def LDY_ZPX(self):
    print("LDY"),
    self.LDY(self.getZeroPageXOperand())

  def LDY_ABSX(self):
    print("LDY"),
    self.LDY(self.getAbsoluteXOperand())

  def LDY(self, operand):
    self.clearAllFlags()
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regY = operand

  def LDX_ZP(self):
    print("LDX"),
    self.LDX(self.getZeroPageOperand())

  def LDX_IMM(self):
    print("LDX"),
    self.LDX(self.getImmediateOperand())

  def LDX_ABS(self):
    print("LDX"),
    self.LDX(self.getAbsoluteOperand())

  def LDX_ZPY(self):
    print("LDX"),
    self.LDX(self.getZeroPageYOperand())

  def LDX_ABSY(self):
    print("LDX"),
    self.LDX(self.getAbsoluteYOperand())

  def LDX(self, operand):
    self.clearAllFlags()
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regX = operand

  def LDA_INDX(self):
    print("LDA"),
    self.LDA(self.getIndirectXOperand())

  def LDA_ZP(self):
    print("LDA"),
    self.LDA(self.getZeroPageOperand())

  def LDA_IMM(self):
    print("LDA"),
    self.LDA(self.getImmediateOperand())

  def LDA_ABS(self):
    print("LDA"),
    self.LDA(self.getAbsoluteOperand())

  def LDA_INDY(self):
    print("LDA"),
    self.LDA(self.getIndirectYOperand())

  def LDA_ZPX(self):
    print("LDA"),
    self.LDA(self.getZeroPageXOperand())

  def LDA_ABSY(self):
    print("LDA"),
    self.LDA(self.getAbsoluteYOperand())

  def LDA_ABSX(self):
    print("LDA"),
    self.LDA(self.getAbsoluteXOperand())

  def LDA(self, operand):
    self.clearAllFlags()
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regA = operand

  def CMP_IMM(self):
    print("CMP"),
    self.CMP(self.getImmediateOperand())
  
  def CMP_ZP(self):
    print("CMP"),
    self.CMP(self.getZeroPageOperand())
  
  def CMP_ZPX(self):
    print("CMP"),
    self.CMP(self.getZeroPageXOperand())
  
  def CMP_ABS(self):
    print("CMP"),
    self.CMP(self.getAbsoluteOperand())
  
  def CMP_ABSX(self):
    print("CMP"),
    self.CMP(self.getAbsoluteXOperand())
  
  def CMP_ABSY(self):
    print("CMP"),
    self.CMP(self.getAbsoluteYOperand())
  
  def CMP_INDX(self):
    print("CMP"),
    self.CMP(self.getIndirectXOperand())
  
  def CMP_INDY(self):
    print("CMP"),
    self.CMP(self.getIndirectYOperand())
  
  def CMP(self, operand):
    self.clearAllFlags()
    if self.regA >= operand:
      self.setCarry()
    self.setZeroIfZero(self.regA)
    self.setNegativeIfNegative(self.regA)

  def CPY_IMM(self):
    print("CPY"),
    self.CPY(self.getImmediateOperand())

  def CPY_ZP(self):
    print("CPY"),
    self.CPY(self.getZeroPageOperand())

  def CPY_ABS(self):
    print("CPY"),
    self.CPY(self.getAbsoluteOperand())

  def CPY(self, operand):
    self.clearAllFlags()
    if self.regY > operand:
      self.setCarry()
    self.setZeroIfZero(self.regY)
    self.setNegativeIfNegative(self.regY)

  def CPX_IMM(self):
    print("CPX"),
    self.CPX(self.getImmediateOperand())

  def CPX_ZP(self):
    print("CPX"),
    self.CPX(self.getZeroPageOperand())

  def CPX_ABS(self):
    print("CPX"),
    self.CPX(self.getAbsoluteOperand())

  def CPX(self, operand):
    self.clearAllFlags()
    if self.regX > operand:
      self.setCarry()
    self.setZeroIfZero(self.regX)
    self.setNegativeIfNegative(self.regX)
  
  def DEY(self):
    print("DEY"),
    self.clearAllFlags()
    self.regY -= 1
    self.setZeroIfZero(self.regY)
    self.setNegativeIfNegative(self.regY)
    self.getImpliedOperand()
  
  def INY(self):
    print("INY"),
    self.clearAllFlags()
    self.regY += 1
    self.setZeroIfZero(self.regY)
    self.setNegativeIfNegative(self.regY)
    self.getImpliedOperand()
  
  def DEX(self):
    print("DEX"),
    self.clearAllFlags()
    self.regX -= 1
    self.setZeroIfZero(self.regX)
    self.setNegativeIfNegative(self.regX)
    self.getImpliedOperand()
  
  def INX(self):
    print("INX"),
    self.clearAllFlags()
    self.regX += 1
    self.setZeroIfZero(self.regX)
    self.setNegativeIfNegative(self.regX)
    self.getImpliedOperand()

  def DEC_ZP(self):
    print("DEC"),
    self.DEC(self.getZeroPageAdress(), self.getZeroPageOperand())

  def DEC_ZPX(self):
    print("DEC"),
    self.DEC(self.getZeroPageXAdress(), self.getZeroPageXOperand())

  def DEC_ABS(self):
    print("DEC"),
    self.DEC(self.getAbsoluteAdress(), self.getAbsoluteOperand())

  def DEC_ABSX(self):
    print("DEC"),
    self.DEC(self.getAbsoluteXAdress(), self.getAbsoluteXOperand())

  def DEC(self, adress, operand):
    self.clearAllFlags()
    operand -= 1
    self.writeByte(adress, operand)
    self.setZeroIfZero(operand)
    self.setNegativeIfNegative(operand)
  
  def INC_ZP(self):
    print("INC"),
    self.INC(self.getZeroPageAdress(), self.getZeroPageOperand())
  
  def INC_ZPX(self):
    print("INC"),
    self.INC(self.getZeroPageXAdress(), self.getZeroPageXOperand())
  
  def INC_ABS(self):
    print("INC"),
    self.INC(self.getAbsoluteAdress(), self.getAbsoluteOperand())
  
  def INC_ABSX(self):
    print("INC"),
    self.INC(self.getAbsoluteXAdress(), self.getAbsoluteXOperand())
  
  def INC(self, adress, operand):
    self.clearAllFlags()
    operand += 1
    self.writeByte(adress, operand)
    self.setZeroIfZero(operand)
    self.setNegativeIfNegative(operand)