import threading
import pygame
from pygame.locals import *

#Address range Size  Description
#$0000-$0FFF $1000 Pattern table 0
#$1000-$1FFF $1000 Pattern Table 1
#$2000-$23FF $0400 Nametable 0
#$2400-$27FF $0400 Nametable 1
#$2800-$2BFF $0400 Nametable 2
#$2C00-$2FFF $0400 Nametable 3
#$3000-$3EFF $0F00 Mirrors of $2000-$2EFF
#$3F00-$3F1F $0020 Palette RAM indexes
#$3F20-$3FFF $00E0 Mirrors of $3F00-$3F1F
class PpuR2C02 (threading.Thread):
  def __init__(self, memory, writeLock, readLock):
    threading.Thread.__init__(self)
    self.sharedMemory = memory
    self.writeLock = writeLock
    self.readLock = readLock

    self.ramSize = 64*1024 #10kB PPU internal RAM, 64kB adressable
    self.ram = [0]*self.ramSize

    self.clock = 0
    self.evenOddFrame = 0

    #8*8 pixel tilemap -> tilemap[32][30]

    #palette table

    #Display init
    pygame.init()
    size = width, height = 256, 240
    grey = 128,128,128
    red = 255,0,0

    surface = pygame.display.set_mode(size)
    surface.fill(red)
    self.pxarray = pygame.PixelArray(surface)
    pygame.display.flip()

  def displayNameTable(self):
    self.ctrl = self.readPPUCTRL()
    self.ppumask = self.readPPUMASK()
    self.scroll = self.readPPUSCROLL()

    self.ntno = (self.ctrl & 0x3)*0x400
    self.ptno = ((self.ctrl & 0x10) >> 4)*0x1000

    #First 960 bytes are control for cell, attribute table is last 64 bytes
    self.nametable = [0]*0x400 #1024 byte nametable
    i = 0
    self.readLock.acquire()
    for address in range(0x2000,0x2400):
      self.nametable[i] = self.sharedMemory[address + self.ntno]
      if self.nametable[i] != 0:
        print(self.nametable[i])
      i += 1
    self.readLock.release()

    #Draw pixels
    for tile_y in range(0,240,8):
      for tile_x in range(0,256,8):
        for x in range(8):
          for y in range(8):
            self.pxarray[tile_x+x, tile_y+y] = pygame.Color(self.nametable[tile_x >> 8 + (tile_y >> 8)*32], 0, 0)

    pygame.display.flip()

  def run(self):
    #30, 8-pixel-tiles/frame -> 240 y-pixels/frame + 6 dummy lines
    #32, 8-pixel-tiles/frame -> 256 x-pixels/frame
    
    #Get sprite ram (OAM)
    #for visibleScanline in range (0,240):
    #  self.drawVisibleScanLine(visibleScanline)
    #self.postRender() #Renders 240-260
    #self.preRender() #Renders 261

    #self.evenOddFrame = ~self.evenOddFrame + 2 #Toggle even/odd

    # Render frame
    #pygame.display.flip()

    self.displayNameTable()

  def readTile(self):
    #Conceptually, the PPU does this 33 times for each scanline:
        #Fetch a nametable entry from $2000-$2FBF.
        #Fetch the corresponding attribute table entry from $23C0-$2FFF and increment the current VRAM address within the same row.
        #Fetch the low-order byte of an 8x1 pixel sliver of pattern table from $0000-$0FF7 or $1000-$1FF7.
        #Fetch the high-order byte of this sliver from an address 8 bytes higher.
        #Turn the attribute data and the pattern table data into palette indices, and combine them with data from sprite data using priority.

    #Read NT (Name Table) Byte
    #Read AT (Attribute Table) Byte
    #Read low BG tile Byte
    #Read high BG tile Byte
    pass

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
    self.readLock.acquire()
    for i in range(0x2000, 0x4000, 8):
      self.sharedMemory[i] = value
    self.readLock.release()

  def readPPUCTRL(self):
    self.readLock.acquire()
    r = self.sharedMemory[0x2000]
    self.readLock.release()
    return r

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
    self.readLock.acquire()
    for i in range(0x2001, 0x4000, 8):
      self.sharedMemory[i] = value
    self.readLock.release()

  def readPPUMASK(self):
    self.readLock.acquire()
    r = self.sharedMemory[0x2001]
    self.readLock.release()
    return r

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
    self.readLock.acquire()
    for i in range(0x2002, 0x4000, 8):
      self.sharedMemory[i] = value
    self.readLock.release()

  def readPPUSTATUS(self):
    self.readLock.acquire()
    r = self.sharedMemory[0x2002]
    self.readLock.release()
    return r

  #$2003 - OAMADDR [aaaa aaaa]
            #OAM read/write address
  def writeOAMADRR(self, value):
    self.readLock.acquire()
    for i in range(0x2003, 0x4000, 8):
      self.sharedMemory[i] = value
    self.readLock.release()

  def readOAMADDR(self):
    self.readLock.acquire()
    r = self.sharedMemory[0x2003]
    self.readLock.release()
    return r

  #$2004 - OAMDATA [dddd dddd]
            #OAM data read/write
  def writeOAMDATA(self, value):
    self.readLock.acquire()
    for i in range(0x2004, 0x4000, 8):
      self.sharedMemory[i] = value
    self.readLock.release()

  def readOAMDATA(self):
    self.readLock.acquire()
    r = self.sharedMemory[0x2004]
    self.readLock.release()
    return r

  #$2005 - PPUSCROLL [xxxx xxxx]
            #Fine scroll position (two writes: X, Y)
  #7  bit  0
  #---- ----
  #.... ..YX
  #       ||
  #       |+- 1: Add 256 to the X scroll position
  #       +-- 1: Add 240 to the Y scroll position
  def writePPUSCROLL(self, value):
    self.readLock.acquire()
    for i in range(0x2005, 0x4000, 8):
      self.sharedMemory[i] = value
    self.readLock.release()

  def readPPUSCROLL(self):
    self.readLock.acquire()
    r = self.sharedMemory[0x2005]
    self.readLock.release()
    return r

  #$2006 - PPUADDR [aaaa aaaa]
            #PPU read/write address (two writes: MSB, LSB)
  def writePPUADDR(self, value):
    self.readLock.acquire()
    for i in range(0x2006, 0x4000, 8):
      self.sharedMemory[i] = value
    self.readLock.release()

  def readPPUADDR(self):
    self.readLock.acquire()
    r = self.sharedMemory[0x2006]
    self.readLock.release()
    return r

  #$2006 - PPUDATA [dddd dddd]
            #PPU data read/write
  def writePPUDATA(self, value):
    self.readLock.acquire()
    for i in range(0x2007, 0x4000, 8):
      self.sharedMemory[i] = value
    self.readLock.release()

  def readPPUDATA(self):
    self.readLock.acquire()
    r = self.sharedMemory[0x2007]
    self.readLock.release()
    return r

  #$4014 - OAMDMA [aaaa aaaa]
            #OAM DMA high address
  def writeOAMDMA(self, value):
    self.readLock.acquire()
    self.sharedMemory[0x4014] = value
    self.readLock.release()

  def readOAMDMA(self):
    self.readLock.acquire()
    r = self.sharedMemory[0x4014]
    self.readLock.release()
    return r


  #----------------------------------------------------------------------
  # LOGIC
  #----------------------------------------------------------------------

  def readNTByte(self):
    pass
  
  def readATByte(self):
    pass

  def readLowBGTileByte(self):
    pass

  def readHighBGTileByte(self):
    pass

  def drawVisibleScanLine(self, scanline):
    #1 Scanline lasts for 341PPU clock cycles, with each clock cycle producing one pixel. 
    #1 CPU cycle = 3 PPU Cycles
    
    self.readLock.acquire()
    for pixelNo in range(0,256):
      #Fetch background tile data - 2bits/pixel

      #fine_x selects a bit

      #Mux with priority sprite

      #Draw pixel
      self.pxarray[pixelNo, scanline] = pygame.Color(255, pixelNo, scanline)

      #Update
    self.readLock.release()

    self.clock += 341
    #self.readLock.acquire()
    #print(scanline)
    #self.readLock.release()

  def postRender(self):
    self.clock += 341

  def preRender(self):
    self.clock += 341