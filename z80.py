class z80:
    A = "11111111"
    F = "11111111"
    A1 = "11111111"#shadow registers seem to equal the value in the real register if not initialized
    F1 = "11111111"
    B = "11111111"
    C = "11111111"
    D = "11111111"
    E = "11111111"
    H = "00000000"
    L = "00000000"
    B1 = "11111111"
    C1 = "11111111"
    D1 = "11111111"
    E1 = "11111111"
    H1 = "00000000"
    L1 = "00000000"
    IX = "0000000000000000"
    IY = "0000000000000000"
    PC = 0
    R = 1
    SP = 65535
    a0 = a1 = a2 = a3 = a4 = a5 = a6 = a7 = a8 = a9 = a10 = a11 = a12 = a13 = a14 = a15 = False
    d0 = d1 = d2 = d3 = d4 = d5 = d6 = d7 = False
    RD = False 
    WR = True 
    debugline = ""
    delay = 0
    instructionname = ""
    opcode = ""
    operand1 = ""
    operand2 = ""
    needmorebits = False
    execute = False
    prejumppc = 0
    stage = ""
    interupts = False
    halt = False 
    opx = ""
    opy = ""
    preopcode = ""
    I = "00000000"

    
#********************************************************what we do each clock tick*************************************
    def clock(self,clockval):
        
      
        
        
        if self.WR == True:
        

            binaddr = bin(self.PC)[2:].zfill(16)
            
            
        
            if binaddr[15] == "1": self.a0 = True 
            else: self.a0 = False
            if binaddr[14] == "1": self.a1 = True
            else: self.a1 = False
            if binaddr[13] == "1": self.a2 = True
            else: self.a2 = False
            if binaddr[12] == "1": self.a3 = True 
            else: self.a3 = False
            if binaddr[11] == "1": self.a4 = True
            else: self.a4 = False
            if binaddr[10] == "1": self.a5 = True
            else: self.a5 = False
            if binaddr[9] == "1": self.a6 = True 
            else: self.a6 = False
            if binaddr[8] == "1": self.a7 = True 
            else: self.a7 = False
            if binaddr[7] == "1": self.a8 = True 
            else: self.a8 = False
            if binaddr[6] == "1": self.a9 = True
            else: self.a9 = False
            if binaddr[5] == "1": self.a10 = True
            else: self.a10 = False
            if binaddr[4] == "1": self.a11 = True 
            else: self.a11 = False
            if binaddr[3] == "1": self.a12 = True 
            else: self.a12 = False
            if binaddr[2] == "1": self.a13 = True
            else: self.a13 = False
            if binaddr[1] == "1": self.a14 = True
            else: self.a14 = False
            if binaddr[0] == "1": self.a15 = True 
            else: self.a15 = False

        if clockval == True:# are we on a postive clock cycle
 
            if self.d7: data = "1"
            else: data = "0"
            if self.d6: data = data + "1"
            else: data = data + "0"
            if self.d5: data = data + "1"
            else: data = data + "0"
            if self.d4: data = data + "1"
            else: data = data + "0"
            if self.d3: data = data + "1"
            else: data = data + "0"
            if self.d2: data = data + "1"
            else: data = data + "0"
            if self.d1: data = data + "1"
            else: data = data + "0"
            if self.d0: data = data + "1"
            else: data = data + "0"
            
            
            if self.halt == True: 
                data = "01110110"
                self.RD = not self.RD
            if self.delay == 0: self.instructionname = "Unknown"
            

#***************************************************we are ready to build a new instruction*******************************************
            if self.needmorebits == False:
                

                if self.delay == 0 and self.opcode == "":

                    self.youdopc = True

                    if data == "11101101": 
                        self.fetchanddecodestage1(False,True,"xx80xx",3,data,True,False)#ED
                        self.youdopc = False
                    if data == "11001011":
                        if self.preopcode == "": self.fetchanddecodestage1(False,True,"xxBITxx",4,data,True,False)#CB
                        if self.preopcode != "": self.fetchanddecodestage1(False,True,"xxBITxx",3,data,True,False)#CB
                    if data == "11000000": #C0
                        self.youdopc = False
                        if self.checkFlag(self.F[1]) == "0": self.fetchanddecodestage1(False,True,"RET NZ",4,data,True,False)
                        else:                self.fetchanddecodestage1(False,True,"RET NZ",5,data,False,True)
                    if data == "11010000": #D0
                        self.youdopc = False
                        if self.checkFlag(self.F[7]) == "0": self.fetchanddecodestage1(False,True,"RET NC",4,data,True,False)
                        else:                self.fetchanddecodestage1(False,True,"RET NC",5,data,False,True)
                    if data == "11100000": #E0
                        self.youdopc = False
                        if self.checkFlag(self.F[5]) == "0": self.fetchanddecodestage1(False,True,"RET PO",4,data,True,False)
                        else:                self.fetchanddecodestage1(False,True,"RET PO",5,data,False,True)
                    if data == "11110000": #F0
                        self.youdopc = False
                        if self.checkFlag(self.F[0]) == "0": self.fetchanddecodestage1(False,True,"RET P",4,data,True,False)
                        else:                self.fetchanddecodestage1(False,True,"RET P",5,data,False,True)
                    if data == "11001000": #C8
                        self.youdopc = False
                        if self.checkFlag(self.F[1]) == "1": self.fetchanddecodestage1(False,True,"RET Z",4,data,True,False)
                        else:                self.fetchanddecodestage1(False,True,"RET Z",5,data,False,True)
                    if data == "11011000": #D8
                        self.youdopc = False
                        if self.checkFlag(self.F[7]) == "1": self.fetchanddecodestage1(False,True,"RET C",4,data,True,False)
                        else:                self.fetchanddecodestage1(False,True,"RET C",5,data,False,True)
                    if data == "11101000": #E8
                        self.youdopc = False
                        if self.checkFlag(self.F[5]) == "1": self.fetchanddecodestage1(False,True,"RET PE",4,data,True,False)
                        else:                self.fetchanddecodestage1(False,True,"RET PE",5,data,False,True)
                    if data == "11111000": #F8
                        self.youdopc = False
                        if self.checkFlag(self.F[0]) == "1": self.fetchanddecodestage1(False,True,"RET M",4,data,True,False)
                        else:                self.fetchanddecodestage1(False,True,"RET M",5,data,False,True)
                    if data == "01110111": 
                        self.youdopc = False
                        if self.preopcode == "": self.fetchanddecodestage1(False,True,"LD (HL),A",4,data,True,False)#77
                        if self.preopcode != "": self.fetchanddecodestage1(False,True,"LD (IXY+d),A",3,data,True,False)#77
                    if data == "01110000": 
                        self.youdopc = False
                        if self.preopcode == "": self.fetchanddecodestage1(False,True,"LD (HL),B",4,data,True,False)#70
                        if self.preopcode != "": self.fetchanddecodestage1(False,True,"LD (IXY+d),B",3,data,True,False)#70
                    if data == "01110010": 
                        self.youdopc = False
                        if self.preopcode == "": self.fetchanddecodestage1(False,True,"LD (HL),D",4,data,True,False)#72
                        if self.preopcode != "": self.fetchanddecodestage1(False,True,"LD (IXY+d),D",3,data,True,False)#72
                    if data == "01110001": 
                        self.youdopc = False
                        if self.preopcode == "": self.fetchanddecodestage1(False,True,"LD (HL),C",4,data,True,False)#71
                        if self.preopcode != "": self.fetchanddecodestage1(False,True,"LD (IXY+d),C",3,data,True,False)#71
                    if data == "01110011": 
                        self.youdopc = False
                        if self.preopcode == "": self.fetchanddecodestage1(False,True,"LD (HL),C",4,data,True,False)#73
                        if self.preopcode != "": self.fetchanddecodestage1(False,True,"LD (IXY+d),C",3,data,True,False)#73
                    if data == "01110100": 
                        self.youdopc = False
                        if self.preopcode == "": self.fetchanddecodestage1(False,True,"LD (HL),H",4,data,True,False)#74
                        if self.preopcode != "": self.fetchanddecodestage1(False,True,"LD (IXY+d),H",3,data,True,False)#74
                    if data == "01110101": 
                        self.youdopc = False
                        if self.preopcode == "": self.fetchanddecodestage1(False,True,"LD (HL),L",4,data,True,False)#75
                        if self.preopcode != "": self.fetchanddecodestage1(False,True,"LD (IXY+d),L",3,data,True,False)#75
                    
                    if data == "00000000": self.fetchanddecodestage1(True,True,"NOP",3,data,False,True)#00
                    if data == "00000001": self.fetchanddecodestage1(True,True,"LD BC,nn",4,data,True,False)#01
                    if data == "00000010": 
                        self.fetchanddecodestage1(True,False,"LD (BC),A",4,data,True,False)#02
                        self.youdopc = False
                    if data == "00000011": self.fetchanddecodestage1(True,True,"INC BC",5,data,False,True)#03
                    if data == "00000100": self.fetchanddecodestage1(True,True,"INC B",3,data,False,True)#04
                    if data == "00000101": self.fetchanddecodestage1(True,True,"DEC B",3,data,False,True)#05
                    if data == "00000110": self.fetchanddecodestage1(True,True,"LD B,n",4,data,True,False)#06
                    if data == "00000111": self.fetchanddecodestage1(True,True,"RLCA",3,data,False,True)#07 
                    if data == "00001000": self.fetchanddecodestage1(False,True,"EX AF,AF1",3,data,False,True)#08
                    if data == "00001001": self.fetchanddecodestage1(True,True,"ADD HL,BC",10,data,False,True)#09
                    if data == "00001010": 
                        self.fetchanddecodestage1(False,True,"LD A,(BC)",3,data,True,False)#0A
                        self.youdopc = False
                    if data == "00001011": self.fetchanddecodestage1(True,True,"DEC BC",5,data,False,True)#0B
                    if data == "00001100": self.fetchanddecodestage1(True,True,"INC C",3,data,False,True)#0C
                    if data == "00001101": self.fetchanddecodestage1(True,True,"DEC C",3,data,False,True)#0D
                    if data == "00001110": self.fetchanddecodestage1(True,True,"LD C,n",4,data,True,False)#0E
                    if data == "00001111": self.fetchanddecodestage1(True,True,"RRCA",3,data,False,True)#0F 
                    if data == "00010000": 
                        self.fetchanddecodestage1(False,True,"DJNZ X",4,data,True,False)#10
                        self.youdopc = False
                    if data == "00010001": self.fetchanddecodestage1(True,True,"LD DE,nn",4,data,True,False)#11
                    if data == "00010010": 
                        self.fetchanddecodestage1(True,False,"LD (DE),A",4,data,True,False)#10
                        self.youdopc = False
                    if data == "00010011": self.fetchanddecodestage1(True,True,"INC DE",5,data,False,True)#13
                    if data == "00010100": self.fetchanddecodestage1(True,True,"INC D",3,data,False,True)#14
                    if data == "00010101": self.fetchanddecodestage1(True,True,"DEC D",3,data,False,True)#15
                    if data == "00010110": self.fetchanddecodestage1(True,True,"LD D,n",4,data,True,False)#16
                    if data == "00010111": self.fetchanddecodestage1(True,True,"RLA",3,data,False,True)#17 
                    if data == "00011000": self.fetchanddecodestage1(False,True,"JR n",4,data,True,False)#18
                    if data == "00011001": self.fetchanddecodestage1(True,True,"ADD HL,DE",10,data,False,True)#19
                    if data == "00011010": 
                        self.fetchanddecodestage1(False,True,"LD A,(DE)",3,data,True,False)#1A
                        self.youdopc = False
                    if data == "00011011": self.fetchanddecodestage1(True,True,"DEC DE",5,data,False,True)#1B
                    if data == "00011100": self.fetchanddecodestage1(True,True,"INC E",3,data,False,True)#1C
                    if data == "00011101": self.fetchanddecodestage1(True,True,"DEC E",3,data,False,True)#1D
                    if data == "00011110": self.fetchanddecodestage1(True,True,"LD E,n",4,data,True,False)#1E
                    if data == "00011111": self.fetchanddecodestage1(True,True,"RRA",3,data,False,True)#1F 
                    if data == "00100000": self.fetchanddecodestage1(False,True,"JR NZ,n",4,data,True,False)#20
                    if data == "00100001": self.fetchanddecodestage1(True,True,"LD HL,nn",4,data,True,False)#21
                    if data == "00100010": 
                       self.fetchanddecodestage1(False,True,"LD (XX),HL",3,data,True,False); self.prejumppc = self.PC#22
                       self.youdopc = False
                    if data == "00100011": self.fetchanddecodestage1(True,True,"INC HL",5,data,False,True)#23
                    if data == "00100100": self.fetchanddecodestage1(True,True,"INC H",3,data,False,True)#24
                    if data == "00100101": self.fetchanddecodestage1(True,True,"DEC H",3,data,False,True)#25
                    if data == "00100110": self.fetchanddecodestage1(True,True,"LD H,n",4,data,True,False)#26
                    if data == "00100111": self.fetchanddecodestage1(False,True,"DAA",3,data,False,True)#27
                    if data == "00101000": self.fetchanddecodestage1(False,True,"JR Z,n",4,data,True,False)#28
                    if data == "00101001": self.fetchanddecodestage1(True,True,"ADD HL,HL",10,data,False,True)#29
                    if data == "00101010": 
                        self.fetchanddecodestage1(False,True,"LD HL,(XX)",3,data,True,False); self.prejumppc = self.PC#2A
                        self.youdopc = False
                    if data == "00101011": self.fetchanddecodestage1(True,True,"DEC HL",5,data,False,True)#2B
                    if data == "00101100": self.fetchanddecodestage1(True,True,"INC L",3,data,False,True)#2C
                    if data == "00101101": self.fetchanddecodestage1(True,True,"DEC L",3,data,False,True)#2D
                    if data == "00101110": self.fetchanddecodestage1(True,True,"LD L,n",4,data,True,False)#2E
                    if data == "00101111": self.fetchanddecodestage1(True,True,"CPL",3,data,False,True)#2F
                    if data == "00110000": self.fetchanddecodestage1(False,True,"JR NC,n",4,data,True,False)#30
                    if data == "00110001": self.fetchanddecodestage1(True,True,"LD SP,nn",4,data,True,False)#31
                    if data == "00110010": 
                        self.fetchanddecodestage1(False,True,"LD (XX),A",3,data,True,False); self.prejumppc = self.PC#32
                        self.youdopc = False
                    if data == "00110011": self.fetchanddecodestage1(True,True,"INC SP",5,data,False,True)#33
                    if data == "00110100": 
                        self.fetchanddecodestage1(False,True,"INC (HL)",3,data,True,False); self.prejumppc = self.PC#34
                        self.youdopc = False
                    if data == "00110101": 
                        self.fetchanddecodestage1(False,True,"DEC (HL)",3,data,True,False); self.prejumppc = self.PC#35
                        self.youdopc = False
                    if data == "00110110": 
                        self.fetchanddecodestage1(False,True,"LD (HL),X",3,data,True,False); self.prejumppc = self.PC#36
                        self.youdopc = False
                    if data == "00110111": self.fetchanddecodestage1(False,True,"SCF",3,data,False,True)#37
                    if data == "00111000": self.fetchanddecodestage1(False,True,"JR C,n",4,data,True,False)#38
                    if data == "00111001": self.fetchanddecodestage1(True,True,"ADD HL,SP",10,data,False,True)#39
                    if data == "00111010": 
                        self.fetchanddecodestage1(False,True,"LD A,(XX)",3,data,True,False); self.prejumppc = self.PC#3A
                        self.youdopc = False
                    if data == "00111011": self.fetchanddecodestage1(True,True,"DEC SP",5,data,False,True)#3B
                    if data == "00111100": self.fetchanddecodestage1(True,True,"INC A",3,data,False,True)#3C
                    if data == "00111101": self.fetchanddecodestage1(True,True,"DEC A",3,data,False,True)#3D
                    if data == "00111110": self.fetchanddecodestage1(True,True,"LD A,n",4,data,True,False)#3E
                    if data == "00111111": self.fetchanddecodestage1(True,True,"CCF",3,data,False,True)#3F
                    if data == "01000000": self.fetchanddecodestage1(True,True,"LD B,B",3,data,False,True)#40
                    if data == "01000001": self.fetchanddecodestage1(True,True,"LD B,C",3,data,False,True)#41
                    if data == "01000010": self.fetchanddecodestage1(True,True,"LD B,D",3,data,False,True)#42
                    if data == "01000011": self.fetchanddecodestage1(True,True,"LD B,E",3,data,False,True)#43
                    if data == "01000100": self.fetchanddecodestage1(True,True,"LD B,H",3,data,False,True)#44 
                    if data == "01000101": self.fetchanddecodestage1(True,True,"LD B,L",3,data,False,True)#45
                    if data == "01000110": 
                        self.fetchanddecodestage1(False,True,"LD B,(HL)",3,data,True,False)#46
                        self.youdopc = False
                    if data == "01000111": self.fetchanddecodestage1(True,True,"LD B,A",3,data,False,True)#47
                    if data == "01001000": self.fetchanddecodestage1(True,True,"LD C,B",3,data,False,True)#48
                    if data == "01001001": self.fetchanddecodestage1(True,True,"LD C,C",3,data,False,True)#49
                    if data == "01001010": self.fetchanddecodestage1(True,True,"LD C,D",3,data,False,True)#4A
                    if data == "01001011": self.fetchanddecodestage1(True,True,"LD C,E",3,data,False,True)#4B
                    if data == "01001100": self.fetchanddecodestage1(True,True,"LD C,H",3,data,False,True)#4C
                    if data == "01001101": self.fetchanddecodestage1(True,True,"LD C,L",3,data,False,True)#4D
                    if data == "01001110": 
                        self.fetchanddecodestage1(False,True,"LD C,(HL)",3,data,True,False)#4E
                        self.youdopc = False
                    if data == "01001111": self.fetchanddecodestage1(True,True,"LD C,A",3,data,False,True)#4F
                    if data == "01010000": self.fetchanddecodestage1(True,True,"LD D,B",3,data,False,True)#50
                    if data == "01010001": self.fetchanddecodestage1(True,True,"LD D,C",3,data,False,True)#51
                    if data == "01010010": self.fetchanddecodestage1(True,True,"LD D,D",3,data,False,True)#52
                    if data == "01010011": self.fetchanddecodestage1(True,True,"LD D,E",3,data,False,True)#53
                    if data == "01010100": self.fetchanddecodestage1(True,True,"LD D,H",3,data,False,True)#54 
                    if data == "01010101": self.fetchanddecodestage1(True,True,"LD D,L",3,data,False,True)#55 
                    if data == "01010110": 
                        self.fetchanddecodestage1(False,True,"LD D,(HL)",3,data,True,False)#56
                        self.youdopc = False
                    if data == "01010111": self.fetchanddecodestage1(True,True,"LD D,A",3,data,False,True)#57
                    if data == "01011000": self.fetchanddecodestage1(True,True,"LD E,B",3,data,False,True)#58
                    if data == "01011001": self.fetchanddecodestage1(True,True,"LD E,C",3,data,False,True)#59
                    if data == "01011010": self.fetchanddecodestage1(True,True,"LD E,D",3,data,False,True)#5A
                    if data == "01011011": self.fetchanddecodestage1(True,True,"LD E,E",3,data,False,True)#5B
                    if data == "01011100": self.fetchanddecodestage1(True,True,"LD E,H",3,data,False,True)#5C 
                    if data == "01011101": self.fetchanddecodestage1(True,True,"LD E,L",3,data,False,True)#5D 
                    if data == "01011110": 
                        self.fetchanddecodestage1(False,True,"LD E,(HL)",3,data,True,False)#5E
                        self.youdopc = False
                    if data == "01011111": self.fetchanddecodestage1(True,True,"LD E,A",3,data,False,True)#5F 
                    if data == "01100000": self.fetchanddecodestage1(True,True,"LD H,B",3,data,False,True)#60
                    if data == "01100001": self.fetchanddecodestage1(True,True,"LD H,C",3,data,False,True)#61
                    if data == "01100010": self.fetchanddecodestage1(True,True,"LD H,D",3,data,False,True)#62
                    if data == "01100011": self.fetchanddecodestage1(True,True,"LD H,E",3,data,False,True)#63
                    if data == "01100100": self.fetchanddecodestage1(True,True,"LD H,H",3,data,False,True)#64
                    if data == "01100101": self.fetchanddecodestage1(True,True,"LD H,L",3,data,False,True)#65
                    if data == "01100110": 
                        self.fetchanddecodestage1(False,True,"LD H,(HL)",3,data,True,False)#66
                        self.youdopc = False
                    if data == "01100111": self.fetchanddecodestage1(True,True,"LD H,A",3,data,False,True)#67
                    if data == "01101000": self.fetchanddecodestage1(True,True,"LD L,B",3,data,False,True)#68
                    if data == "01101001": self.fetchanddecodestage1(True,True,"LD L,C",3,data,False,True)#69
                    if data == "01101010": self.fetchanddecodestage1(True,True,"LD L,D",3,data,False,True)#6A
                    if data == "01101011": self.fetchanddecodestage1(True,True,"LD L,E",3,data,False,True)#6B
                    if data == "01101100": self.fetchanddecodestage1(True,True,"LD L,H",3,data,False,True)#6C
                    if data == "01101101": self.fetchanddecodestage1(True,True,"LD L,L",3,data,False,True)#6D
                    if data == "01101110": 
                        self.fetchanddecodestage1(False,True,"LD L,(HL)",3,data,True,False)#6E
                        self.youdopc = False
                    if data == "01101111": self.fetchanddecodestage1(True,True,"LD L,A",3,data,False,True)#6F
                    if data == "01110110": 
                        self.fetchanddecodestage1(False,True,"HALT",4,data,False,True)#76
                        self.youdopc = False
                    if data == "01111000": self.fetchanddecodestage1(True,True,"LD A,B",3,data,False,True)#78
                    if data == "01111001": self.fetchanddecodestage1(True,True,"LD A,C",3,data,False,True)#79
                    if data == "01111010": self.fetchanddecodestage1(True,True,"LD A,D",3,data,False,True)#7A
                    if data == "01111011": self.fetchanddecodestage1(True,True,"LD A,E",3,data,False,True)#7B
                    if data == "01111100": self.fetchanddecodestage1(True,True,"LD A,H",3,data,False,True)#7C
                    if data == "01111101": self.fetchanddecodestage1(True,True,"LD A,L",3,data,False,True)#7D
                    if data == "01111110": 
                        self.fetchanddecodestage1(False,True,"LD A,(HL)",3,data,True,False)#7E
                        self.youdopc = False
                    if data == "01111111": self.fetchanddecodestage1(True,True,"LD A,A",3,data,False,True)#7F
                    if data == "10000000": self.fetchanddecodestage1(True,True,"ADD B",3,data,False,True)#80 
                    if data == "10000001": self.fetchanddecodestage1(True,True,"ADD C",3,data,False,True)#81
                    if data == "10000010": self.fetchanddecodestage1(True,True,"ADD D",3,data,False,True)#82
                    if data == "10000011": self.fetchanddecodestage1(True,True,"ADD E",3,data,False,True)#83
                    if data == "10000100": self.fetchanddecodestage1(True,True,"ADD H",3,data,False,True)#84
                    if data == "10000101": self.fetchanddecodestage1(True,True,"ADD L",3,data,False,True)#85
                    if data == "10000110": 
                        self.fetchanddecodestage1(False,True,"ADD A,(HL)",3,data,True,False);
                        self.prejumppc = self.PC#86
                        self.youdopc = False
                    if data == "10000111": self.fetchanddecodestage1(True,True,"ADD A",3,data,False,True)#87
                    if data == "10001000": self.fetchanddecodestage1(True,True,"ADC B",3,data,False,True)#88
                    if data == "10001001": self.fetchanddecodestage1(True,True,"ADC C",3,data,False,True)#89
                    if data == "10001010": self.fetchanddecodestage1(True,True,"ADC D",3,data,False,True)#8A
                    if data == "10001011": self.fetchanddecodestage1(True,True,"ADC E",3,data,False,True)#8B
                    if data == "10001100": self.fetchanddecodestage1(True,True,"ADC H",3,data,False,True)#8C
                    if data == "10001101": self.fetchanddecodestage1(True,True,"ADC L",3,data,False,True)#8D
                    if data == "10001110": 
                        self.fetchanddecodestage1(False,True,"ADC A,(HL)",3,data,True,False);
                        self.prejumppc = self.PC#8E
                        self.youdopc = False
                    if data == "10001111": self.fetchanddecodestage1(True,True,"ADC A",3,data,False,True)#8F
                    if data == "10010000": self.fetchanddecodestage1(True,True,"SUB B",3,data,False,True)#90 
                    if data == "10010001": self.fetchanddecodestage1(True,True,"SUB C",3,data,False,True)#91
                    if data == "10010010": self.fetchanddecodestage1(True,True,"SUB D",3,data,False,True)#92
                    if data == "10010011": self.fetchanddecodestage1(True,True,"SUB E",3,data,False,True)#93
                    if data == "10010100": self.fetchanddecodestage1(True,True,"SUB H",3,data,False,True)#94
                    if data == "10010101": self.fetchanddecodestage1(True,True,"SUB L",3,data,False,True)#95
                    if data == "10010110": 
                        self.fetchanddecodestage1(False,True,"SUB (HL)",3,data,True,False)#96
                        self.youdopc = False
                    if data == "10010111": self.fetchanddecodestage1(True,True,"SUB A",3,data,False,True)#97
                    if data == "10011000": self.fetchanddecodestage1(True,True,"SBC B",3,data,False,True)#98 
                    if data == "10011001": self.fetchanddecodestage1(True,True,"SBC C",3,data,False,True)#99
                    if data == "10011010": self.fetchanddecodestage1(True,True,"SBC D",3,data,False,True)#9A
                    if data == "10011011": self.fetchanddecodestage1(True,True,"SBC E",3,data,False,True)#9B
                    if data == "10011100": self.fetchanddecodestage1(True,True,"SBC H",3,data,False,True)#9C
                    if data == "10011101": self.fetchanddecodestage1(True,True,"SBC L",3,data,False,True)#9D
                    if data == "10011110": 
                        self.fetchanddecodestage1(False,True,"SBC A,(HL)",3,data,True,False); 
                        self.prejumppc = self.PC#9E
                        self.youdopc = False
                    if data == "10011111": self.fetchanddecodestage1(True,True,"SBC A",3,data,False,True)#9F
                    if data == "10100000": self.fetchanddecodestage1(True,True,"AND B",3,data,False,True)#A0
                    if data == "10100001": self.fetchanddecodestage1(True,True,"AND C",3,data,False,True)#A1
                    if data == "10100010": self.fetchanddecodestage1(True,True,"AND D",3,data,False,True)#A2
                    if data == "10100011": self.fetchanddecodestage1(True,True,"AND E",3,data,False,True)#A3
                    if data == "10100100": self.fetchanddecodestage1(True,True,"AND H",3,data,False,True)#A4
                    if data == "10100101": self.fetchanddecodestage1(True,True,"AND L",3,data,False,True)#A5
                    if data == "10100110": 
                        self.fetchanddecodestage1(False,True,"AND (HL)",3,data,True,False)#A6
                        self.youdopc = False
                    if data == "10100111": self.fetchanddecodestage1(True,True,"AND A",3,data,False,True)#A7
                    if data == "10101000": self.fetchanddecodestage1(True,True,"XOR B",3,data,False,True)#A8
                    if data == "10101001": self.fetchanddecodestage1(True,True,"XOR C",3,data,False,True)#A9
                    if data == "10101010": self.fetchanddecodestage1(True,True,"XOR D",3,data,False,True)#AA
                    if data == "10101011": self.fetchanddecodestage1(True,True,"XOR E",3,data,False,True)#AB
                    if data == "10101100": self.fetchanddecodestage1(True,True,"XOR H",3,data,False,True)#AC
                    if data == "10101101": self.fetchanddecodestage1(True,True,"XOR L",3,data,False,True)#AD
                    if data == "10101110": 
                        self.fetchanddecodestage1(False,True,"XOR (HL)",3,data,True,False)#AE
                        self.youdopc = False
                    if data == "10101111": self.fetchanddecodestage1(True,True,"XOR A",3,data,False,True)#AF
                    if data == "10110000": self.fetchanddecodestage1(True,True,"OR B",3,data,False,True)#B0
                    if data == "10110001": self.fetchanddecodestage1(True,True,"OR C",3,data,False,True)#B1
                    if data == "10110010": self.fetchanddecodestage1(True,True,"OR D",3,data,False,True)#B2
                    if data == "10110011": self.fetchanddecodestage1(True,True,"OR E",3,data,False,True)#B3
                    if data == "10110100": self.fetchanddecodestage1(True,True,"OR H",3,data,False,True)#B4
                    if data == "10110101": self.fetchanddecodestage1(True,True,"OR L",3,data,False,True)#B5
                    if data == "10110110": 
                        self.fetchanddecodestage1(False,True,"OR (HL)",3,data,True,False)#B6
                        self.youdopc = False
                    if data == "10110111": self.fetchanddecodestage1(True,True,"OR A",3,data,False,True)#B7
                    if data == "10111000": self.fetchanddecodestage1(True,True,"CP B",3,data,False,True)#B8
                    if data == "10111001": self.fetchanddecodestage1(True,True,"CP C",3,data,False,True)#B9
                    if data == "10111010": self.fetchanddecodestage1(True,True,"CP D",3,data,False,True)#BA
                    if data == "10111011": self.fetchanddecodestage1(True,True,"CP E",3,data,False,True)#BB
                    if data == "10111100": self.fetchanddecodestage1(True,True,"CP H",3,data,False,True)#BC
                    if data == "10111101": self.fetchanddecodestage1(True,True,"CP L",3,data,False,True)#BD
                    if data == "10111110": 
                        self.fetchanddecodestage1(False,True,"CP (HL)",3,data,True,False)#BE
                        self.youdopc = False
                    if data == "10111111": self.fetchanddecodestage1(True,True,"CP A",3,data,False,True)#BF
                    if data == "11000001": 
                        self.fetchanddecodestage1(False,True,"POP BC",3,data,True,False) #C1
                        self.youdopc = False
                    if data == "11000010": self.fetchanddecodestage1(False,True,"JP NZ,nn,n",4,data,True,False)#C2
                    if data == "11000011": self.fetchanddecodestage1(True,True,"JP nn",4,data,True,False)#C3
                    if data == "11000100": 
                        self.fetchanddecodestage1(False,True,"CALL NZ,nn",3,data,True,False)#C4
                        self.youdopc = False
                    if data == "11000101": 
                        self.fetchanddecodestage1(True,False,"PUSH BC",3,data,True,False)
                        self.youdopc = False
                    if data == "11000110": self.fetchanddecodestage1(True,True,"ADD A,n",4,data,True,False)#C6
                    if data == "11000111": 
                        self.fetchanddecodestage1(False,True,"RST 00H",3,data,True,False)#C7
                        self.youdopc = False
                    if data == "11001001": 
                        self.fetchanddecodestage1(False,True,"RET",3,data,True,False) #C9
                        self.youdopc = False
                    if data == "11001010": self.fetchanddecodestage1(False,True,"JP Z,nn,n",4,data,True,False)#CA
                    if data == "11001100": 
                        self.fetchanddecodestage1(False,True,"CALL Z,nn",3,data,True,False)#CC
                        self.youdopc = False
                    if data == "11001101": 
                        self.fetchanddecodestage1(False,True,"CALL nn",3,data,True,False)#CD
                        self.youdopc = False
                    if data == "11001110": self.fetchanddecodestage1(True,True,"ADC A,n",4,data,True,False)#CE
                    if data == "11001111": 
                        self.fetchanddecodestage1(False,True,"RST 08H",3,data,True,False)#CF
                        self.youdopc = False
                    if data == "11010001": 
                        self.fetchanddecodestage1(False,True,"POP DE",3,data,True,False) #D1
                        self.youdopc = False
                    if data == "11010010": self.fetchanddecodestage1(False,True,"JP NC,nn,n",4,data,True,False)#D2
                    if data == "11010011": 
                        self.fetchanddecodestage1(False,True,"OUT (X),A",3,data,True,False); self.prejumppc = self.PC#D3
                        self.youdopc = False
                    if data == "11010100": 
                        self.fetchanddecodestage1(False,True,"CALL NC,nn",3,data,True,False)#D4
                        self.youdopc = False
                    if data == "11010101": 
                        self.fetchanddecodestage1(True,False,"PUSH DE",3,data,True,False)
                        self.youdopc = False
                    if data == "11010110": self.fetchanddecodestage1(True,True,"SUB n",4,data,True,False)#D6
                    if data == "11010111": 
                        self.fetchanddecodestage1(False,True,"RST 10H",3,data,True,False)#D7
                        self.youdopc = False
                    if data == "11011001": self.fetchanddecodestage1(False,True,"EXX",3,data,False,True)#D9
                    if data == "11011010": self.fetchanddecodestage1(False,True,"JP C,nn,n",4,data,True,False)#DA
                    if data == "11011011": 
                        self.fetchanddecodestage1(False,True,"IN (X),A",3,data,True,False); self.prejumppc = self.PC#DB
                        self.youdopc = False
                    if data == "11011100": 
                        self.fetchanddecodestage1(False,True,"CALL C,nn",3,data,True,False)#DC
                        self.youdopc = False
                    if data == "11011101": self.fetchanddecodestage1(False,True,"xxIXxx",3,data,False,True); self.preopcode = "11011101"#DD
                    if data == "11011110": self.fetchanddecodestage1(True,True,"SBC A,n",4,data,True,False)#DE
                    if data == "11011111": 
                        self.fetchanddecodestage1(False,True,"RST 18H",3,data,True,False)#DF
                        self.youdopc = False
                    if data == "11100001": 
                        self.fetchanddecodestage1(False,True,"POP HL",3,data,True,False) #E1
                        self.youdopc = False
                    if data == "11100010": self.fetchanddecodestage1(False,True,"JP PO,nn,n",4,data,True,False)#E2
                    if data == "11100011": 
                        self.fetchanddecodestage1(False,True,"EX (SP),HL",3,data,True,False); self.prejumppc = self.PC#E3
                        self.youdopc = False
                    if data == "11100100": 
                        self.fetchanddecodestage1(False,True,"CALL PO,nn",3,data,True,False)#E4
                        self.youdopc = False
                    if data == "11100101": 
                        self.fetchanddecodestage1(True,False,"PUSH HL",3,data,True,False)
                        self.youdopc = False
                    if data == "11100110": self.fetchanddecodestage1(True,True,"AND n",4,data,True,False)#E6
                    if data == "11100111": 
                        self.fetchanddecodestage1(False,True,"RST 20H",3,data,True,False)#E7
                        self.youdopc = False
                    if data == "11101001": self.fetchanddecodestage1(False,True,"JP (HL)",4,data,False,True)#E9
                    if data == "11101010": self.fetchanddecodestage1(False,True,"JP PE,nn,n",4,data,True,False)#EA
                    if data == "11101011": self.fetchanddecodestage1(False,True,"EX DE,HL",3,data,False,True)#EB
                    if data == "11101100": 
                        self.fetchanddecodestage1(False,True,"CALL PE,nn",3,data,True,False)#EC
                        self.youdopc = False
                    if data == "11101110": self.fetchanddecodestage1(True,True,"XOR n",4,data,True,False)#EE
                    if data == "11101111": 
                        self.fetchanddecodestage1(False,True,"RST 28H",3,data,True,False)#EF
                        self.youdopc = False
                    if data == "11110001": 
                        self.fetchanddecodestage1(False,True,"POP AF",3,data,True,False) #F1
                        self.youdopc = False
                    if data == "11110010": self.fetchanddecodestage1(False,True,"JP P,nn,n",4,data,True,False)#F2
                    if data == "11110011": self.fetchanddecodestage1(False,True,"DI",3,data,False,True)#F3
                    if data == "11110100": 
                        self.fetchanddecodestage1(False,True,"CALL P,nn",3,data,True,False)#F4
                        self.youdopc = False
                    if data == "11110101": 
                        self.fetchanddecodestage1(False,True,"PUSH AF",3,data,True,False)
                        self.youdopc = False
                    if data == "11110110": self.fetchanddecodestage1(True,True,"OR n",4,data,True,False)#F6
                    if data == "11110111": 
                        self.fetchanddecodestage1(False,True,"RST 30H",3,data,True,False)#F7
                        self.youdopc = False
                    if data == "11111001": self.fetchanddecodestage1(False,True,"LD SP,HL",5,data,False,True)#F9
                    if data == "11111010": self.fetchanddecodestage1(False,True,"JP M,nn,n",4,data,True,False)#FA
                    if data == "11111011": self.fetchanddecodestage1(False,True,"EI",3,data,False,True)#FB
                    if data == "11111100": 
                        self.fetchanddecodestage1(False,True,"CALL M,nn",3,data,True,False)#FC
                        self.youdopc = False
                    if data == "11111101": self.fetchanddecodestage1(False,True,"xxIYxx",3,data,False,True); self.preopcode = "11111101"#FD
                    if data == "11111110": self.fetchanddecodestage1(True,True,"CP X",4,data,True,False)#FE
                    if data == "11111111": 
                        self.fetchanddecodestage1(False,True,"RST 38H",3,data,True,False)#FF
                        self.youdopc = False


 
#***************************************we have an opcode and are now adding operands***********************************
            else:

                if self.delay == 0:

                    if self.opcode == "11101101":#ED
                        self.instructionname = "xx80xx" 

                        #********************RET N*******************
                        if self.operand1 == "01110101" or self.operand1 == "01000101" or self.operand1 == "01010101" or self.operand1 == "01100101" or self.operand1 == "01011101" or self.operand1 == "01101101" or self.operand1 == "01001101" or self.operand1 == "01111101":
                            self.instructionname = "RET N/I"
                           
                            if self.stage == "5":
                                #pc = int(data + self.operand2,2)
                                addr = self.setPC(data + self.operand2)
                                self.PC = int(addr,2)
                                self.finalstage(1)
 
                            if self.stage == "4":
                                #self.SP = self.SP + 1
                                self.SP = self.incNoFlags(self.SP)
                                self.nextstage(2,"5")
                                self.instructionname = "RET " + self.operand2 + ":" + data

                            if self.stage == "3":
                                self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                #self.SP = self.SP + 1
                                self.SP = self.incNoFlags(self.SP)
                                #self.PC = self.SP
                                self.PC = int(self.setPC(format(self.SP,'016b')),2)
                                self.stage = "4"
                                self.instructionname = "RET " + data
 
                            if self.stage == "2":
                                #self.PC = self.SP
                                self.PC = int(self.setPC(format(self.SP,'016b')),2)
                                self.nextstage(3,"3")

                            if self.stage == "1": self.nextstage(1,"2")

                        #********************IN R (C)*******************
                        if self.operand1 == "01000000" or self.operand1 == "01001000" or self.operand1 == "01010000" or self.operand1 == "01011000" or self.operand1 == "01100000" or self.operand1 == "01101000" or self.operand1 == "01110000" or self.operand1 == "01111000":
                            self.instructionname = "IN R (C)"
 
                            if self.stage == "4":
                                self.PC = self.prejumppc + 1
                                self.finalstage(1)

                            if self.stage == "3":
                                self.delay = 3
                                if self.operand1 == "01000000": self.B = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                                if self.operand1 == "01001000": self.C = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                                if self.operand1 == "01010000": self.D = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                                if self.operand1 == "01011000": self.E = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                                if self.operand1 == "01100000": self.H = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                                if self.operand1 == "01101000": self.L = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                                if self.operand1 == "01110000": self.F = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                                if self.operand1 == "01111000": self.A = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                                self.stage = "4"
                                Z = "0"
                                if data == "00000000": Z = "1"
                                S = data[0]
                                #                F3          0      F5                                 0    C
                                self.F = S + Z + self.F[2] + "0" + self.F[4] + self.getparity(data) + "0" + self.F[7]
 
                            if self.stage == "2":
                                self.prejumppc = self.PC
                                self.PC = int(self.B + self.C,2)
                                self.nextstage(1,"3")

                            if self.stage == "1": self.nextstage(1,"2")
                                
                     #********************RLD*******************
                        if self.operand1 == "01101111":
                            self.instructionname = "RLD"

                            if self.stage == "4":
                                #self.PC = self.prejumppc + 1
                                self.PC = self.incNoFlags(self.prejumppc)

                                self.readmode()
                                self.finalstage(1)

                            if self.stage == "3":
                                self.writemode()
                                #addr = format(self.PC,'016b')
                                #addr = str(addr)
                                self.regtoaddrbus(format(self.PC,'016b'))
                                
                                self.regtodatabus(data[4] + data[5] + data[6] + data[7] + self.A[4] + self.A[5] + self.A[6] + self.A[7])
                                
                                #self.A = self.A[0] + self.A[1] + self.A[2] + self.A[3] + data[0] + data[1] + data[2] + data[3]
                                self.A = self.singleload( self.A[0] , self.A[1] , self.A[2] , self.A[3] , data[0] , data[1] , data[2] , data[3])


                                self.delay = 9
                                self.stage = "4"
                                Z = "0"
                                if self.A == "00000000": Z = "1"
                                #        S           Z   F3          0      F5         parity                    0    C
                                self.F = self.A[0] + Z + self.F[2] + "0" + self.F[4] + self.getparity(self.A) + "0" + self.F[7]

                            if self.stage == "2":
                                #self.prejumppc = self.PC
                                self.prejumppc = self.setPC(self.PC)
                                #addr = self.H + self.L
                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC(self.H + self.L),2)
                                self.nextstage(1,"3")

                            if self.stage == "1": self.nextstage(1,"2")

                     #********************RRD*******************
                        if self.operand1 == "01100111":
                            self.instructionname = "RRD"

                            if self.stage == "4":
                                #self.PC = self.prejumppc + 1
                                self.PC = self.incNoFlags(self.prejumppc)

                                self.readmode()
                                self.finalstage(1)

                            if self.stage == "3":
                                self.writemode()
                                #addr = format(self.PC,'016b')
                                #addr = str(addr)
                                self.regtoaddrbus(format(self.PC,'016b'))

                                self.regtodatabus(self.A[4] + self.A[5] + self.A[6] + self.A[7] + data[0] + data[1] + data[2] + data[3])
                                
                                #self.A = self.A[0] + self.A[1] + self.A[2] + self.A[3] + data[4] + data[5] + data[6] + data[7]
                                self.A = self.singleload(  self.A[0] , self.A[1] , self.A[2] , self.A[3] , data[4] , data[5] , data[6] , data[7]  )
                                
                                self.delay = 9
                                self.stage = "4"
                                Z = "0"
                                if self.A == "00000000": Z = "1"
                                #        S           Z   F3          0      F5         parity                    0    C
                                self.F = self.A[0] + Z + self.F[2] + "0" + self.F[4] + self.getparity(self.A) + "0" + self.F[7]

                            if self.stage == "2":
                                #self.prejumppc = self.PC
                                self.prejumppc = self.setPC(self.PC)
                                #addr = self.H + self.L
                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC(self.H + self.L),2)
                                self.nextstage(1,"3")

                            if self.stage == "1": self.nextstage(1,"2")

                        #********************LD A,R*******************
                        if self.operand1 == "01011111":
                            self.instructionname = "LD A,R"
                            if self.stage == "2":
                                temp = format(self.R + 1,'08b')
                                self.A = self.singleload(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7])
                                self.finalstage(1)
                                self.PC = self.PC + 1
                                Z = "0"
                                if self.A == "00000000": Z = "1"
                                IFF = int(self.interupts)
                                #        S           Z   F3          0      F5         parity                    0    C
                                self.F = self.A[0] + Z + self.F[2] + "0" + self.F[4] + str(IFF) + "0" + self.F[7]
 
                            if self.stage == "1": self.nextstage(2,"2")

                        #********************LD R,A*******************
                        if self.operand1 == "01001111":
                            self.instructionname = "LD R,A"
                            if self.stage == "2":
                                self.R = int(self.singleload(self.A[0],self.A[1],self.A[2],self.A[3],self.A[4],self.A[5],self.A[6],self.A[7]),2)
                                self.finalstage(1)
                                self.PC = self.PC + 1
                                #Z = "0"
                                #if self.A == "00000000": Z = "1"
                                IFF = int(self.interupts)
                                #        S           Z   F3          0      F5         parity                    0    C
                                #self.F = self.A[0] + Z + self.F[2] + "0" + self.F[4] + str(IFF) + "0" + self.F[7]
 
                            if self.stage == "1": self.nextstage(2,"2")

                        #********************LD A,I*******************
                        if self.operand1 == "01010111":
                            self.instructionname = "LD A,I"
                            if self.stage == "2":
                                self.A = self.singleload(self.I[0],self.I[1],self.I[2],self.I[3],self.I[4],self.I[5],self.I[6],self.I[7])
                                self.finalstage(1)
                                self.PC = self.PC + 1
                                Z = "0"
                                if self.A == "00000000": Z = "1"
                                IFF = int(self.interupts)
                                #        S           Z   F3          0      F5         parity                    0    C
                                self.F = self.A[0] + Z + self.F[2] + "0" + self.F[4] + str(IFF) + "0" + self.F[7]
 
                            if self.stage == "1": self.nextstage(2,"2")

                        #********************LD I,A*******************
                        if self.operand1 == "01000111":
                            self.instructionname = "LD I,A"
                            if self.stage == "2":
                                self.I = self.singleload(self.A[0],self.A[1],self.A[2],self.A[3],self.A[4],self.A[5],self.A[6],self.A[7]) 
                                self.finalstage(1)
                                self.PC = self.PC + 1
                                # Z = "0"
                                # if self.A == "00000000": Z = "1"
                                IFF = int(self.interupts)
                                #        S           Z   F3          0      F5         parity                    0    C
                                #self.F = self.A[0] + Z + self.F[2] + "0" + self.F[4] + str(IFF) + "0" + self.F[7]
 
                            if self.stage == "1": self.nextstage(2,"2")

                        #********************IMM 0,1,2*******************
                        if self.operand1 == "01000110" or self.operand1 == "01010110" or self.operand1 == "01011110":
                            #not relevent for this emulation so do nothing
                            self.instructionname = "IM 0,1,2"
                            if self.stage == "2":
                                self.finalstage(1)
                                self.PC = self.PC + 1
 
                            if self.stage == "1": self.nextstage(1,"2")

                        #********************ADC HL,RR*******************
                        if self.operand1 == "01000010" or self.operand1 == "01010010" or self.operand1 == "01100010" or self.operand1 == "01110010":
                            self.instructionname = "SBC HL,RR"
                            if self.stage == "2":
                                if self.operand1 == "01000010": self.hlsbc(self.B + self.C)                             
                                if self.operand1 == "01010010": self.hlsbc(self.D + self.E)
                                if self.operand1 == "01100010": self.hlsbc(self.H + self.L)
                                if self.operand1 == "01110010": self.hlsbc(format(self.SP,'016b'))
                                self.finalstage(1)
                                self.PC = self.PC + 1

                            if self.stage == "1": self.nextstage(8,"2")

                        #********************SBC HL,RR*******************
                        if self.operand1 == "01001010" or self.operand1 == "01011010" or self.operand1 == "01101010" or self.operand1 == "01111010":
                            self.instructionname = "ADC HL,RR"
                            if self.stage == "2":
                                if self.operand1 == "01001010": self.hladc(self.B + self.C)                             
                                if self.operand1 == "01011010": self.hladc(self.D + self.E)
                                if self.operand1 == "01101010": self.hladc(self.H + self.L)
                                if self.operand1 == "01111010": self.hladc(format(self.SP,'016b'))
                                self.finalstage(1)
                                self.PC = self.PC + 1

                            if self.stage == "1": self.nextstage(8,"2")

                        #********************LD RR (XX)*******************
                        if self.operand1 == "01001011" or self.operand1 == "01011011" or self.operand1 == "01101011" or self.operand1 == "01111011":
                            self.instructionname = "LD RR (XX)"
                             
                            if self.stage == "6":
                                self.finalstage(1)
                                self.PC = self.prejumppc + 2
                                if self.operand1 == "01001011": self.B = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                                if self.operand1 == "01011011": self.D = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                if self.operand1 == "01101011": self.H = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                if self.operand1 == "01111011":
                                    SP = format(self.SP,'016b')
                                    SP = str(SP)
                                    self.SP = int(self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) + SP[8:16],2)

                            if self.stage == "5":
                                self.PC = self.PC + 1
                                if self.operand1 == "01001011": self.C = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                if self.operand1 == "01011011": self.E = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                if self.operand1 == "01101011": self.L = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                if self.operand1 == "01111011": 
                                    SP = format(self.SP,'016b')
                                    SP = str(SP)
                                    self.SP = int(SP[8:16] + self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]),2)
                                self.nextstage(3,"6")

                            if self.stage == "4":
                                self.PC = int(data + self.operand2,2)
                                self.nextstage(3,"5")

                            if self.stage == "3":
                                self.operand2 = data
                                self.PC = self.PC + 1
                                self.nextstage(3,"4")

                            if self.stage == "2":
                                self.PC = self.PC + 1
                                self.prejumppc = self.PC
                                self.nextstage(3,"3")

                            if self.stage == "1": self.nextstage(1,"2")

                        #********************LD (XX) RR***********************
                        if self.operand1 == "01000011" or self.operand1 == "01010011" or self.operand1 == "01100011" or self.operand1 == "01110011":
                            self.instructionname = "LD (CC) RR"

                            if self.stage == "6":
                                self.readmode()
                                self.finalstage(1)
                                self.PC = self.prejumppc + 2

                            if self.stage == "5":
                                if self.operand1 == "01000011": self.regtodatabus(self.B)
                                if self.operand1 == "01010011": self.regtodatabus(self.D)
                                if self.operand1 == "01100011": self.regtodatabus(self.H)
                                if self.operand1 == "01110011": 
                                    SP = format(self.SP,'016b')
                                    SP = str(SP)
                                    self.regtodatabus(SP[0:8])

                                self.PC = self.PC + 1
                                addr = format(self.PC,'016b')
                                addr = str(addr)
                                self.regtoaddrbus(addr)
                                self.nextstage(2,"6")

                            if self.stage == "4":
                                self.writemode()
                                if self.operand1 == "01000011": self.regtodatabus(self.C)
                                if self.operand1 == "01010011": self.regtodatabus(self.E)
                                if self.operand1 == "01100011": self.regtodatabus(self.L)
                                if self.operand1 == "01110011":
                                    SP = format(self.SP,'016b')
                                    SP = str(SP)
                                    self.regtodatabus(SP[8:16])
                                self.PC = int(data + self.operand2,2)
                                addr = format(self.PC,'016b')
                                addr = str(addr)
                                self.regtoaddrbus(addr)
                                self.nextstage(3,"5")

                            if self.stage == "3":
                                self.operand2 = data
                                self.PC = self.PC + 1
                                self.nextstage(4,"4")

                            if self.stage == "2":
                                self.PC = self.PC + 1
                                self.prejumppc = self.PC
                                self.nextstage(3,"3")

                            if self.stage == "1": self.nextstage(1,"2")

                        #***************** OUT ******************
                        if self.operand1 == "01111001" or self.operand1 == "01101001" or self.operand1 == "01011001" or self.operand1 == "01001001" or self.operand1 == "01000001" or self.operand1 == "01010001" or self.operand1 == "01100001" or self.operand1 == "01110001":
                            self.instructionname = "xx80xx OUT"
                  
                            if self.stage == "3":
                                self.finalstage(1)
                                self.readmode()
                                self.PC = self.prejumppc + 1

                            if self.stage == "2":
                                self.PC = int(self.B + self.C,2)
                                if self.operand1 == "01111001": self.regtodatabus(self.A)
                                if self.operand1 == "01101001": self.regtodatabus(self.L)
                                if self.operand1 == "01011001": self.regtodatabus(self.E)
                                if self.operand1 == "01001001": self.regtodatabus(self.C)
                                if self.operand1 == "01000001": self.regtodatabus(self.B)
                                if self.operand1 == "01010001": self.regtodatabus(self.D)
                                if self.operand1 == "01100001": self.regtodatabus(self.H)
                                if self.operand1 == "01110001": self.regtodatabus(self.F)
                                addr = format(self.PC,'016b')
                                addr = str(addr)
                                self.regtoaddrbus(addr)
                                self.nextstage(4,"3")

                            if self.stage == "1":
                                self.operand1 = data
                                self.writemode()
                                self.prejumppc = self.PC
                                self.nextstage(1,"2")
                             
                        #******************LDD*****************
                        if self.operand1 == "10101000" or self.operand1 == "10111000":
                            self.instructionname = "LDD(R)"
 
                            if self.stage == "4":
                                self.finalstage(1)
                                self.readmode()
                                
                                #rr = int(self.H + self.L,2)
                                #rr = rr - 1
                                #if rr < 0:
                                #    rr = rr + 65536
                                #total = format(rr,'016b')
                                total = format(self.decNoFlags(int(self.H + self.L,2)),'016b')

                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #self.H = r1
                                #self.L = r2
                                self.H = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.L = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])
                                
                                #rr = int(self.D + self.E,2)
                                #rr = rr - 1
                                #if rr < 0:
                                #    rr = rr + 65536
                                #total = format(rr,'016b')
                                total = format(self.decNoFlags(int(self.D + self.E,2)),'016b')

                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #self.D = r1
                                #self.E = r2
                                self.D = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.E = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])

                                #self.PC = self.prejumppc + 1
                                self.PC = self.incNoFlags(self.prejumppc)

                                if self.B + self.C != "0000000000000000" and self.operand1 == "10111000":
                                    #self.PC = self.prejumppc - 1
                                    self.PC = self.decNoFlags(self.prejumppc)

                                BC = int(self.B + self.C,2)
                                P = "0"
                                if BC != 0: P = "1" 
                                #        NA          NA          F3          Reset F5          ?           Reset NA  
                                self.F = self.F[0] + self.F[1] + self.F[2] + "0" + self.F[4] + P + "0" + self.F[7]
 
                            if self.stage == "3":
                                self.delay = 4
                                if self.B + self.C != "0000000000000000" and self.operand1 == "10111000": self.delay = 9
                                self.writemode()
                                #self.operand2 = data
                                self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])

                                self.regtodatabus(self.operand2)


                                #addr = self.D + self.E
                                self.regtoaddrbus(self.D + self.E)
                                #addr = int(addr,2)
                                
                                #self.PC = addr
                                self.PC = int(self.setPC(self.D + self.E  ),2)
                                self.stage = "4"

                            if self.stage == "2":
                                #self.prejumppc = self.PC
                                self.prejumppc = int(self.setPC(format(self.PC,'016b')  ),2)
                                
                                #addr = self.H + self.L
                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC( self.H + self.L ),2)

                                #rr = int(self.B + self.C,2)
                                #rr = rr - 1
                                #if rr < 0:
                                #    rr = rr + 65536
                                #total = format(rr, '016b')
                                total = format(self.decNoFlags(int(self.B + self.C,2)),'016b')

                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7] 
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #self.B = r1
                                #self.C = r2
                                self.B = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.C = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])
                                self.nextstage(4,"3")

                            if self.stage == "1":
                                #self.operand1 = data
                                self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                self.nextstage(1,"2")
 
                        #******************INI*****************
                        if self.operand1 == "10100010" or self.operand1 == "10110010":
                            self.instructionname = "INI(R)"
 
                            if self.stage == "4":
                                self.finalstage(1)
                                self.readmode()
                                
                                total = format(self.incNoFlags(int(self.H + self.L,2)),'016b')

                                self.H = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.L = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])
                     

                                self.B = format(    self.eightBitDecNoFlags(int(self.B,2))      ,'08b')

                                Z = "0"
                                if self.B == "00000000": Z = "1"

                                #self.PC = self.prejumppc + 1
                                self.PC = self.incNoFlags(self.prejumppc)

                                if self.operand1 == "10110010": 
                                    self.PC = self.decNoFlags(self.prejumppc)

                                if self.B == "00000000" and self.operand1 == "10110010":
                                    self.PC = self.incNoFlags(self.prejumppc)


                                BC = int(self.B + self.C,2)
                                #documentaion says N = 1 but my real CPU says random
                                self.debugline = "data = " + self.A
                                                                #        NA          NA          F3          ?           F5          ?           set   NA  
                                if self.operand1 == "10100010": self.F = self.F[0] + Z         + self.F[2] + self.F[3] + self.F[4] + self.F[5] + "1" + self.F[7]
                                if self.operand1 == "10110010": self.F = self.F[0] + "1"       + self.F[2] + self.F[3] + self.F[4] + self.F[5] + "0" + "0"
 
                            if self.stage == "3":
                                self.delay = 2
                                if self.B != "00000001" and self.operand1 == "10110010": self.delay = 7#we havnt dec'ed B yet so checking for 00000000 is 00000001
                                #addr = self.H + self.L
                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC(self.H + self.L),2)
 
                                self.writemode()
                                self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                self.regtodatabus(self.operand2)
                                self.regtoaddrbus(self.H + self.L)
                                self.stage = "4"
                           
                            if self.stage == "2":
                                #self.prejumppc = self.PC
                                self.prejumppc = self.setPC(self.PC)

                                #addr = self.B + self.C
                                #addr = int(addr,2)
                                #self.PC = addr

                                self.PC = int(self.setPC(self.B + self.C),2)
                                self.nextstage(5,"3")

                            if self.stage == "1": self.nextstage(2,"2")

                        #******************OUTI*****************
                        if self.operand1 == "10100011" or self.operand1 == "10110011":
                            self.instructionname = "OUTI(R)"
 
                            if self.stage == "4":
                                self.finalstage(1)
                                self.readmode()
                                
                                #rr = int(self.H + self.L,2)
                                #rr = rr + 1
                                #if rr > 65535:
                                #    rr = rr - 65536
                                #total = format(rr,'016b')
                                total = format(self.incNoFlags(int(self.H + self.L,2)),'016b')

                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #self.H = r1
                                #self.L = r2
                                self.H = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.L = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])
                                
                                Z = "0"
                                if self.B == "00000000": Z = "1"

                                #self.PC = self.prejumppc + 1
                                self.PC = self.incNoFlags(self.prejumppc)

                                if self.operand1 == "10110011":
                                    #self.PC = self.prejumppc - 1
                                    self.PC = self.decNoFlags(self.prejumppc)
                                    
                                if self.B == "00000000" and self.operand1 == "10110011":
                                    #self.PC = self.prejumppc + 1
                                    self.PC = self.incNoFlags(self.prejumppc)

                                BC = int(self.B + self.C,2)
                                                                #        NA          NA          F3          ?           F5          ?           set   NA  
                                if self.operand1 == "10100011": self.F = self.F[0] + Z         + self.F[2] + self.F[3] + self.F[4] + self.F[5] + "1" + self.F[7]
                                if self.operand1 == "10110011": self.F = self.F[0] + "1"       + self.F[2] + self.F[3] + self.F[4] + self.F[5] + "0" + "0"
 
                            if self.stage == "3":
                                #r = int(self.B,2)
                                #r = r - 1
                                #if r < 0:
                                #    r = r + 256
                                #self.B = format(r,'08b')
                                self.B = format(    self.eightBitDecNoFlags(int(self.B,2))      ,'08b')

                                self.delay = 4
                                if self.B != "00000000" and self.operand1 == "10110011": self.delay = 9#we havnt dec'ed B yet so checking for 00000000 is 00000001

                                #addr = self.B + self.C
                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC(self.B + self.C),2)

                                self.writemode()
                                self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                self.regtodatabus(self.operand2)
                                self.regtoaddrbus(self.B + self.C)
                                self.stage = "4"
 
                            if self.stage == "2":
                                #self.prejumppc = self.PC
                                self.prejumppc = self.setPC(self.PC)
                                #addr = self.H + self.L
                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC(self.H + self.L),2)
                                self.nextstage(3,"3")

                            if self.stage == "1": self.nextstage(2,"2")

                        #******************OUTD*****************
                        if self.operand1 == "10101011" or self.operand1 == "10111011":
                            self.instructionname = "OUTD(R)"
 
                            if self.stage == "4":
                                self.finalstage(1)
                                self.readmode()
                                
                                #r = int(self.H + self.L,2)
                                #r = rr - 1
                                #f rr < 0:
                                #   rr = rr + 65536
                                #otal = format(rr,'016b')
                                total = format(self.decNoFlags(int(self.H + self.L,2)),'016b')

                                #1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
                                #2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #elf.H = r1
                                #elf.L = r2
                                self.H = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.L = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])
                                
                                Z = "0"
                                if self.B == "00000000": Z = "1"

                                #elf.PC = self.prejumppc + 1
                                self.PC = self.incNoFlags(self.prejumppc)

                                if self.operand1 == "10111011":
                                    #self.PC = self.prejumppc - 1
                                    self.PC = self.decNoFlags(self.prejumppc)

                                if self.B == "00000000" and self.operand1 == "10111011":
                                    #self.PC = self.prejumppc + 1
                                    self.PC = self.incNoFlags(self.prejumppc)

                                BC = int(self.B + self.C,2)
                                                                #        NA          NA          F3          ?           F5          ?           set   NA  
                                if self.operand1 == "10101011": self.F = self.F[0] + Z         + self.F[2] + self.F[3] + self.F[4] + self.F[5] + "1" + self.F[7]
                                if self.operand1 == "10111011": self.F = self.F[0] + "1"       + self.F[2] + self.F[3] + self.F[4] + self.F[5] + "0" + "0"
 
                            if self.stage == "3":
                                #r = int(self.B,2)
                                #r = r - 1
                                #if r < 0:
                                #    r = r + 256
                                #self.B = format(r,'08b')
                                self.B = format(    self.eightBitDecNoFlags(int(self.B,2))      ,'08b')

                                self.delay = 4

                                if self.B != "00000000" and self.operand1 == "10111011": self.delay = 9#we havnt dec'ed B yet so checking for 00000000 is 00000001

                                #addr = self.B + self.C
                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC(self.B + self.C),2)

                                self.writemode()
                                self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                self.regtodatabus(self.operand2)
                                self.regtoaddrbus(self.B + self.C)
                                self.stage = "4"
                           
                            if self.stage == "2":
                                #self.prejumppc = self.PC
                                self.prejumppc = self.setPC(self.PC)
                                #addr = self.H + self.L
                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC(self.H + self.L),2)
                                self.nextstage(3,"3")

                            if self.stage == "1": self.nextstage(2,"2")

                        #******************IND*****************
                        if self.operand1 == "10101010" or self.operand1 == "10111010":
                            self.instructionname = "IND(R)"
 
                            if self.stage == "4":
                                self.instructionname = "IND (R) stage 4"
                                self.finalstage(1)
                                self.readmode()
                                
                                #rr = int(self.H + self.L,2)
                                #rr = rr - 1
                                #if rr > 65535:
                                #    rr = rr - 65536
                                #total = format(rr,'016b')
                                total = format(self.decNoFlags(int(self.H + self.L,2)),'016b')

                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #self.H = r1
                                #self.L = r2
                                self.H = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.L = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])
                                
                                #r = int(self.B,2)
                                #r = r - 1
                                #if r < 0:
                                #    r = r + 256
                                #self.B = format(r,'08b')
                                self.B = format(    self.eightBitDecNoFlags(int(self.B,2))      ,'08b')

                                Z = "0"
                                if self.B == "00000000": Z = "1"

                                #self.PC = self.prejumppc + 1
                                self.PC = self.incNoFlags(self.prejumppc)


                                if self.operand1 == "10111010": 
                                    #self.PC = self.prejumppc - 1
                                    self.PC = self.decNoFlags(self.prejumppc)

                                if self.B == "00000000" and self.operand1 == "10111010":
                                    #self.PC = self.prejumppc + 1
                                    self.PC = self.incNoFlags(self.prejumppc)

                                BC = int(self.B + self.C,2)
                                                                #        NA          NA          F3          ?           F5          ?           set   NA  
                                if self.operand1 == "10101010": self.F = self.F[0] + Z         + self.F[2] + self.F[3] + self.F[4] + self.F[5] + "1" + self.F[7]
                                if self.operand1 == "10111010": self.F = self.F[0] + "1"       + self.F[2] + self.F[3] + self.F[4] + self.F[5] + "1" + self.F[7] 
                                #documentation says N = 0 for INDR but my CPU sets it to 0? 

                            if self.stage == "3":
                                self.instructionname = "IND (R) stage 3 B = " + self.B + " operand1 = " + self.operand1
                               
                                self.delay = 2
                                if self.B != "00000001" and self.operand1 == "10111010": self.delay = 7#we havnt dec'ed B yet so checking for 00000000 is 00000001

                                #addr = self.H + self.L
                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC(self.H + self.L),2)

                                self.writemode()
                                self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                self.regtodatabus(self.operand2)
                                self.regtoaddrbus(self.H + self.L)
                                self.stage = "4"
                           
                            if self.stage == "2":
                                #self.prejumppc = self.PC
                                self.prejumppc = self.setPC(self.PC)

                                #addr = self.B + self.C
                                #addr = int(addr,2)
                                #self.PC = addr

                                self.PC = int(self.setPC(self.B + self.C),2)
                                self.nextstage(5,"3")

                            if self.stage == "1": self.nextstage(2,"2")

                        #******************LDI*****************
                        if self.operand1 == "10100000" or self.operand1 == "10110000":
                            self.instructionname = "LDI(R)"
 
                            if self.stage == "4":
                                self.finalstage(1)
                                self.readmode()



                                #rr = int(self.H + self.L,2)
                                #rr = rr + 1
                                #if rr > 65535:
                                #    rr = rr - 65536
                                #total = format(rr,'016b')
                                total = format(self.incNoFlags(int(self.H + self.L,2)),'016b')
                                
                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #self.H = r1
                                #self.L = r2
                                self.H = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.L = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])
                                
                                #rr = int(self.D + self.E,2)
                                #rr = rr + 1
                                #if rr > 65535:
                                #    rr = rr - 65536
                                #total = format(rr,'016b')
                                total = format(self.incNoFlags(int(self.D + self.E,2)),'016b')
 
                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #self.D = r1
                                #self.E = r2
                                self.D = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.E = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])
 
                                #self.PC = self.prejumppc + 1
                                self.PC = self.incNoFlags(self.prejumppc)

                                if self.B + self.C != "0000000000000000" and self.operand1 == "10110000":
                                    #self.PC = self.prejumppc - 1
                                    self.PC = self.decNoFlags(self.prejumppc)


                                BC = int(self.B + self.C,2)
                                P = "0"
                                if BC != 0: P = "1" 
                                #        NA          NA          F3          Reset F5          ?           Reset NA  
                                self.F = self.F[0] + self.F[1] + self.F[2] + "0" + self.F[4] + P + "0" + self.F[7]
 
                            if self.stage == "3":
                                self.delay = 4
                                if self.B + self.C != "0000000000000000" and self.operand1 == "10110000": self.delay = 9
                                self.writemode()
                                #self.operand2 = data
                                self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                
                                self.regtodatabus(self.operand2)
                                
                                
                                #addr = self.D + self.E
                                self.regtoaddrbus(self.D + self.E)

                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC(self.D + self.E  ),2)
                                self.stage = "4"

                            if self.stage == "2":
                                #self.prejumppc = self.PC
                                self.prejumppc = int(self.setPC(format(self.PC,'016b')  ),2)
                                
                                #addr = self.H + self.L
                                #addr = int(addr,2)
                                #self.PC = addr

                                self.PC = int(self.setPC( self.H + self.L ),2)



                                #rr = int(self.B + self.C,2)
                                #rr = rr - 1
                                #if rr < 0:
                                #    rr = rr + 65536
                                total = format(self.decNoFlags(int(self.B + self.C,2)),'016b')
                                #total = format(rr, '016b')

                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7] 
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #self.B = r1
                                #self.C = r2
                                self.B = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.C = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])
                                self.nextstage(4,"3")

                            if self.stage == "1":
                                #self.operand1 = data
                                self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                self.nextstage(1,"2")

                        #******************CPI*****************
                        if self.operand1 == "10100001" or self.operand1 == "10110001":
                            self.instructionname = "CPI(R)"
 
                            if self.stage == "4":
                                self.finalstage(1)
                                self.readmode()

                                Z = "0"
                                #if self.operand2 == self.A: Z = "1"
                                if self.eightBitSubNoFlagsUnsigned(int(self.operand2,2),int(self.A,2)) == 0: Z = "1"
                                
                                #rr = int(self.H + self.L,2)
                                #rr = rr + 1
                                #if rr > 65535:
                                #    rr = rr - 65536
                                #total = format(rr,'016b')
                                total = format(self.incNoFlags(int(self.H + self.L,2)),'016b')

                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #self.H = r1
                                #self.L = r2
                                self.H = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.L = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])
                                

                                #self.PC = self.prejumppc + 1
                                self.PC = self.incNoFlags(self.prejumppc)

                                if self.operand1 == "10110001":

                                    if self.B + self.C != "0000000000000000" and self.A != self.operand2:
                                        #self.PC = self.prejumppc - 1
                                        self.PC = self.decNoFlags(self.prejumppc)


                                BC = int(self.B + self.C,2)
                                P = "0"
                                if BC != 0: P = "1" 
                                
                                A = int(self.A,2)
                                N = int(self.operand2,2)
                                result = A - N
                                result = format(result,'08b')

                                #****** S *****
                                sflag = int(self.operand2,2) - 128 - int(self.A,2)
                                if sflag < -127: sflag = sflag + 256

                                S = "0"
                                if sflag <= 0: S = "1"
                                
                                H = "0"
                                X = int(self.A[4] + self.A[5] + self.A[6] + self.A[7],2)
                                Y = int(self.operand2[4] + self.operand2[5] + self.operand2[6] + self.operand2[7],2)
        
                                if (X - Y) < 0: H = "1"
 
                                #                    OK  NA                NA          ok  set   preserved 
                                self.F = S + Z + self.F[2] + H + self.F[4] + P + "1" + self.F[7]
 
                            if self.stage == "3":
                                delay = 4
                                if self.operand1 == "10110001":
                                    if self.B + self.C != "0000000000000000" and self.A != data:
                                        delay = 9 
                                    
     
                                self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                self.nextstage(delay,"4")

                            if self.stage == "2":
                                #self.prejumppc = self.PC
                                self.prejumppc = int(self.setPC(format(self.PC,'016b')  ),2)

                                #addr = self.H + self.L
                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC( self.H + self.L ),2)

                                #rr = int(self.B + self.C,2)
                                #rr = rr - 1
                                #if rr < 0:
                                #    rr = rr + 65536
                                #total = format(rr, '016b')
                                total = format(self.decNoFlags(int(self.B + self.C,2)),'016b')

                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7] 
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]
                                self.B = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.C = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])

                                #self.B = r1
                                #self.C = r2
                                self.nextstage(4,"3")

                            if self.stage == "1":
                                self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                self.nextstage(1,"2")

                        #******************CPD*****************
                        if self.operand1 == "10101001" or self.operand1 == "10111001":
                            self.instructionname = "CPD(R)"
 
                            if self.stage == "4":
                                self.finalstage(1)
                                self.readmode()

                                Z = "0"
                                #if self.operand2 == self.A: Z = "1"
                                if self.eightBitSubNoFlagsUnsigned(int(self.operand2,2),int(self.A,2)) == 0: Z = "1"
                                
                                #rr = int(self.H + self.L,2)
                                #rr = rr - 1
                                #if rr < 0:
                                #    rr = rr + 65536
                                #total = format(rr,'016b')
                                total = format(self.decNoFlags(int(self.H + self.L,2)),'016b')

                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #self.H = r1
                                #self.L = r2
                                self.H = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.L = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])
                                
                                #self.PC = self.prejumppc + 1
                                self.PC = self.incNoFlags(self.prejumppc)

                                if self.operand1 == "10111001":

                                    if self.B + self.C != "0000000000000000" and self.A != self.operand2:
                                        #self.PC = self.prejumppc - 1
                                        self.PC = self.decNoFlags(self.prejumppc)


                                BC = int(self.B + self.C,2)
                                P = "0"
                                if BC != 0: P = "1" 
                                
                                A = int(self.A,2)
                                N = int(self.operand2,2)
                                result = A - N
                                result = format(result,'08b')


                                sflag = int(self.operand2,2) - 128 - int(self.A,2)
                                if sflag < -127: sflag = sflag + 256
                                #****** S *****

                                S = "0"
                                if sflag <= 0: S = "1"

                                #***** H *****
                                H = "0"
                                X = int(self.A[4] + self.A[5] + self.A[6] + self.A[7],2)
                                Y = int(self.operand2[4] + self.operand2[5] + self.operand2[6] + self.operand2[7],2)
        
                                if (X - Y) < 0: H = "1"
 
                                #                    OK  NA                NA          ok  set   preserved 
                                self.F = S + Z + self.F[2] + H + self.F[4] + P + "1" + self.F[7]
 
                            if self.stage == "3":
                                delay = 4
                                if self.operand1 == "10111001":
                                    if self.B + self.C != "0000000000000000" and self.A != data:
                                        delay = 9 
     
                                self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                self.nextstage(delay,"4")
                           
                            if self.stage == "2":
                                #self.prejumppc = self.PC
                                self.prejumppc = int(self.setPC(format(self.PC,'016b')  ),2)


                                #addr = self.H + self.L
                                #addr = int(addr,2)
                                #self.PC = addr
                                self.PC = int(self.setPC( self.H + self.L ),2)

                                #rr = int(self.B + self.C,2)
                                #rr = rr - 1
                                #if rr < 0:
                                #    rr = rr + 65536
                                #total = format(rr, '016b')
                                total = format(self.decNoFlags(int(self.B + self.C,2)),'016b')


                                #r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7] 
                                #r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

                                #self.B = r1
                                #self.C = r2
                                self.B = self.singleload(total[0],total[1],total[2],total[3],total[4],total[5],total[6],total[7])
                                self.C = self.singleload(total[8],total[9],total[10],total[11],total[12],total[13],total[14],total[15])


                                self.nextstage(4,"3")

                            if self.stage == "1":
                                self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                                self.nextstage(1,"2")

                        #************ NEG ***************
                        if self.operand1 == "01111100" or self.operand1 == "01101100" or self.operand1 == "01011100" or self.operand1 == "01001100" or self.operand1 == "01000100" or self.operand1 == "01010100" or self.operand1 == "01100100" or self.operand1 == "01110100":#NEG
                            self.instructionname = "xx80xx NEG"                         

                            if self.stage == "2":
                                self.PC = self.PC + 1
                                self.finalstage(1)
                        
                            if self.stage == "1":
                                self.operand1 = data
                                A = int(self.A,2)
                                B = 0
                                #sub = B - A
                                sub = self.neg(A)

                                if sub < 0: sub = sub + 256
                                sub = format(sub,'08b')
                                
                                #set flags
                                H = "0"
                                X = int(self.A[4] + self.A[5] + self.A[6] + self.A[7],2)
                                Y = 0
                                Z = Y - X
                                if Z < 0: H = "1"
        
                                P = "0"
                                if self.A == "10000000": P = "1"

                                C = "0"
                                if self.A != "00000000": C = "1"

                                self.F = sub[0] + self.getZflag(sub) + sub[2] + H + sub[4] + P + "1" + C
                                self.A = sub
                                self.nextstage(1,"2")
                        
                        if self.stage == "1":
                            self.operand1 = data 

                        if self.stage == "":
                            self.PC = self.PC + 1      
                            self.nextstage(2,"1")

                    if self.opcode == "11001011":#CB
                        if self.preopcode != "":
                            self.instructionname = "IX/IY xxBITxx"

                            if self.stage == "5":
                                self.finalstage(1)
                                self.PC = self.prejumppc + 2
                                self.readmode()

                            if self.stage == "4":
                                temp = self.xxbitxx(data)

                                if self.opx > 7 and self.opy == 15: self.A = temp
                                if self.opx > 7 and self.opy == 7: self.A = temp
                                if self.opx > 7 and self.opy == 10: self.D = temp
                                if self.opx > 7 and self.opy == 11: self.E = temp
                                if self.opx > 7 and self.opy == 2: self.D = temp
                                if self.opx > 7 and self.opy == 3: self.E = temp
                                if self.opx > 7 and self.opy == 0: self.B = temp
                                if self.opx > 7 and self.opy == 8: self.B = temp
                                if self.opx > 7 and self.opy == 1: self.C = temp
                                if self.opx > 7 and self.opy == 9: self.C = temp
                                if self.opx > 7 and self.opy == 12: self.H = temp
                                if self.opx > 7 and self.opy == 13: self.L = temp
                                if self.opx > 7 and self.opy == 5: self.L = temp
                                if self.opx > 7 and self.opy == 4: self.H = temp

                                if self.opx < 4 and self.opy == 0: self.B = temp
                                if self.opx < 4 and self.opy == 1: self.C = temp
                                if self.opx < 4 and self.opy == 2: self.D = temp
                                if self.opx < 4 and self.opy == 3: self.E = temp
                                if self.opx < 4 and self.opy == 4: self.H = temp
                                if self.opx < 4 and self.opy == 5: self.L = temp
                                if self.opx < 4 and self.opy == 7: self.A = temp
                                if self.opx < 4 and self.opy == 8: self.B = temp
                                if self.opx < 4 and self.opy == 9: self.C = temp
                                if self.opx < 4 and self.opy == 10: self.D = temp
                                if self.opx < 4 and self.opy == 11: self.E = temp
                                if self.opx < 4 and self.opy == 12: self.H = temp
                                if self.opx < 4 and self.opy == 13: self.L = temp
                                if self.opx < 4 and self.opy == 15: self.A = temp
                                self.writemode()
                                self.regtodatabus(temp)
                                addr = format(self.PC,'016b')
                                addr = str(addr)
                                self.regtoaddrbus(addr)
                                self.nextstage(4,"5")
                                if self.opx > 3 and self.opx < 8: self.delay = 1                             

            
                            if self.stage == "3":
                                addr = 0
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)
                                
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.nextstage(3,"4")
            
                            if self.stage == "2":
                                self.operand2 = data
                                self.opy = int(data[4] + data[5] + data[6] + data[7],2)
                                self.opx = int(data[0] + data[1] + data[2] + data[3],2)
                                self.nextstage(3,"3")
 
                            if self.stage == "1":
                                self.operand1 = data
                                self.PC = self.PC + 1
                                self.nextstage(2,"2")

                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.prejumppc = self.PC
                                self.nextstage(3,"1")

                        if self.preopcode == "":
                            self.instructionname = "xxBITxx"
                            if self.stage == "3":
                                self.PC = self.prejumppc  + 1
                                self.readmode()
                                self.finalstage(1)
                            
                            if self.stage == "2":
                                temp = self.xxbitxx(data)
                                self.writemode()
                                self.regtodatabus(temp)
                                self.nextstage(6,"3")
                                if self.opx == 4 or self.opx == 5 or self.opx == 6 or self.opx == 7: self.delay = 3
 
                            if self.stage == "1":
                                self.needmorebits = True
                                self.execute = False
                                self.writemode()
                                self.prejumppc = self.PC
                                addr = self.H + self.L
                                addr = int(addr,2)
                                self.PC = addr
                                self.nextstage(1,"2")
 
                            if self.stage == "":
                                self.finalstage(3)
                                self.opy = int(data[4] + data[5] + data[6] + data[7],2)
                                self.opx = int(data[0] + data[1] + data[2] + data[3],2)
                                self.instructionname = "xxBITxx"
                        
                                if self.opy != 6 and self.opy != 14:
                                    self.needmorebits = False
                                    self.execute = True
                            
                                if self.opy == 6 or self.opy == 14:
                                    self.needmorebits = True
                                    self.execute = False
                                    self.stage = "1"
                                    self.delay = 3

                    if self.opcode == "11000011":# C3
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3
                            self.instructionname = "JP (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "JP (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(3)


                    if self.opcode == "01110111" or self.opcode == "01110000" or self.opcode == "01110001" or self.opcode == "01110010" or self.opcode == "01110011" or self.opcode == "01110100" or self.opcode == "01110101":
                        if self.preopcode == "": 
                            self.instructioname = "LD (HL),R"
  
                            if self.stage == "1":
                                self.stage = "2"
                                self.PC = self.prejumppc + 1
                                self.readmode()
                                self.finalstage(1)
   
                            if self.stage == "":
                                self.instructionname = "LD (HL),R"
                                self.writemode()
                                self.prejumppc = self.PC
                                if self.opcode == "01110111": self.regtodatabus(self.A)
                                if self.opcode == "01110000": self.regtodatabus(self.B)
                                if self.opcode == "01110001": self.regtodatabus(self.C)
                                if self.opcode == "01110010": self.regtodatabus(self.D)
                                if self.opcode == "01110011": self.regtodatabus(self.E)
                                if self.opcode == "01110100": self.regtodatabus(self.H)
                                if self.opcode == "01110101": self.regtodatabus(self.L)

                                addr = format(int(self.H + self.L,2),'016b')
                                self.PC = int(addr,2)
                                addr = str(addr)
                                self.regtoaddrbus(addr)
                                self.nextstage(2,"1")

                        if self.preopcode != "":
                            self.instructionname = "LD (IX+d),R"

                            if self.stage == "2":
                                self.stage = "2"
                                self.PC = self.prejumppc + 1
                                self.readmode()
                                self.finalstage(1)
                                
                            if self.stage == "1":
                                self.prejumppc = self.PC
                                self.writemode()

                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)

                                self.operand1 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                
                               
                                if self.opcode == "01110111": self.regtodatabus(self.A)
                                if self.opcode == "01110000": self.regtodatabus(self.B)
                                if self.opcode == "01110001": self.regtodatabus(self.C)
                                if self.opcode == "01110010": self.regtodatabus(self.D)
                                if self.opcode == "01110011": self.regtodatabus(self.E)
                                if self.opcode == "01110100": self.regtodatabus(self.H)
                                if self.opcode == "01110101": self.regtodatabus(self.L)

                                addr = format(self.PC,'016b')
                                addr = str(addr)
                                self.regtoaddrbus(addr)
                                self.nextstage(2,"2")

                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.nextstage(9,"1")

                    if self.opcode == "00111110": self.fetchanddecodestage2(data,2,"LD A,n (" + data + ")",False,True)#3E
                    if self.opcode == "00100110": self.fetchanddecodestage2(data,2,"LD H,n (" + data + ")",False,True)#26 
                    if self.opcode == "00101110": self.fetchanddecodestage2(data,2,"LD H,n (" + data + ")",False,True)#2E 
                    if self.opcode == "00000110": self.fetchanddecodestage2(data,2,"LD B,n (" + data + ")",False,True)#06 
                    if self.opcode == "00001110": self.fetchanddecodestage2(data,2,"LD C,n (" + data + ")",False,True)#0e 
                    if self.opcode == "00010110": self.fetchanddecodestage2(data,2,"LD D,n (" + data + ")",False,True)#16 
                    if self.opcode == "00011110": self.fetchanddecodestage2(data,2,"LD E,n (" + data + ")",False,True)#1e 
                    if self.opcode == "00011000": self.fetchanddecodestage2(data,8,"JR n (" + data + ")",False,True)#18
                    if self.opcode == "00101000": 
                        if self.checkFlag(self.F[1]) == "1":
                            self.fetchanddecodestage2(data,8,"JR Z,n (" + data + ")",False,True)#28
                        else:
                            self.fetchanddecodestage2(data,3,"JR Z,n (" + data + ")",False,True)#28
                    if self.opcode == "00111000": 
                        if self.checkFlag(self.F[7]) == "1":
                            self.fetchanddecodestage2(data,8,"JR C,n (" + data + ")",False,True)#38
                        else:
                            self.fetchanddecodestage2(data,3,"JR C,n (" + data + ")",False,True)#38
                    if self.opcode == "00100000": 
                        if self.checkFlag(self.F[1]) == "0":
                            self.fetchanddecodestage2(data,8,"JR NZ,n (" + data + ")",False,True)#20
                        else:
                            self.fetchanddecodestage2(data,3,"JR NZ,n (" + data + ")",False,True)#20
                    if self.opcode == "00110000": 
                        if self.checkFlag(self.F[7]) == "0":
                            self.fetchanddecodestage2(data,8,"JR NC,n (" + data + ")",False,True)#30
                        else:
                            self.fetchanddecodestage2(data,3,"JR NC,n (" + data + ")",False,True)#30
 
                    if self.opcode == "11001010":
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3  
                            self.instructionname = "JP Z (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "JP Z (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(3)
                    
                    if self.opcode == "11000010":
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3  
                            self.instructionname = "JP NZ (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "JP NZ (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(3)
 
                    if self.opcode == "11011010":
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3
                            self.instructionname = "JP C (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "JP C (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(3)
 
                    if self.opcode == "11010010":
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3
                            self.instructionname = "JP NC (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "JP NC (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(3)
                    
                    if self.opcode == "11111010":
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3
                            self.instructionname = "JP M (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "JP M (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(3)
 
                    if self.opcode == "11110010":
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3
                            self.instructionname = "JP P (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "JP P (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(3)
 
                    if self.opcode == "11101010":
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3
                            self.instructionname = "JP PE (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "JP PE (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(3)
 
                    if self.opcode == "11100010":
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3
                            self.instructionname = "JP PO (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "JP PO (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(3)
 
                    if self.opcode == "01111110": self.A = self.loadhlr(data,self.A)#7E
                    if self.opcode == "01000110": self.B = self.loadhlr(data,self.B)#46
                    if self.opcode == "01001110": self.C = self.loadhlr(data,self.C)#4E
                    if self.opcode == "01010110": self.D = self.loadhlr(data,self.D)#56
                    if self.opcode == "01011110": self.E = self.loadhlr(data,self.E)#5E
                    if self.opcode == "01100110": self.H = self.loadhlr(data,self.H)#66
                    if self.opcode == "01101110": self.L = self.loadhlr(data,self.L)#6E
                    if self.opcode == "00001010": self.A = self.loadsixteen(data,self.A,self.B,self.C)#0A
                    if self.opcode == "00011010": self.A = self.loadsixteen(data,self.A,self.D,self.E)#1A
                    
                    if self.opcode == "00100001": # 21
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3
                            self.instructionname = "LD HL,nn (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "LD HL,nn (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(2)
                    
                    if self.opcode == "00000001": # 01
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3
                            self.instructionname = "LD BC,nn (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "LD BC,nn (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(2)

                    if self.opcode == "00010001": # 11
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3
                            self.instructionname = "LD DE,nn (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "LD DE,nn (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(2)

                    if self.opcode == "00110001": # 31
                        if self.operand1 == "":
                            self.operand1 = data
                            self.delay = 3
                            self.instructionname = "LD SP,nn (" + self.operand1
                            self.needmorebits = True
                        else:
                            self.operand2 = data
                            self.instructionname = "LD SP,nn (" + self.operand1 + ":" + self.operand2 + ")"
                            self.finalstage(2)

                    if self.opcode == "11001101": self.callinst(",",data)#CD
                    if self.opcode == "11000100": self.callinst("NZ,",data)#C4
                    if self.opcode == "11010100": self.callinst("NC,",data)#D4
                    if self.opcode == "11100100": self.callinst("PO,",data)#E4
                    if self.opcode == "11110100": self.callinst("P,",data)#F4
                    if self.opcode == "11001100": self.callinst("Z,",data)#CC
                    if self.opcode == "11011100": self.callinst("C,",data)#DC
                    if self.opcode == "11101100": self.callinst("PE,",data)#EC
                    if self.opcode == "11111100": self.callinst("M,",data)#FC
                    if self.opcode == "11000111": self.rstinst()#C7
                    if self.opcode == "11010111": self.rstinst()#D7
                    if self.opcode == "11100111": self.rstinst()#E7
                    if self.opcode == "11110111": self.rstinst()#F7
                    if self.opcode == "11001111": self.rstinst()#CF
                    if self.opcode == "11011111": self.rstinst()#DF
                    if self.opcode == "11101111": self.rstinst()#EF
                    if self.opcode == "11111111": self.rstinst()#FF
                        
                    if self.opcode == "11001001":#C9
                        self.instructionname = "RET"

                        if self.stage == "2":
                            self.operand2 = data
                            self.finalstage(3)
                            self.SP = self.SP + 1

                        if self.stage == "1":
                            self.operand1 = data
                            self.SP = self.SP + 1
                            self.PC = self.SP
                            self.stage = "2"

                        if self.stage == "":
                            self.PC = self.SP
                            self.nextstage(3,"1")

                    if self.opcode == "11000000":#C0
                        self.instructionname = "RET NZ"

                        if self.stage == "2":
                            self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                            self.finalstage(3)
                            self.SP = self.incNoFlags(self.SP)

                        if self.stage == "1":
                            self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.stage = "2"

                        if self.stage == "":
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.nextstage(3,"1")

                    if self.opcode == "11010000":#D0
                        self.instructionname = "RET NC"

                        if self.stage == "2":
                            self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                            self.finalstage(3)
                            self.SP = self.incNoFlags(self.SP)

                        if self.stage == "1":
                            self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.stage = "2"

                        if self.stage == "":
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.nextstage(3,"1")

                    if self.opcode == "11100000":#E0
                        self.instructionname = "RET PO"

                        if self.stage == "2":
                            self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                            self.finalstage(3)
                            self.SP = self.incNoFlags(self.SP)

                        if self.stage == "1":
                            self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.stage = "2"

                        if self.stage == "":
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.nextstage(3,"1")

                    if self.opcode == "11110000":#F0
                        self.instructionname = "RET P"

                        if self.stage == "2":
                            self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                            self.finalstage(3)
                            self.SP = self.incNoFlags(self.SP)

                        if self.stage == "1":
                            self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.stage = "2"

                        if self.stage == "":
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.nextstage(3,"1")

                    if self.opcode == "11001000":#C8
                        self.instructionname = "RET Z"

                        if self.stage == "2":
                            self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                            self.finalstage(3)
                            self.SP = self.incNoFlags(self.SP)

                        if self.stage == "1":
                            self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.stage = "2"

                        if self.stage == "":
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.nextstage(3,"1")

                    if self.opcode == "11011000":#D8
                        self.instructionname = "RET C"

                        if self.stage == "2":
                            self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                            self.finalstage(3)
                            self.SP = self.incNoFlags(self.SP)

                        if self.stage == "1":
                            self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.stage = "2"

                        if self.stage == "":
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.nextstage(3,"1")

                    if self.opcode == "11101000":#E8
                        self.instructionname = "RET PE"

                        if self.stage == "2":
                            self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                            self.finalstage(3)
                            self.SP = self.incNoFlags(self.SP)

                        if self.stage == "1":
                            self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.stage = "2"

                        if self.stage == "":
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.nextstage(3,"1")

                    if self.opcode == "11111000":#F8
                        self.instructionname = "RET M"

                        if self.stage == "2":
                            self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) 
                            self.finalstage(3)
                            self.SP = self.incNoFlags(self.SP)

                        if self.stage == "1":
                            self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.stage = "2"

                        if self.stage == "":
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.nextstage(3,"1")

                    if self.opcode == "10110110":#B6
                        if self.preopcode == "":
                            if self.operand1 == "":
                                self.fetchanddecodestage2(data,2,"OR (HL)",True,False)
                                addr = self.H + self.L
                                addr = int(addr,2)
                                self.prejumppc = self.PC
                                self.PC = addr
                            else:
                                self.operand1 = data
                                self.fetchanddecodestage2(data,2,"OR (HL) " + data,False,True)
                        if self.preopcode != "":
                            self.instructionname = "OR (IXY+d)"
                            if self.stage == "2":
                                self.operand1 = data
                                self.finalstage(2)
 
                            if self.stage == "1":
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)

                                self.operand1 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.nextstage(2,"2")

                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.prejumppc = self.PC
                                self.nextstage(8,"1")

                    if self.opcode == "00110100":#34
                        if self.preopcode == "":
                            self.instructionname = "INC (HL)"
                            if self.stage == "2":
                                self.readmode()
                                self.finalstage(2)
 
                            if self.stage == "1":
                                opcode = self.opcode
                                inced = self.eightbitinc(data)
                                self.opcode = opcode
                                self.writemode()
                                self.regtodatabus(inced)
                                self.nextstage(3,"2")
                            
                            if self.stage == "":
                                addr = self.H + self.L
                                addr = int(addr,2)
                                self.PC = addr
                                self.nextstage(3,"1")

                        if self.preopcode != "":
                            self.instructionname = "INC (IXY+d)"

                            if self.stage == "3":
                                self.readmode()
                                self.finalstage(2)
 
                            if self.stage == "2":
                                opcode = self.opcode
                                temp  = self.preopcode
                                inced = self.eightbitinc(data)
                                self.preopcode = temp
                                self.opcode = opcode
                                self.writemode()
                                self.regtodatabus(inced)
                                self.nextstage(3,"3")
 
                            if self.stage == "1":
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)

                                self.operand1 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.nextstage(3,"2")

                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.prejumppc = self.prejumppc + 1
                                self.nextstage(8,"1")

                    if self.opcode == "10001110":#8E
                        if self.preopcode == "":
                            self.instructionname = "ADC A,(HL)"
                            if self.stage == "1":
                                opcode = self.opcode
                                self.A = self.eightbitadd(data)
                                self.opcode = opcode 
                                self.finalstage(2)
                            
                            if self.stage == "":
                                addr = self.H + self.L
                                addr = int(addr,2)
                                self.PC = addr
                                self.nextstage(2,"1")

                        if self.preopcode != "":
                            self.instructionname = "ADC A,(IXY+d)"
     
                            if self.stage == "2":
                                opcode = self.opcode
                                operand1 = self.operand1
                                operand2 = self.operand2
                                execute = self.execute
                                stage = self.stage
                                opx = self.opx
                                opy= self.opy
                                preopcode = self.preopcode

                                delay = self.delay
                        
                                self.A = self.eightbitadd(data)

                                self.opcode = opcode
                                self.operand1 = operand1
                                self.operand2 = operand2
                                self.execute = execute
                                self.stage = stage
                                self.opx = opx
                                self.opy = opy
                                self.preopcode = preopcode
                                self.delay = delay

                                self.finalstage(2)





                            if self.stage == "1":
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)

                                self.operand1 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.nextstage(2,"2")

                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.prejumppc = self.PC
                                self.nextstage(8,"1")

                    if self.opcode == "10000110":#86
                        if self.preopcode == "":
                            self.instructionname = "ADD A,(HL)"
                            if self.stage == "1":
                                opcode = self.opcode
                                self.A = self.eightbitadd(data)
                                self.opcode = opcode 
                                self.finalstage(2)
                            
                            if self.stage == "":
                                addr = self.H + self.L
                                addr = int(addr,2)
                                self.PC = addr
                                self.nextstage(2,"1")





                        if self.preopcode != "":
                            self.instructionname = "ADD A,(IXY+d)"
     
                            if self.stage == "2":
                                opcode = self.opcode
                                operand1 = self.operand1
                                operand2 = self.operand2
                                execute = self.execute
                                stage = self.stage
                                opx = self.opx
                                opy= self.opy
                                preopcode = self.preopcode

                                delay = self.delay
                        
                                self.A = self.eightbitadd(data)

                                self.opcode = opcode
                                self.operand1 = operand1
                                self.operand2 = operand2
                                self.execute = execute
                                self.stage = stage
                                self.opx = opx
                                self.opy = opy
                                self.preopcode = preopcode
                                self.delay = delay

                                self.finalstage(2)

                            if self.stage == "1":
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)

                                self.operand1 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.nextstage(2,"2")

                            if self.stage == "":
                                #self.PC = self.PC + 1
                                self.PC = self.incNoFlags(self.PC)

                                self.prejumppc = self.prejumppc + 1
                                self.nextstage(8,"1")





                    if self.opcode == "10011110":#9E
                        if self.preopcode == "":
                            self.instructionname = "SBC A,(HL)"
                            if self.stage == "1":
                                opcode = self.opcode
                                self.A = self.eightbitsub(data)
                                self.opcode = opcode 
                                self.finalstage(2)
                            
                            if self.stage == "":
                                addr = self.H + self.L
                                addr = int(addr,2)
                                self.PC = addr
                                self.nextstage(2,"1")

                        if self.preopcode != "":
                            self.instructionname = "SBC A,(IXY+d)"
     
                            if self.stage == "2":
                                opcode = self.opcode
                                operand1 = self.operand1
                                operand2 = self.operand2
                                execute = self.execute
                                stage = self.stage
                                opx = self.opx
                                opy= self.opy
                                preopcode = self.preopcode

                                delay = self.delay
                        
                                self.A = self.eightbitsub(data)

                                self.opcode = opcode
                                self.operand1 = operand1
                                self.operand2 = operand2
                                self.execute = execute
                                self.stage = stage
                                self.opx = opx
                                self.opy = opy
                                self.preopcode = preopcode
                                self.delay = delay

                                self.finalstage(2)


                            if self.stage == "1":
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)

                                self.operand1 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.nextstage(2,"2")

                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.prejumppc = self.PC
                                self.nextstage(8,"1")
 
                    if self.opcode == "00110101":#35
                        if self.preopcode == "":
                            self.instructionname = "DEC (HL)"
                            if self.stage == "2":
                                self.readmode()
                                self.finalstage(2)
 
                            if self.stage == "1":
                                opcode = self.opcode
                                deced = self.eightbitdec(data)
                                self.opcode = opcode 
                                self.writemode()
                                self.regtodatabus(deced)
                                self.nextstage(3,"2")
                             
                            if self.stage == "":
                                addr = self.H + self.L
                                addr = int(addr,2)
                                self.PC = addr
                                self.nextstage(3,"1")

                        if self.preopcode != "":
                            self.instructionname = "DEC (IXY+d)"
                            if self.stage == "3":
                                self.readmode()
                                self.finalstage(2)
 
                            if self.stage == "2":
                                opcode = self.opcode
                                temp  = self.preopcode
                                inced = self.eightbitdec(data)
                                self.preopcode = temp
                                self.opcode = opcode 
                                self.writemode()
                                self.regtodatabus(inced)
                                self.nextstage(3,"3")
 
                            if self.stage == "1":
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)

                                self.operand1 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.nextstage(3,"2")
 
                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.prejumppc = self.prejumppc + 1
                                self.nextstage(8,"1")

                    if self.opcode == "10101110":#AE
                        if self.preopcode == "":
                            if self.operand1 == "":
                                self.fetchanddecodestage2(data,2,"XOR (HL)",True,False)
                                addr = self.H + self.L
                                addr = int(addr,2)
                                self.prejumppc = self.PC
                                self.PC = addr
                            else:
                                self.operand1 = data
                                self.fetchanddecodestage2(data,2,"XOR (HL) " + data,False,True)
                        if self.preopcode != "":
                            self.instructionname = "XOR (IXY+d)"
                            if self.stage == "2":
                                self.operand1 = data
                                self.finalstage(2)
 
                            if self.stage == "1":
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)

                                self.operand1 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.nextstage(2,"2")

                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.prejumppc = self.PC
                                self.nextstage(8,"1")

                    if self.opcode == "10111110":#BE
                        if self.preopcode == "":
                            if self.operand1 == "":
                                self.fetchanddecodestage2(data,2,"CP (HL)",True,False)
                                addr = self.H + self.L
                                addr = int(addr,2)
                                self.prejumppc = self.PC
                                self.PC = addr
                            else:
                                self.operand1 = data
                                self.fetchanddecodestage2(data,2,"CP (HL) " + data,False,True)

                        if self.preopcode != "":
                            self.instructionname = "CP (IXY+d)"
                            if self.stage == "2":
                                self.operand1 = data
                                self.finalstage(2)
 
                            if self.stage == "1":
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)

                                self.operand1 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.nextstage(2,"2")

                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.prejumppc = self.PC
                                self.nextstage(8,"1")

                    if self.opcode == "10100110":#A6
                        if self.preopcode == "":
                            if self.operand1 == "":
                                self.fetchanddecodestage2(data,2,"AND (HL)",True,False)
                                addr = self.H + self.L
                                addr = int(addr,2)
                                self.prejumppc = self.PC
                                self.PC = addr
                            else:
                                self.operand1 = data
                                self.fetchanddecodestage2(data,2,"AND (HL) " + data,False,True)

                        if self.preopcode != "":
                            self.instructionname = "AND (IXY+d)"
                            if self.stage == "2":
                                self.operand1 = data
                                self.finalstage(2)
 
                            if self.stage == "1":
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)

                                self.operand1 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.nextstage(2,"2")

                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.prejumppc = self.PC
                                self.nextstage(8,"1")
 
                    if self.opcode == "10010110":#96
                        if self.preopcode == "":
                            if self.operand1 == "":
                                self.fetchanddecodestage2(data,2,"SUB (HL)",True,False)
                                addr = self.H + self.L
                                addr = int(addr,2)
                                self.prejumppc = self.PC
                                self.PC = addr
                            else:
                                self.operand1 = data
                                self.fetchanddecodestage2(data,2,"SUB (HL) " + data,False,True)

                        if self.preopcode != "":
                            self.instructionname = "SUB (IXY+d)"
                            if self.stage == "2":
                                self.operand1 = data
                                self.finalstage(2)
 
                            if self.stage == "1":
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)

                                self.operand1 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.nextstage(2,"2")

                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.prejumppc = self.PC
                                self.nextstage(8,"1")

                    if self.opcode == "11000110": self.fetchanddecodestage2(data,2,"ADD A,n (" + data + ")",False,True)#C6
                    if self.opcode == "11001110": self.fetchanddecodestage2(data,2,"ADC A,n (" + data + ")",False,True)#CE
                    if self.opcode == "11011110": self.fetchanddecodestage2(data,2,"SBC A,n (" + data + ")",False,True)#DE
                    if self.opcode == "11110110": self.fetchanddecodestage2(data,2,"OR n (" + data + ")",False,True)#F6
                    if self.opcode == "11100110": self.fetchanddecodestage2(data,2,"AND n (" + data + ")",False,True)#E6
                    if self.opcode == "11101110": self.fetchanddecodestage2(data,2,"XOR n (" + data + ")",False,True)#EE
                    if self.opcode == "11010110": self.fetchanddecodestage2(data,2,"SUB n (" + data + ")",False,True)#D6
                    if self.opcode == "11110101":#F5
                        self.instructionname = "PUSH AF"
                   
                        if self.stage == "3":
                            self.finalstage(1)
                            self.readmode()
                            self.PC = self.prejumppc + 1

                        if self.stage == "2":
                            #self.SP = self.SP - 1
                            #if self.SP < 0: self.SP = self.SP + 65536
                            self.SP = self.decNoFlags(self.SP)
                            self.PC = self.SP
                            self.regtodatabus(self.F)
                            addr = format(self.SP,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.nextstage(2,"3")
 
                        if self.stage == "1":
                            #self.SP = self.SP - 1
                            #if self.SP < 0: self.SP = self.SP + 65536
                            self.SP = self.decNoFlags(self.SP)
                            self.PC = self.SP
                            self.regtodatabus(self.A)
                            addr = format(self.SP,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.nextstage(3,"2")

                        if self.stage == "":
                            self.writemode()
                            self.prejumppc = self.PC
                            self.nextstage(2,"1")

                    if self.opcode == "11000101":#C5
                        self.instructionname = "PUSH BC"
                   
                        if self.stage == "3":
                            self.finalstage(1)
                            self.readmode()
                            self.PC = self.prejumppc + 1

                        if self.stage == "2":
                            #self.SP = self.SP - 1
                            #if self.SP < 0: self.SP = self.SP + 65536
                            self.SP = self.decNoFlags(self.SP)
                            self.PC = self.SP
                            self.regtodatabus(self.C)
                            addr = format(self.SP,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.nextstage(2,"3")
 
                        if self.stage == "1":
                            #self.SP = self.SP - 1
                            #if self.SP < 0: self.SP = self.SP + 65536
                            self.SP = self.decNoFlags(self.SP)
                            self.PC = self.SP
                            self.regtodatabus(self.B)
                            addr = format(self.SP,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.nextstage(3,"2")

                        if self.stage == "":
                            self.writemode()
                            self.prejumppc = self.PC
                            self.nextstage(2,"1")

                    if self.opcode == "11010101":#D5
                        self.instructionname = "PUSH DE"
                   
                        if self.stage == "3":
                            self.finalstage(1)
                            self.readmode()
                            self.PC = self.prejumppc + 1

                        if self.stage == "2":
                            #self.SP = self.SP - 1
                            #if self.SP < 0: self.SP = self.SP + 65536
                            self.SP = self.decNoFlags(self.SP)
                            self.PC = self.SP
                            self.regtodatabus(self.E)
                            addr = format(self.SP,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.nextstage(2,"3")
 
                        if self.stage == "1":
                            #self.SP = self.SP - 1
                            #if self.SP < 0: self.SP = self.SP + 65536
                            self.SP = self.decNoFlags(self.SP)
                            self.PC = self.SP
                            self.regtodatabus(self.D)
                            addr = format(self.SP,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.nextstage(3,"2")

                        if self.stage == "":
                            self.writemode()
                            self.prejumppc = self.PC
                            self.nextstage(2,"1")

                    if self.opcode == "11100101":#E5
                        self.instructionname = "PUSH HL"
                   
                        if self.stage == "3":
                            self.finalstage(1)
                            self.readmode()
                            self.PC = self.prejumppc + 1

                        if self.stage == "2":
                            #self.SP = self.SP - 1
                            #if self.SP < 0: self.SP = self.SP + 65536
                            self.SP = self.decNoFlags(self.SP)
                            self.PC = self.SP
                            if self.preopcode == "": self.regtodatabus(self.L)
                            if self.preopcode == "11011101": self.regtodatabus(self.IX[8] + self.IX[9] + self.IX[10] + self.IX[11] + self.IX[12] + self.IX[13] + self.IX[14] + self.IX[15])
                            if self.preopcode == "11111101": self.regtodatabus(self.IY[8] + self.IY[9] + self.IY[10] + self.IY[11] + self.IY[12] + self.IY[13] + self.IY[14] + self.IY[15])
                            addr = format(self.SP,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.nextstage(2,"3")
 
                        if self.stage == "1":
                            #self.SP = self.SP - 1
                            #if self.SP < 0: self.SP = self.SP + 65536
                            self.SP = self.decNoFlags(self.SP)
                            self.PC = self.SP
                            if self.preopcode == "":  self.regtodatabus(self.H)
                            if self.preopcode == "11011101": self.regtodatabus(self.IX[0] + self.IX[1] + self.IX[2] + self.IX[3] + self.IX[4] + self.IX[5] + self.IX[6] + self.IX[7])
                            if self.preopcode == "11111101": self.regtodatabus(self.IY[0] + self.IY[1] + self.IY[2] + self.IY[3] + self.IY[4] + self.IY[5] + self.IY[6] + self.IY[7])
                            addr = format(self.SP,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.nextstage(3,"2")

                        if self.stage == "":
                            self.writemode()
                            self.prejumppc = self.PC
                            self.nextstage(2,"1")

                    if self.opcode == "00010000":#10
                        if self.stage == "1":
                            self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            if self.B == "00000000":
                                #self.PC = self.PC + 1
                                self.PC = self.incNoFlags(self.PC)
                            else:
                                n = int(self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7]),2)
                                if self.checkFlag(self.operand1[0]) == "1":
                                    n = self.eightBitSubNoFlags(0,(255-n))
                                else:
                                    n = self.incNoFlags(n)
                                self.PC = self.sixteenBitAddNoFlags(self.PC,n)
                                
                                #if data[0] == "1": self.PC = self.PC - (127 - int(data[1] + data[2] + data[3] + data[4] + data[5] + data[6] + data[7],2))
                                #if data[0] == "0": self.PC = self.PC + 1 + int(data[1] + data[2] + data[3] + data[4] + data[5] + data[6] + data[7],2)

                            self.instructionname = "DJNZ " + self.operand1
                            self.finalstage(1)

                        if self.stage == "":
                            #self.PC = self.PC + 1      
                            self.PC = self.incNoFlags(self.PC)

                            #b = int(self.B,2)
                            #b = b - 1
                            #if b == -1: b = 255
                            #self.B = format(b, '08b')
                            self.B = format(    self.eightBitDecNoFlags(int(self.B,2)),'08b')


                            self.instructionname = "DJNZ X"
                            self.nextstage(8,"1")
                            if self.B == "00000000": self.delay = 3
 
                    if self.opcode == "11100011":#E3

                        if self.stage == "4":
                            if self.preopcode == "":
                                self.H = self.singleload(self.operand2[0],self.operand2[1],self.operand2[2],self.operand2[3],self.operand2[4],self.operand2[5],self.operand2[6],self.operand2[7])
                                self.L = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                            if self.preopcode == "11011101":
                                self.IX = self.singleload(self.operand2[0],self.operand2[1],self.operand2[2],self.operand2[3],self.operand2[4],self.operand2[5],self.operand2[6],self.operand2[7]) + self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])

                            if self.preopcode == "11111101":
                                self.IY = self.singleload(self.operand2[0],self.operand2[1],self.operand2[2],self.operand2[3],self.operand2[4],self.operand2[5],self.operand2[6],self.operand2[7]) + self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])

                           


                            self.readmode()
                            #self.PC = self.prejumppc + 1
                            self.PC = self.incNoFlags(self.prejumppc)

                            self.finalstage(1)


                        if self.stage == "3":
                            #self.PC = self.PC - 1
                            self.PC = self.decNoFlags(self.PC)

                            if self.preopcode == "": self.regtodatabus(self.L)
                            if self.preopcode == "11011101": self.regtodatabus(self.IX[8:16])
                            if self.preopcode == "11111101": self.regtodatabus(self.IY[8:16])
                            addr = format(self.PC,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.instructionname = "EX (SP),HL"
                            self.nextstage(4,"4")
                            
                        if self.stage == "2":
                            self.writemode()
                            if self.preopcode == "": self.regtodatabus(self.H)
                            if self.preopcode == "11011101": self.regtodatabus(self.IX[0:8])
                            if self.preopcode == "11111101": self.regtodatabus(self.IY[0:8])
                            addr = format(self.PC,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.instructionname = "EX (SP),HL"
                            #self.operand2 = data
                            self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.nextstage(4,"3")

                        if self.stage == "1":
                            self.instructionname = "EX (SP),HL"
                            #self.PC = self.PC + 1
                            self.PC = self.incNoFlags(self.PC)
                            self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.nextstage(4,"2")

                        if self.stage == "":
                          #  self.debugline = "HL =  " + self.H + ":" + self.L
                            self.PC = int(self.setPC(format(self.SP,'016b')),2)
                            self.instructionname = "EX (SP),HL"
                            self.nextstage(3,"1")

                    if self.opcode == "00100010":#22

                        if self.stage == "4":
                            self.readmode()
                            self.PC = self.prejumppc + 3
                            self.finalstage(1)

                        if self.stage == "3":
                            self.PC = int(self.operand2 + self.operand1,2) + 1
                            if self.preopcode == "": self.regtodatabus(self.H)
                            if self.preopcode == "11011101": self.regtodatabus(self.IX[0:8])
                            if self.preopcode == "11111101": self.regtodatabus(self.IY[0:8])
                            addr = format(self.PC,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.instructionname = "LD (" + self.operand1 + ":" + self.operand2 + "),HL"
                            self.nextstage(2,"4")
                            
                        if self.stage == "2":
                            self.operand2 = data
                            self.writemode()
                            self.PC = int(self.operand2 + self.operand1,2)
                            if self.preopcode == "": self.regtodatabus(self.L)
                            if self.preopcode == "11011101": self.regtodatabus(self.IX[8:16])
                            if self.preopcode == "11111101": self.regtodatabus(self.IY[8:16])
                            addr = format(self.PC,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.instructionname = "LD (" + self.operand1 + ":" + self.operand2 + "),HL"
                            self.nextstage(3,"3")

                        if self.stage == "1":
                            self.operand1 = data
                            self.instructionname = "LD (" + self.operand1 + ":XXXXXXXX),HL"
                            self.PC = self.PC + 1
                            self.nextstage(4,"2")

                        if self.stage == "":
                            self.PC = self.PC + 1      
                            self.instructionname = "LD (XX),HL"
                            self.nextstage(3,"1")
 
                    if self.opcode == "00110010":#32

                        if self.stage == "3":
                            self.readmode()
                            self.PC = self.prejumppc + 3
                            self.finalstage(1)

                        if self.stage == "2":
                            self.operand2 = data
                            self.writemode()
                            self.PC = int(self.operand2 + self.operand1,2)
                            self.regtodatabus(self.A)
                            addr = format(self.PC,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.instructionname = "LD (" + self.operand1 + ":" + self.operand2 + "),A"
                            self.nextstage(2,"3")

                        if self.stage == "1":
                            self.operand1 = data
                            self.instructionname = "LD (" + self.operand1 + ":XXXXXXXX),A"
                            self.PC = self.PC + 1
                            self.nextstage(4,"2")
                       
                        if self.stage == "":
                            self.PC = self.PC + 1      
                            self.instructionname = "LD (XX),A"
                            self.nextstage(3,"1")
                     
                    if self.opcode == "00110110":#36
                        if self.preopcode == "":
                            if self.stage == "3":
                                self.readmode()
                                self.PC = self.prejumppc + 2
                                self.finalstage(1)

                            if self.stage == "2":
                                self.writemode()
                                self.PC = int(self.H + self.L,2)
                                self.regtodatabus(self.operand1)
                                addr = format(self.PC,'016b')
                                addr = str(addr)
                                self.regtoaddrbus(addr)
                                self.instructionname = "LD (" + self.H + ":" + self.L + ")," + self.operand1
                                self.nextstage(2,"3")

                            if self.stage == "1":
                                self.operand1 = data
                                self.instructionname = "LD (HL)," + self.operand1
                                self.nextstage(2,"2")
                       
                            if self.stage == "":
                                self.PC = self.PC + 1      
                                self.instructionname = "LD (HL),X"
                                self.nextstage(2,"1")

                        if self.preopcode != "":
                            self.instructionname = "LD (IXY+d),X"

                            if self.stage == "4":
                                self.readmode()
                                self.PC = self.prejumppc + 2
                                self.finalstage(1)

                            if self.stage == "3":
                                self.regtodatabus(self.operand2)
                                addr = format(self.PC,'016b')
                                addr = str(addr)
                                self.regtoaddrbus(addr)
                                self.nextstage(1,"4")

                            if self.stage == "2":
                                if self.preopcode == "11011101": addr = int(self.IX,2)
                                if self.preopcode == "11111101": addr = int(self.IY,2)
                                self.operand2 = data
                                if self.operand1[0] == "1": self.PC = addr - (128 - int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2))
                                if self.operand1[0] == "0": self.PC = addr + int(self.operand1[1] + self.operand1[2] + self.operand1[3] + self.operand1[4] + self.operand1[5] + self.operand1[6] + self.operand1[7],2)
                                self.writemode()
                                self.nextstage(1,"3")

                            if self.stage == "1":
                                self.operand1 = data
                                self.PC = self.PC + 1
                                self.nextstage(6,"2")

                            if self.stage == "":
                                self.PC = self.PC + 1
                                self.prejumppc = self.PC
                                self.nextstage(3,"1")
 
                    if self.opcode == "00111010":#3A

                        if self.stage == "3":
                            self.PC = self.prejumppc + 3
                            self.finalstage(1)
                            self.A = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])

                        if self.stage == "2":
                            self.operand2 = data
                            self.PC = int(self.operand2 + self.operand1,2)
                            self.instructionname = "LD A,(" + self.operand1 + ":" + self.operand2 + ")"
                            self.nextstage(3,"3")

                        if self.stage == "1":
                            self.operand1 = data
                            self.instructionname = "LD A,(" + self.operand1 + ":XXXXXXXX)"
                            self.PC = self.PC + 1
                            self.nextstage(3,"2")
                       
                        if self.stage == "":
                            self.PC = self.PC + 1      
                            self.instructionname = "LD A,(XX)"
                            self.nextstage(3,"1")

                    if self.opcode == "00101010":#2A

                        if self.stage == "5":
                            self.finalstage(1)
                            self.PC = self.prejumppc + 3

                        if self.stage == "4":
                            self.instructionname = "LD HL,(" + self.operand1 + ":" + self.operand2 + ")"
                            if self.preopcode == "": self.H = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            if self.preopcode == "11011101": self.IX = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) + self.singleload(self.IX[8],self.IX[9],self.IX[10],self.IX[11],self.IX[12],self.IX[13],self.IX[14],self.IX[15])
                            if self.preopcode == "11111101": self.IY = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) + self.singleload(self.IY[8],self.IY[9],self.IY[10],self.IY[11],self.IY[12],self.IY[13],self.IY[14],self.IY[15])
                            self.nextstage(1,"5")
 
                        if self.stage == "3":
                            self.instructionname = "LD HL,(" + self.operand1 + ":" + self.operand2 + ")"
                            if self.preopcode == "": self.L = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            if self.preopcode == "11011101": self.IX = self.singleload(self.IX[0],self.IX[1],self.IX[2],self.IX[3],self.IX[4],self.IX[5],self.IX[6],self.IX[7]) + self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            if self.preopcode == "11111101": self.IY = self.singleload(self.IY[0],self.IY[1],self.IY[2],self.IY[3],self.IY[4],self.IY[5],self.IY[6],self.IY[7]) + self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.PC = self.PC + 1
                            self.nextstage(2,"4")

                        if self.stage == "2":
                            self.operand2 = data
                            self.PC = int(self.operand2 + self.operand1,2)
                            self.instructionname = "LD HL,(" + self.operand1 + ":" + self.operand2 + ")"
                            self.nextstage(3,"3")

                        if self.stage == "1":
                            self.operand1 = data
                            self.instructionname = "LD HL,(" + self.operand1 + ":XXXXXXXX)"
                            self.PC = self.PC + 1
                            self.nextstage(3,"2")
                       
                        if self.stage == "":
                            self.PC = self.PC + 1      
                            self.instructionname = "LD HL,(XX)"
                            self.nextstage(3,"1")

                    if self.opcode == "11010011":#D3

                        if self.stage == "2":
                            self.finalstage(0)
                            self.PC = self.prejumppc + 2
                            self.instructionname = "OUT (" + self.operand1 + "),A"
                        
                        if self.stage == "1":
                            self.operand1 = data
                            self.writemode()
                            self.PC = int(self.A + self.operand1,2)
                            self.regtodatabus(self.A)
                            addr = format(self.PC,'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.instructionname = "OUT (" + self.operand1 + "),A"
                            self.nextstage(4,"2")

                        if self.stage == "":
                            self.PC = self.PC + 1      
                            self.instructionname = "OUT (X),A"
                            self.nextstage(3,"1")
                        
                    if self.opcode == "11011011":#DB

                        if self.stage == "2":
                            self.finalstage(0)
                            self.PC = self.prejumppc + 2
                            self.instructionname = "IN (" + self.operand1 + "),A"
                            self.A = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                        
                        if self.stage == "1":
                            self.operand1 = data
                            self.PC = int(self.A + self.operand1,2)
                            self.instructionname = "IN (" + self.operand1 + "),A"
                            self.nextstage(4,"2")
                        
                        if self.stage == "":
                            self.PC = self.PC + 1      
                            self.instructionname = "IN (X),A"
                            self.nextstage(3,"1")
                                             
                    if self.opcode == "11110001":#F1
                        self.instructionname = "POP AF"
                        if self.stage == "3":
                            self.finalstage(1)
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = self.prejumppc + 1 
 
                        if self.stage == "2":
                            self.A = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])

                            self.nextstage(1,"3")

                        if self.stage == "1":
                            self.F = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = self.SP
                            self.nextstage(2,"2")

                        if self.stage == "":
                            self.prejumppc = self.PC
                            self.PC = self.SP
                            self.nextstage(3,"1")

                    if self.opcode == "11000001":#C1
                        self.instructionname = "POP BC"
                        if self.stage == "3":
                            self.finalstage(1)
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = self.prejumppc + 1 
 
                        if self.stage == "2":
                            self.B = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.nextstage(1,"3")

                        if self.stage == "1":
                            self.C = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = self.SP
                            self.nextstage(2,"2")

                        if self.stage == "":
                            self.prejumppc = self.PC
                            self.PC = self.SP
                            self.nextstage(3,"1")

                    if self.opcode == "11010001":#D1
                        self.instructionname = "POP DE"
                        if self.stage == "3":
                            self.finalstage(1)
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = self.prejumppc + 1 
 
                        if self.stage == "2":
                            self.D = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.nextstage(1,"3")

                        if self.stage == "1":
                            self.E = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = self.SP
                            self.nextstage(2,"2")

                        if self.stage == "":
                            self.prejumppc = self.PC
                            self.PC = self.SP
                            self.nextstage(3,"1")

                    if self.opcode == "11100001":#E1
                        self.instructionname = "POP HL/IX/IY"

                        if self.stage == "3":
                            self.finalstage(1)
                            #self.SP = self.SP + 1
                            #if self.SP == 65536: self.SP = 0

                            self.SP = self.incNoFlags(self.SP)
                            self.PC = self.prejumppc + 1 
 
                        if self.stage == "2":
                            if self.preopcode == "":
                                self.H = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            if self.preopcode == "11011101":
                                self.IX = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) + self.singleload(self.IX[8],self.IX[9],self.IX[10],self.IX[11],self.IX[12],self.IX[13],self.IX[14],self.IX[15]) 
                                self.preopcode = ""
                            if self.preopcode == "11111101":
                                self.IY = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]) + self.singleload(self.IY[8],self.IY[9],self.IY[10],self.IY[11],self.IY[12],self.IY[13],self.IY[14],self.IY[15]) 
                                self.preopcode = ""
                            self.nextstage(1,"3")

                        if self.stage == "1":
                            if self.preopcode == "":
                                self.L = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            if self.preopcode == "11011101":
                                self.IX = self.singleload(self.IX[0],self.IX[1],self.IX[2],self.IX[3],self.IX[4],self.IX[5],self.IX[6],self.IX[7]) + self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            if self.preopcode == "11111101":
                                self.IY = self.singleload(self.IY[0],self.IY[1],self.IY[2],self.IY[3],self.IY[4],self.IY[5],self.IY[6],self.IY[7]) + self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
                            #self.SP = self.SP + 1
                            #if self.SP == 65536: self.SP = 0
                            
                            self.SP = self.incNoFlags(self.SP)
                            self.PC = self.SP
                            self.nextstage(2,"2")

                        if self.stage == "":
                            self.prejumppc = self.PC
                            self.PC = self.SP
                            self.nextstage(3,"1")
 
                    if self.opcode == "11111110":#FE
                            self.instructionname = "CP X (" + data + ")"
                            self.operand1 = data  
                            self.finalstage(2)

                    if self.opcode == "00010010" or self.opcode == "00000010":
                        self.instructionname = "LD (RR),A"
                        if self.stage == "2":
                            self.PC = self.prejumppc + 1
                            self.execute = True
                            self.needmorebits = False
                            self.readmode()

                        if self.stage == "1":
                            self.PC = self.PC 
                            self.nextstage(1,"2")

                        if self.stage == "":
                            self.regtodatabus(self.A)
                            self.prejumppc = self.PC
                            self.writemode()
                            if self.opcode == "00010010": addr = format(int(self.D + self.E,2),'016b')
                            if self.opcode == "00000010": addr = format(int(self.B + self.C,2),'016b')
                            addr = str(addr)
                            self.regtoaddrbus(addr)
                            self.PC = int(addr,2)
                            self.nextstage(1,"1")


                                  
#*************************************cound down the clock tick where we do nothing*******************************
            if self.delay > 0:
                self.delay = self.delay - 1
             
#**********************if we have nothing to do icrement the PC and read the next instruction*********************
            if self.halt == False and self.delay == 0 and self.execute == False and self.youdopc == True:
                self.readmode()
                self.PC = self.PC + 1
                if self.PC == 65536: self.PC = 0
                if self.opcode == "11001011":
                    if self.opy == 6 and self.preopcode == "": self.PC = self.PC - 1
                    if self.opy == 14 and self.preopcode == "":  self.PC = self.PC - 1
                    if self.preopcode != "": self.PC = self.PC - 1
            
#*******************************************excute the instruction**********************************************
            if self.delay == 0 and self.execute == True:
                self.R = self.R + 1 #semi documented feature - Its suposed to count M1 states but doesnt allways count them, doubt this is accurate, descoped as are not emulating DRAM (or the refreshed it needs)

                if self.opcode == "11101101": #ED = xx80xx
                    self.clearop()
                
                if self.opcode == "11011101": #DD = xxIXxx
                    self.opcode = ""
                    self.operand1 = ""
                    self.operamd2 = ""
                    self.execute = False
                    self.stage = ""
                    self.opx = ""
                    self.opy = ""
                    self.delay = 1
                
                if self.opcode == "11111101": #FD = xxIYxx
                    self.opcode = ""
                    self.operand1 = ""
                    self.operamd2 = ""
                    self.execute = False
                    self.stage = ""
                    self.opx = ""
                    self.opy = ""
                    self.delay = 1
                
                if self.opcode == "11001011": #CB = xxBITxx
                    if self.preopcode == "":                   
                        if self.opy == 0: self.B = self.xxbitxx(self.B) 
                        if self.opy == 1: self.C = self.xxbitxx(self.C) 
                        if self.opy == 2: self.D = self.xxbitxx(self.D) 
                        if self.opy == 3: self.E = self.xxbitxx(self.E) 
                        if self.opy == 4: self.H = self.xxbitxx(self.H) 
                        if self.opy == 5: self.L = self.xxbitxx(self.L) 
                        if self.opy == 7: self.A = self.xxbitxx(self.A) 
                        if self.opy == 8: self.B = self.xxbitxx(self.B) 
                        if self.opy == 9: self.C = self.xxbitxx(self.C) 
                        if self.opy == 10: self.D = self.xxbitxx(self.D) 
                        if self.opy == 11: self.E = self.xxbitxx(self.E) 
                        if self.opy == 12: self.H = self.xxbitxx(self.H) 
                        if self.opy == 13: self.L = self.xxbitxx(self.L) 
                        if self.opy == 15: self.A = self.xxbitxx(self.A) 
                    
                        self.delay = 1
                        if self.opy == 6 or self.opy == 14: self.delay = 0
                    self.clearop()
                
                if self.opcode == "11000011": #C3 = JP nn
                    #addr = self.operand2 + self.operand1
                    addr = self.setPC(self.operand2 + self.operand1)
                    self.PC = int(addr,2)
                    self.clearop()
                    #flags preserved
                
                if self.opcode == "11101001": #E9 = JP (HL)
                    if self.preopcode == "": addr = self.H + self.L
                    if self.preopcode == "11011101": addr = self.IX
                    if self.preopcode == "11111101": addr = self.IY
                    #self.PC = int(addr,2)
                    addr = int(addr,2)

                    self.PC = int(   self.setPC( format(addr,'016b')     ),2)
                    self.clearop()
                
                if self.opcode == "11101011": #EB = EX DE,HL
                    tempD = self.singleload(self.D[0],self.D[1],self.D[2],self.D[3],self.D[4],self.D[5],self.D[6],self.D[7]) 
                    tempE = self.singleload(self.E[0],self.E[1],self.E[2],self.E[3],self.E[4],self.E[5],self.E[6],self.E[7]) 
                    self.D = self.singleload(self.H[0],self.H[1],self.H[2],self.H[3],self.H[4],self.H[5],self.H[6],self.H[7]) 
                    self.E = self.singleload(self.L[0],self.L[1],self.L[2],self.L[3],self.L[4],self.L[5],self.L[6],self.L[7]) 
                    self.H = self.singleload(tempD[0],tempD[1],tempD[2],tempD[3],tempD[4],tempD[5],tempD[6],tempD[7]) 
                    self.L = self.singleload(tempE[0],tempE[1],tempE[2],tempE[3],tempE[4],tempE[5],tempE[6],tempE[7]) 
                    self.clearop()
                    self.delay = 1
                
                if self.opcode == "00001000": #08 = EX AF,AF1
                    tempA = self.singleload(self.A[0],self.A[1],self.A[2],self.A[3],self.A[4],self.A[5],self.A[6],self.A[7])
                    tempF = self.singleload(self.F[0],self.F[1],self.F[2],self.F[3],self.F[4],self.F[5],self.F[6],self.F[7])
                    self.A = self.singleload(self.A1[0],self.A1[1],self.A1[2],self.A1[3],self.A1[4],self.A1[5],self.A1[6],self.A1[7])
                    self.F = self.singleload(self.F1[0],self.F1[1],self.F1[2],self.F1[3],self.F1[4],self.F1[5],self.F1[6],self.F1[7]) 
                    self.A1 = self.singleload(tempA[0],tempA[1],tempA[2],tempA[3],tempA[4],tempA[5],tempA[6],tempA[7])
                    self.F1 = self.singleload(tempF[0],tempF[1],tempF[2],tempF[3],tempF[4],tempF[5],tempF[6],tempF[7]) 
                    self.clearop()
                    self.delay = 1
 
                if self.opcode == "11000010": #C2 = JP NZ,n
                    nz = "0"
                    if self.F[1] == "0":
                        nz = "1"
                    else: 
                        nz = "0"
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,nz)
                    if addr != False: self.PC = int(addr,2)
                    else: self.PC = self.PC + 1
                    self.clearop()
 
                if self.opcode == "11001010": #CA = JP Z,nn
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,self.F[1])
                    if addr != False: self.PC = int(addr,2)
                    else: self.PC = self.PC + 1
                    self.clearop()
 
                if self.opcode == "11111010": #FA = JP M,nn
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,self.F[0])
                    if addr != False: self.PC = int(addr,2)
                    else: self.PC = self.PC + 1
                    self.clearop()
 
                if self.opcode == "11110010": #F2 = JP P,nn
                    p = "0"
                    if self.F[0] == "0":
                        p = "1"
                    else: 
                        p = "0"
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,p)
                    if addr != False: self.PC = int(addr,2)
                    else: self.PC = self.PC + 1
                    self.clearop()
 
                if self.opcode == "11101010": #EA = JP PE,nn
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,self.F[5])
                    if addr != False: self.PC = int(addr,2)
                    else: self.PC = self.PC + 1
                    self.clearop()
 
                if self.opcode == "11100010": #E2 = JP PO,nn
                    po = "0"
                    if self.F[5] == "0":
                        po = "1"
                    else: 
                        po = "0"
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,po)
                    if addr != False: self.PC = int(addr,2)
                    else: self.PC = self.PC + 1
                    self.clearop()
                 
                if self.opcode == "11011010": #DA = JP C,nn
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,self.F[7])

                    if addr != False: self.PC = int(addr,2)
                    else: self.PC = self.PC + 1
                    
                    self.clearop()
 
                if self.opcode == "11010010": #DA = JP NC,nn
                    nc = "0"
                    if self.F[7] == "0":
                        nc = "1"
                    else: 
                        nc = "0"
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,nc)
                    if addr != False: self.PC = int(addr,2)
                    else: self.PC = self.PC + 1
                    self.clearop()
 
                if self.opcode == "00000000": #00 NOP
                    self.clearop()
                    self.delay = 1
               
                if self.opcode == "00011000": #18 JR n
                    n = int(self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7]),2)
                    
                    if self.checkFlag(self.operand1[0]) == "1":
                        n = self.eightBitSubNoFlags(0,(255-n))
                    else:
                        n = self.incNoFlags(n)
                 
                    self.PC = self.sixteenBitAddNoFlags(self.PC,n)
                    self.clearop()

                if self.opcode == "00100000": #20 JR NZ,n
                    if self.checkFlag(self.F[1]) == "0":
                        n = int(self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7]),2)
                        if self.checkFlag(self.operand1[0]) == "1":
                            n = self.eightBitSubNoFlags(0,(255-n))
                        else:
                            n = self.incNoFlags(n)
                        self.PC = self.sixteenBitAddNoFlags(self.PC,n)
                    else:
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()

                if self.opcode == "00101000": #28 JR Z,n
                    if self.checkFlag(self.F[1]) == "1":
                        n = int(self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7]),2)
                        if self.checkFlag(self.operand1[0]) == "1":
                            n = self.eightBitSubNoFlags(0,(255-n))
                        else:
                            n = self.incNoFlags(n)
                        self.PC = self.sixteenBitAddNoFlags(self.PC,n)
 
                    else:
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()

                if self.opcode == "00111000": #38 JR C,n
                    if self.checkFlag(self.F[7]) == "1":
                        n = int(self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7]),2)
                        if self.checkFlag(self.operand1[0]) == "1":
                            n = self.eightBitSubNoFlags(0,(255-n))
                        else:
                            n = self.incNoFlags(n)
                        self.PC = self.sixteenBitAddNoFlags(self.PC,n)
                    else:
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()

                if self.opcode == "00110000": #38 JR NC,n
                    if self.checkFlag(self.F[7]) == "0":
                        n = int(self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7]),2)
                        if self.checkFlag(self.operand1[0]) == "1":
                            n = self.eightBitSubNoFlags(0,(255-n))
                        else:
                            n = self.incNoFlags(n)
                        self.PC = self.sixteenBitAddNoFlags(self.PC,n)
                    else:
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()

                if self.opcode == "00100111": #27
                    upper4 = int(self.A[0] + self.A[1] + self.A[2] + self.A[3],2)
                    lower4 = int(self.A[4] + self.A[5] + self.A[6] + self.A[7],2)
                    N = self.F[6]
                    C = self.F[7]
                    H = self.F[3]

                    A = int(self.A,2)

                    #C_out = "0"
                    C_out = str(int(self.setBoolValue(False)))

                    
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "0" and upper4 >= 10 and lower4 <= 9: A = self.eightBitSubNoFlagsNotSigned(A,160); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "1" and self.checkFlag(H) == "0" and upper4 >= 10 and lower4 <= 9: A = self.eightBitSubNoFlagsNotSigned(A,160); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "0" and upper4 >= 9 and lower4 >= 10: A = self.eightBitSubNoFlagsNotSigned(A,154); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and upper4 == 9 and lower4 >= 10: A = self.eightBitSubNoFlagsNotSigned(A,154); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and upper4 >= 10:                 A = self.eightBitSubNoFlagsNotSigned(A,154); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "1" and self.checkFlag(H) == "0" and upper4 >= 9 and lower4 >= 10: A = self.eightBitSubNoFlagsNotSigned(A,154); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "1" and self.checkFlag(H) == "1" and upper4 >= 10:                 A = self.eightBitSubNoFlagsNotSigned(A,154); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "1" and self.checkFlag(H) == "1" and upper4 == 9 and lower4 >= 10: A = self.eightBitSubNoFlagsNotSigned(A,154); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "0" and self.checkFlag(H) == "0" and upper4 >= 9 and lower4 >= 10: A = self.eightBitSubNoFlagsNotSigned(A,102); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and upper4 == 9 and lower4 >= 10: A = self.eightBitSubNoFlagsNotSigned(A,102); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and upper4 >= 10:                 A = self.eightBitSubNoFlagsNotSigned(A,102); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "1" and self.checkFlag(H) == "1" and upper4 == 6 and lower4 >= 6:  A = self.eightBitSubNoFlagsNotSigned(A,102); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "1" and self.checkFlag(H) == "1" and upper4 >= 7:                  A = self.eightBitSubNoFlagsNotSigned(A,102); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "0" and self.checkFlag(H) == "0" and upper4 >= 10 and lower4 <= 9: A = self.eightBitSubNoFlagsNotSigned(A,96); C_out = str(int(self.setBoolValue(True)))


                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "0" and self.checkFlag(H) == "0" and upper4 <= 8 and lower4 >= 10: A = self.eightBitSubNoFlagsNotSigned(A,6)
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and upper4 == 0 and lower4 >= 6:  A = self.eightBitSubNoFlagsNotSigned(A,6)
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and upper4 >= 1 and upper4 <= 8:  A = self.eightBitSubNoFlagsNotSigned(A,6)
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and upper4 == 9 and lower4 <= 9:  A = self.eightBitSubNoFlagsNotSigned(A,6)

                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "0" and upper4 == 0 and lower4 >= 6:  A = A 
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "0" and upper4 <= 8 and lower4 <= 9:  A = A 
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "0" and upper4 == 9 and lower4 <= 9:  A = A 
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "0" and self.checkFlag(H) == "0" and upper4 <= 9 and lower4 <= 9:  A = A 

                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "0" and upper4 <= 8 and lower4 >= 10: A = self.eightBitAddNoFlagsNotSigned(A,6)
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and upper4 <= 8:                  A = self.eightBitAddNoFlagsNotSigned(A,6)
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and upper4 == 9 and lower4 <= 9:  A = self.eightBitAddNoFlagsNotSigned(A,6)

                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "1" and self.checkFlag(H) == "0" and upper4 <= 9 and lower4 <= 9:  A = self.eightBitAddNoFlagsNotSigned(A,96); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "1" and self.checkFlag(H) == "0" and upper4 <= 8 and lower4 >= 10: A = self.eightBitAddNoFlagsNotSigned(A,102); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "1" and self.checkFlag(H) == "1" and upper4 <= 8:                  A = self.eightBitAddNoFlagsNotSigned(A,102); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "1" and self.checkFlag(H) == "1" and upper4 == 9 and lower4 <= 9:  A = self.eightBitAddNoFlagsNotSigned(A,102); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "1" and self.checkFlag(H) == "1" and upper4 <= 5:                  A = self.eightBitAddNoFlagsNotSigned(A,154); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "1" and self.checkFlag(H) == "1" and upper4 == 6 and lower4 <= 5:  A = self.eightBitAddNoFlagsNotSigned(A,154); C_out = str(int(self.setBoolValue(True)))
 
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and upper4 == 0 and lower4 <= 5:  A = self.eightBitAddNoFlagsNotSigned(A,250)

                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "1" and self.checkFlag(H) == "0" and upper4 <= 5 and lower4 <= 9:  A = self.eightBitAddNoFlagsNotSigned(A,160); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "1" and self.checkFlag(H) == "0" and upper4 <= 5 and lower4 >= 10: A = self.eightBitAddNoFlagsNotSigned(A,154); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "1" and self.checkFlag(H) == "0" and upper4 >= 6 and lower4 <= 9:  A = self.eightBitSubNoFlagsNotSigned(A,96); C_out = str(int(self.setBoolValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "1" and self.checkFlag(H) == "0" and upper4 >= 6 and lower4 >= 10: A = self.eightBitSubNoFlagsNotSigned(A,102); C_out = str(int(self.setBoolValue(True)))

                    if A > 255: A = A - 256
                    if A < 0: A = A + 256

                    self.A = format(A, '08b')


                    H_out = str(int(self.setBoolValue(False)))

                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "0" and lower4 >= 10: H_out = str(int(self.setBooValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "1" and self.checkFlag(H) == "0" and lower4 >= 10: H_out = str(int(self.setBooValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and lower4 >= 10: H_out = str(int(self.setBooValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "0" and self.checkFlag(H) == "1" and lower4 <= 5:  H_out = str(int(self.setBooValue(True)))
                    if self.checkFlag(N) == "0" and self.checkFlag(C) == "1" and self.checkFlag(H) == "1" and lower4 >= 10: H_out = str(int(self.setBooValue(True)))
                    if self.checkFlag(N) == "1" and self.checkFlag(C) == "1" and self.checkFlag(H) == "1" and lower4 <= 5:  H_out = str(int(self.setBooValue(True)))



                    #       (S)         (Z)                     (F5)         H      (F3)       (P)                      (N)        (C)
                    #       ok          ok                       ok                  ok         ok                       ok         ok 
                    self.F = self.A[0] + self.getZflag(self.A) + self.A[2] + H_out + self.A[4] + self.getparity(self.A)+ self.F[6] + C_out

                    self.clearop()
                    self.delay = 1

                if self.opcode == "11011001": #D9
                    self.interupts = False
                    tempB = self.singleload(self.B[0],self.B[1],self.B[2],self.B[3],self.B[4],self.B[5],self.B[6],self.B[7]) 
                    self.B = self.singleload(self.B1[0],self.B1[1],self.B1[2],self.B1[3],self.B1[4],self.B1[5],self.B1[6],self.B1[7]) 
                    self.B1 = self.singleload(tempB[0],tempB[1],tempB[2],tempB[3],tempB[4],tempB[5],tempB[6],tempB[7]) 
                    tempC = self.singleload(self.C[0],self.C[1],self.C[2],self.C[3],self.C[4],self.C[5],self.C[6],self.C[7]) 
                    self.C = self.singleload(self.C1[0],self.C1[1],self.C1[2],self.C1[3],self.C1[4],self.C1[5],self.C1[6],self.C1[7]) 
                    self.C1 = self.singleload(tempC[0],tempC[1],tempC[2],tempC[3],tempC[4],tempC[5],tempC[6],tempC[7]) 
                    tempD = self.singleload(self.D[0],self.D[1],self.D[2],self.D[3],self.D[4],self.D[5],self.D[6],self.D[7]) 
                    self.D = self.singleload(self.D1[0],self.D1[1],self.D1[2],self.D1[3],self.D1[4],self.D1[5],self.D1[6],self.D1[7]) 
                    self.D1 = self.singleload(tempD[0],tempD[1],tempD[2],tempD[3],tempD[4],tempD[5],tempD[6],tempD[7]) 
                    tempE = self.singleload(self.E[0],self.E[1],self.E[2],self.E[3],self.E[4],self.E[5],self.E[6],self.E[7]) 
                    self.E = self.singleload(self.E1[0],self.E1[1],self.E1[2],self.E1[3],self.E1[4],self.E1[5],self.E1[6],self.E1[7]) 
                    self.E1 = self.singleload(tempE[0],tempE[1],tempE[2],tempE[3],tempE[4],tempE[5],tempE[6],tempE[7]) 
                    tempH = self.singleload(self.H[0],self.H[1],self.H[2],self.H[3],self.H[4],self.H[5],self.H[6],self.H[7]) 
                    self.H = self.singleload(self.H1[0],self.H1[1],self.H1[2],self.H1[3],self.H1[4],self.H1[5],self.H1[6],self.H1[7]) 
                    self.H1 = self.singleload(tempH[0],tempH[1],tempH[2],tempH[3],tempH[4],tempH[5],tempH[6],tempH[7]) 
                    tempL = self.singleload(self.L[0],self.L[1],self.L[2],self.L[3],self.L[4],self.L[5],self.L[6],self.L[7]) 
                    self.L = self.singleload(self.L1[0],self.L1[1],self.L1[2],self.L1[3],self.L1[4],self.L1[5],self.L1[6],self.L1[7]) 
                    self.L1 = self.singleload(tempL[0],tempL[1],tempL[2],tempL[3],tempL[4],tempL[5],tempL[6],tempL[7]) 
                    self.clearop()
                    self.delay = 1

                if self.opcode == "11110011": #F3
                    self.interupts = self.setBoolValue(False)
                    self.clearop()
                    self.delay = 1
  
                if self.opcode == "11111011": #FB
                    self.interupts = self.setBoolValue(True)
                    self.clearop()
                    self.delay = 1
                
                if self.opcode == "00111110": #3E =  LD A,N
                    self.A = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    self.clearop()
                    self.delay = 1
 
                if self.opcode == "11111001": #F9 =  LD SP,HL
                    if self.preopcode == "": self.SP = int(self.singleload(self.H[0],self.H[1],self.H[2],self.H[3],self.H[4],self.H[5],self.H[6],self.H[7]) + self.singleload(self.L[0],self.L[1],self.L[2],self.L[3],self.L[4],self.L[5],self.L[6],self.L[7]),2)
                    if self.preopcode == "11011101": self.SP = int(self.singleload(self.IX[0],self.IX[1],self.IX[2],self.IX[3],self.IX[4],self.IX[5],self.IX[6],self.IX[7]) + self.singleload(self.IX[8],self.IX[9],self.IX[10],self.IX[11],self.IX[12],self.IX[13],self.IX[14],self.IX[15]),2)
                    if self.preopcode == "11111101": self.SP = int(self.singleload(self.IY[0],self.IY[1],self.IY[2],self.IY[3],self.IY[4],self.IY[5],self.IY[6],self.IY[7]) + self.singleload(self.IY[8],self.IY[9],self.IY[10],self.IY[11],self.IY[12],self.IY[13],self.IY[14],self.IY[15]),2)
                    self.clearop()
                    self.delay = 1
               
                if self.opcode == "00100110": #26 =  LD H,N
                    if self.preopcode == "": self.H = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    if self.preopcode == "11011101": self.IX = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7]) + self.singleload(self.IX[8],self.IX[9],self.IX[10],self.IX[11],self.IX[12],self.IX[13],self.IX[14],self.IX[15])
                    if self.preopcode == "11111101": self.IY = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7]) + self.singleload(self.IY[8],self.IY[9],self.IY[10],self.IY[11],self.IY[12],self.IY[13],self.IY[14],self.IY[15])
                    self.clearop()
                    self.delay = 1
                    #No flags effected

                if self.opcode == "00101110": #2E =  LD L,N
                    if self.preopcode == "": self.L = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    if self.preopcode == "11011101": self.IX = self.singleload(self.IX[0],self.IX[1],self.IX[2],self.IX[3],self.IX[4],self.IX[5],self.IX[6],self.IX[7]) + self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    if self.preopcode == "11111101": self.IY = self.singleload(self.IY[0],self.IY[1],self.IY[2],self.IY[3],self.IY[4],self.IY[5],self.IY[6],self.IY[7]) + self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    self.clearop()
                    self.delay = 1
                    #No flags effected

                if self.opcode == "00000110": #06 =  LD B,N
                    self.B = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    self.clearop()
                    self.delay = 1
                    #No flags effected

                if self.opcode == "00001110": #0e =  LD C,N
                    self.C = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    self.clearop()
                    self.delay = 1
                    #No flags effected

                if self.opcode == "00010110": #16 =  LD D,N
                    self.D = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    self.clearop()
                    self.delay = 1
                    #No flags effected

                if self.opcode == "00011110": #1e =  LD E,N
                    self.E = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    self.clearop()
                    self.delay = 1
                    #No flags effected

                if self.opcode == "00100001": # 21 = LD HL,nn
                    if self.preopcode == "":
                        self.H = self.singleload(self.operand2[0],self.operand2[1],self.operand2[2],self.operand2[3],self.operand2[4],self.operand2[5],self.operand2[6],self.operand2[7])
                        self.L = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    if self.preopcode == "11011101":
                        self.IX = self.singleload(self.operand2[0],self.operand2[1],self.operand2[2],self.operand2[3],self.operand2[4],self.operand2[5],self.operand2[6],self.operand2[7]) + self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                        self.preopcode = ""
                    if self.preopcode == "11111101":
                        self.IY = self.singleload(self.operand2[0],self.operand2[1],self.operand2[2],self.operand2[3],self.operand2[4],self.operand2[5],self.operand2[6],self.operand2[7]) + self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                        self.preopcode = ""
                    self.clearop()
                    self.delay = 1
                    # normally no flags effected
                
                if self.opcode == "00000001": # 01 = LD BC,nn
                    self.B = self.singleload(self.operand2[0],self.operand2[1],self.operand2[2],self.operand2[3],self.operand2[4],self.operand2[5],self.operand2[6],self.operand2[7])
                    self.C = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    
                    self.clearop()
                    self.delay = 1
                    # normally no flags effected

                if self.opcode == "00010001": # 11 = LD DE,nn
                    self.D = self.singleload(self.operand2[0],self.operand2[1],self.operand2[2],self.operand2[3],self.operand2[4],self.operand2[5],self.operand2[6],self.operand2[7])
                    self.E = self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7])
                    
                    self.clearop()
                    self.delay = 1
                    # normally no flags effected

                if self.opcode == "00110001": # 31 = LD SP,nn
                    nn = int(self.singleload(self.operand2[0],self.operand2[1],self.operand2[2],self.operand2[3],self.operand2[4],self.operand2[5],self.operand2[6],self.operand2[7]) + self.singleload(self.operand1[0],self.operand1[1],self.operand1[2],self.operand1[3],self.operand1[4],self.operand1[5],self.operand1[6],self.operand1[7]),2)
                    self.SP = nn
                    self.clearop()
                    self.delay = 1
                    # normally no flags effected

                if self.opcode == "01111110": self.clearop()#7E = LD A,(HL)
                if self.opcode == "01000110": self.clearop()#46 = LD B,(HL)
                if self.opcode == "01001110": self.clearop()#4E = LD C,(HL)
                if self.opcode == "01010110": self.clearop()#56 = LD D,(HL)
                if self.opcode == "01011110": self.clearop()#5E = LD E,(HL)
                if self.opcode == "01100110": self.clearop()#66 = LD H,(HL)
                if self.opcode == "01101110": self.clearop()#6E = LD L,(HL)
                if self.opcode == "00001010": self.clearop()#66 = LD A,(BC)
                if self.opcode == "00011010": self.clearop()#6E = LD A,(DE)

                if self.opcode == "10110110": #B6 = OR (HL)
                    self.A = self.eightbitor(self.operand1)
                    self.PC = self.prejumppc + 1
                    self.clearop()
                    self.delay = 0
                if self.opcode == "00110100": #34 = INC (HL)
                    self.PC = self.prejumppc + 1
                    self.clearop()
                    self.delay = 0
                if self.opcode == "10001110": #8E = ADC A,(HL)
                    self.PC = self.prejumppc + 1
                    self.clearop()
                    self.delay = 0
                if self.opcode == "10000110": #86 = ADD A,(HL)
                    self.PC = self.prejumppc + 1
                    self.clearop()
                    self.delay = 0
                if self.opcode == "10011110": #9E = SBC  A,(HL)
                    self.PC = self.prejumppc + 1
                    self.clearop()
                    self.delay = 0
                if self.opcode == "00110101": #35 = DEC (HL)
                    self.PC = self.prejumppc + 1
                    self.clearop()
                    self.delay = 0
                if self.opcode == "10101110": #AE = XOR (HL)
                    self.A = self.eightbitxor(self.operand1)
                    self.PC = self.prejumppc + 1
                    self.clearop()
                    self.delay = 0
                if self.opcode == "10111110": #BE = CP (HL)
                    self.eightbitcp(self.operand1)
                    self.PC = self.prejumppc + 1
                    self.clearop()
                    self.delay = 0
                if self.opcode == "10100110": #A6 = AND (HL)
                    self.A = self.eightbitand(self.operand1)
                    self.PC = self.prejumppc + 1
                    self.clearop()
                    self.delay = 0
                if self.opcode == "10010110": #96 = SUB (HL)
                    self.A = self.eightbitsub(self.operand1)
                    self.PC = self.prejumppc + 1
                    self.clearop()
                    self.delay = 0
                if self.opcode == "11001101": #CD = CALL nn
                    pc = int(self.setPC(self.operand2 + self.operand1),2)
                    self.PC = pc
                    self.clearop()
                    self.readmode()

                if self.opcode == "11000111": #C7 = RST 00H
                    self.PC = int(self.setPC("0000000000000000"),2)
                    self.clearop()
                    self.readmode()
                if self.opcode == "11010111": #D7 = RST 10H
                    self.PC = int(self.setPC("0000000000010000"),2)
                    self.clearop()
                    self.readmode()
                if self.opcode == "11100111": #E7 = RST 20H
                    self.PC = int(self.setPC("0000000000100000"),2)
                    self.clearop()
                    self.readmode()
                if self.opcode == "11110111": #F7 = RST 30H
                    self.PC = int(self.setPC("0000000000110000"),2)
                    self.clearop()
                    self.readmode()
                if self.opcode == "11001111": #CF = RST 08H
                    self.PC = int(self.setPC("0000000000001000"),2)
                    self.clearop()
                    self.readmode()
                if self.opcode == "11011111": #DF = RST 18H
                    self.PC = int(self.setPC("0000000000011000"),2)
                    self.clearop()
                    self.readmode()
                if self.opcode == "11101111": #EF = RST 28H
                    self.PC = int(self.setPC("0000000000101000"),2)
                    self.clearop()
                    self.readmode()
                if self.opcode == "11111111": #FF = RST 38H
                    self.PC = int(self.setPC("0000000000111000"),2)
                    self.clearop()
                    self.readmode()
                
                if self.opcode == "11000100": #C4 = CALL NZ,nn
                    nz = "0"
                    if self.F[1] == "0":
                        nz = "1"
                    else: 
                        nz = "0"
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,nz)
                    if addr != False: self.PC = int(addr,2)
                    self.clearop()
                    self.readmode()

                if self.opcode == "11010100": #D4 = CALL NC,nn
                    nc = "0"
                    if self.F[7] == "0":
                        nc = "1"
                    else: 
                        nc = "0"
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,nc)
                    if addr != False: self.PC = int(addr,2)
                    #else: self.PC = self.PC + 1   
                    
                    #if self.F[7] == "0":
                    #    pc = int(self.operand2 + self.operand1,2)
                    #    self.PC = pc
                    self.clearop()
                    self.readmode()

                if self.opcode == "11100100": #E4 = CALL PO.nn
                    PO = "0"
                    if self.F[5] == "0":
                        PO = "1"
                    else: 
                        PO = "0"
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,PO)
                    if addr != False: self.PC = int(addr,2)
                    self.clearop()
                    self.readmode()

                if self.opcode == "11110100": #F4 = P,CALL nn
                    P = "0"
                    if self.F[0] == "0":
                        P = "1"
                    else: 
                        P = "0"
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,P)
                    if addr != False: self.PC = int(addr,2)
                    self.clearop()
                    self.readmode()

                if self.opcode == "11001100": #CC = CALL Z,nn
                    #if self.F[1] == "1":
                    #    pc = int(self.operand2 + self.operand1,2)
                    #    self.PC = pc
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,self.F[1])
                    self.debugline = str(addr)
                    if addr != False: self.PC = int(addr,2)

                    self.clearop()
                    self.readmode()

                if self.opcode == "11011100": #DC = CALL C,nn
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,self.F[7])
                    self.debugline = str(addr)
                    if addr != False: self.PC = int(addr,2)
                    self.clearop()
                    self.readmode()

                if self.opcode == "11101100": #EC = CALL PE.nn
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,self.F[5])
                    self.debugline = str(addr)
                    if addr != False: self.PC = int(addr,2)
                    self.clearop()
                    self.readmode()

                if self.opcode == "11111100": #FC = M,CALL nn
                    addr = self.conditionalSetPC(self.operand2 + self.operand1,self.F[0])
                    self.debugline = str(addr)
                    if addr != False: self.PC = int(addr,2)
                    self.clearop()
                    self.readmode()

                if self.opcode == "11001001": #C9 = RET
                    self.instructionname = "RET"
                    #pc = int(self.operand2 + self.operand1,2)
                    addr = self.setPC(self.operand2 + self.operand1)
                    self.PC = int(addr,2)
                    self.clearop()
                
                if self.opcode == "11000000": #C0 RET NZ
                    if self.checkFlag(self.F[1]) == "0":
                        pc = int(self.operand2 + self.operand1,2)
                        self.PC = int(self.setPC(format(pc,'016b')),2)
                    else:
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()
                    self.readmode()
                
                if self.opcode == "11010000": #D0 RET NC
                    if self.checkFlag(self.F[7]) == "0":
                        pc = int(self.operand2 + self.operand1,2)
                        self.PC = int(self.setPC(format(pc,'016b')),2)
                    else:
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()
                    self.readmode()
                
                if self.opcode == "11100000": #E0 RET PO
                    if self.checkFlag(self.F[5]) == "0":
                        pc = int(self.operand2 + self.operand1,2)
                        self.PC = int(self.setPC(format(pc,'016b')),2)
                    else:
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()
                    self.readmode()
                
                if self.opcode == "11110000": #F0 RET P
                    if self.checkFlag(self.F[0]) == "0":
                        pc = int(self.operand2 + self.operand1,2)
                        self.PC = int(self.setPC(format(pc,'016b')),2)
                    else: 
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()
                    self.readmode()

                if self.opcode == "11001000": #C8 RET Z
                    if self.checkFlag(self.F[1]) == "1":
                        pc = int(self.operand2 + self.operand1,2)
                        self.PC = int(self.setPC(format(pc,'016b')),2)
                    else:
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()
                    self.readmode()
                
                if self.opcode == "11011000": #D8 RET C
                    if self.checkFlag(self.F[7]) == "1":
                        pc = int(self.operand2 + self.operand1,2)
                        self.PC = int(self.setPC(format(pc,'016b')),2)
                    else:
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()
                    self.readmode()
                
                if self.opcode == "11101000": #E8 RET PE
                    if self.checkFlag(self.F[5]) == "1":
                        pc = int(self.operand2 + self.operand1,2)
                        self.PC = int(self.setPC(format(pc,'016b')),2)
                    else:
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()
                    self.readmode()
                
                if self.opcode == "11111000": #F8 RET M
                    if self.checkFlag(self.F[0]) == "1":
                        pc = int(self.operand2 + self.operand1,2)
                        self.PC = int(self.setPC(format(pc,'016b')),2)
                    else: 
                        self.PC = self.incNoFlags(self.PC)
                    self.clearop()
                    self.readmode()
                
                if self.opcode == "00110110": #36 = LD (HL),X
                    self.clearop()
                    self.instructionname = "LD (HL),X"

                if self.opcode == "01110111": self.clearop()
                if self.opcode == "01110000": self.clearop()
                if self.opcode == "01110001": self.clearop()
                if self.opcode == "01110010": self.clearop()
                if self.opcode == "01110011": self.clearop()
                if self.opcode == "01110100": self.clearop()
                if self.opcode == "01110101": self.clearop()
                if self.opcode == "00000010": self.clearop() #02 = LD (BC),A
                if self.opcode == "00010010": self.clearop() #12 = LD (DE),A
 
                if self.opcode == "01110110": #76 HALT
                    if self.halt == False: self.PC = self.PC + 1
                    #self.halt = True
                    self.halt = self.setBoolValue(True)
                    self.clearop()
                    self.delay = 1
 
                if self.opcode == "00110111": #37 = SCF
                    self.clearop()
                    self.delay = 1

                    self.scf()
                    #        S           Z           F3            H    F5          P            N     C
                    #self.F = self.F[0] + self.F[1] + self.F[2] + "0" + self.F[4] + self.F[5] + "0" + "1"
 
                if self.opcode == "11110110": #F6 = OR n
                    A = int(self.A,2)
                    operand = int(self.operand1,2)
                    #ored = bin(A | operand)[2:].zfill(8)

                    ored = bin(self.singleor(A,operand))[2:].zfill(8)

                    self.A = ored
                    
                    #set flags
                    self.F = self.A[0] + self.getZflag(self.A) + self.A[2] + "0" + self.A[4] + self.getparity(self.A) + "0" + "0"
                    self.clearop()
                    self.delay =  1
                
                if self.opcode == "11101110": #EE = XOR n
                    A = int(self.A,2)
                    #operand = int(self.operand1,2)
                    #xored = bin(A ^ operand)[2:].zfill(8)
                    self.A = self.eightbitxor(self.operand1)
                    #self.A = xored
                    #set flags
                    self.F = self.A[0] + self.getZflag(self.A) + self.A[2] + "0" + self.A[4] + self.getparity(self.A) + "0" + "0" 
                    self.clearop()
                    self.delay =  1

                if self.opcode == "11100110": #E6 = AND n
                    A = int(self.A,2)
                    operand = int(self.operand1,2)
                    #anded = bin(A & operand)[2:].zfill(8)
                    
                    anded = bin(self.singleand(A,operand))[2:].zfill(8)
                    
                    self.A = str(anded)
                    self.clearop()
                    self.delay = 1
                    
                    #set flags
                    self.F = self.A[0] + self.getZflag(self.A) + self.A[2] + "1" + self.A[4] + self.getparity(self.A) + "0" + "0"

                if self.opcode == "00111100": self.A = self.eightbitinc(self.A)#3C = INC A
                if self.opcode == "00001100": self.C = self.eightbitinc(self.C)#0C = INC C
                if self.opcode == "00010100": self.D = self.eightbitinc(self.D)#14 = INC D
                if self.opcode == "00011100": self.E = self.eightbitinc(self.E)#1C = INC E
                if self.opcode == "00100100": 
                    if self.preopcode == "": self.H = self.eightbitinc(self.H)#24 = INC H
                    if self.preopcode == "11011101": self.IX = self.eightbitinc(self.IX[0:8]) + self.IX[8:16]
                    if self.preopcode == "11111101": self.IY = self.eightbitinc(self.IY[0:8]) + self.IY[8:16] 
                if self.opcode == "00101100":
                    if self.preopcode == "": self.L = self.eightbitinc(self.L)#2C = INC L
                    if self.preopcode == "11011101": self.IX = self.IX[0:8] + self.eightbitinc(self.IX[8:16]) 
                    if self.preopcode == "11111101": self.IY = self.IY[0:8] + self.eightbitinc(self.IY[8:16]) 
                if self.opcode == "00000100": self.B = self.eightbitinc(self.B)#04 = INC B
                if self.opcode == "00000011": self.sixteenbitinc(self.B,self.C)#03 = INC BC
                if self.opcode == "00010011": self.sixteenbitinc(self.D,self.E)#13 = INC DE
                if self.opcode == "00100011": self.sixteenbitinc(self.H,self.L)#23 = INC HL
                if self.opcode == "00110011": self.sixteenbitinc(self.SP,"SP")#33 = INC SP
                if self.opcode == "00111101": self.A = self.eightbitdec(self.A)#3D = DEC A
                if self.opcode == "00010101": self.D = self.eightbitdec(self.D)#15 = DEC D
                if self.opcode == "00011101": self.E = self.eightbitdec(self.E)#1D = DEC E
                if self.opcode == "00000101": self.B = self.eightbitdec(self.B)#05 = DEC B
                if self.opcode == "00100101": 
                    if self.preopcode == "":self.H = self.eightbitdec(self.H)#25 = DEC H
                    if self.preopcode == "11011101": self.IX = self.eightbitdec(self.IX[0:8]) + self.IX[8:16]
                    if self.preopcode == "11111101": self.IY = self.eightbitdec(self.IY[0:8]) + self.IY[8:16] 
                if self.opcode == "00001101": self.C = self.eightbitdec(self.C)#0D = DEC C
                if self.opcode == "00101101": 
                    if self.preopcode == "": self.L = self.eightbitdec(self.L)#2D = DEC L
                    if self.preopcode == "11011101": self.IX = self.IX[0:8] + self.eightbitdec(self.IX[8:16]) 
                    if self.preopcode == "11111101": self.IY = self.IY[0:8] + self.eightbitdec(self.IY[8:16]) 
                if self.opcode == "00001011": self.sixteenbitdec(self.B,self.C)#0B = DEC BC
                if self.opcode == "00011011": self.sixteenbitdec(self.D,self.E)#1B = DEC DE
                if self.opcode == "00101011": self.sixteenbitdec(self.H,self.L)#2B = DEC HL
                if self.opcode == "00111011": self.sixteenbitdec(self.SP,"SP")#3B = DEC SP
                if self.opcode == "10110000": self.A = self.eightbitor(self.B)#B0 = OR B 
                if self.opcode == "10110001": self.A = self.eightbitor(self.C)#B1 = OR C
                if self.opcode == "10110010": self.A = self.eightbitor(self.D)#B2 = OR D
                if self.opcode == "10110011": self.A = self.eightbitor(self.E)#B3 = OR E
                if self.opcode == "10110100": 
                    if self.preopcode == "": self.A = self.eightbitor(self.H)#B4 = OR H
                    if self.preopcode == "11011101": self.A = self.eightbitor(self.IX[0:8]) 
                    if self.preopcode == "11111101": self.A = self.eightbitor(self.IY[0:8]) 
                if self.opcode == "10110101": 
                    if self.preopcode == "": self.A = self.eightbitor(self.L)#B5 = OR L
                    if self.preopcode == "11011101": self.A = self.eightbitor(self.IX[8:16]) 
                    if self.preopcode == "11111101": self.A = self.eightbitor(self.IY[8:16]) 
                if self.opcode == "10110111": self.A = self.eightbitor(self.A)#B7 = OR A
                if self.opcode == "10100000": self.A = self.eightbitand(self.B)#A0 = AND B 
                if self.opcode == "10100001": self.A = self.eightbitand(self.C)#A1 = AND C
                if self.opcode == "10100010": self.A = self.eightbitand(self.D)#A2 = AND D
                if self.opcode == "10100011": self.A = self.eightbitand(self.E)#A3 = AND E
                if self.opcode == "10100100": 
                    if self.preopcode == "": self.A = self.eightbitand(self.H)#A4 = AND H
                    if self.preopcode == "11011101": self.A = self.eightbitand(self.IX[0:8])
                    if self.preopcode == "11111101": self.A = self.eightbitand(self.IY[0:8])
                if self.opcode == "10100101": 
                    if self.preopcode == "": self.A = self.eightbitand(self.L)#A5 = AND L
                    if self.preopcode == "11011101": self.A = self.eightbitand(self.IX[8:16])
                    if self.preopcode == "11111101": self.A = self.eightbitand(self.IY[8:16])
                if self.opcode == "10100111": self.A = self.eightbitand(self.A)#A7 = AND A
                if self.opcode == "10101000": self.A = self.eightbitxor(self.B)#A8 = XOR B 
                if self.opcode == "10101001": self.A = self.eightbitxor(self.C)#A9 = XOR C
                if self.opcode == "10101010": self.A = self.eightbitxor(self.D)#AA = XOR D
                if self.opcode == "10101011": self.A = self.eightbitxor(self.E)#AB = XOR E
                if self.opcode == "10101100": 
                    if self.preopcode == "": self.A = self.eightbitxor(self.H)#AC = XOR H
                    if self.preopcode == "11011101": self.A = self.eightbitxor(self.IX[0:8]) 
                    if self.preopcode == "11111101": self.A = self.eightbitxor(self.IY[0:8]) 
                if self.opcode == "10101101": 
                    if self.preopcode == "": self.A = self.eightbitxor(self.L)#AD = XOR L
                    if self.preopcode == "11011101": self.A = self.eightbitxor(self.IX[8:16]) 
                    if self.preopcode == "11111101": self.A = self.eightbitxor(self.IY[8:16]) 
                if self.opcode == "10101111": self.A = self.eightbitxor(self.A)#AF = XOR A
                if self.opcode == "10111000": self.eightbitcp(self.B)#B8 = CP B 
                if self.opcode == "10111001": self.eightbitcp(self.C)#B9 = CP C
                if self.opcode == "10111010": self.eightbitcp(self.D)#BA = CP D
                if self.opcode == "10111011": self.eightbitcp(self.E)#BB = CP E
                if self.opcode == "10111100": 
                    if self.preopcode == "": self.eightbitcp(self.H)#BC = CP H
                    if self.preopcode == "11011101": self.eightbitcp(self.IX[0:8]) 
                    if self.preopcode == "11111101": self.eightbitcp(self.IY[0:8]) 
                if self.opcode == "10111101":
                    if self.preopcode == "": self.eightbitcp(self.L)#BD = CP L
                    if self.preopcode == "11011101": self.eightbitcp(self.IX[8:16]) 
                    if self.preopcode == "11111101": self.eightbitcp(self.IY[8:16]) 
                if self.opcode == "10111111": self.eightbitcp(self.A)#BF = CP A
                if self.opcode == "11111110": self.eightbitcp(self.operand1)#FE = CP X
                if self.opcode == "10010000": self.A = self.eightbitsub(self.B)#90 = SUB B 
                if self.opcode == "10010001": self.A = self.eightbitsub(self.C)#91 = SUB C
                if self.opcode == "10010010": self.A = self.eightbitsub(self.D)#92 = SUB D
                if self.opcode == "10010011": self.A = self.eightbitsub(self.E)#93 = SUB E
                if self.opcode == "10010100": 
                    if self.preopcode == "": self.A = self.eightbitsub(self.H)#94 = SUB H
                    if self.preopcode == "11011101": self.A = self.eightbitsub(self.IX[0:8]) 
                    if self.preopcode == "11111101": self.A = self.eightbitsub(self.IY[0:8]) 
                if self.opcode == "10010101": 
                    if self.preopcode == "": self.A = self.eightbitsub(self.L)#95 = SUB L
                    if self.preopcode == "11011101": self.A = self.eightbitsub(self.IX[8:16]) 
                    if self.preopcode == "11111101": self.A = self.eightbitsub(self.IY[8:16]) 
                if self.opcode == "10010111": self.A = self.eightbitsub(self.A)#97 = SUB A
                if self.opcode == "10011000": self.A = self.eightbitsub(self.B)#98 = SBC B 
                if self.opcode == "10011001": self.A = self.eightbitsub(self.C)#99 = SBC C
                if self.opcode == "10011010": self.A = self.eightbitsub(self.D)#9A = SBC D
                if self.opcode == "10011011": self.A = self.eightbitsub(self.E)#9B = SBC E
                if self.opcode == "10011100": 
                    if self.preopcode == "": self.A = self.eightbitsub(self.H)#9C = SBC H
                    if self.preopcode == "11011101": self.A = self.eightbitsub(self.IX[0:8]) 
                    if self.preopcode == "11111101": self.A = self.eightbitsub(self.IY[0:8]) 
                if self.opcode == "10011101": 
                    if self.preopcode == "": self.A = self.eightbitsub(self.L)#9D = SBC L
                    if self.preopcode == "11011101": self.A = self.eightbitsub(self.IX[8:16]) 
                    if self.preopcode == "11111101": self.A = self.eightbitsub(self.IY[8:16]) 
                if self.opcode == "10011111": self.A = self.eightbitsub(self.A)#9E = SBC A
                if self.opcode == "11011110": self.A = self.eightbitsub(data)#DE = SBC A,n
                if self.opcode == "10000000": self.A = self.eightbitadd(self.B)#80 = ADD B 
                if self.opcode == "10000001": self.A = self.eightbitadd(self.C)#81 = ADD C
                if self.opcode == "10000010": self.A = self.eightbitadd(self.D)#82 = ADD D
                if self.opcode == "10000011": self.A = self.eightbitadd(self.E)#83 = ADD E
                if self.opcode == "10000100": 
                    if self.preopcode == "": self.A = self.eightbitadd(self.H)#84 = ADD H
                    if self.preopcode == "11011101": self.A = self.eightbitadd(self.IX[0:8]) 
                    if self.preopcode == "11111101": self.A = self.eightbitadd(self.IY[0:8]) 
                if self.opcode == "10000101": 
                    if self.preopcode == "": self.A = self.eightbitadd(self.L)#85 = ADD L
                    if self.preopcode == "11011101": self.A = self.eightbitadd(self.IX[8:16]) 
                    if self.preopcode == "11111101": self.A = self.eightbitadd(self.IY[8:16]) 
                if self.opcode == "10000111": self.A = self.eightbitadd(self.A)#87 = ADD A
                if self.opcode == "10001000": self.A = self.eightbitadd(self.B)#88 = ADC B
                if self.opcode == "10001001": self.A = self.eightbitadd(self.C)#89 = ADC C
                if self.opcode == "10001010": self.A = self.eightbitadd(self.D)#8A = ADC D
                if self.opcode == "10001011": self.A = self.eightbitadd(self.E)#8B = ADC E
                if self.opcode == "10001100": 
                    if self.preopcode == "": self.A = self.eightbitadd(self.H)#8C = ADC H
                    if self.preopcode == "11011101": self.A = self.eightbitadd(self.IX[0:8])
                    if self.preopcode == "11111101": self.A = self.eightbitadd(self.IY[0:8])
                if self.opcode == "10001101": 
                    if self.preopcode == "": self.A = self.eightbitadd(self.L)#8D = ADC L
                    if self.preopcode == "11011101": self.A = self.eightbitadd(self.IX[8:16])
                    if self.preopcode == "11111101": self.A = self.eightbitadd(self.IY[8:16])
                if self.opcode == "10001111": self.A = self.eightbitadd(self.A)#8F = ADC A
                if self.opcode == "11001110": self.A = self.eightbitadd(data)#CE = ADC A,n
                if self.opcode == "00001001": self.hladd(self.B + self.C)#09 = ADD HL,BC
                if self.opcode == "00011001": self.hladd(self.D + self.E)#19 = ADC HL,DE
                if self.opcode == "00101001" and self.preopcode == "": self.hladd(self.H + self.L)#29 = ADC HL,HL
                if self.opcode == "00101001" and self.preopcode == "11011101": self.hladd(self.IX)#29 = ADC HL,HL
                if self.opcode == "00101001" and self.preopcode == "11111101": self.hladd(self.IY)#29 = ADC HL,HL
                if self.opcode == "00111001": self.hladd(format(self.SP,'016b'))#39 = ADC HL,SP
                if self.opcode == "11000110": self.A = self.eightbitadd(self.operand1)#C6 = ADD A,n
                if self.opcode == "11010110": self.A = self.eightbitsub(self.operand1) #D6 = SUB n
                if self.opcode == "11110101": self.clearop() #F5 = PUSH AF
                if self.opcode == "11000101": self.clearop() #C5 = PUSH BC
                if self.opcode == "11010101": self.clearop() #D5 = PUSH DE
                if self.opcode == "11100101": self.clearop() #E5 = PUSH HL

                if self.opcode == "11010011": #D3 = OUT (X)
                    self.clearop()
                    self.instructioname = "OUT (X),A"
                    self.readmode()
                    self.delay = 0
                    #self.PC = self.PC + 1  
 
                if self.opcode == "11011011": #DB = IN (X)
                    self.clearop()
                    self.instructioname = "IN (X),A"
                    self.readmode()
                    self.delay = 0
                    #self.PC = self.PC + 1  
                
                if self.opcode == "00100010": #22 = LD (XX),HL
                    self.clearop()
                    self.instructioname = "LD (XX),HL"
                
                if self.opcode == "11100011": #E3 = EX (SP),HL
                    self.clearop()
                    self.instructioname = "EX (SP),HL"
                
                if self.opcode == "00110010": #32 = LD (XX),A
                    self.clearop()
                    self.instructioname = "LD (XX),A"
 
                if self.opcode == "00010000": #10 = DJNZ X
                    self.clearop()
                    self.instructioname = "DJNZ X"
 
                if self.opcode == "00111010": #3A = LD A,(XX)
                    self.clearop()
                    self.instructioname = "LD (XX),A"
                
                if self.opcode == "00101010": #2A = LD HL,(XX)
                    self.clearop()
                    self.instructioname = "LD HL,(XX)"
 
                if self.opcode == "11110001": self.clearop() #F1
                if self.opcode == "11000001": self.clearop() #C1
                if self.opcode == "11010001": self.clearop() #D1
                if self.opcode == "11100001": self.clearop() #E1
                if self.opcode == "01000001": self.B = self.eightbitld(self.B,self.C)#41 = LD B,C
                if self.opcode == "01111000": self.A = self.eightbitld(self.A,self.B)#78 = LD A,B
                if self.opcode == "01111001": self.A = self.eightbitld(self.A,self.C)#79 = LD A,C
                if self.opcode == "01111010": self.A = self.eightbitld(self.A,self.D)#7A = LD A,D
                if self.opcode == "01111011": self.A = self.eightbitld(self.A,self.E)#7B = LD A,E
                if self.opcode == "01111100": 
                    if self.preopcode == "": self.A = self.eightbitld(self.A,self.H)#7C = LD A,H
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01111101": 
                    if self.preopcode == "": self.A = self.eightbitld(self.A,self.L)#7D = LD A,L
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01001000": self.C = self.eightbitld(self.C,self.B)#48 = LD C,B
                if self.opcode == "01001001": self.C = self.eightbitld(self.C,self.C)#49 = LD C,C
                if self.opcode == "01001010": self.C = self.eightbitld(self.C,self.D)#4A = LD C,D
                if self.opcode == "01001011": self.C = self.eightbitld(self.C,self.E)#4B = LD C,E
                if self.opcode == "01001100": 
                    if self.preopcode == "": self.C = self.eightbitld(self.C,self.H)#4C = LD C,#H
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01001101": 
                    if self.preopcode == "": self.C = self.eightbitld(self.C,self.L)#4D = LD C,L
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01000000": self.B = self.eightbitld(self.B,self.B)#40 = LD B,B
                if self.opcode == "01000111": self.B = self.eightbitld(self.B,self.A)#47 = LD B,A
                if self.opcode == "01000100": 
                    if self.preopcode == "": self.B = self.eightbitld(self.B,self.H)#44 = LD B,H
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01000101":#45 = LD B,L
                    if self.preopcode == "": self.B = self.eightbitld(self.B,self.L)
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01011100": 
                    if self.preopcode == "": self.E = self.eightbitld(self.E,self.H)#5C = LD E,H
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01011101": 
                    if self.preopcode == "": self.E = self.eightbitld(self.E,self.L)#5D = LD E,L
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01011111": self.E = self.eightbitld(self.E,self.A)#5F = LD E,A
                if self.opcode == "01010100": 
                    if self.preopcode == "": self.D = self.eightbitld(self.D,self.H)#54 = LD D,H
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01010101": 
                    if self.preopcode == "": self.D = self.eightbitld(self.D,self.L)#55 = LD D,L
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01010000": self.D = self.eightbitld(self.D,self.B)#50 = LD D,B
                if self.opcode == "01010001": self.D = self.eightbitld(self.D,self.C)#51 = LD D,C
                if self.opcode == "01010010": self.D = self.eightbitld(self.D,self.D)#52 = LD D,D
                if self.opcode == "01010011": self.D = self.eightbitld(self.D,self.E)#53 = LD D,E
                if self.opcode == "01100000": self.H = self.eightbitld(self.H,self.B)#60 = LD H,B
                if self.opcode == "01100001": self.H = self.eightbitld(self.H,self.C)#61 = LD H,C
                if self.opcode == "01100010": self.H = self.eightbitld(self.H,self.D)#62 = LD H,D
                if self.opcode == "01100011": self.H = self.eightbitld(self.H,self.E)#63 = LD H,E
                if self.opcode == "01101000": self.L = self.eightbitld(self.L,self.B)#68 = LD L,B
                if self.opcode == "01101001": self.L = self.eightbitld(self.L,self.C)#69 = LD L,C
                if self.opcode == "01101010": self.L = self.eightbitld(self.L,self.D)#6A = LD L,D
                if self.opcode == "01101011": self.L = self.eightbitld(self.L,self.E)#6B = LD L,E
                if self.opcode == "01101100": 
                    if self.preopcode == "": self.L = self.eightbitld(self.L,self.H)#6C = LD L,H
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01101101": 
                    if self.preopcode == "": self.L = self.eightbitld(self.L,self.L)#6D = LD L,L
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01011000": self.E = self.eightbitld(self.E,self.B)#58 = LD E,B
                if self.opcode == "01011001": self.E = self.eightbitld(self.E,self.C)#59 = LD E,C
                if self.opcode == "01011010": self.E = self.eightbitld(self.E,self.D)#5A = LD E,D
                if self.opcode == "01011011": self.E = self.eightbitld(self.E,self.E)#5B = LD E,E
                if self.opcode == "01000010": self.B = self.eightbitld(self.B,self.D)#42 = LD B,D
                if self.opcode == "01000011": self.B = self.eightbitld(self.B,self.E)#43 = LD B,E
                if self.opcode == "01100100": 
                    if self.preopcode == "": self.H = self.eightbitld(self.H,self.H)#64 = LD H,H
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01100101": 
                    if self.preopcode == "": self.H = self.eightbitld(self.H,self.L)#65 = LD H,L
                    if self.preopcode != "": self.eightbitld("1","1")
                if self.opcode == "01001111": self.C = self.eightbitld(self.C,self.A)#4F = LD C,A
                if self.opcode == "01010111": self.D = self.eightbitld(self.D,self.A)#57 = LD D,A
                if self.opcode == "01100111": self.H = self.eightbitld(self.H,self.A)#67 = LD H,A
                if self.opcode == "01101111": self.L = self.eightbitld(self.L,self.A)#6F = LD L,A
                if self.opcode == "01111111": self.A = self.eightbitld(self.A,self.A)#7F = LD A,A
                if self.opcode == "00010111": #17 = RLA
                    C = self.A[0]
                    self.A = self.rotate(self.A[1],self.A[2],self.A[3],self.A[4],self.A[5],self.A[6],self.A[7],self.F[7])
                    self.clearop()
                    self.delay = 1
                    
                    #set flags
                    self.F = self.F[0] + self.F[1] + self.A[2] + "0" + self.A[4] + self.F[5] + "0" + C

                if self.opcode == "00011111": #1F = RRA
                    C = self.A[7]
                    self.A = self.rotate(self.F[7],self.A[0],self.A[1],self.A[2],self.A[3],self.A[4],self.A[5],self.A[6])
                    self.clearop()
                    self.delay = 1
                    
                    #set flags
                    self.F = self.F[0] + self.F[1] + self.A[2] + "0" + self.A[4] + self.F[5] + "0" + C

                if self.opcode == "00001111": #0F = RRCA
                    C = self.A[7]
                    self.A = self.rotate(self.A[7],self.A[0],self.A[1],self.A[2],self.A[3],self.A[4],self.A[5],self.A[6])
                    self.clearop()
                    self.delay = 1
                    
                    #set flags
                    self.F = self.F[0] + self.F[1] + self.A[2] + "0" + self.A[4] + self.F[5] + "0" + C

                if self.opcode == "00000111": #07 = RLCA
                    C = self.A[0]
                    self.A = self.rotate(self.A[1],self.A[2],self.A[3],self.A[4],self.A[5],self.A[6],self.A[7],self.A[0])
                    self.clearop()
                    self.delay = 1
                    
                    #set flags
                    self.F = self.F[0] + self.F[1] + self.A[2] + "0" + self.A[4] + self.F[5] + "0" + C

                if self.opcode == "00101111": #2F = CPL
                    if self.checkFlag(self.A[0]) == "1": bit0 = str(int(self.setBoolValue(False)))
                    if self.checkFlag(self.A[0]) == "0": bit0 = str(int(self.setBoolValue(True)))
                    if self.checkFlag(self.A[1]) == "1": bit1 = str(int(self.setBoolValue(False)))
                    if self.checkFlag(self.A[1]) == "0": bit1 = str(int(self.setBoolValue(True)))
                    if self.checkFlag(self.A[2]) == "1": bit2 = str(int(self.setBoolValue(False)))
                    if self.checkFlag(self.A[2]) == "0": bit2 = str(int(self.setBoolValue(True)))
                    if self.checkFlag(self.A[3]) == "1": bit3 = str(int(self.setBoolValue(False)))
                    if self.checkFlag(self.A[3]) == "0": bit3 = str(int(self.setBoolValue(True)))
                    if self.checkFlag(self.A[4]) == "1": bit4 = str(int(self.setBoolValue(False)))
                    if self.checkFlag(self.A[4]) == "0": bit4 = str(int(self.setBoolValue(True)))
                    if self.checkFlag(self.A[5]) == "1": bit5 = str(int(self.setBoolValue(False)))
                    if self.checkFlag(self.A[5]) == "0": bit5 = str(int(self.setBoolValue(True)))
                    if self.checkFlag(self.A[6]) == "1": bit6 = str(int(self.setBoolValue(False)))
                    if self.checkFlag(self.A[6]) == "0": bit6 = str(int(self.setBoolValue(True)))
                    if self.checkFlag(self.A[7]) == "1": bit7 = str(int(self.setBoolValue(False)))
                    if self.checkFlag(self.A[7]) == "0": bit7 = str(int(self.setBoolValue(True)))

                    self.A = bit0 + bit1 + bit2 + bit3 + bit4 + bit5 + bit6 + bit7
                     
                    self.F = self.F[0] + self.F[1] + self.A[2] + "1" + self.A[4] + self.F[5] + "1" + self.F[7]

                    self.clearop()
                    self.delay = 1

                if self.opcode == "00111111": #3F = CCF
                   # if self.F[7] == "1": invc = "0"
                    #if self.F[7] == "0": invc = "1"

                    if self.checkFlag(self.F[7]) == "1": invc = str(int(self.setBoolValue(False)))
                    if self.checkFlag(self.F[7]) == "0": invc = str(int(self.setBoolValue(True)))

                    #if self.checkFlag(self.F[3]) == "1": invh = "0"
                    #if self.checkFlag(self.F[3]) == "0": invh = "1"



                    self.F = self.F[0] + self.F[1] + self.A[2] + self.F[7] + self.A[4] + self.F[5] + "0" + invc
                    self.clearop()
                    self.delay = 1
                    
           
#*********************************************other functions***************************************************
    def reset(self):#bug that doesnt read first instruciton
        self.A = "11111111"
        self.F = "11111111"
        self.A1 = "11111111"
        self.F1 = "11111111"
        self.B = "11111111"
        self.C = "11111111"
        self.D = "11111111"
        self.E = "11111111"
        self.H = "00000000"
        self.L = "00000000"
        self.B1 = "11111111"
        self.C1 = "11111111"
        self.D1 = "11111111"
        self.E1 = "11111111"
        self.H1 = "00000000"
        self.L1 = "00000000"
        self.IX = "0000000000000000"
        self.IY = "0000000000000000"
        self.PC = 0
        self.SP = 65535
        self.a0 = self.a1 = self.a2 = self.a3 = self.a4 = self.a5 = self.a6 = self.a7 = self.a8 = self.a9 = self.a10 = self.a11 = self.a12 = self.a13 = self.a14 = self.a15 = False
        self.RD = False 
        self.WR = True 
        self.debugline = ""
        self.delay = 0
        self.instructionname = ""
        self.opcode = ""
        self.operand1 = ""
        self.operand2 = ""
        self.needmorebits = False
        self.execute = False
        self.prejumppc = 0
        self.stage = ""
        self.interupts = False 
        self.halt = False
        self.opx = ""
        self.opy = ""
        self.R = 1
        self.preopcode = ""
        self.I = "00000000"

    def clearop(self):
        self.opcode = ""
        self.operand1 = ""
        self.operand2 = ""
        self.execute = False
        self.stage = ""
        self.opx = ""
        self.opy = ""
        self.preopcode = ""

    def nextstage(self,delay,stage):
        self.delay = delay
        self.stage = stage

    def finalstage(self,delay):
        self.delay = delay
        self.needmorebits = False
        self.execute = True

    def writemode(self):
        self.RD = True
        self.WR = False

    def readmode(self):
        self.RD = False
        self.WR = True

    def fetchanddecodestage1(self,read,write,name,delay,opcode,needmorebits,execute):
        self.RD = read
        self.WR = write
        self.instructionname = name
        self.delay = delay
        self.opcode = opcode
        self.execute = execute
        self.needmorebits = needmorebits

    def fetchanddecodestage2(self,operand,delay,name,needmorebits,execute):
        self.operand1 = operand
        self.delay = delay
        self.instructionname = name
        self.needmorebits = needmorebits
        self.execute = execute

    def getZflag(self,flag):
        Z = "0"
        if flag == "00000000": Z = "1"
        return Z
   
    def regtodatabus(self,register):
        self.d7 = bool(int(register[0]))
        self.d6 = bool(int(register[1]))
        self.d5 = bool(int(register[2]))
        self.d4 = bool(int(register[3]))
        self.d3 = bool(int(register[4]))
        self.d2 = bool(int(register[5]))
        self.d1 = bool(int(register[6]))
        self.d0 = bool(int(register[7]))

    def regtoaddrbus(self,register):
        self.a15 = bool(int(register[0]))
        self.a14 = bool(int(register[1]))
        self.a13 = bool(int(register[2]))
        self.a12 = bool(int(register[3]))
        self.a11 = bool(int(register[4]))
        self.a10 = bool(int(register[5]))
        self.a9 = bool(int(register[6]))
        self.a8 = bool(int(register[7]))
        self.a7 = bool(int(register[8]))
        self.a6 = bool(int(register[9]))
        self.a5 = bool(int(register[10]))
        self.a4 = bool(int(register[11]))
        self.a3 = bool(int(register[12]))
        self.a2 = bool(int(register[13]))
        self.a1 = bool(int(register[14]))
        self.a0 = bool(int(register[15]))
 
    def getparity(self,register):
        paritycount = 0
        x = 0 
        while x < 8:
            paritycount = paritycount + int(register[x])
            x = x + 1

        if paritycount % 2 ==0:
            return "1"
        else:
            return "0"

    def eightbitinc(self,register):
        x = int(register,2)
        x = x + 1 

        if x == 256: x = 0
        register = format(x, '08b')
        self.clearop()
        self.delay = 1
                    
        #Set flags
        H = "0"
        P = "0"
        N = "0"
        C = self.F[7]
        if register  == "10000000": P = "1"
        if register[7] == "0" and register[6] == "0" and register[5] == "0" and register[4] == "0": H = "1"
        self.F = register[0] + self.getZflag(register) + register[2] + H + register[4] + P + "0" + C
        return register

    def eightbitdec(self,register):
        x = int(register,2)
        x = x - 1
        if x == -1: x = 255
        register = format(x, '08b')
        self.clearop()
        self.delay = 1
                    
        #set flags
        H = "0"
        if register[7] == "1" and register[6] == "1" and register[5] == "1" and register[4] == "1": H = "1"
        P = "0"
        if register == "01111111": P = "1"
        self.F = register[0] + self.getZflag(register) + register[2] + H + register[4] + P + "1" + self.F[7]
        return register


    def eightbitld(self,register1,register2):
        
        if self.preopcode == "11011101" and self.opcode == "01100000": self.IX = register2 + self.IX[8:16]
        if self.preopcode == "11111101" and self.opcode == "01100000": self.IY = register2 + self.IY[8:16]
        if self.preopcode == "11011101" and self.opcode == "01100001": self.IX = register2 + self.IX[8:16]
        if self.preopcode == "11111101" and self.opcode == "01100001": self.IY = register2 + self.IY[8:16]
        if self.preopcode == "11011101" and self.opcode == "01100010": self.IX = register2 + self.IX[8:16]
        if self.preopcode == "11111101" and self.opcode == "01100010": self.IY = register2 + self.IY[8:16]
        if self.preopcode == "11011101" and self.opcode == "01100011": self.IX = register2 + self.IX[8:16]
        if self.preopcode == "11111101" and self.opcode == "01100011": self.IY = register2 + self.IY[8:16]
        if self.preopcode == "11011101" and self.opcode == "01100111": self.IX = register2 + self.IX[8:16]
        if self.preopcode == "11111101" and self.opcode == "01100111": self.IY = register2 + self.IY[8:16]

        if self.preopcode == "11011101" and self.opcode == "01101000": self.IX = self.IX[0:8] + register2
        if self.preopcode == "11111101" and self.opcode == "01101000": self.IY = self.IY[0:8] + register2
        if self.preopcode == "11011101" and self.opcode == "01101001": self.IX = self.IX[0:8] + register2
        if self.preopcode == "11111101" and self.opcode == "01101001": self.IY = self.IY[0:8] + register2
        if self.preopcode == "11011101" and self.opcode == "01101010": self.IX = self.IX[0:8] + register2
        if self.preopcode == "11111101" and self.opcode == "01101010": self.IY = self.IY[0:8] + register2
        if self.preopcode == "11011101" and self.opcode == "01101011": self.IX = self.IX[0:8] + register2
        if self.preopcode == "11111101" and self.opcode == "01101011": self.IY = self.IY[0:8] + register2
        if self.preopcode == "11011101" and self.opcode == "01101111": self.IX = self.IX[0:8] + register2
        if self.preopcode == "11111101" and self.opcode == "01101111": self.IY = self.IY[0:8] + register2

        if self.preopcode == "11011101" and self.opcode == "01000100": self.B = self.IX[0:8]
        if self.preopcode == "11111101" and self.opcode == "01000100": self.B = self.IY[0:8]
        if self.preopcode == "11011101" and self.opcode == "01000101": self.B = self.IX[8:16]
        if self.preopcode == "11111101" and self.opcode == "01000101": self.B = self.IY[8:16]

        if self.preopcode == "11011101" and self.opcode == "01010100": self.D = self.IX[0:8]
        if self.preopcode == "11111101" and self.opcode == "01010100": self.D = self.IY[0:8]
        if self.preopcode == "11011101" and self.opcode == "01010101": self.D = self.IX[8:16]
        if self.preopcode == "11111101" and self.opcode == "01010101": self.D = self.IY[8:16]

        if self.preopcode == "11011101" and self.opcode == "01001100": self.C = self.IX[0:8]
        if self.preopcode == "11111101" and self.opcode == "01001100": self.C = self.IY[0:8]
        if self.preopcode == "11011101" and self.opcode == "01001101": self.C = self.IX[8:16]
        if self.preopcode == "11111101" and self.opcode == "01001101": self.C = self.IY[8:16]

        if self.preopcode == "11011101" and self.opcode == "01111100": self.A = self.IX[0:8]
        if self.preopcode == "11111101" and self.opcode == "01111100": self.A = self.IY[0:8]
        if self.preopcode == "11011101" and self.opcode == "01111101": self.A = self.IX[8:16]
        if self.preopcode == "11111101" and self.opcode == "01111101": self.A = self.IY[8:16]

        if self.preopcode == "11011101" and self.opcode == "01011100": self.E = self.IX[0:8]
        if self.preopcode == "11111101" and self.opcode == "01011100": self.E = self.IY[0:8]
        if self.preopcode == "11011101" and self.opcode == "01011101": self.E = self.IX[8:16]
        if self.preopcode == "11111101" and self.opcode == "01011101": self.E = self.IY[8:16]

        if self.preopcode == "11011101" and self.opcode == "01101100": self.IX = self.IX[0:8] + self.IX[0:8]
        if self.preopcode == "11111101" and self.opcode == "01101100": self.IY = self.IY[0:8] + self.IY[0:8]

        if self.preopcode == "11011101" and self.opcode == "01100101": self.IX = self.IX[8:16] + self.IX[8:16]
        if self.preopcode == "11111101" and self.opcode == "01100101": self.IY = self.IY[8:16] + self.IY[8:16]

        if self.preopcode == "11011101" and self.opcode == "01000000": register1 = self.B
        if self.preopcode == "11111101" and self.opcode == "01000000": register1 = self.B
        if self.preopcode == "11011101" and self.opcode == "01000001": register1 = self.C
        if self.preopcode == "11111101" and self.opcode == "01000001": register1 = self.C
        if self.preopcode == "11011101" and self.opcode == "01000010": register1 = self.D
        if self.preopcode == "11111101" and self.opcode == "01000010": register1 = self.D
        if self.preopcode == "11011101" and self.opcode == "01000011": register1 = self.E
        if self.preopcode == "11111101" and self.opcode == "01000011": register1 = self.E

        if self.preopcode == "11011101" and self.opcode == "01010000": register1 = self.B
        if self.preopcode == "11111101" and self.opcode == "01010000": register1 = self.B
        if self.preopcode == "11011101" and self.opcode == "01010001": register1 = self.C
        if self.preopcode == "11111101" and self.opcode == "01010001": register1 = self.C
        if self.preopcode == "11011101" and self.opcode == "01010010": register1 = self.D
        if self.preopcode == "11111101" and self.opcode == "01010010": register1 = self.D
        if self.preopcode == "11011101" and self.opcode == "01010011": register1 = self.E
        if self.preopcode == "11111101" and self.opcode == "01010011": register1 = self.E

        if self.preopcode == "11011101" and self.opcode == "01000111": register1 = self.A
        if self.preopcode == "11111101" and self.opcode == "01000111": register1 = self.A

        if self.preopcode == "11011101" and self.opcode == "01001000": register1 = self.B
        if self.preopcode == "11111101" and self.opcode == "01001000": register1 = self.B
        if self.preopcode == "11011101" and self.opcode == "01001001": register1 = self.C
        if self.preopcode == "11111101" and self.opcode == "01001001": register1 = self.C
        if self.preopcode == "11011101" and self.opcode == "01001010": register1 = self.D
        if self.preopcode == "11111101" and self.opcode == "01001010": register1 = self.D
        if self.preopcode == "11011101" and self.opcode == "01001011": register1 = self.E
        if self.preopcode == "11111101" and self.opcode == "01001011": register1 = self.E

        if self.preopcode == "11011101" and self.opcode == "01001111": register1 = self.A
        if self.preopcode == "11111101" and self.opcode == "01001111": register1 = self.A

        if self.preopcode == "11011101" and self.opcode == "01010111": register1 = self.A
        if self.preopcode == "11111101" and self.opcode == "01010111": register1 = self.A

        if self.preopcode == "11011101" and self.opcode == "01011000": register1 = self.B
        if self.preopcode == "11111101" and self.opcode == "01011000": register1 = self.B
        if self.preopcode == "11011101" and self.opcode == "01011001": register1 = self.C
        if self.preopcode == "11111101" and self.opcode == "01011001": register1 = self.C
        if self.preopcode == "11011101" and self.opcode == "01011010": register1 = self.D
        if self.preopcode == "11111101" and self.opcode == "01011010": register1 = self.D
        if self.preopcode == "11011101" and self.opcode == "01011011": register1 = self.E
        if self.preopcode == "11111101" and self.opcode == "01011011": register1 = self.E

        if self.preopcode == "11011101" and self.opcode == "01011111": register1 = self.A
        if self.preopcode == "11111101" and self.opcode == "01011111": register1 = self.A

        if self.preopcode == "11011101" and self.opcode == "01111000": register1 = self.B
        if self.preopcode == "11111101" and self.opcode == "01111000": register1 = self.B
        if self.preopcode == "11011101" and self.opcode == "01111001": register1 = self.C
        if self.preopcode == "11111101" and self.opcode == "01111001": register1 = self.C
        if self.preopcode == "11011101" and self.opcode == "01111010": register1 = self.D
        if self.preopcode == "11111101" and self.opcode == "01111010": register1 = self.D
        if self.preopcode == "11011101" and self.opcode == "01111011": register1 = self.E
        if self.preopcode == "11111101" and self.opcode == "01111011": register1 = self.E

        if self.preopcode == "11011101" and self.opcode == "01111111": register1 = self.A
        if self.preopcode == "11111101" and self.opcode == "01111111": register1 = self.A

        if self.preopcode == "":
            register1 = register2

        self.clearop()
        self.delay = 1
        #No flags effected
        return register1

    def eightbitor(self,register):
        A = int(self.A,2)
        oredwith = int(register,2)
        ored = bin(A | oredwith)[2:].zfill(8)
       
        #set flags
        self.F = ored[0] + self.getZflag(ored) + ored[2] + "0" + ored[4] + self.getparity(ored) + "0" + "0" 
        self.clearop()
        self.delay =  1

        return ored
    
    def eightbitand(self,register):
        A = int(self.A,2)
        andwith = int(register,2)
        anded = bin(A & andwith)[2:].zfill(8)
                    
        #set flags
        self.F = anded[0] + self.getZflag(anded) + anded[2] + "1" + anded[4] + self.getparity(anded) + "0" + "0" 
        self.clearop()
        self.delay =  1

        return anded

    def eightbitxor(self,register):
        A = int(self.A,2)
        xorwith = int(register,2)
        
        xored = bin(A ^ xorwith)[2:].zfill(8)
                    
        #set flags
        self.F = xored[0] + self.getZflag(xored) + xored[2] + "0" + xored[4] + self.getparity(xored) + "0" + "0" 
        self.clearop()
        self.delay =  1

        return xored

    def eightbitcp(self,register):
        A = int(self.A,2)
        N = int(register,2)
        
        #***** Z *****
        Z = "0"
        if A == N: Z = "1"
        
        result = A - N

        C = "0"
        if result < 0: 
            result = result + 256
            C = "1"
        result = format(result,'08b')
      
        #****** S *****
        S = result[0]
        
        #***** H *****
        H = "0"
        X = int(self.A[4] + self.A[5] + self.A[6] + self.A[7],2)
        Y = int(register[4] + register[5] + register[6] + register[7],2)
        
        if (X - Y) < 0: H = "1"
 
        #***** P *****
        P = "0"  
        if self.A[0] == "0" and register[0] == "1" and result[0] == "1": P = "1"
        if self.A[0] == "1" and register[0] == "0" and result[0] == "0": P = "1" 
                    
        #set flags
        #F3 and F5 flags not right
        #       (S) (Z) (F5)          H   (F3)        (P)  (N)  (C)
        self.F = S + Z + self.F[2] + H + self.F[4] + P + "1" + C 
        self.clearop()
        self.delay =  1

    def eightbitsub(self,register):
        A = int(self.A,2)
        B = int(register,2)
        sub = A - B
 
        minus = 0 
        if self.F[7] == "1" and self.opcode == "10011000": minus = 1
        if self.F[7] == "1" and self.opcode == "10011001": minus = 1
        if self.F[7] == "1" and self.opcode == "10011010": minus = 1
        if self.F[7] == "1" and self.opcode == "10011011": minus = 1
        if self.F[7] == "1" and self.opcode == "10011100": minus = 1
        if self.F[7] == "1" and self.opcode == "10011101": minus = 1
        if self.F[7] == "1" and self.opcode == "10011111": minus = 1
        if self.F[7] == "1" and self.opcode == "10011110": minus = 1
        if self.F[7] == "1" and self.opcode == "11011110": minus = 1
        sub = sub - minus

        C = "0"
        P = "0"
        if sub < 0:
            sub = sub  + 256
            C = "1"
        sub = format(sub, '08b')
        self.clearop()
        self.delay = 1
               
        #set flags
        H = "0"
        X = int(self.A[4] + self.A[5] + self.A[6] + self.A[7],2)
        Y = int(register[4] + register[5] + register[6] + register[7],2)
        Z = X - Y
        Z = Z - minus
        
        if Z < 0: H = "1"
        
        P = "0"
        if self.A[0] == "0" and register[0] == "1" and sub[0] == "1": P = "1"
        if self.A[0] == "1" and register[0] == "0" and sub[0] == "0": P = "1" 

        self.F = sub[0] + self.getZflag(sub) + sub[2] + H + sub[4] + P + "1" + C
        return sub

    def eightbitadd(self,register):
        A = int(self.A,2)
        B = int(register,2)

        addition = 0
        if self.F[7] == "1" and self.opcode == "10001000": addition = 1
        if self.F[7] == "1" and self.opcode == "10001001": addition = 1
        if self.F[7] == "1" and self.opcode == "10001010": addition = 1
        if self.F[7] == "1" and self.opcode == "10001011": addition = 1
        if self.F[7] == "1" and self.opcode == "10001100": addition = 1
        if self.F[7] == "1" and self.opcode == "10001101": addition = 1
        if self.F[7] == "1" and self.opcode == "10001111": addition = 1
        if self.F[7] == "1" and self.opcode == "10001110": addition = 1
        if self.F[7] == "1" and self.opcode == "11001110": addition = 1

        total = A + (B + addition)
 
        C = "0"
        P = "0"
        if total > 255:
            total = total - 256
            C = "1"
            
        total = format(total, '08b')
        self.clearop()
        self.delay = 1
               
        #set flags
        H = "0"
        X = int(self.A[4] + self.A[5] + self.A[6] + self.A[7],2)
        Y = int(register[4] + register[5] + register[6] + register[7],2)
        Z = X + Y + addition
        #Z = Z + addition
        if Z > 15: H = "1"   

        if self.A[0] == "0" and register[0] == "0" and total[0] == "1": P = "1"
        if self.A[0] == "1" and register[0] == "1" and total[0] == "0": P = "1"

        self.F = total[0] + self.getZflag(total) + total[2] + H + total[4] + P + "0" + C
        return total

    def sixteenbitinc(self,register1,register2):
        if self.opcode == "00110011":
            rr = int(format(self.SP,'016b'),2)
        else:
            rr = int(register1 + register2,2)
        if self.opcode == "00100011" and self.preopcode == "11011101":
            rr = int(self.IX,2)
        if self.opcode == "00100011" and self.preopcode == "11111101":
            rr = int(self.IY,2)

        rr = rr + 1
        if rr > 65535:
            rr = rr - 65536
        total = format(rr, '016b')

        r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
        r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]
        
        if self.opcode == "00000011": 
            self.B = r1
            self.C = r2
        if self.opcode == "00010011": 
            self.D = r1
            self.E = r2
        if self.opcode == "00100011" and self.preopcode == "": 
            self.H = r1
            self.L = r2
        if self.opcode == "00100011" and self.preopcode == "11011101":
            self.IX = r1 + r2
        if self.opcode == "00100011" and self.preopcode == "11111101":
            self.IY = r1 + r2

        if self.opcode == "00110011": 
            self.SP = rr         
       
        self.clearop()
        self.delay = 1

    def sixteenbitdec(self,register1,register2):
        if self.opcode == "00111011":
            rr = int(format(self.SP,'016b'),2)
        else:
            rr = int(register1 + register2,2)

        if self.opcode == "00101011" and self.preopcode == "11011101":
            rr = int(self.IX,2)
        if self.opcode == "00101011" and self.preopcode == "11111101":
            rr = int(self.IY,2)

        rr = rr - 1
        if rr < 0:
            rr = rr + 65536
        total = format(rr, '016b')

        r1 = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
        r2 = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]
        
        if self.opcode == "00001011": 
            self.B = r1
            self.C = r2
        if self.opcode == "00011011": 
            self.D = r1
            self.E = r2
        if self.opcode == "00101011" and self.preopcode == "": 
            self.H = r1
            self.L = r2
        if self.opcode == "00111011": 
            self.SP = rr         
        if self.opcode == "00101011" and self.preopcode == "11011101":
            self.IX = r1 + r2
        if self.opcode == "00101011" and self.preopcode == "11111101":
            self.IY = r1 + r2

        self.clearop()
        self.delay = 1

    def loadhlr(self,data,original):
        if self.preopcode == "":
            if self.stage == "1":
                stage = ""
                self.delay = 1
                self.needmorebits = False
                self.execute = True
                register = data
                self.PC = self.prejumppc + 1
                self.instructionname = "LD R,(HL) (" + data + ")"
                return register

            if self.stage == "":
                self.stage = "1"
                self.delay = 3

                hl = int(self.H + self.L,2)
                self.prejumppc = self.PC
                self.PC = hl
                self.instructionname = "LD R,(HL) (" + data  + ")"
                return original
        else:
            self.instructionname = "LD R,(IXY + d)"
            if self.stage == "3":
                self.delay = 1
                self.needmorebits = False
                self.execute = True
                self.PC = self.prejumppc + 2
                return data
            
            if self.stage == "2":
                self.stage = "3"
                self.delay = 3

                if self.preopcode == "11011101":
                    if data[0] == "1": self.PC = int(self.IX,2) - (128 - int(data[1] + data[2] + data[3] + data[4] + data[5] + data[6] + data[7],2))
                    if data[0] == "0": self.PC = int(self.IX,2) +  int(data[1] + data[2] + data[3] + data[4] + data[5] + data[6] + data[7],2)
                if self.preopcode == "11111101":
                    if data[0] == "1": self.PC = int(self.IY,2) - (128 - int(data[1] + data[2] + data[3] + data[4] + data[5] + data[6] + data[7],2))
                    if data[0] == "0": self.PC = int(self.IY,2) +  int(data[1] + data[2] + data[3] + data[4] + data[5] + data[6] + data[7],2)

                return original

            if self.stage == "1":
                self.stage = "2"
                self.delay = 4
                return original

            if self.stage == "":
                self.stage = "1"
                self.delay = 4
                self.prejumppc = self.PC
                self.PC = self.PC + 1
                return original
    
    def loadsixteen(self,data,original,register1,register2):
        if self.stage == "1":
            stage = ""
            self.delay = 1
            self.needmorebits = False
            self.execute = True
            register = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
            self.PC = self.prejumppc + 1
            self.instructionname = "LD R,(NN) (" + data + ")"
            return register

        if self.stage == "":
            self.stage = "1"
            self.delay = 3
            self.prejumppc = self.PC
            self.PC = int(register1 + register2,2)
            self.instructionname = "LD R,(nn), (" + data  + ")"
            return original
    
    def callinst(self,check,data):
        jumping = "0"

        if self.opcode == "11001101": jumping = "1"
        if self.opcode == "11000100" and self.F[1] == "0": jumping = "1"
        if self.opcode == "11010100" and self.F[7] == "0": jumping = "1"
        if self.opcode == "11100100" and self.F[5] == "0": jumping = "1"
        if self.opcode == "11110100" and self.F[0] == "0": jumping = "1"
        if self.opcode == "11001100" and self.F[1] == "1": jumping = "1"
        if self.opcode == "11011100" and self.F[7] == "1": jumping = "1"
        if self.opcode == "11101100" and self.F[5] == "1": jumping = "1"
        if self.opcode == "11111100" and self.F[0] == "1": jumping = "1"

        if self.stage == "4" and jumping == "1":
            pc = format(self.prejumppc + 1,'016b')
            second8pc = pc[8] + pc[9] + pc[10] + pc[11] + pc[12] + pc[13] + pc[14] + pc[15]
            self.delay = 3
            self.instructionname = "CALL " + check +  "nn Pushing PC (" + second8pc + ")"
            self.needmorebits = False
            self.execute = True
            self.writemode()
                        
            #stick it on the stack
            #self.SP = self.SP - 1
            #if self.SP < 0: self.SP = self.SP + 65536
            self.SP = self.decNoFlags(self.SP)

            self.regtodatabus(second8pc)
            addr = format(self.SP,'016b')
            addr = str(addr)
            self.PC = self.SP
            self.regtoaddrbus(addr)
            self.stage = "6"
                       
        if self.stage == "3" and jumping == "1":

            pc = format(self.prejumppc + 1,'016b')
            first8pc = pc[0] + pc[1] + pc[2] + pc[3] + pc[4] + pc[5] + pc[6] + pc[7]
            self.delay = 3
            self.instructionname = "CALL " + check + "nn, Pushing PC (" + first8pc + ")"
            self.needmorebits = True
            self.execute = False
            self.writemode()
                         
            #stick it on the stack
            #self.SP = self.SP - 1
            #if self.SP < 0: self.SP = self.SP + 65536
            self.SP = self.decNoFlags(self.SP)

            self.regtodatabus(first8pc)
            addr = format(self.SP,'016b')
            addr = str(addr)
            self.PC = self.SP
            self.regtoaddrbus(addr)
            self.stage = "4"
                            
        if self.stage == "2" and jumping == "1":
            self.operand2 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
            self.prejumppc = self.PC
            self.delay = 2
            self.instructionname = "CALL " + check + "nn (" + self.operand1 + ":" + self.operand2 + ")"
            self.needmorebits = True
            self.stage = "3"
                       
        if self.stage == "1" and jumping == "1":
            self.operand1 = self.singleload(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
            self.delay = 3
            self.instructionname = "CALL " + check + "nn (" + self.operand1
            self.needmorebits = True
            self.PC = self.PC + 1
            self.stage = "2"

        if self.stage == "" and jumping == "1":
            self.delay = 3
            self.instructionname = "CALL " + check+ "nn "
            self.needmorebits = True
            self.stage = "1"
            self.PC = self.PC + 1

        if jumping == "0":
            self.instructionname = "CALL NZ"

            if self.stage == "2":
                self.delay = 1
                self.needmorebits = False
                self.execute = True
                self.PC = self.PC + 1

            if self.stage == "1":
                self.delay = 3
                self.stage = "2"
                self.PC = self.PC + 1

            if self.stage == "":
                self.delay = 3
                self.stage = "1"
                self.PC = self.PC + 1

    def hladc(self,register):
        hl12 = int((self.H + self.L)[-12:],2)
        add12 = int(register[-12:],2) + int(self.F[7])
            
        A = int(self.H + self.L,2)
        B = int(register,2)
        total = A + B + int(self.F[7])

        C = "0"
        if total > 65535:
            total = total - 65536
            C = "1"
        Z = "0"
        if total == 0: Z = "1"
        total = format(total, '016b')

        H = "0"
        if (add12 + hl12) > 4095: H = "1"


        P = "0"
        if self.H[0] == "0" and register[0] == "0" and total[0] == "1": P = "1"
        if self.H[0] == "1" and register[0] == "1" and total[0] == "0": P = "1"


        self.H = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
        self.L = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]


        #        S          Z   F3          H   F5          P   N     C
        self.F = total[0] + Z + self.F[2] + H + self.F[4] + P + "0" + C

    def hlsbc(self,register):
        hl12 = int((self.H + self.L)[-12:],2)
        sub12 = int(register[-12:],2) - int(self.F[7])


        A = int(self.H + self.L,2)
        B = int(register,2)
        total = A - B - int(self.F[7])
        
        C = "0"
        if total < 0:
            total = total + 65536
            C = "1"
        Z = "0"
        if total == 0: Z = "1"
        total = format(total, '016b')

        H = "0"
        if sub12 > hl12: H = "1"

        P = "0"
        if self.H[0] == "0" and register[0] == "1" and total[0] == "1": P = "1"
        if self.H[0] == "1" and register[0] == "0" and total[0] == "0": P = "1"


        self.H = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
        self.L = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]

        #        S          Z   F3          H   F5          P    N    C
        self.F = total[0] + Z + self.F[2] + H + self.F[4] + P + "1" + C

    def hladd(self,register):
        hl12 = int((self.H + self.L)[-12:],2)
        add12 = int(register[-12:],2)

        if self.preopcode == "": A = int(self.H  + self.L,2)
        if self.preopcode == "11011101": A = int(self.IX,2)
        if self.preopcode == "11111101": A = int(self.IY,2)

        B = int(register,2)
        total = A + B
 
        C = "0"
        P = "0"
        if total > 65535:
            total = total - 65536
            C = "1"
            
        total = format(total, '016b')

        if self.preopcode == "":
            self.H = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7]
            self.L = total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]
            
        if self.preopcode == "11011101":
            self.IX = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7] + total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]
        if self.preopcode == "11111101":
            self.IY = total[0] + total[1] + total[2] + total[3] + total[4] + total[5] + total[6] + total[7] + total[8] + total[9] + total[10] + total[11] + total[12] + total[13] + total[14] + total[15]
 
        self.clearop()
        self.delay = 1
               
        #set flags
        H = "0"
        if (add12 + hl12) > 4095: H = "1"

        self.F = self.F[0] + self.F[1] + self.H[2] + H + self.H[4] + self.F[5] + "0" + C

    def rstinst(self):
        
        if self.stage == "4":
            pc = format(self.prejumppc + 1,'016b')
            second8pc = pc[8] + pc[9] + pc[10] + pc[11] + pc[12] + pc[13] + pc[14] + pc[15]
            self.delay = 3
            self.instructionname = "RST Pushing PC (" + second8pc + ")"
            self.needmorebits = False
            self.execute = True
            self.writemode()
                       
            #stick it on the stack
            self.SP = self.decNoFlags(self.SP)
            self.PC = self.SP
            self.regtodatabus(second8pc)
            addr = format(self.SP,'016b')
            addr = str(addr)
            self.regtoaddrbus(addr)
            self.stage = "6"
                       
        if self.stage == "3":
            pc = format(self.prejumppc + 1,'016b')
            first8pc = pc[0] + pc[1] + pc[2] + pc[3] + pc[4] + pc[5] + pc[6] + pc[7]
            self.delay = 3
            self.instructionname = "RST, Pushing PC (" + first8pc + ")"
            self.needmorebits = True
            self.execute = False
            self.writemode()
                         
            #stick it on the stack
            self.SP = self.decNoFlags(self.SP)
            self.PC = self.SP
            self.regtodatabus(first8pc)
            addr = format(self.SP,'016b')
            addr = str(addr)
            self.regtoaddrbus(addr)
            self.stage = "4"
                            
        if self.stage == "":
            self.prejumppc = self.PC
            self.delay = 2
            self.instructionname = "RST"
            self.needmorebits = True
            self.stage = "3"

    def xxbitxx(self,register):
        if self.opy < 8:
            bit = 0
            if self.opx == 4: bit = 0
            if self.opx == 5: bit = 2
            if self.opx == 6: bit = 4
            if self.opx == 7: bit = 6
 
            if self.opx > 3 and self.opx < 8:
                notbit = not bool(int(register[7 - bit]))
                notbit = str(int(notbit))
                self.F = "0" + notbit + self.F[2] + "1" + self.F[4] + "0"  + "0" + self.F[7]
      
            if self.opx == 8: 
                register = register[0]  + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + "0"
                self.instructionname = "xxBITxx RES 0"
            if self.opx == 9: 
                register = register[0]  + register[1] + register[2] + register[3] + register[4] +         "0" + register[6] + register[7] 
                self.instructionname = "xxBITxx RES 2"
            if self.opx == 10: 
                register = register[0] + register[1] + register[2] + "0"         + register[4] + register[5] + register[6] + register[7] 
                self.instructionname = "xxBITxx RES 4"
            if self.opx == 11: 
                register = register[0] + "0"         + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] 
                self.instructionname = "xxBitxx RES 6"
            if self.opx == 12: register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + "1"
            if self.opx == 13: register = register[0] + register[1] + register[2] + register[3] + register[4] +         "1" + register[6] + register[7] 
            if self.opx == 14: register = register[0] + register[1] + register[2] + "1"         + register[4] + register[5] + register[6] + register[7] 
            if self.opx == 15: register = register[0] + "1"         + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] 
            
            if self.opx == 3: 
                temp = register
                register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + "1"
                X = int(temp,2)
                Y = int(register,2)
                C = "0"
                if X >= Y: C = "1"
                self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C 
            
            if self.opx == 2: 
                C = register[0]
                register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + "0"
                self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C 
                  
            if self.opx == 1: 
                temp = register
                C = register[0]
                register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + self.F[7]
                self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C 
                            
            if self.opx == 0: 
                temp = register
                C = register[0]
                #register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + register[0]
                register = self.rotate(register[1] , register[2] , register[3] , register[4] , register[5] , register[6] , register[7] , register[0])
                self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C 
                self.debugline = "Here"
             
        if self.opy > 7:
            bit = 0
            if self.opx == 4: bit = 1
            if self.opx == 5: bit = 3
            if self.opx == 6: bit = 5
            if self.opx == 7: bit = 7
 
            if self.opx > 3 and self.opx < 8:
                notbit = not bool(int(register[7 - bit]))
                notbit = str(int(notbit))
                self.F = "0" + notbit + self.F[2] + "1" + self.F[4] + "0"  + "0" + self.F[7]
 
            if self.opx == 8: 
                register = register[0]  + register[1] + register[2] + register[3] + register[4] + register[5] +         "0" + register[7]  
                self.instrucitonname = "xxBITxx RES 1"
            if self.opx == 9: 
                register = register[0]  + register[1] + register[2] + register[3] +         "0" + register[5] + register[6] + register[7] 
                self.instructionname = "xxBITxx RES 3"
            if self.opx == 10: 
                register = register[0] + register[1] +         "0" + register[3] + register[4] + register[5] + register[6] + register[7] 
                self.instructionname = "xxBITxx RES 5"
            if self.opx == 11: 
                register = "0"         + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] 
                self.instructionname = "xxBITxx RES 7"
            
            if self.opx == 12: register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] +         "1" + register[7]  
            if self.opx == 13: register = register[0] + register[1] + register[2] + register[3] +         "1" + register[5] + register[6] + register[7] 
            if self.opx == 14: register = register[0] + register[1] +         "1" + register[3] + register[4] + register[5] + register[6] + register[7] 
            if self.opx == 15: register = "1"         + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] 

            if self.opx == 3: 
                C = register[7]
                register = "0" + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] 
                self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C 

            if self.opx == 2: 
                C = register[7]
                register = register[0] + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6]
                self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C 
 
            if self.opx == 1: 
                temp = register
                C = register[7]
                register = self.F[7] + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6]
                self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C 
 
            if self.opx == 0: 
                temp = register
                C = register[7] 
                register = register[7] + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6]
                self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C 
                    
        return register

    def scf(self):
        self.F = self.F[0] + self.F[1] + self.F[2] + "0" + self.F[4] + self.F[5] + "0" + "1"
        
    def neg(self,register):
        return 0 - register
 
    def singleand(self,register1,register2):
        return (register1 & register2)
 
    def singleor(self,register1,register2):
        return (register1 | register2)
 
    def rotate(self,bit0,bit1,bit2,bit3,bit4,bit5,bit6,bit7):
        return bit0 + bit1 + bit2 + bit3 + bit4 + bit5 + bit6 + bit7

    def singleload(self,bit0,bit1,bit2,bit3,bit4,bit5,bit6,bit7):
        return bit0 + bit1 + bit2 + bit3 + bit4 + bit5 + bit6 + bit7

    def setPC(self,addr):
        return addr

    def conditionalSetPC(self,addr,condition):
        if condition == "1": return addr
        else: return False

    def decNoFlags(self,number):
        number = number - 1
        if number < 0: number = number + 65536
        return number
 
    def incNoFlags(self,number):
        number = number + 1
        if number == 65536: number = 0
        return number
       
    def eightBitDecNoFlags(self,number):
        number = number - 1
        if number < 0: number = number +  256
        return number
 
    def checkFlag(self,condition):
        if condition == "1": return "1"
        else: return "0"

    def sixteenBitAddNoFlags(self,number1,number2):
        output = number1 + number2
        if output < 0: output = output + 65536
        if output > 65535: output = output - 65536
        return output
    
    def eightBitAddNoFlagsNotSigned(self,number1,number2):
        output = number1 + number2
        if output < 0: output = output + 256 
        if output > 255: output = output - 256
        return output
 
    def eightBitSubNoFlagsNotSigned(self,number1,number2):
        output = number1 - number2
        if output < 0: output = output + 256
        if output > 255: output = output - 256
        return output
 
    def eightBitSubNoFlags(self,number1,number2):
        output = number1 - number2
        return output

    def eightBitSubNoFlagsUnsigned(self,number1,number2):
        output = number1 - number2
        return output


    def setBoolValue(self,value):
        return value
