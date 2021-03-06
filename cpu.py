import threading
import sys
import binascii

class CpuR2A03 (threading.Thread):
  def __init__(self, memory, writeLock, readLock):
    threading.Thread.__init__(self)
    #Clock
    #Clocked 1.789773Mhz for NTSC (System 21.47727Mhz / 12) and
    #1.773447Mhz for PAL (System 26.601171Mhz / 15)
    clockHertz = 1.773447*1000000 #PAL

    self.ramSize = 64*1024 #2kB CPU internal RAM, 64kB adressable
    #self.ram = [0]*self.ramSize

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
      '0x03' : self.ILLEGAL_SLO_INDX,
      '0x04' : self.ILLEGAL_NOP_ZP,
      '0x05' : self.ORA_ZP,
      '0x06' : self.ASL_ZP,
      '0x07' : self.ILLEGAL_SLO_ZP,      
      '0x08' : self.PHP,
      '0x09' : self.ORA_IMM,
      '0x0a' : self.ASL_ACC,
      '0x0c' : self.ILLEGAL_NOP_ABS,
      '0x0d' : self.ORA_ABS,
      '0x0e' : self.ASL_ABS,
      '0x0f' : self.ILLEGAL_SLO_ABS,
      '0x10' : self.BPL,
      '0x11' : self.ORA_INDY,
      '0x13' : self.ILLEGAL_SLO_INDY,
      '0x14' : self.ILLEGAL_NOP_ZPX,
      '0x15' : self.ORA_ZPX,
      '0x16' : self.ASL_ZPX,
      '0x17' : self.ILLEGAL_SLO_ZPX,
      '0x18' : self.CLC,
      '0x19' : self.ORA_ABSY,
      '0x1a' : self.ILLEGAL_NOP_IMP,
      '0x1b' : self.ILLEGAL_SLO_ABSY,
      '0x1c' : self.ILLEGAL_NOP_ABSX,
      '0x1d' : self.ORA_ABSX,
      '0x1e' : self.ASL_ABSX,
      '0x1f' : self.ILLEGAL_SLO_ABSX,
      '0x20' : self.JSR,
      '0x21' : self.AND_INDX,
      '0x23' : self.ILLEGAL_RLA_INDX,
      '0x24' : self.BIT_ZP,
      '0x25' : self.AND_ZP,
      '0x26' : self.ROL_ZP,
      '0x27' : self.ILLEGAL_RLA_ZP,
      '0x28' : self.PLP,
      '0x29' : self.AND_IMM,
      '0x2a' : self.ROL_ACC,
      '0x2c' : self.BIT_ABS,
      '0x2d' : self.AND_ABS,
      '0x2e' : self.ROL_ABS,
      '0x2f' : self.ILLEGAL_RLA_ABS,
      '0x30' : self.BMI,
      '0x31' : self.AND_INDY,
      '0x33' : self.ILLEGAL_RLA_INDY,
      '0x34' : self.ILLEGAL_NOP_ZPX,
      '0x35' : self.AND_ZPX,
      '0x36' : self.ROL_ZPX,
      '0x37' : self.ILLEGAL_RLA_ZPX,
      '0x38' : self.SEC,
      '0x39' : self.AND_ABSY,
      '0x3a' : self.ILLEGAL_NOP_IMP,
      '0x3b' : self.ILLEGAL_RLA_ABSY,
      '0x3c' : self.ILLEGAL_NOP_ABSX,
      '0x3d' : self.AND_ABSX,
      '0x3e' : self.ROL_ABSX,
      '0x3f' : self.ILLEGAL_RLA_ABSX,
      '0x40' : self.RTI,
      '0x41' : self.EOR_INDX,
      '0x43' : self.ILLEGAL_SRE_INDX,
      '0x44' : self.ILLEGAL_NOP_ZP,
      '0x45' : self.EOR_ZP,
      '0x46' : self.LSR_ZP,
      '0x47' : self.ILLEGAL_SRE_ZP,
      '0x48' : self.PHA,
      '0x49' : self.EOR_IMM,
      '0x4a' : self.LSR_ACC,
      '0x4c' : self.JMP_ABS,
      '0x4d' : self.EOR_ABS,
      '0x4e' : self.LSR_ABS,
      '0x4f' : self.ILLEGAL_SRE_ABS,
      '0x50' : self.BVC,
      '0x51' : self.EOR_INDY,
      '0x53' : self.ILLEGAL_SRE_INDY,
      '0x54' : self.ILLEGAL_NOP_ZPX,
      '0x55' : self.EOR_ZPX,
      '0x56' : self.LSR_ZPX,
      '0x57' : self.ILLEGAL_SRE_ZPX,
      '0x58' : self.CLI,
      '0x59' : self.EOR_ABSY,
      '0x5a' : self.ILLEGAL_NOP_IMP,
      '0x5b' : self.ILLEGAL_SRE_ABSY,
      '0x5c' : self.ILLEGAL_NOP_ABSX,
      '0x5d' : self.EOR_ABSX,
      '0x5e' : self.LSR_ABSX,
      '0x5f' : self.ILLEGAL_SRE_ABSX,
      '0x60' : self.RTS,
      '0x61' : self.ADC_INDX,
      '0x63' : self.ILLEGAL_RRA_INDX,
      '0x64' : self.ILLEGAL_NOP_ZP,
      '0x65' : self.ADC_ZP,
      '0x66' : self.ROR_ZP,
      '0x67' : self.ILLEGAL_RRA_ZP,
      '0x68' : self.PLA,
      '0x69' : self.ADC_IMM,
      '0x6a' : self.ROR_ACC,
      '0x6c' : self.JMP_IND,
      '0x6d' : self.ADC_ABS,
      '0x6e' : self.ROR_ABS,
      '0x6f' : self.ILLEGAL_RRA_ABS,
      '0x70' : self.BVS,
      '0x71' : self.ADC_INDY,
      '0x73' : self.ILLEGAL_RRA_INDY,
      '0x74' : self.ILLEGAL_NOP_ZPX,
      '0x75' : self.ADC_ZPX,
      '0x76' : self.ROR_ZPX,
      '0x77' : self.ILLEGAL_RRA_ZPX,
      '0x78' : self.SEI,
      '0x79' : self.ADC_ABSY,
      '0x7a' : self.ILLEGAL_NOP_IMP,
      '0x7b' : self.ILLEGAL_RRA_ABSY,
      '0x7c' : self.ILLEGAL_NOP_ABSX,
      '0x7d' : self.ADC_ABSX,
      '0x7e' : self.ROR_ABSX,
      '0x7f' : self.ILLEGAL_RRA_ABSX,
      '0x80' : self.ILLEGAL_NOP_IMM,
      '0x81' : self.STA_INDX,
      '0x83' : self.ILLEGAL_SAX_INDX,
      '0x84' : self.STY_ZP,
      '0x85' : self.STA_ZP,
      '0x86' : self.STX_ZP,
      '0x87' : self.ILLEGAL_SAX_ZP,
      '0x88' : self.DEY,
      '0x8a' : self.TXA,
      '0x8c' : self.STY_ABS,
      '0x8d' : self.STA_ABS,
      '0x8e' : self.STX_ABS,
      '0x8f' : self.ILLEGAL_SAX_ABS,
      '0x90' : self.BCC,
      '0x91' : self.STA_INDY,
      '0x94' : self.STY_ZPX,
      '0x95' : self.STA_ZPX,
      '0x96' : self.STX_ZPY,
      '0x97' : self.ILLEGAL_SAX_ZPY,
      '0x98' : self.TYA,
      '0x99' : self.STA_ABSY,
      '0x9a' : self.TXS,
      '0x9d' : self.STA_ABSX,
      '0xa0' : self.LDY_IMM,
      '0xa1' : self.LDA_INDX,
      '0xa2' : self.LDX_IMM,
      '0xa3' : self.ILLEGAL_LAX_INDX,
      '0xa4' : self.LDY_ZP,
      '0xa5' : self.LDA_ZP,
      '0xa6' : self.LDX_ZP,
      '0xa7' : self.ILLEGAL_LAX_ZP,
      '0xa8' : self.TAY,
      '0xa9' : self.LDA_IMM,
      '0xaa' : self.TAX,
      '0xac' : self.LDY_ABS,
      '0xad' : self.LDA_ABS,
      '0xae' : self.LDX_ABS,
      '0xaf' : self.ILLEGAL_LAX_ABS,
      '0xb0' : self.BCS,
      '0xb1' : self.LDA_INDY,
      '0xb3' : self.ILLEGAL_LAX_INDY,
      '0xb4' : self.LDY_ZPX,
      '0xb5' : self.LDA_ZPX,
      '0xb6' : self.LDX_ZPY,
      '0xb7' : self.ILLEGAL_LAX_ZPY,
      '0xb8' : self.CLV,
      '0xb9' : self.LDA_ABSY,
      '0xba' : self.TSX,
      '0xbc' : self.LDY_ABSX,
      '0xbd' : self.LDA_ABSX,
      '0xbe' : self.LDX_ABSY,
      '0xbf' : self.ILLEGAL_LAX_ABSY,
      '0xc0' : self.CPY_IMM,
      '0xc1' : self.CMP_INDX,
      '0xc3' : self.ILLEGAL_DCP_INDX,
      '0xc4' : self.CPY_ZP,
      '0xc5' : self.CMP_ZP,
      '0xc6' : self.DEC_ZP,
      '0xc7' : self.ILLEGAL_DCP_ZP,
      '0xc8' : self.INY,
      '0xc9' : self.CMP_IMM,
      '0xca' : self.DEX,
      '0xcc' : self.CPY_ABS,
      '0xcd' : self.CMP_ABS,
      '0xce' : self.DEC_ABS,
      '0xcf' : self.ILLEGAL_DCP_ABS,
      '0xd0' : self.BNE,
      '0xd1' : self.CMP_INDY,
      '0xd3' : self.ILLEGAL_DCP_INDY,
      '0xd5' : self.CMP_ZPX,
      '0xd4' : self.ILLEGAL_NOP_ZPX,
      '0xd6' : self.DEC_ZPX,
      '0xd7' : self.ILLEGAL_DCP_ZPX,
      '0xd8' : self.CLD,
      '0xd9' : self.CMP_ABSY,
      '0xda' : self.ILLEGAL_NOP_IMP,
      '0xdb' : self.ILLEGAL_DCP_ABSY,
      '0xdc' : self.ILLEGAL_NOP_ABSX,
      '0xdd' : self.CMP_ABSX,
      '0xde' : self.DEC_ABSX,
      '0xdf' : self.ILLEGAL_DCP_ABSX,
      '0xe0' : self.CPX_IMM,
      '0xe1' : self.SBC_INDX,
      '0xe3' : self.ILLEGAL_ISB_INDX,
      '0xe4' : self.CPX_ZP,
      '0xe5' : self.SBC_ZP,
      '0xe6' : self.INC_ZP,
      '0xe7' : self.ILLEGAL_ISB_ZP,
      '0xe8' : self.INX,
      '0xe9' : self.SBC_IMM,
      '0xea' : self.NOP,
      '0xeb' : self.ILLEGAL_SBC_IMM,
      '0xec' : self.CPX_ABS,
      '0xed' : self.SBC_ABS,
      '0xee' : self.INC_ABS,
      '0xef' : self.ILLEGAL_ISB_ABS,
      '0xf0' : self.BEQ,
      '0xf1' : self.SBC_INDY,
      '0xf3' : self.ILLEGAL_ISB_INDY,
      '0xf4' : self.ILLEGAL_NOP_ZPX,
      '0xf5' : self.SBC_ZPX,
      '0xf6' : self.INC_ZPX,
      '0xf7' : self.ILLEGAL_ISB_ZPX,
      '0xf8' : self.SED,
      '0xf9' : self.SBC_ABSY,
      '0xfa' : self.ILLEGAL_NOP_IMP,
      '0xfb' : self.ILLEGAL_ISB_ABSY,
      '0xfc' : self.ILLEGAL_NOP_ABSX,
      '0xfd' : self.SBC_ABSX,
      '0xfe' : self.INC_ABSX,
      '0xff' : self.ILLEGAL_ISB_ABSX
      }

  #----------------------------------------------------------------------
  # CPU MAIN LOGIC
  #----------------------------------------------------------------------

  def printRegisters(self):
    print('A:%(ra)02X X:%(rx)02X Y:%(ry)02X P:%(rp)02X SP:%(rs)02X CYC:%(clc)4d' %\
          {"ra":self.currentRegA, "rx":self.currentRegX, "ry":self.currentRegY, "rs":self.currentRegS, "rp":self.currentRegP,"clc":self.currentClock})
    
  def load(self, filename):
    #print("Loading " + str(filename) + " ...")
    #Load bytes from file
    tempRam = [0]*self.ramSize
    f = open(filename, 'rb')
    try:
      byte = f.read(1)
      i = 0
      while byte:
        x = binascii.hexlify(byte)
        tempRam[i] = int(str(x,'ascii'), 16)
        byte = f.read(1)
        i += 1
    finally:
      f.close()
      #print(str(i) + " = 0x" + format(i, "04X") + " bytes loaded")
      
    #Verify 'NES' + MS-DOS end-of-file
    if (tempRam[0] != 0x4e) or (tempRam[1] != 0x45) or (tempRam[2] != 0x53) or (tempRam[3] != 0x1a):
      print("String 'NES' not found. Aborting loading.")
      return
    
    self.nrOf16kbPrgRomBanks = tempRam[4]
    self.nrOf8kbChrRomBanks = tempRam[5] #0 means CHR RAM (AKA VRAM)
    self.romControlByte1 = tempRam[6]
    self.romControlByte2 = tempRam[7]
    self.nrOf8kbPrgRamBanks = tempRam[8]

    #print(str(self.nrOf16kbPrgRomBanks) + " 16kbPrgRomBank(s) detected")
    #print(str(self.nrOf8kbChrRomBanks) + " 8kbChrRomBank(s) detected")
    #print(str(self.nrOf8kbPrgRamBanks) + " 8kbPrgRomBank(s) detected")

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
    #print("Loading complete.")
    
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

  def startPC(self, pc):
    self.PC = pc;

  def run(self):
    for i in range(0,8991):
      #Fetch opcode, print
      self.readLock.acquire()
      self.currentOpcode = self.ram[self.PC]
      print("%(pc)04X  %(op)02X " % {"pc":self.PC, "op":self.currentOpcode}, end="")
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

      self.readLock.release()

  def dumpRomData(self):
    for i in range(0xffff):
      print(format(i, "04X") + ": " + format(self.ram[i], "02X"))

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
    self.regS = self.regS % 0x100

  def popStack(self):
    self.regS += 1
    self.regS = self.regS % 0x100
    returnValue = self.readByte(self.regS + self.stackOffset)
    return returnValue;

  #Mirror memory if write to certain adresses
  def writeByte(self, adress, value):
    if adress <= 0x00ff or (0x0800 <= adress <= 0x08ff) or (0x1000 <= adress <= 0x10ff) or (0x1800 < adress <= 0x18ff): #Zero page
      self.ram[adress] = value
      self.ram[adress + 0x0800] = value
      self.ram[adress + 0x1000] = value
      self.ram[adress + 0x1800] = value
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

  def printImpliedOp(self, op):
    print("      " + op + "                            ", end="")

  def printImmOp(self, op, operand):
    print(format(operand, "02X") + "    ", end="")
    print(op + " #$" + format(operand, "02X") + "                       ", end="")

  def printRelativeOp(self, op, adress, operand):
    print(format(operand, "02X") + "     ", end="")
    print(op + " $" + format(adress, "04X") + "                      ", end="")

  def printZP(self, op, zpadress, operand):
    print(format(zpadress,"02X") + "    ", end="")
    print(op + " $" + format(zpadress,"02X") + " = ", end="")
    print(format(operand, "02X") + "                   ", end="")

  def printZPX(self, op, adress1, adress2, operand):
    print(format(adress1, "02X") + "    ", end="")
    print(op + " $" + format(adress1, "02X") + ",X @ " + format(adress2, "02X") + " = ", end="")
    print(format(operand, "02X") + "            ", end="")

  def printZPY(self, op, adress1, adress2, operand):
    print(format(adress1, "02X") + "     ", end="")
    print(op + " $" + format(adress1, "02X") + ",Y @ " + format(adress2, "02X") + " = ", end="")
    print(format(operand, "02X") + "            ", end="")

  def printABS(self, op, adress, operand):
    print(format(adress & 0x00ff, "02X") + " " + format(adress >> 8, "02X") + " ", end="")
    print(op + " $" + format(adress, "04X") + " = ", end="")
    print(format(operand, "02X") + "                 ", end="")

  def printABSX(self, op, adress1, adress2, operand):
    print(format(adress1 & 0x00ff, "02X") + " " + format((adress1 & 0xff00) >> 8, "02X") + " ", end="")
    print(op + " $" + format(adress1, "04X") + ",X @ " + format(adress2, "04X") + " = ", end="")
    print(format(operand, "02X") + "        ", end="")

  def printABSY(self, op, adress1, adress2, operand):    
    print(format(adress1 & 0x00ff, "02X") + " " + format((adress1 & 0xff00) >> 8, "02X") + " ", end="")
    print(op + " $" + format(adress1, "04X") + ",Y @ " + format(adress2, "04X") + " = ", end="")
    print(format(operand, "02X") + "        ", end="")

  def printIND(self, op, adress, operand):
    print(format(adress & 0x00ff, "02X") + " " + format((adress & 0xff00) >> 8, "02X") + "  ", end="")
    print(op + " ($" + format(adress, "04X") + ") = " + format(operand, "04X") + "             ", end="")

  def printINDX(self, op, adress1, adress2, adress3, operand):
    print(format(adress1, "02X") + "    ", end="")
    print(op + " ($" + format(adress1, "02X") + ",X) @ " + format(adress2, "02X") + " = ", end="")
    print(format(adress3, "04X") + " = " + format(operand, "02X") + "   ", end="")

  def printINDY(self, op, adress1, adress2, adress3, operand):
    print(format(adress1, "02X") + "    ", end="")
    print(op + " ($" + format(adress1, "02X") + "),Y = ", end="")
    print(format(adress2, "04X") + " @ " + format(adress3, "04X") + " = ", end="")
    print(format(operand, "02X") + " ", end="")  

  def printJMPJSR(self, op, adress, operand):
    print(format(operand & 0x00ff, "02X") + " " + format(operand >> 8, "02X") + "  ", end="")
    print(op + " $" + format(adress, "04X") + "                      ", end="")

  #----------------------------------------------------------------------
  # ADRESSING MODES
  #----------------------------------------------------------------------

  def getImpliedOperand(self):
    self.PC += 1

  def getAccumulatorOperand(self):
    self.PC += 1

  def getImmediateOperand(self):
    operand = self.readByte(self.PC + 1)
    self.PC += 2
    return operand

  def getZP(self, reg):
    adress1 = self.readByte(self.PC + 1)
    adress2 = (adress1  + reg) & 0x00ff # Zero page wrapping
    operand = self.readByte(adress2)
    self.PC += 2
    return adress1, adress2, operand

  def getABS(self, reg):
    adress1 = self.readWord(self.PC + 1)
    adress2 = (adress1 + reg) & 0xffff
    operand = self.readByte(adress2)
    self.PC += 3
    return adress1, adress2, operand

  def getIND(self):
    adress1 = self.readWord(self.PC + 1)
    adress2 = self.readWord(adress1)
    operand = self.readByte(adress2)
    self.PC += 3
    return adress1, adress2

  #AKA Indexed Indirect or pre-indexed
  #    Indirect addressing modes do not handle page boundary crossing at all.
  #    When the parameter's low byte is $FF, the effective address wraps
  #    around and the CPU fetches high byte from $xx00 instead of $xx00+$0100.
  #    E.g. JMP ($01FF) fetches PCL from $01FF and PCH from $0100,
  #    and LDA ($FF),Y fetches the base address from $FF and $00.
  def getINDX(self):
    adress1 = self.readByte(self.PC + 1)
    adress2 = (adress1 + self.regX) & 0xff
    low = self.ram[adress2]
    high = self.ram[(adress2 + 1) & 0xff] << 8
    adress3 = high + low
    operand = self.readByte(adress3)
    self.PC += 2
    return adress1, adress2, adress3, operand

  #AKA Indirect Indexed or post-indexed
  #    Zero page adress indexing, i.e wraparound when adress1 is over 0xff
  def getINDY(self):
    adress1 = self.readByte(self.PC + 1)
    low = self.ram[adress1]
    high = self.ram[(adress1 + 1) & 0xff] << 8
    adress2 = low + high
    adress3 = (adress2 + self.regY) & 0xffff
    operand = self.readByte(adress3)
    self.PC += 2
    return adress1, adress2, adress3, operand

  #Relative adressing do not handle page boundary crossing at all.
  def getRelativeOperand(self):
    operand = self.readByte(self.PC + 1)
    tempPage = self.PC & 0xff00
    adress = self.PC + operand + 2
    if (operand & 0x80): #Negative adress
      adress = (adress & 0x00ff) + tempPage
    return adress, operand
   	
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
    self.clearNegative()
    if (operand & 0x80):
      self.setNegative()

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
    self.setZero()
    if operand:
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
    self.pushStack(self.PC >> 8)
    self.pushStack(self.PC & 0x00ff)
    self.pushStack(self.regP)
    self.PC = self.readWord(0xfffe)
    self.setBreak()
    self.getImpliedOperand()
    self.clock += 7
    self.printImpliedOp(" BRK")

  def NOP(self):
    self.getImpliedOperand()
    self.clock += 2
    self.printImpliedOp(" NOP")

  def AND_IMM(self):
    operand = self.getImmediateOperand()
    self.AND(operand)
    self.clock += 2
    self.printImmOp(" AND", operand)

  def AND_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.AND(operand)
    self.clock += 3
    self.printZP(" AND", adress2, operand)

  def AND_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.AND(operand)
    self.clock += 4
    self.printZPX(" AND", adress1, adress2, operand)

  def AND_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.AND(operand)
    self.clock += 4
    self.printABS(" AND", adress2, operand)

  def AND_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.AND(operand)
    self.clock += 4
    self.printABSX(" AND", adress1, adress2, operand)

  def AND_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.AND(operand)
    self.clock += 4
    self.printABSY(" AND", adress1, adress2, operand)

  def AND_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.AND(operand)
    self.clock += 6
    self.printINDX(" AND", adress1, adress2, adress3, operand)

  def AND_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.AND(operand)
    self.clock += 5
    self.printINDY(" AND", adress1, adress2, adress3, operand)

  def AND(self, operand):
    self.regA = operand & self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)

  def ORA_IMM(self):
    operand = self.getImmediateOperand()
    self.ORA(operand)
    self.clock += 2
    self.printImmOp(" ORA", operand)

  def ORA_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.ORA(operand)
    self.clock += 3
    self.printZP(" ORA", adress2, operand)

  def ORA_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.ORA(operand)
    self.clock += 4
    self.printZPX(" ORA", adress1, adress2, operand)

  def ORA_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.ORA(operand)
    self.clock += 4
    self.printABS(" ORA", adress2, operand)

  def ORA_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.ORA(operand)
    self.clock += 4
    self.printABSX(" ORA", adress1, adress2, operand)

  def ORA_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.ORA(operand)
    self.clock += 4
    self.printABSY(" ORA", adress1, adress2, operand)

  def ORA_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.ORA(operand)
    self.clock += 6
    self.printINDX(" ORA", adress1, adress2, adress3, operand)

  def ORA_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.ORA(operand)
    self.clock += 5
    self.printINDY(" ORA", adress1, adress2, adress3, operand)

  def ORA(self, operand):
    self.regA = operand | self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)

  def EOR_IMM(self):
    operand = self.getImmediateOperand()
    self.EOR(operand)
    self.clock += 2
    self.printImmOp(" EOR", operand)

  def EOR_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.EOR(operand)
    self.clock += 3
    self.printZP(" EOR", adress2, operand)

  def EOR_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.EOR(operand)
    self.clock += 4
    self.printZPX(" EOR", adress1, adress2, operand)

  def EOR_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.EOR(operand)
    self.clock += 4
    self.printABS(" EOR", adress2, operand)

  def EOR_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.EOR(operand)
    self.clock += 4
    self.printABSX(" EOR", adress1, adress2, operand)

  def EOR_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.EOR(operand)
    self.clock += 4
    self.printABSY(" EOR", adress1, adress2, operand)

  def EOR_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.EOR(operand)
    self.clock += 6
    self.printINDX(" EOR", adress1, adress2, adress3, operand)

  def EOR_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.EOR(operand)
    self.clock += 5
    self.printINDY(" EOR", adress1, adress2, adress3, operand)

  def EOR(self, operand):
    self.regA = operand ^ self.regA
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
  
  def ADC_IMM(self):
    operand = self.getImmediateOperand()
    self.ADC(operand)
    self.clock += 2
    self.printImmOp(" ADC", operand)
  
  def ADC_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.ADC(operand)
    self.clock += 3
    self.printZP(" ADC", adress2, operand)
  
  def ADC_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.ADC(operand)
    self.clock += 4
    self.printZPX(" ADC", adress1, adress2, operand)
  
  def ADC_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.ADC(operand)
    self.clock += 4
    self.printABS(" ADC", adress2, operand)
  
  def ADC_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.ADC(operand)
    self.clock += 4
    self.printABSX(" ADC", adress1, adress2, operand)
  
  def ADC_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.ADC(operand)
    self.clock += 4
    self.printABSY(" ADC", adress1, adress2, operand)
  
  def ADC_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.ADC(operand)
    self.clock += 6
    self.printINDX(" ADC", adress1, adress2, adress3, operand)
  
  def ADC_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.ADC(operand)
    self.clock += 5
    self.printINDY(" ADC", adress1, adress2, adress3, operand)
  
  def ADC(self, operand):
    sum = self.regA + operand + self.getCarry() #A + M + C -> A
    self.clearCarry()
    if sum > 0xff: #Outside 8-bit unsigned range
      self.setCarry()
    self.clearOverflow()
    self.regP |= (~(self.regA ^ operand) & (self.regA ^ sum) & 0x80) >> 1 #Overflow
    self.clearNegative()
    self.regP |= sum & 0x80 #Negative
    self.regA = sum & 0xff
    self.setZeroIfZero(self.regA)

  def SBC_IMM(self):
    operand = self.getImmediateOperand()
    self.SBC(operand)
    self.clock += 2
    self.printImmOp(" SBC", operand)

  def SBC_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.SBC(operand)
    self.clock += 3
    self.printZP(" SBC", adress2, operand)

  def SBC_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.SBC(operand)
    self.clock += 4
    self.printZPX(" SBC", adress1, adress2, operand)

  def SBC_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.SBC(operand)
    self.clock += 4
    self.printABS(" SBC", adress2, operand)

  def SBC_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.SBC(operand)
    self.clock += 4
    self.printABSX(" SBC", adress1, adress2, operand)

  def SBC_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.SBC(operand)
    self.clock += 4
    self.printABSY(" SBC", adress1, adress2, operand)

  def SBC_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.SBC(operand)
    self.clock += 6
    self.printINDX(" SBC", adress1, adress2, adress3, operand)

  def SBC_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.SBC(operand)
    self.clock += 5
    self.printINDY(" SBC", adress1, adress2, adress3, operand)

  def SBC(self, operand):
    self.ADC(~operand & 0xff)

  def JMP_ABS(self):
    adress = self.readWord(self.PC + 1)
    self.PC += 3
    self.JMP(adress)
    self.clock += 3
    self.printJMPJSR("JMP", adress, adress)

  #AN INDIRECT JUMP MUST NEVER USE A
  #VECTOR BEGINNING ON THE LAST BYTE
  #OF A PAGE
  #    For example if address $3000 contains $40, $30FF contains $80, 
  #    and $3100 contains $50, the result of JMP ($30FF) will be a transfer of
  #    control to $4080 rather than $5080 as you intended i.e. the 6502 took 
  #    the low byte of the address from $30FF and the high byte from $3000. 
  def JMP_IND(self):
    adress, operand = self.getIND()
    #Check if jump is on last byte of a page (boundary check)
    if (adress & 0x00ff == 0xff):
      lowAdress = self.ram[adress]
      highAdress = self.ram[adress & 0xff00] << 8
      newOperand = highAdress + lowAdress
      self.JMP(newOperand)
    else:
      self.JMP(operand)
    self.clock += 5
    self.printIND("JMP", adress, operand);

  def JMP(self, operand):
    self.PC = operand

  def JSR(self):
    adress = self.readWord(self.PC + 1)
    self.PC += 2
    self.pushStack(self.PC >> 8)
    self.pushStack(self.PC & 0x00ff)
    self.PC = adress
    self.clock += 6
    self.printJMPJSR("JSR", adress, adress)

  def RTS(self):
    #Pop reverse order JSR
    self.PC = self.popStack()
    self.PC += self.popStack() << 8
    self.getImpliedOperand()
    self.clock += 6
    self.printImpliedOp(" RTS")
 
  def RTI(self):
    self.regP = self.popStack()
    self.regP |= 0x20 #TODO: why set this bit
    self.PC = self.popStack()
    self.PC += self.popStack() << 8
    self.clock += 6
    self.printImpliedOp(" RTI")

  def BMI(self):
    adress, operand = self.getRelativeOperand()
    if self.getNegative():
      self.PC = adress
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2
    self.printRelativeOp("BMI", adress, operand)

  def BVC(self):
    adress, operand = self.getRelativeOperand()
    if self.getOverflow() == 0x00:
      self.PC = adress
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2
    self.printRelativeOp("BVC", adress, operand)

  def BCC(self):
    adress, operand = self.getRelativeOperand()
    if self.getCarry() == 0x00:
      self.PC = adress
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2
    self.printRelativeOp("BCC", adress, operand)
  
  def BVS(self):
    adress, operand = self.getRelativeOperand()
    if self.getOverflow():
      self.PC = adress
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2
    self.printRelativeOp("BVS", adress, operand)

  def BCS(self):
    adress, operand = self.getRelativeOperand()
    if self.getCarry():
      self.PC = adress
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2
    self.printRelativeOp("BCS", adress, operand)

  def BPL(self):
    adress, operand = self.getRelativeOperand()
    if self.getNegative() == 0x00:
      self.PC = adress
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2
    self.printRelativeOp("BPL", adress, operand)
  
  def BEQ(self):
    adress, operand = self.getRelativeOperand()
    if self.getZero():
      self.PC = adress
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2
    self.printRelativeOp("BEQ", adress, operand)
  
  def BNE(self):
    adress, operand = self.getRelativeOperand()
    if self.getZero() == 0x00:
      self.PC = adress
      self.clock += 3
    else:
      self.PC += 2
      self.clock += 2
    self.printRelativeOp("BNE", adress, operand)

  def BIT_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.BIT(operand)
    self.clock += 3
    self.printZP(" BIT", adress2, operand)

  def BIT_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.BIT(operand)
    self.clock += 4
    self.printABS(" BIT", adress2, operand)

  def BIT(self, operand):
    result = self.regA & operand
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(result)
    if self.regA > operand:
      self.setCarry()
    self.clearOverflow()
    self.regP |= operand & 0x40
    #if (operand & 0x40) >> 6:
    #  self.setOverflow()
    #else:
    #  self.clearOverflow()

  def ROL_ACC(self):
    self.regA <<= 1
    self.regA |= self.getCarry()
    self.regA &= 0xff
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.getImpliedOperand()
    self.clock += 2
    self.printImpliedOp(" ROL")

  def ROL_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.ROL(adress2)
    self.clock += 5
    self.printZP(" ROL", adress2, operand)

  def ROL_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.ROL(adress2)
    self.clock += 6
    self.printZPX(" ROL", adress1, adress2, operand)

  def ROL_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.ROL(adress2)
    self.clock += 6
    self.printABS(" ROL", adress2, operand)

  def ROL_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.ROL(adress2)
    self.clock += 7
    self.printABSX(" ROL", adress1, adress2, operand)

  def ROL(self, adress):
    operand = self.readByte(adress)
    bit = (operand & 0x80) >> 7
    operand <<= 1
    operand &= 0xff
    operand |= self.getCarry()
    self.writeByte(adress, operand)
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.clearCarry()
    self.regP |= bit
  
  def ROR_ACC(self):
    zerobit = self.regA & 0x01
    self.regA >>= 1
    self.regA |= self.getCarry() << 7
    self.clearCarry()
    self.regP |= zerobit #Carry
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.getImpliedOperand()
    self.clock += 2
    self.printImpliedOp(" ROR")
  
  def ROR_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.ROR(adress2)
    self.clock += 5
    self.printZP(" ROR", adress2, operand)
  
  def ROR_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.ROR(adress2)
    self.clock += 6
    self.printZPX(" ROR", adress1, adress2, operand)
  
  def ROR_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.ROR(adress2)
    self.clock += 6
    self.printABS(" ROR", adress2, operand)
  
  def ROR_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.ROR(adress2)
    self.clock += 7
    self.printABSX(" ROR", adress1, adress2, operand)
  
  def ROR(self, adress):
    operand = self.readByte(adress)
    tempCarry = operand & 0x01
    operand >>= 1
    operand |= self.getCarry() << 7
    self.regP |= tempCarry
    self.writeByte(adress, operand)
    self.clearNegative()
    if operand & 0x80:
      self.setNegative() 
    self.setZeroIfZero(operand)

  def LSR_ACC(self):
    self.clearCarry()
    self.regP |= self.regA & 0x01
    self.regA >>= 1
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.getImpliedOperand()
    self.clock += 2
    self.printImpliedOp(" LSR")

  def LSR_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.LSR(adress2)
    self.clock += 5
    self.printZP(" LSR", adress2, operand)

  def LSR_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.LSR(adress2)
    self.clock += 6
    self.printZPX(" LSR", adress1, adress2, operand)

  def LSR_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.LSR(adress2)
    self.clock += 6
    self.printABS(" LSR", adress2, operand)

  def LSR_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.LSR(adress2)
    self.clock += 7
    self.printABSX(" LSR", adress1, adress2, operand)

  def LSR(self, adress):
    operand = self.readByte(adress)
    self.clearCarry()
    self.regP |= (operand & 0x01)
    operand >>= 1
    self.writeByte(adress, operand)
    self.setNegativeIfNegative(operand)
    self.clearZero()
    if (operand == 0):
      self.setZero()

  def ASL_ACC(self):
    self.clearCarry()
    self.regP |= (self.regA & 0x80) >> 7
    self.regA <<= 1
    self.regA &= 0xff
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.clock += 2
    self.getImpliedOperand()
    self.printImpliedOp(" ASL")

  def ASL_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.ASL(adress2)
    self.clock += 5
    self.printZP(" ASL", adress2, operand)

  def ASL_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.ASL(adress2)
    self.clock += 6
    self.printZPX(" ASL", adress1, adress2, operand)

  def ASL_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.ASL(adress2)
    self.clock += 6
    self.printABS(" ASL", adress2, operand)

  def ASL_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.ASL(adress2)
    self.clock += 7
    self.printABSX(" ASL", adress1, adress2, operand)

  def ASL(self, adress):
    operand = self.readByte(adress)
    self.clearCarry()
    self.regP |= ((operand & 0x80) >> 7)
    operand <<= 1
    operand &= 0xff
    self.writeByte(adress, operand)
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)

  def SEC(self):
    self.getImpliedOperand()
    self.setCarry()
    self.clock += 2
    self.printImpliedOp(" SEC")
  
  def SEI(self):
    self.getImpliedOperand()
    self.setInterrupt()
    self.clock += 2
    self.printImpliedOp(" SEI")
  
  def SED(self):
    self.getImpliedOperand()
    self.setDecimal()
    self.clock += 2
    self.printImpliedOp(" SED")
  
  def CLD(self):
    self.getImpliedOperand()
    self.clearDecimal()
    self.clock += 2
    self.printImpliedOp(" CLD")
  
  def CLV(self):
    self.getImpliedOperand()
    self.clearOverflow()
    self.clock += 2
    self.printImpliedOp(" CLV")
  
  def CLC(self):
    self.getImpliedOperand()
    self.clearCarry()
    self.clock += 2
    self.printImpliedOp(" CLC")
  
  def CLI(self):
    self.getImpliedOperand()
    self.clearInterrupt()
    self.clock += 2
    self.printImpliedOp(" CLI")
  
  def TXA(self):
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regX)
    self.setZeroIfZero(self.regX)
    self.regA = self.regX
    self.clock += 2
    self.printImpliedOp(" TXA")
  
  def TYA(self):
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regY)
    self.setZeroIfZero(self.regY)
    self.regA = self.regY
    self.clock += 2
    self.printImpliedOp(" TYA")

  def TAY(self):
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.regY = self.regA
    self.clock += 2
    self.printImpliedOp(" TAY")
  
  def TAX(self):
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regA)
    self.setZeroIfZero(self.regA)
    self.regX = self.regA
    self.clock += 2
    self.printImpliedOp(" TAX")
  
  def TSX(self):
    self.getImpliedOperand()
    self.setNegativeIfNegative(self.regS)
    self.setZeroIfZero(self.regS)
    self.regX = self.regS
    self.clock += 2
    self.printImpliedOp(" TSX")
  
  def TXS(self):
    self.getImpliedOperand()
    self.regS = self.regX
    self.clock += 2
    self.printImpliedOp(" TXS")

  def PHP(self):
    self.getImpliedOperand()
    self.pushStack(self.regP)
    self.clock += 3
    self.printImpliedOp(" PHP")

  def PHA(self):
    self.getImpliedOperand()
    self.pushStack(self.regA)
    self.clock += 3
    self.printImpliedOp(" PHA")

  def PLP(self):
    self.getImpliedOperand()
    self.regP = (self.popStack() | 0x20) & 0xef #Set unused P register bit & clear (B)inary
    self.clock += 4
    self.printImpliedOp(" PLP")
  
  def PLA(self):
    self.getImpliedOperand()
    self.regA = self.popStack()
    self.setZeroIfZero(self.regA)
    self.setNegativeIfNegative(self.regA)
    self.clock += 4
    self.printImpliedOp(" PLA")

  def LDY_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.LDY(operand)
    self.clock += 3
    self.printZP(" LDY", adress2, operand)
  
  def LDY_IMM(self):
    operand = self.getImmediateOperand()
    self.LDY(operand)
    self.clock += 2
    self.printImmOp(" LDY", operand)

  def LDY_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.LDY(operand)
    self.clock += 4
    self.printABS(" LDY", adress2, operand)

  def LDY_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.LDY(operand)
    self.clock += 4
    self.printZPX(" LDY", adress1, adress2, operand)

  def LDY_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.LDY(operand)
    self.clock += 4
    self.printABSX(" LDY", adress1, adress2, operand)

  def LDY(self, operand):
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regY = operand

  def LDX_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.LDX(operand)
    self.clock += 3
    self.printZP(" LDX", adress2, operand)

  def LDX_IMM(self):
    operand = self.getImmediateOperand()
    self.LDX(operand)
    self.clock += 2
    self.printImmOp(" LDX", operand)

  def LDX_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.LDX(operand)
    self.clock += 4
    self.printABS(" LDX", adress2, operand)

  def LDX_ZPY(self):
    adress1, adress2, operand = self.getZP(self.regY)
    self.LDX(operand)
    self.clock += 4
    self.printZPY("LDX", adress1, adress2, operand)

  def LDX_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.LDX(operand)
    self.clock += 4
    self.printABSY(" LDX", adress1, adress2, operand)

  def LDX(self, operand):
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regX = operand

  def LDA_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.LDA(operand)
    self.clock += 6
    self.printINDX(" LDA", adress1, adress2, adress3, operand)

  def LDA_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.LDA(operand)
    self.clock += 3
    self.printZP(" LDA", adress2, operand)

  def LDA_IMM(self):
    operand = self.getImmediateOperand()
    self.LDA(operand)
    self.clock += 2
    self.printImmOp(" LDA", operand)

  def LDA_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.LDA(operand)
    self.clock += 4
    self.printABS(" LDA", adress2, operand)

  def LDA_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.LDA(operand)
    self.clock += 5
    self.printINDY(" LDA", adress1, adress2, adress3, operand)

  def LDA_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.LDA(operand)
    self.clock += 4
    self.printZPX(" LDA", adress1, adress2, operand)

  def LDA_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.LDA(operand)
    self.clock += 4
    self.printABSY(" LDA", adress1, adress2, operand)

  def LDA_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.LDA(operand)
    self.clock += 4
    self.printABSX(" LDA", adress1, adress2, operand)

  def LDA(self, operand):
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.regA = operand

  def STA_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.STA(adress2)
    self.clock += 3
    self.printZP(" STA", adress2, operand)

  def STA_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.STA(adress2)
    self.clock += 4
    self.printZPX(" STA", adress1, adress2, operand)

  def STA_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.STA(adress2)
    self.clock += 4
    self.printABS(" STA", adress2, operand)

  def STA_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.STA(adress2)
    self.clock += 5
    self.printABSX(" STA", adress1, adress2, operand)

  def STA_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.STA(adress2)
    self.clock += 5
    self.printABSY(" STA", adress1, adress2, operand)

  def STA_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.STA(adress3)
    self.clock += 6
    self.printINDX(" STA", adress1, adress2, adress3, operand)

  def STA_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.STA(adress3)
    self.clock += 6
    self.printINDY(" STA", adress1, adress2, adress3, operand)

  def STA(self, adress):
    self.writeByte(adress, self.regA)
  
  def STY_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.STY(adress2)
    self.clock += 3
    self.printZP(" STY", adress2, operand)
  
  def STY_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.STY(adress2)
    self.clock += 4
    self.printZPX(" STY", adress1, adress2, operand)
  
  def STY_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.STY(adress2)
    self.clock += 4
    self.printABS(" STY", adress2, operand)
  
  def STY(self, adress):
    self.writeByte(adress, self.regY)
  
  def STX_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.STX(adress2)
    self.clock += 3
    self.printZP(" STX", adress2, operand)
  
  def STX_ZPY(self):
    adress1, adress2, operand = self.getZP(self.regY)
    self.STX(adress2)
    self.clock += 4
    self.printZPY("STX", adress1, adress2, operand)
  
  def STX_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.STX(adress2)
    self.clock += 4
    self.printABS(" STX", adress2, operand)
  
  def STX(self, adress):
    self.writeByte(adress, self.regX)

  def CMP_IMM(self):
    operand = self.getImmediateOperand()
    self.CMP(operand)
    self.clock += 2
    self.printImmOp(" CMP", operand)
  
  def CMP_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.CMP(operand)
    self.clock += 3
    self.printZP(" CMP", adress2, operand)
  
  def CMP_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.CMP(operand)
    self.clock += 4
    self.printZPX(" CMP", adress1, adress2, operand)
  
  def CMP_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.CMP(operand)
    self.clock += 4
    self.printABS(" CMP", adress2, operand)
  
  def CMP_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.CMP(operand)
    self.clock += 4
    self.printABSX(" CMP", adress1, adress2, operand)
  
  def CMP_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.CMP(operand)
    self.clock += 4
    self.printABSY(" CMP", adress1, adress2, operand)
  
  def CMP_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.CMP(operand)
    self.clock += 6
    self.printINDX(" CMP", adress1, adress2, adress3, operand)
  
  def CMP_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.CMP(operand)
    self.clock += 5
    self.printINDY(" CMP", adress1, adress2, adress3, operand)
  
  def CMP(self, operand):
    self.clearCarry()
    if self.regA >= operand:
      self.setCarry()
    self.clearZero()
    if self.regA == operand:
      self.setZero()
    self.clearNegative()
    if (self.regA - operand) & 0x80:
      self.setNegative()

  def CPY_IMM(self):
    operand = self.getImmediateOperand()
    self.CPY(operand)
    self.clock += 2
    self.printImmOp(" CPY", operand)

  def CPY_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.CPY(operand)
    self.clock += 3
    self.printZP(" CPY", adress2, operand)

  def CPY_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.CPY(operand)
    self.clock += 4
    self.printABS(" CPY", adress2, operand)

  def CPY(self, operand):
    self.clearCarry()
    if self.regY >= operand:
      self.setCarry()
    self.setZeroIfZero(self.regY - operand)
    self.setNegativeIfNegative(self.regY - operand)

  def CPX_IMM(self):
    operand = self.getImmediateOperand()
    self.CPX(operand)
    self.clock += 2
    self.printImmOp(" CPX", operand)

  def CPX_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.CPX(operand)
    self.clock += 3
    self.printZP(" CPX", adress2, operand)

  def CPX_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.CPX(operand)
    self.clock += 4
    self.printABS(" CPX", adress2, operand)

  def CPX(self, operand):
    if self.regX >= operand:
      self.setCarry()
    else:
      self.clearCarry()
    self.setZeroIfZero(self.regX - operand)
    self.setNegativeIfNegative(self.regX - operand)
  
  def DEY(self):
    self.regY -= 1
    if self.regY < 0x00:
      self.regY = 256 + self.regY
    self.setZeroIfZero(self.regY)
    self.setNegativeIfNegative(self.regY)
    self.getImpliedOperand()
    self.clock += 2
    self.printImpliedOp(" DEY")
  
  def INY(self):
    self.regY += 1
    self.regY &= 0xff
    self.setZeroIfZero(self.regY)
    self.setNegativeIfNegative(self.regY)
    self.getImpliedOperand()
    self.clock += 2
    self.printImpliedOp(" INY")
  
  def DEX(self):
    self.regX -= 1
    if self.regX < 0x00:
      self.regX = 256 + self.regX
    self.setZeroIfZero(self.regX)
    self.setNegativeIfNegative(self.regX)
    self.getImpliedOperand()
    self.clock += 2
    self.printImpliedOp(" DEX")
  
  def INX(self):
    self.regX += 1
    self.regX &= 0xff
    self.setZeroIfZero(self.regX)
    self.setNegativeIfNegative(self.regX)
    self.getImpliedOperand()
    self.clock += 2
    self.printImpliedOp(" INX")

  def DEC_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.DEC(adress2, operand)
    self.clock += 5
    self.printZP(" DEC", adress2, operand)

  def DEC_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.DEC(adress2, operand)
    self.clock += 6
    self.printZPX(" DEC", adress1, adress2, operand)

  def DEC_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.DEC(adress2, operand)
    self.clock += 6
    self.printABS(" DEC", adress2, operand)

  def DEC_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.DEC(adress2, operand)
    self.clock += 7
    self.printABSX(" DEC", adress1, adress2, operand)

  def DEC(self, adress, operand):
    operand -= 1
    operand &= 0xff
    self.writeByte(adress, operand)
    self.setZeroIfZero(operand)
    self.setNegativeIfNegative(operand)
  
  def INC_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.INC(adress2, operand)
    self.clock += 5
    self.printZP(" INC", adress2, operand)
  
  def INC_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.INC(adress2, operand)
    self.clock += 6
    self.printZPX(" INC", adress1, adress2, operand)
  
  def INC_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.INC(adress2, operand)
    self.clock += 6
    self.printABS(" INC", adress2, operand)
  
  def INC_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.INC(adress2, operand)
    self.clock += 7
    self.printABSX(" INC", adress1, adress2, operand)
  
  def INC(self, adress, operand):
    operand += 1
    operand &= 0xff
    self.writeByte(adress, operand)
    self.setZeroIfZero(operand)
    self.setNegativeIfNegative(operand)

  #----------------------------------------------------------------------
  # ILLEGAL OPCODES
  #----------------------------------------------------------------------

  def ILLEGAL_NOP_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.clock += 3
    self.printZP("*NOP", adress2, operand)

  def ILLEGAL_NOP_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.clock += 4
    self.printABS("*NOP", adress2, operand)

  def ILLEGAL_NOP_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.clock += 4
    self.printZPX("*NOP", adress1, adress2, operand)

  def ILLEGAL_NOP_IMP(self):
    self.getImpliedOperand()
    self.clock += 7
    self.printImpliedOp("*NOP")

  def ILLEGAL_NOP_IMM(self):
    operand = self.getImmediateOperand()
    self.clock += 2
    self.printImmOp("*NOP", operand)

  def ILLEGAL_NOP_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.clock += 4
    self.printABSX("*NOP", adress1, adress2, operand)

  def ILLEGAL_LAX_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.regA = operand
    self.regX = operand
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.clock += 6
    self.printINDX("*LAX", adress1, adress2, adress3, operand)

  def ILLEGAL_LAX_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.regA = operand
    self.regX = operand
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.clock += 3
    self.printZP("*LAX", adress2, operand)

  def ILLEGAL_LAX_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.regA = operand
    self.regX = operand
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.clock += 4
    self.printABS("*LAX", adress2, operand)

  def ILLEGAL_LAX_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.regA = operand
    self.regX = operand
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.clock += 5
    self.printINDY("*LAX", adress1, adress2, adress3, operand)

  def ILLEGAL_LAX_ZPY(self):
    adress1, adress2, operand = self.getZP(self.regY)
    self.regA = operand
    self.regX = operand
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.clock += 4
    self.printZPY("*LAX", adress1, adress2, operand)

  def ILLEGAL_LAX_ABSY(self):    
    adress1, adress2, operand = self.getABS(self.regY)
    self.regA = operand
    self.regX = operand
    self.setNegativeIfNegative(operand)
    self.setZeroIfZero(operand)
    self.clock += 4
    self.printABSY("*LAX", adress1, adress2, operand)

  def ILLEGAL_SAX_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    toStore = self.regA & self.regX
    self.writeByte(adress3, toStore)
    self.clock += 6
    self.printINDX("*SAX", adress1, adress2, adress3, operand)

  def ILLEGAL_SAX_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    toStore = self.regA & self.regX
    self.writeByte(adress2, toStore)
    self.clock += 4
    self.printABS("*SAX", adress2, operand)

  def ILLEGAL_SAX_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    toStore = self.regA & self.regX
    self.writeByte(adress2, toStore)
    self.clock += 3
    self.printZP("*SAX", adress2, operand)

  def ILLEGAL_SAX_ZPY(self):
    adress1, adress2, operand = self.getZP(self.regY)
    toWrite = self.regA & self.regX
    self.writeByte(adress2, toWrite)
    self.clock += 4
    self.printZPY("*SAX", adress1, adress2, operand)

  def ILLEGAL_SBC_IMM(self):
    operand = self.getImmediateOperand()
    self.SBC(operand)
    self.clock += 2
    self.printImmOp("*SBC", operand)

  def ILLEGAL_DCP(self, adress, operand):
    self.DEC(adress, operand)
    self.CMP(operand - 1)
    self.clearZero()
    if operand == 0x00:
      self.setZero()

  def ILLEGAL_DCP_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.ILLEGAL_DCP(adress2, operand)
    self.clock += 5
    self.printZP("*DCP", adress2, operand)

  def ILLEGAL_DCP_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.ILLEGAL_DCP(adress2, operand)
    self.clock += 6
    self.printZPX("*DCP", adress1, adress2, operand)

  def ILLEGAL_DCP_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.ILLEGAL_DCP(adress2, operand)
    self.clock += 6
    self.printABS("*DCP", adress2, operand)

  def ILLEGAL_DCP_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.ILLEGAL_DCP(adress2, operand)
    self.clock += 7
    self.printABSY("*DCP", adress1, adress2, operand)

  def ILLEGAL_DCP_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.ILLEGAL_DCP(adress2, operand)
    self.clock += 7
    self.printABSX("*DCP", adress1, adress2, operand)

  def ILLEGAL_DCP_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.ILLEGAL_DCP(adress3, operand)
    self.clock += 8
    self.printINDX("*DCP", adress1, adress2, adress3, operand)

  def ILLEGAL_DCP_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.ILLEGAL_DCP(adress3, operand)
    self.clock += 8
    self.printINDY("*DCP", adress1, adress2, adress3, operand)

  def ILLEGAL_ISB(self, adress, operand):
    self.INC(adress, operand)
    self.SBC(operand + 1)

  def ILLEGAL_ISB_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.ILLEGAL_ISB(adress2, operand)
    self.clock += 5
    self.printZP("*ISB", adress2,operand)

  def ILLEGAL_ISB_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.ILLEGAL_ISB(adress2, operand)
    self.clock += 6
    self.printZPX("*ISB", adress1, adress2, operand)

  def ILLEGAL_ISB_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.ILLEGAL_ISB(adress2, operand)
    self.clock += 6
    self.printABS("*ISB", adress2, operand)

  def ILLEGAL_ISB_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.ILLEGAL_ISB(adress2, operand)
    self.clock += 7
    self.printABSY("*ISB", adress1, adress2, operand)

  def ILLEGAL_ISB_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.ILLEGAL_ISB(adress3, operand)
    self.clock += 8
    self.printINDX("*ISB", adress1, adress2, adress3, operand)

  def ILLEGAL_ISB_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.ILLEGAL_ISB(adress3, operand)
    self.clock += 8
    self.printINDY("*ISB", adress1, adress2, adress3, operand)

  def ILLEGAL_ISB_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.ILLEGAL_ISB(adress2, operand)
    self.clock += 7
    self.printABSX("*ISB", adress1, adress2, operand)

  def ILLEGAL_SLO(self, adress):
    self.ASL(adress)
    operand = self.readByte(adress)
    self.ORA(operand)

  def ILLEGAL_SLO_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.ILLEGAL_SLO(adress3)
    self.clock += 8
    self.printINDX("*SLO", adress1, adress2, adress3, operand)

  def ILLEGAL_SLO_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.ILLEGAL_SLO(adress2)
    self.clock += 5
    self.printZP("*SLO", adress2, operand)

  def ILLEGAL_SLO_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.ILLEGAL_SLO(adress2)
    self.clock += 6
    self.printABS("*SLO", adress2, operand)

  def ILLEGAL_SLO_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.ILLEGAL_SLO(adress3)
    self.clock += 8
    self.printINDY("*SLO", adress1, adress2, adress3, operand)

  def ILLEGAL_SLO_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.ILLEGAL_SLO(adress2)
    self.clock += 6
    self.printZPX("*SLO", adress1, adress2, operand)

  def ILLEGAL_SLO_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.ILLEGAL_SLO(adress2)
    self.clock += 7
    self.printABSY("*SLO", adress1, adress2, operand)

  def ILLEGAL_SLO_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.ILLEGAL_SLO(adress2)
    self.clock += 7
    self.printABSX("*SLO", adress1, adress2, operand)

  def ILLEGAL_RLA(self, adress):
    self.ROL(adress)
    operand = self.readByte(adress)
    self.AND(operand)

  def ILLEGAL_RLA_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.ILLEGAL_RLA(adress3)
    self.clock += 8
    self.printINDX("*RLA", adress1, adress2, adress3, operand)

  def ILLEGAL_RLA_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.ILLEGAL_RLA(adress2)
    self.clock += 5
    self.printZP("*RLA", adress2, operand)

  def ILLEGAL_RLA_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.ILLEGAL_RLA(adress2)
    self.clock += 6
    self.printABS("*RLA", adress2, operand)

  def ILLEGAL_RLA_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.ILLEGAL_RLA(adress3)
    self.clock += 8
    self.printINDY("*RLA", adress1, adress2, adress3, operand)

  def ILLEGAL_RLA_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.ILLEGAL_RLA(adress2)
    self.clock += 6
    self.printZPX("*RLA", adress1, adress2, operand)

  def ILLEGAL_RLA_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.ILLEGAL_RLA(adress2)
    self.clock += 7
    self.printABSY("*RLA", adress1, adress2, operand)

  def ILLEGAL_RLA_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.ILLEGAL_RLA(adress2)
    self.clock += 7
    self.printABSX("*RLA", adress1, adress2, operand)

  def ILLEGAL_SRE(self, adress):
    self.LSR(adress)
    operand = self.readByte(adress)
    self.EOR(operand)

  def ILLEGAL_SRE_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.ILLEGAL_SRE(adress3)
    self.clock += 8
    self.printINDX("*SRE", adress1, adress2, adress3, operand)

  def ILLEGAL_SRE_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.ILLEGAL_SRE(adress2)
    self.clock += 5
    self.printZP("*SRE", adress2, operand)

  def ILLEGAL_SRE_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.ILLEGAL_SRE(adress2)
    self.clock += 6
    self.printABS("*SRE", adress2, operand)

  def ILLEGAL_SRE_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.ILLEGAL_SRE(adress3)
    self.clock += 8
    self.printINDY("*SRE", adress1, adress2, adress3, operand)

  def ILLEGAL_SRE_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.ILLEGAL_SRE(adress2)
    self.clock += 6
    self.printZPX("*SRE", adress1, adress2, operand)

  def ILLEGAL_SRE_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.ILLEGAL_SRE(adress2)
    self.clock += 7
    self.printABSY("*SRE", adress1, adress2, operand)

  def ILLEGAL_SRE_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.ILLEGAL_SRE(adress2)
    self.clock += 7
    self.printABSX("*SRE", adress1, adress2, operand)

  def ILLEGAL_RRA(self, adress):
    self.ROR(adress)
    operand = self.readByte(adress)
    self.ADC(operand)

  def ILLEGAL_RRA_INDX(self):
    adress1, adress2, adress3, operand = self.getINDX()
    self.ILLEGAL_RRA(adress3)
    self.clock += 8
    self.printINDX("*RRA", adress1, adress2, adress3, operand)

  def ILLEGAL_RRA_ZP(self):
    adress1, adress2, operand = self.getZP(0)
    self.ILLEGAL_RRA(adress2)
    self.clock += 5
    self.printZP("*RRA", adress2, operand)

  def ILLEGAL_RRA_ABS(self):
    adress1, adress2, operand = self.getABS(0)
    self.ILLEGAL_RRA(adress2)
    self.clock += 6
    self.printABS("*RRA", adress2, operand)

  def ILLEGAL_RRA_INDY(self):
    adress1, adress2, adress3, operand = self.getINDY()
    self.ILLEGAL_RRA(adress3)
    self.clock += 8
    self.printINDY("*RRA", adress1, adress2, adress3, operand)

  def ILLEGAL_RRA_ZPX(self):
    adress1, adress2, operand = self.getZP(self.regX)
    self.ILLEGAL_RRA(adress2)
    self.clock += 6
    self.printZPX("*RRA", adress1, adress2, operand)

  def ILLEGAL_RRA_ABSY(self):
    adress1, adress2, operand = self.getABS(self.regY)
    self.ILLEGAL_RRA(adress2)
    self.clock += 7
    self.printABSY("*RRA", adress1, adress2, operand)

  def ILLEGAL_RRA_ABSX(self):
    adress1, adress2, operand = self.getABS(self.regX)
    self.ILLEGAL_RRA(adress2)
    self.clock += 7
    self.printABSX("*RRA", adress1, adress2, operand)