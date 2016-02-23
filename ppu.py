import threading

class PpuR2C02 (threading.Thread):
  #Constants
  #xRes = 256 
  #yRes = 240 #224 for NTSC
  def __init__(self):
    threading.Thread.__init__(self)
    self.spriteArray = []

  def run(self):
  	print("Entering ppu thread")
  	print("Exiting ppu thread")
