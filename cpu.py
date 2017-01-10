import threading

class CpuR2A03 (threading.Thread):
  def __init__(self, memory, writeLock, readLock):
    threading.Thread.__init__(self)
    #Clock
    #Clocked 1.789773Mhz for NTSC (System 21.47727Mhz / 12) and
    #1.773447Mhz for PAL (System 26.601171Mhz / 15)
    clockHertz = 1.773447*1000000 #PAL

    self.ramSize = 64*1024 #2kB CPU internal RAM, 64kB adressable
    self.ram = [0]*self.ramSize

    #self.sharedMemory = memory
    self.ram = memory
    self.writeLock = writeLock
    self.readLock = readLock

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

    self.powerUp()
        
    # OPcodes
    self.ops = {
      '0x00' : self.BRK,
      '0x01' : self.ORA_INDX,
      '0x05' : self.ORA_ZP,
      '0x06' : self.ASL_ZP,
      '0x08' : self.PHP,
      '0x09' : self.ORA_IMM,
      '0x0a' : self.ASL_ACC,
      '0x0d' : self.ORA_ABS,
      '0x0e' : self.ASL_ABS,
      '0x10' : self.BPL,
      '0x11' : self.ORA_INDY,
      '0x15' : self.ORA_ZPX,
      '0x16' : self.ASL_ZPX,
      '0x18' : self.CLC,
      '0x19' : self.ORA_ABSY,
      '0x1d' : self.ORA_ABSX,
      '0x1e' : self.ASL_ABSX,
      '0x20' : self.JSR,
      '0x21' : self.AND_INDX,
      '0x24' : self.BIT_ZP,
      '0x25' : self.AND_ZP,
      '0x26' : self.ROL_ZP,
      '0x28' : self.PLP,
      '0x29' : self.AND_IMM,
      '0x2a' : self.ROL_ACC,
      '0x2c' : self.BIT_ABS,
      '0x2d' : self.AND_ABS,
      '0x2e' : self.ROL_ABS,
      '0x30' : self.BMI,
      '0x31' : self.AND_INDY,
      '0x35' : self.AND_ZPX,
      '0x36' : self.ROL_ZPX,
      '0x38' : self.SEC,
      '0x39' : self.AND_ABSY,
      '0x3d' : self.AND_ABSX,
      '0x3e' : self.ROL_ABSX,
      '0x40' : self.RTI,
      '0x41' : self.EOR_INDX,
      '0x45' : self.EOR_ZP,
      '0x46' : self.LSR_ZP,
      '0x48' : self.PHA,
      '0x49' : self.EOR_IMM,
      '0x4a' : self.LSR_ACC,
      '0x4c' : self.JMP_ABS,
      '0x4d' : self.EOR_ABS,
      '0x4e' : self.LSR_ABS,
      '0x50' : self.BVC,
      '0x51' : self.EOR_INDY,
      '0x55' : self.EOR_ZPX,
      '0x56' : self.LSR_ZPX,
      '0x58' : self.CLI,
      '0x59' : self.EOR_ABSY,
      '0x5d' : self.EOR_ABSX,
      '0x5e' : self.LSR_ABSX,
      '0x60' : self.RTS,
      '0x61' : self.ADC_INDX,
      '0x65' : self.ADC_ZP,
      '0x66' : self.ROR_ZP,
      '0x68' : self.PLA,
      '0x69' : self.ADC_IMM,
      '0x6a' : self.ROR_ACC,
      '0x6c' : self.JMP_IND,
      '0x6d' : self.ADC_ABS,
      '0x6e' : self.ROR_ABS,
      '0x70' : self.BVS,
      '0x71' : self.ADC_INDY,
      '0x75' : self.ADC_ZPX,
      '0x76' : self.ROR_ZPX,
      '0x78' : self.SEI,
      '0x79' : self.ADC_ABSY,
      '0x7d' : self.ADC_ABSX,
      '0x7e' : self.ROR_ABSX,
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
    print('A:%(ra)02x, X:%(rx)02x, Y:%(ry)02x, P:%(rp)02x, S:%(rs)02x, CLC:%(clc)04x' %\
          {"ra":self.currentRegA, "rx":self.currentRegX, "ry":self.currentRegY, "rs":self.currentRegS, "rp":self.currentRegP,"clc":self.currentClock})

  def load(self, filename):
    print("Loading " + str(filename) + " ...")
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


    #self.sharedMemory = self.ram[:]
    print("Loading complete.")
    
  def powerUp(self):
    #Start-up state
    self.clock = 0
    self.ram[0x4015] = 0x00 #All sound disabled
    self.ram[0x4017] = 0x00 #Frame IRQ enabled
    for i in range(0, 16):
      self.ram[0x4000 + i] = 0x00

    #Registers
    self.regA = 0 #Accumulator register, 8 bit
    self.regX = 0 #Index register 1, 8 bit
    self.regY = 0 #Index register 2, 8 bit
    self.regS = 0xfd #Stack pointer, 8 bit, offset from $0100, wraps around on overflow
    self.regP = 0x24 #Processor status flag bits, 8 bit
    self.PC = 0x8000 #Program counter, 16 bit (0x8000 start of prg-rom)

  def run(self):
    print("Entering cpu thread")
    i = 0
    self.readLock.acquire()
    while (i < 160):
      #Fetch opcode, print
      self.currentOpcode = self.ram[self.PC]
      print("%(pc)04x:%(op)02x" % {"pc":self.PC, "op":self.currentOpcode}),
      #Save current registers for output
      self.currentRegA = self.regA
      self.currentRegX = self.regX
      self.currentRegY = self.regY
      self.currentRegS = self.regS
      self.currentRegP = self.regP
      self.currentClock = self.clock

      #Execute instruction
      try:
        self.ops[format(self.currentOpcode, '#04x')]()
        #Print registers
        self.printRegisters()
      except KeyError:
        print("Key ", format(self.currentOpcode, '#04x'), " not found")

      i += 1

    self.readLock.release()

    print("Exiting cpu thread")

  def reset(self):
    self.clock = 0
    #A,X,Y not affected
    self.regS -= 0x03 #S decremented by 3
    self.setInterrupt() #ADC flag is set
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

  def setNegative(self):
    self.regP |= 0x80
  def getNegative(self):
    return (self.regP & 0x80) >> 7
  def clearNegative(self):
    self.regP &= 0x7f
  def setNegativeIfNegative(self, operand):
    if (operand & 0x80):
      self.setNegative()
    else:
      self.clearNegative()

  def setOverflow(self):
    self.regP |= 0x40
  def getOverflow(self):
    return (self.regP & 0x40) >> 6
  def clearOverflow(self):
    self.regP &= 0xbf

  def setBreak(self):
    self.regP |= 0x10
  def getBreak(self):
    return (self.regP & 0x10) >> 4
  def clearBreak(self):
    self.regP &= 0xef

  def setDecimal(self):
    self.regP |= 0x08
  def getDecimal(self):
    return (self.regP & 0x08) >> 3
  def clearDecimal(self):
    self.regP &= 0xf7

  def setInterrupt(self):
    self.regP |= 0x04
  def getDecimal(self):
    return (self.regP & 0x04) >> 2
  def clearInterrupt(self):
    self.regP &= 0xfb

  def setZero(self):
    self.regP |= 0x02
  def getZero(self):
    return (self.regP & 0x02) >> 1
  def setZeroIfZero(self, operand):
    if operand:
      self.clearZero()
    else:
      self.setZero()
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
    self.clock += 7

  def NOP(self):
    print("NOP"),
    self.getImpliedOperand()
    self.clock += 2

  def AND_IMM(self):
    print("AND"),
    self.AND(self.getImmediateOperand())
    self.clock += 2

  def AND_ZP(self):
    print("AND"),
    self.AND(self.getZeroPageOperand())
    self.clock += 3

  def AND_ZPX(self):
    print("AND"),
    self.AND(self.getZeroPageXOperand())
    self.clock += 4

  def AND_ABS(self):
    print("AND"),
    self.AND(self.getAbsoluteOperand())
    self.clock += 4

  def AND_ABSX(self):
    print("AND"),
    self.AND(self.getAbsoluteXOperand())
    self.clock += 4

  def AND_ABSY(self):
    print("AND"),
    self.AND(self.getAbsoluteYOperand())
    self.clock += 4

  def AND_INDX(self):
    print("AND"),
    self.AND(self.getIndirectXOperand())
    self.clock += 6

  def AND_INDY(self):
    print("AND"),
    self.AND(self.getIndirectYOperand())    
    self.clock += 5

  def AND(self, operand):
    self.regA = operand & self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)

  def ORA_IMM(self):
    print("ORA"),
    self.ORA(self.getImmediateOperand())
    self.clock += 2

  def ORA_ZP(self):
    print("ORA"),
    self.ORA(self.getZeroPageOperand())
    self.clock += 3

  def ORA_ZPX(self):
    print("ORA"),
    self.ORA(self.getZeroPageXOperand())
    self.clock += 4

  def ORA_ABS(self):
    print("ORA"),
    self.ORA(self.getAbsoluteOperand())
    self.clock += 4

  def ORA_ABSX(self):
    print("ORA"),
    self.ORA(self.getAbsoluteXOperand())
    self.clock += 4

  def ORA_ABSY(self):
    print("ORA"),
    self.ORA(self.getAbsoluteYOperand())
    self.clock += 4

  def ORA_INDX(self):
    print("ORA"),
    self.ORA(self.getIndirectXOperand())
    self.clock += 6

  def ORA_INDY(self):
    print("ORA"),
    self.ORA(self.getIndirectYOperand())
    self.clock += 5

  def ORA(self, operand):
    self.regA = operand | self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)

  def EOR_IMM(self):
    print("EOR"),
    self.EOR(self.getImmediateOperand())
    self.clock += 2

  def EOR_ZP(self):
    print("EOR"),
    self.EOR(self.getZeroPageOperand())
    self.clock += 3

  def EOR_ZPX(self):
    print("EOR"),
    self.EOR(self.getZeroPageXOperand())
    self.clock += 4

  def EOR_ABS(self):
    print("EOR"),
    self.EOR(self.getAbsoluteOperand())
    self.clock += 4

  def EOR_ABSX(self):
    print("EOR"),
    self.EOR(self.getAbsoluteXOperand())
    self.clock += 4

  def EOR_ABSY(self):
    print("EOR"),
    self.EOR(self.getAbsoluteYOperand())
    self.clock += 4

  def EOR_INDX(self):
    print("EOR"),
    self.EOR(self.getIndirectXOperand())
    self.clock += 6

  def EOR_INDY(self):
    print("EOR"),
    self.EOR(self.getIndirectYOperand())
    self.clock += 5

  def EOR(self, operand):
    self.regA = operand ^ self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
  
  def ADC_IMM(self):
    print("ADC"),
    self.ADC(self.getImmediateOperand())
    self.clock += 2
  
  def ADC_ZP(self):
    print("ADC"),
    self.ADC(self.getZeroPageOperand())
    self.clock += 3
  
  def ADC_ZPX(self):
    print("ADC"),
    self.ADC(self.getZeroPageXOperand)
    self.clock += 4
  
  def ADC_ABS(self):
    print("ADC"),
    self.ADC(self.getAbsoluteOperand)
    self.clock += 4
  
  def ADC_ABSX(self):
    print("ADC"),
    self.ADC(self.getAbsoluteXOperand)
    self.clock += 4
  
  def ADC_ABSY(self):
    print("ADC"),
    self.ADC(self.getAbsoluteYOperand)
    self.clock += 4
  
  def ADC_INDX(self):
    print("ADC"),
    self.ADC(self.getIndirectXOperand)
    self.clock += 6
  
  def ADC_INDY(self):
    print("ADC"),
    self.ADC(self.getIndirectYOperand)
    self.clock += 5
  
  def ADC(self, operand):
    oldNegativeBit = self.regA & 0x80
    #if (operand & 0x80) >> 7: #Negative
    #  operand = ~operand + 1 #Two complement
    self.regA += operand + self.getCarry()
    if oldNegativeBit != (self.regA & 0x80):
      self.setOverflow()
    else:
      self.clearOverflow()
    if self.regA > 0xff:
      self.setCarry()
    else:
      self.clearCarry()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.regA = self.regA & 0xff

  def SBC_IMM(self):
    print("SBC"),
    self.SBC(self.getImmediateOperand())
    self.clock += 2

  def SBC_ZP(self):
    print("SBC"),
    self.SBC(self.getZeroPageOperand())
    self.clock += 3

  def SBC_ZPX(self):
    print("SBC"),
    self.SBC(self.getZeroPageXOperand())
    self.clock += 4

  def SBC_ABS(self):
    print("SBC"),
    self.SBC(self.getAbsoluteOperand())
    self.clock += 4

  def SBC_ABSX(self):
    print("SBC"),
    self.SBC(self.getAbsoluteXOperand())
    self.clock += 4

  def SBC_ABSY(self):
    print("SBC"),
    self.SBC(self.getAbsoluteYOperand())
    self.clock += 4

  def SBC_INDX(self):
    print("SBC"),
    self.SBC(self.getIndirectXOperand())
    self.clock += 6

  def SBC_INDY(self):
    print("SBC"),
    self.SBC(self.getIndirectYOperand())
    self.clock += 5

  def SBC(self, operand):
    oldNegativeBit = self.regA & 0x80
    self.regA -= operand + self.getCarry()
    if oldNegativeBit != (self.regA & 0x80):
      self.setOverflow()
    else:
      self.clearOverflow()
    if self.regA < 0x00:
      self.setCarry()
    else:
      self.clearCarry()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.regA = self.regA & 0xff

  #Hack implementation!
  def JMP_ABS(self):
    print("JMP"),
    adress = self.readWord(self.PC + 1)
    print("$" + format(adress, "04x") + "  "),
    self.PC += 3
    self.JMP(adress)
    self.clock += 3

  def JMP_IND(self):
    print("JMP"),
    self.JMP(self.getIndirectOperand())
    self.clock += 5

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
    self.clock += 6

  def RTS(self):
    print("RTS"),
    #Pop reverse order JSR
    self.PC = self.popStack()
    self.PC += self.popStack() << 8
    self.getImpliedOperand()
    self.clock += 6
 
  def RTI(self):
    print("RTI        "),
    self.PC = self.popStack() << 8
    self.PC += self.popStack()
    self.clock += 6

  def BMI(self):
    print("BMI"),
    result = self.getRelativeOperand()
    if self.getNegative() == 0x01:
      self.PC = result
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2

  def BVC(self):
    print("BVC"),
    result = self.getRelativeOperand()
    if self.getOverflow() == 0x00:
      self.PC = result
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2

  def BCC(self):
    print("BCC"),
    result = self.getRelativeOperand()
    if self.getCarry() == 0x00:
      self.PC = result
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2
  
  def BVS(self):
    print("BVS"),
    result = self.getRelativeOperand()
    if self.getOverflow() == 0x01:
      self.PC = result
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2

  def BCS(self):
    print("BCS"),
    result = self.getRelativeOperand()
    if self.getCarry() == 0x01:
      self.PC = result
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2

  def BPL(self):
    print("BPL"),
    result = self.getRelativeOperand()
    if self.getNegative() == 0x00:
      self.PC = result
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2
  
  def BEQ(self):
    print("BEQ"),
    adress = self.getRelativeOperand()
    if self.getZero() == 0x01:
      self.PC = adress
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2
  
  def BNE(self):
    print("BNE"),
    adress = self.getRelativeOperand()
    if self.getZero() == 0x00:
      self.PC = adress
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2

  def BIT_ZP(self):
    print("BIT"),
    self.BIT(self.getZeroPageOperand())
    self.clock += 3

  def BIT_ABS(self):
    print("BIT"),
    self.BIT(self.getAbsoluteOperand())
    self.clock += 4

  def BIT(self, operand):
    result = self.regA & operand
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(result)
    if self.regA > operand:
      self.setCarry()
    if (operand & 0x40) >> 6:
      self.setOverflow()
    else:
      self.clearOverflow()

  def ROL_ACC(self):
    print("ROL"),
    self.regA <<= 1
    self.regA |= self.getCarry()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.getImpliedOperand()
    self.clock += 2

  def ROL_ZP(self):
    print("ROL"),
    self.ROL(self.getZeroPageAdress())
    self.clock += 5

  def ROL_ZPX(self):
    print("ROL"),
    self.ROL(self.getZeroPageXAdress())
    self.clock += 6

  def ROL_ABS(self):
    print("ROL"),
    self.ROL(self.getAbsoluteAdress())
    self.clock += 6

  def ROL_ABSX(self):
    print("ROL"),
    self.ROL(self.getAbsoluteXAdress())
    self.clock += 7

  def ROL(self, adress):
    operand = readByte(adress)
    operand <<= 1
    operand |= self.getCarry()
    self.writeByte(adress, operand)
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
  
  def ROR_ACC(self):
    print("ROR"),
    self.regA >>= 1
    self.regA |= self.getCarry() << 7
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.getImpliedOperand()
    self.clock += 2
  
  def ROR_ZP(self):
    print("ROR"),
    self.ROR(self.getZeroPageAdress())
    self.clock += 5
  
  def ROR_ZPX(self):
    print("ROR"),
    self.ROR(self.getZeroPageXAdress())
    self.clock += 6
  
  def ROR_ABS(self):
    print("ROR"),
    self.ROR(self.getAbsoluteAdress())
    self.clock += 6
  
  def ROR_ABSX(self):
    print("ROR"),
    self.ROR(self.getAbsoluteXAdress())
    self.clock += 7
  
  def ROR(self, adress):
    operand = readByte(adress)
    operand >>= 1
    operand |= self.getCarry() << 7
    self.writeByte(adress, operand)
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)

  def LSR_ACC(self):
    print("LSR"),
    self.regP |= (self.regA & 0x01)
    self.regA >>= 1
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.getImpliedOperand()
    self.clock += 2

  def LSR_ZP(self):
    print("LSR"),
    adress = self.getZeroPageAdress()
    self.LSR(adress)
    print("$" + format(adress, "02x") + "    "),
    self.clock += 5

  def LSR_ZPX(self):
    print("LSR"),
    adress = self.getZeroPageXAdress()
    self.LSR(adress)
    print("$" + format(adress, "02x") + ",X  "),
    self.clock += 6

  def LSR_ABS(self):
    print("LSR"),
    adress = self.getAbsoluteAdress()
    self.LSR(adress)
    print("$" + format(adress, "04x") + "  "),
    self.clock += 6

  def LSR_ABSX(self):
    print("LSR"),
    adress = self.getAbsoluteXAdress()
    print("$" + format(adress, "04x") + ",X"),
    self.LSR(adress)
    self.clock += 7

  def LSR(self, adress):
    operand = readByte(adress)
    self.regP |= (operand & 0x01)
    operand >>= 1
    self.writeByte(adress, operand)
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)

  def ASL_ACC(self):
    print("ASL"),    
    self.regP |= ((self.regA & 0x80) >> 7)
    self.regA <<= 1
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.clock += 2

  def ASL_ZP(self):
    print("ASL"),
    adress = self.getZeroPageAdress()
    self.ASL(adress)
    print("$" + format(adress, "02x") + "    "),
    self.clock += 5

  def ASL_ZPX(self):
    print("ASL"),
    adress = self.getZeroPageXAdress()
    self.ASL(adress)
    print("$" + format(adress, "02x") + ",X  "),
    self.clock += 6

  def ASL_ABS(self):
    print("ASL"),
    adress = self.getAbsoluteAdress()
    self.ASL(adress)
    print("$" + format(adress, "04x") + "  "),
    self.clock += 6

  def ASL_ABSX(self):
    print("ASL"),
    adress = self.getAbsoluteXAdress()
    self.ASL(adress)
    print("$" + format(adress, "04x") + ",X"),
    self.clock += 7

  def ASL(self, adress):
    operand = readByte(adress)
    self.regP |= ((operand & 0x80) >> 7)
    operand <<= 1
    self.writeByte(adress, operand)
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)

  def SEC(self):
    print("SEC"),
    self.getImpliedOperand()
    self.setCarry()
    self.clock += 2
  
  def SEI(self):
    print("SEI"),
    self.getImpliedOperand()
    self.setInterrupt()
    self.clock += 2
  
  def SED(self):  
    print("SED"),
    self.getImpliedOperand()
    self.setDecimal()
    self.clock += 2
  
  def CLD(self):  
    print("CLD"),
    self.getImpliedOperand()
    self.clearDecimal()
    self.clock += 2
  
  def CLV(self):
    print("CLV"),
    self.getImpliedOperand()
    self.clearOverflow()
    self.clock += 2
  
  def CLC(self):
    print("CLC"),
    self.getImpliedOperand()
    self.clearCarry()
    self.clock += 2
  
  def CLI(self):
    print("CLI"),
    self.getImpliedOperand()
    self.clearInterrupt()
    self.clock += 2
  
  def TXA(self):
    print("TXA"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regX)
    self.setZeroIfZero(self.regX)
    self.regA = self.regX
    self.clock += 2
  
  def TYA(self):
    print("TYA"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regY)
    self.setZeroIfZero(self.regY)
    self.regA = self.regY
    self.clock += 2

  def TAY(self):
    print("TAY"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.regY = self.regA
    self.clock += 2
  
  def TAX(self):
    print("TAX"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.regX = self.regA
    self.clock += 2
  
  def TSX(self):
    print("TSX"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regS)
    self.setZeroIfZero(self.regS)
    self.regX = self.regS
    self.clock += 2
  
  def TXS(self):
    print("TXS"),
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regX)
    self.setZeroIfZero(self.regX)
    self.regS = self.regX
    self.clock += 2

  def PHP(self):
    print("PHP"),
    self.getImpliedOperand()
    self.pushStack(self.regP)
    self.clock += 3

  def PHA(self):
    print("PHA"),
    self.getImpliedOperand()
    self.pushStack(self.regA)
    self.clock += 3

  def PLP(self):
    print("PLP"),
    self.getImpliedOperand()
    self.regP = self.popStack()
    self.clock += 4
  
  def PLA(self):
    print("PLA"),
    self.getImpliedOperand()
    self.regA = self.popStack()
    self.setZeroIfZero(self.regA)
    self.setNegativeIfNegative(self.regA)
    self.clock += 4

  def LDY_ZP(self):
    print("LDY"),
    self.LDY(self.getZeroPageOperand())
    self.clock += 3
  
  def LDY_IMM(self):
    print("LDY"),
    self.LDY(self.getImmediateOperand())
    self.clock += 2

  def LDY_ABS(self):
    print("LDY"),
    self.LDY(self.getAbsoluteOperand())
    self.clock += 4

  def LDY_ZPX(self):
    print("LDY"),
    self.LDY(self.getZeroPageXOperand())
    self.clock += 4

  def LDY_ABSX(self):
    print("LDY"),
    self.LDY(self.getAbsoluteXOperand())
    self.clock += 4

  def LDY(self, operand):
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regY = operand

  def LDX_ZP(self):
    print("LDX"),
    self.LDX(self.getZeroPageOperand())
    self.clock += 3

  def LDX_IMM(self):
    print("LDX"),
    self.LDX(self.getImmediateOperand())
    self.clock += 2

  def LDX_ABS(self):
    print("LDX"),
    self.LDX(self.getAbsoluteOperand())
    self.clock += 4

  def LDX_ZPY(self):
    print("LDX"),
    self.LDX(self.getZeroPageYOperand())
    self.clock += 4

  def LDX_ABSY(self):
    print("LDX"),
    self.LDX(self.getAbsoluteYOperand())
    self.clock += 4

  def LDX(self, operand):
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regX = operand

  def LDA_INDX(self):
    print("LDA"),
    self.LDA(self.getIndirectXOperand())
    self.clock += 6

  def LDA_ZP(self):
    print("LDA"),
    self.LDA(self.getZeroPageOperand())
    self.clock += 3

  def LDA_IMM(self):
    print("LDA"),
    self.LDA(self.getImmediateOperand())
    self.clock += 2

  def LDA_ABS(self):
    print("LDA"),
    self.LDA(self.getAbsoluteOperand())
    self.clock += 4

  def LDA_INDY(self):
    print("LDA"),
    self.LDA(self.getIndirectYOperand())
    self.clock += 5

  def LDA_ZPX(self):
    print("LDA"),
    self.LDA(self.getZeroPageXOperand())
    self.clock += 4

  def LDA_ABSY(self):
    print("LDA"),
    self.LDA(self.getAbsoluteYOperand())
    self.clock += 4

  def LDA_ABSX(self):
    print("LDA"),
    self.LDA(self.getAbsoluteXOperand())
    self.clock += 4

  def LDA(self, operand):
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regA = operand

  def STA_ZP(self):
    print("STA"),
    adress = self.getZeroPageAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STA(adress)
    self.clock += 3

  def STA_ZPX(self):
    print("STA"),
    adress = self.getZeroPageXAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STA(adress)
    self.clock += 4

  def STA_ABS(self):
    print("STA"),
    adress = self.getAbsoluteAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STA(adress)
    self.clock += 4

  def STA_ABSX(self):
    print("STA"),
    adress = self.getAbsoluteXAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STA(adress)
    self.clock += 5

  def STA_ABSY(self):
    print("STA"),
    adress = self.getAbsoluteYAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STA(adress)
    self.clock += 5

  def STA_INDX(self):
    print("STA"),
    adress = self.getIndirectXAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STA(adress)
    self.clock += 6

  def STA_INDY(self):
    print("STA"),
    adress = self.getIndirectYAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STA(adress)
    self.clock += 6

  def STA(self, adress):
    self.writeByte(adress, self.regA)
  
  def STY_ZP(self):
    print("STY"),
    adress = self.getZeroPageAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STY(adress)
    self.clock += 3
  
  def STY_ZPX(self):
    print("STY"),
    adress = self.getZeroPageXAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STY(adress)
    self.clock += 4
  
  def STY_ABS(self):
    print("STY"),
    adress = self.getAbsoluteAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STY(adress)
    self.clock += 4
  
  def STY(self, adress):
    self.writeByte(adress, self.regY)
  
  def STX_ZP(self):
    print("STX"),
    adress = self.getZeroPageAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STX(adress)
    self.clock += 3
  
  def STX_ZPY(self):
    print("STX"),
    adress = self.getZeroPageYAdress()
    print("$" + format(adress, "02x") + "    "),
    self.STX(adress)
    self.clock += 4
  
  def STX_ABS(self):
    print("STX"),
    adress = self.getAbsoluteAdress()
    print("$" + format(adress, "04x") + "  "),
    self.STX(adress)
    self.clock += 4
  
  def STX(self, adress):
    self.writeByte(adress, self.regX)

  def CMP_IMM(self):
    print("CMP"),
    self.CMP(self.getImmediateOperand())
    self.clock += 2
  
  def CMP_ZP(self):
    print("CMP"),
    self.CMP(self.getZeroPageOperand())
    self.clock += 3
  
  def CMP_ZPX(self):
    print("CMP"),
    self.CMP(self.getZeroPageXOperand())
    self.clock += 4
  
  def CMP_ABS(self):
    print("CMP"),
    self.CMP(self.getAbsoluteOperand())
    self.clock += 4
  
  def CMP_ABSX(self):
    print("CMP"),
    self.CMP(self.getAbsoluteXOperand())
    self.clock += 4
  
  def CMP_ABSY(self):
    print("CMP"),
    self.CMP(self.getAbsoluteYOperand())
    self.clock += 4
  
  def CMP_INDX(self):
    print("CMP"),
    self.CMP(self.getIndirectXOperand())
    self.clock += 6
  
  def CMP_INDY(self):
    print("CMP"),
    self.CMP(self.getIndirectYOperand())
    self.clock += 5
  
  def CMP(self, operand):
    if self.regA >= operand:
      self.setCarry()
    if (self.regA == operand):
      self.setZero()
      self.clearNegative()
    #self.setNegativeIfNegative(self.regA)

  def CPY_IMM(self):
    print("CPY"),
    self.CPY(self.getImmediateOperand())
    self.clock += 2

  def CPY_ZP(self):
    print("CPY"),
    self.CPY(self.getZeroPageOperand())
    self.clock += 3

  def CPY_ABS(self):
    print("CPY"),
    self.CPY(self.getAbsoluteOperand())
    self.clock += 4

  def CPY(self, operand):
    if self.regY >= operand:
      self.setCarry()
    if (self.regY == operand):
      self.setZero()
    self.setNegativeIfNegative(self.regY)

  def CPX_IMM(self):
    print("CPX"),
    self.CPX(self.getImmediateOperand())
    self.clock += 2

  def CPX_ZP(self):
    print("CPX"),
    self.CPX(self.getZeroPageOperand())
    self.clock += 3

  def CPX_ABS(self):
    print("CPX"),
    self.CPX(self.getAbsoluteOperand())
    self.clock += 4

  def CPX(self, operand):
    if self.regX > operand:
      self.setCarry()
    if (self.regX == operand):
      self.setZero()
    self.setNegativeIfNegative(self.regX)
  
  def DEY(self):
    print("DEY"),
    self.regY -= 1
    self.setZeroIfZero(self.regY)
    self.setNegativeIfNegative(self.regY)
    self.getImpliedOperand()
    self.clock += 2
  
  def INY(self):
    print("INY"),
    oldNegativeBit = self.regY & 0x80
    self.regY += 1
    if (oldNegativeBit != (self.regY & 0x80)):
      self.setOverflow()
    self.regY &= 0xff
    self.setZeroIfZero(self.regY)
    self.setNegativeIfNegative(self.regY)
    self.getImpliedOperand()
    self.clock += 2
  
  def DEX(self):
    print("DEX"),
    oldNegativeBit = self.regX & 0x80
    self.regX -= 1
    if (oldNegativeBit != (self.regX & 0x80)):
      self.setOverflow()
    self.regX &= 0xff
    self.setZeroIfZero(self.regX)
    self.setNegativeIfNegative(self.regX)
    self.getImpliedOperand()
    self.clock += 2
  
  def INX(self):
    print("INX"),
    oldNegativeBit = self.regX & 0x80
    self.regX += 1
    if (oldNegativeBit != (self.regX & 0x80)):
      self.setOverflow()
    self.regX &= 0xff
    self.setZeroIfZero(self.regX)
    self.setNegativeIfNegative(self.regX)
    self.getImpliedOperand()
    self.clock += 2

  def DEC_ZP(self):
    print("DEC"),
    self.DEC(self.getZeroPageAdress(), self.getZeroPageOperand())
    self.clock += 5

  def DEC_ZPX(self):
    print("DEC"),
    self.DEC(self.getZeroPageXAdress(), self.getZeroPageXOperand())
    self.clock += 6

  def DEC_ABS(self):
    print("DEC"),
    self.DEC(self.getAbsoluteAdress(), self.getAbsoluteOperand())
    self.clock += 6

  def DEC_ABSX(self):
    print("DEC"),
    self.DEC(self.getAbsoluteXAdress(), self.getAbsoluteXOperand())
    self.clock += 7

  def DEC(self, adress, operand):
    operand -= 1
    self.writeByte(adress, operand)
    self.setZeroIfZero(operand)
    self.setNegativeIfNegative(operand)
  
  def INC_ZP(self):
    print("INC"),
    self.INC(self.getZeroPageAdress(), self.getZeroPageOperand())
    self.clock += 5
  
  def INC_ZPX(self):
    print("INC"),
    self.INC(self.getZeroPageXAdress(), self.getZeroPageXOperand())
    self.clock += 6
  
  def INC_ABS(self):
    print("INC"),
    self.INC(self.getAbsoluteAdress(), self.getAbsoluteOperand())
    self.clock += 6
  
  def INC_ABSX(self):
    print("INC"),
    self.INC(self.getAbsoluteXAdress(), self.getAbsoluteXOperand())
    self.clock += 7
  
  def INC(self, adress, operand):
    oldNegativeBit = operand & 0x80
    operand += 1
    if (oldNegativeBit != (operand & 0x80)):
      self.setOverflow()
    operand &= 0xff
    self.writeByte(adress, operand)
    self.setZeroIfZero(operand)
    self.setNegativeIfNegative(operand)