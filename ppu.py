import threading
import cpu

class PpuR2C02 (threading.Thread):
  def __init__(self, memory, writeLock, readLock):
    threading.Thread.__init__(self)
    self.sharedMemory = memory
    self.writeLock = writeLock
    self.readLock = readLock

    self.ramSize = 64*1024 #10kB PPU internal RAM, 64kB adressable
    self.ram = [0]*self.ramSize

    #256*240 pixels
    #8*8 pixel tilemap -> tilemap[32][32]

    #palette table

  def run(self):
    self.readLock.acquire()
    #print("Entering ppu thread")
    #print("PPU: Ram at 0xc000:" + str(format(self.sharedMemory[0xc000], "02x")))
    #print("Exiting ppu thread")
    self.readLock.release()

  def powerUp(self):
    pass

  #----------------------------------------------------------------------
  # REGISTERS
  #----------------------------------------------------------------------
  #$2000 - PPUCTRL [VPHB SINN]
            #NMI enable (V), PPU master/slave (P), sprite height (H), 
            #background tile select (B), sprite tile select (S), 
            #increment mode (I), nametable select (NN)
  #7  bit  0
  #---- ----
  #VPHB SINN
  #|||| ||||
  #|||| ||++- Base nametable address
  #|||| ||    (0 = $2000; 1 = $2400; 2 = $2800; 3 = $2C00)
  #|||| |+--- VRAM address increment per CPU read/write of PPUDATA
  #|||| |     (0: add 1, going across; 1: add 32, going down)
  #|||| +---- Sprite pattern table address for 8x8 sprites
  #||||       (0: $0000; 1: $1000; ignored in 8x16 mode)
  #|||+------ Background pattern table address (0: $0000; 1: $1000)
  #||+------- Sprite size (0: 8x8; 1: 8x16)
  #|+-------- PPU master/slave select
  #|          (0: read backdrop from EXT pins; 1: output color on EXT pins)
  #+--------- Generate an NMI at the start of the
  #           vertical blanking interval (0: off; 1: on)
  def writePPUCTRL(self, value):
    for i in range(0x2000, 0x4000, 8):
      self.sharedMemory[i] = value

  def readPPUCTRL(self):
    return self.sharedMemory[0x2000]

  #$2001 - PPUMASK [BGRs bMmG]
            #Color emphasis (BGR), sprite enable (s), 
            #background enable (b), sprite left column enable (M), 
            #background left column enable (m), greyscale (G)
  #7  bit  0
  #---- ----
  #BGRs bMmG
  #|||| ||||
  #|||| |||+- Grayscale (0: normal color, 1: produce a greyscale display)
  #|||| ||+-- 1: Show background in leftmost 8 pixels of screen, 0: Hide
  #|||| |+--- 1: Show sprites in leftmost 8 pixels of screen, 0: Hide
  #|||| +---- 1: Show background
  #|||+------ 1: Show sprites
  #||+------- Emphasize red*
  #|+-------- Emphasize green*
  #+--------- Emphasize blue*
  def writePPUMASK(self, value):
    for i in range(0x2001, 0x4000, 8):
      self.sharedMemory[i] = value

  def readPPUMASK(self):
    return self.sharedMemory[0x2001]

  #$2002 - PPUSTATUS [VSO- ---]
            #vblank (V), sprite 0 hit (S), 
            #sprite overflow (O), 
            #read resets write pair for $2005/2006
  #7  bit  0
  #---- ----
  #VSO. ....
  #|||| ||||
  #|||+-++++- Least significant bits previously written into a PPU register
  #|||        (due to register not being updated for this address)
  #||+------- Sprite overflow. The intent was for this flag to be set
  #||         whenever more than eight sprites appear on a scanline, but a
  #||         hardware bug causes the actual behavior to be more complicated
  #||         and generate false positives as well as false negatives; see
  #||         PPU sprite evaluation. This flag is set during sprite
  #||         evaluation and cleared at dot 1 (the second dot) of the
  #||         pre-render line.
  #|+-------- Sprite 0 Hit.  Set when a nonzero pixel of sprite 0 overlaps
  #|          a nonzero background pixel; cleared at dot 1 of the pre-render
  #|          line.  Used for raster timing.
  #+--------- Vertical blank has started (0: not in vblank; 1: in vblank).
  #           Set at dot 1 of line 241 (the line *after* the post-render
  #           line); cleared after reading $2002 and at dot 1 of the
  #           pre-render line.
  def writePPUSTATUS(self, value):
    for i in range(0x2002, 0x4000, 8):
      self.sharedMemory[i] = value

  def readPPUSTATUS(self):
    return self.sharedMemory[0x2002]

  #$2003 - OAMADDR [aaaa aaaa]
            #OAM read/write address
  def writeOAMADRR(self, value):
    for i in range(0x2003, 0x4000, 8):
      self.sharedMemory[i] = value

  def readOAMADDR(self):
    return self.sharedMemory[0x2003]

  #$2004 - OAMDATA [dddd dddd]
            #OAM data read/write
  def writeOAMDATA(self, value):
    for i in range(0x2004, 0x4000, 8):
      self.sharedMemory[i] = value

  def readOAMDATA(self):
    return self.sharedMemory[0x2004]

  #$2005 - PPUSCROLL [xxxx xxxx]
            #Fine scroll position (two writes: X, Y)
  #7  bit  0
  #---- ----
  #.... ..YX
  #       ||
  #       |+- 1: Add 256 to the X scroll position
  #       +-- 1: Add 240 to the Y scroll position
  def writePPUSCROLL(self, value):
    for i in range(0x2005, 0x4000, 8):
      self.sharedMemory[i] = value

  def readPPUSCROLL(self):
    return self.sharedMemory[0x2005]

  #$2006 - PPUADDR [aaaa aaaa]
            #PPU read/write address (two writes: MSB, LSB)
  def writePPUADDR(self, value):
    for i in range(0x2006, 0x4000, 8):
      self.sharedMemory[i] = value

  def readPPUADDR(self):
    return self.sharedMemory[0x2006]

  #$2006 - PPUDATA [dddd dddd]
            #PPU data read/write
  def writePPUDATA(self, value):
    for i in range(0x2007, 0x4000, 8):
      self.sharedMemory[i] = value

  def readPPUDATA(self):
    return self.sharedMemory[0x2007]

  #$4014 - OAMDMA [aaaa aaaa]
            #OAM DMA high address
  def writeOAMDMA(self, value):
    self.sharedMemory[0x4014] = value

  def readOAMDMA(self):
    return self.sharedMemory[0x4014]

