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
      '0xa1' : self.LDA,
      '0xa5' : self.LDA,
      '0xa9' : self.LDA,
      '0xad' : self.LDA,
      '0xb1' : self.LDA,
      '0xb5' : self.LDA,
      '0xb9' : self.LDA,
      '0xbd' : self.LDA
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
      self.mode = 0
      self.operand = 0

      #Execute Opcode
      function_name = self.ops[format(self.currentOP, '#04x')].__name__
      print("%(pc)08d:%(op)02x %(mnen)s" % {"pc":self.PC, "op":self.currentOP, "mnen":function_name}),
      self.printRegisters()
      self.operation = format(self.currentOP, '#04x')
      self.ops[self.operation]()

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
  #HEX: 0x00
  def BRK(self):
    self.PC += 1;
    self.regP |= 0x10 #0001 0000

  #ORA (Or Memory With Accumulator)
  #Affects Flags: S Z
  #Performs logical OR on operand and accumulator, stores result in accumulator
  #Mode: Indirect
  def ORA(self):
    pass
    #Operand |= ACCUMULATOR        // OR the two values together.
    #SET_NEGATIVE(Operand);        // Clears the Negative Flag if the Operand is $#00-7F, otherwise sets it.
    #SET_ZERO(Operand);            // Sets the Zero Flag if the Operand is $#00, otherwise clears it.
    #self.regP = self.regP & 
    #ACCUMULATOR = Operand;        // Stores the Operand in the Accumulator Register.
    #self.regA = 

  #LDA (LoaD Accumulator)
  #Affects Flags: S Z
  def LDA(self):
    if self.operation == '0xa1': #Indirect, x
      pass
    elif self.operation == '0xa5': #Zero page
      pass
    elif self.operation == '0xa9': #Immediatate
      self.PC += 1
      operand = self.ram[self.PC]
      if operand > 0x7f :
        pass
        #self.regP |= 0x70
      self.regA = operand
    elif self.operation == '0xad': #Absolute
      pass
    elif self.operation == '0xb1': #Indirect, Y
      pass
    elif self.operation == '0xb5': #Zero page, X
      pass
    elif self.operation == '0xb9': #Absolute, Y
      pass
    elif self.operation == '0xbd': #Absolute, X
      pass
    pass
