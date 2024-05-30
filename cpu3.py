import time
import curses
import os
import atexit
from threading import Timer,Thread,Event
import sys
from datetime import datetime
from z80 import z80
from q80 import q80
import signal

def signal_handler(signal, frame):
    global t
    t.cancel()
    curses.echo()
    curses.endwin()
    running = False
    exit(0)

    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#create emulated cpu
cpu = z80()

#create the Quantum CPU
qpu = q80()

#setup screen output
screen = curses.initscr()
curses.noecho()
screen.nodelay(1)
screen.keypad(1)
curses.start_color()
curses.init_pair(1,curses.COLOR_YELLOW,curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
curses.init_pair(4,curses.COLOR_MAGENTA,curses.COLOR_BLACK)

#make writing of machine code into ram easier
def opcodetoram(code):
    bitstring = "{0:08b}".format(int(code,16))
    BYTE = [bool(int(bitstring[7])),bool(int(bitstring[6])),bool(int(bitstring[5])),bool(int(bitstring[4])),bool(int(bitstring[3])),bool(int(bitstring[2])),bool(int(bitstring[1])),bool(int(bitstring[0]))]
    return BYTE



#************************************setup ram**********************************************************

eRAM = [] #Array for emulated CPUs RAM
qRAM = [] #Array for emulated CPU on a Quantum Computers RAM


def resetram():
    global qpu
    x = 0
    numberofbytes = 65536
    while x < numberofbytes:

        eRAM.append([False,False,False,False,False,False,False,False])
        qRAM.append([False,False,False,False,False,False,False,False])
        x = x + 1

   
    #if we have an input file read it into RAM else load a smaple program
    filename = ""
    address = 0
    if sys.argv[1:]:
        filename = sys.argv[1]
    
        file = open(filename,"rb")
        byte = file.read(1)
        while byte:
            number = int.from_bytes(byte,byteorder='big')
            line = format(int(number),'02x')
            line = line.upper()
            eRAM[address] = opcodetoram(line)
            qRAM[address] = opcodetoram(line)
            address = address + 1
            byte = file.read(1)
    
        file.close()
    else:

        #************************************Example program section**********************************************************


        #increment
        #qpu.QuantumExecute = "INC3"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("04") #with 04
        #eRAM[2] = opcodetoram("3c") #INC A
        #eRAM[3] = opcodetoram("f5") #PUSH AF
        #eRAM[4] = opcodetoram("76") #Halt
        
        #neg
        #qpu.QuantumExecute = "none"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("05") #with AA
        #eRAM[2] = opcodetoram("ed") #xx80xx
        #eRAM[3] = opcodetoram("7c") #NEG
        #eRAM[4] = opcodetoram("f5") #PUSH AF
        #eRAM[5] = opcodetoram("76") #Halt

        #decrement
        #qpu.QuantumExecute = "DEC2"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("07") #with 07
        #eRAM[2] = opcodetoram("3d") #DEC A
        #eRAM[3] = opcodetoram("76") #Halt

        #add
        #qpu.QuantumExecute = "ADD3"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("03") #with 02
        #eRAM[3] = opcodetoram("06") #LOAD B,
        #eRAM[4] = opcodetoram("02") #with 02
        #eRAM[5] = opcodetoram("80") #ADD A,B
        #eRAM[6] = opcodetoram("76") #Halt

        #sub
        #qpu.QuantumExecute = "SUB1"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("03") #with 15
        #eRAM[2] = opcodetoram("06") #LOAD B,
        #eRAM[3] = opcodetoram("02") #with 02
        #eRAM[4] = opcodetoram("90") #SUB B
        #eRAM[5] = opcodetoram("76") #Halt

        #and
        #qpu.QuantumExecute = "AND1"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("05") #with 05
        #eRAM[2] = opcodetoram("06") #LOAD B,
        #eRAM[3] = opcodetoram("04") #with 04
        #eRAM[4] = opcodetoram("a0") #AND A,B
        #eRAM[5] = opcodetoram("f5") #PUSH AF
        #eRAM[6] = opcodetoram("76") #Halt

        #or
        #qpu.QuantumExecute = "OR2"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("07") #with 07
        #eRAM[2] = opcodetoram("06") #LOAD B,
        #eRAM[3] = opcodetoram("07") #with 00
        #eRAM[4] = opcodetoram("b0") #OR A,B
        #eRAM[5] = opcodetoram("f5") #PUSH AF
        #eRAM[6] = opcodetoram("76") #Halt

        #xor
        #qpu.QuantumExecute = "XOR1"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("06") #with 06
        #eRAM[2] = opcodetoram("06") #LOAD B,
        #eRAM[3] = opcodetoram("02") #with 02
        #eRAM[4] = opcodetoram("a8") #XOR A,B
        #eRAM[5] = opcodetoram("f5") #PUSH AF
        #eRAM[6] = opcodetoram("76") #Halt

        #PUSH and POP
        #qpu.QuantumExecute = "XOR2"
        #eRAM[0] = opcodetoram("06") #LOAD B,
        #eRAM[1] = opcodetoram("BB") #with BB
        #eRAM[2] = opcodetoram("0e") #LOAD C,
        #eRAM[3] = opcodetoram("CC") #with CC
        #eRAM[4] = opcodetoram("c5") #PUSH BC
        #eRAM[5] = opcodetoram("06") #LOAD B,
        #eRAM[6] = opcodetoram("11") #with 11
        #eRAM[7] = opcodetoram("0e") #LOAD C,
        #eRAM[8] = opcodetoram("22") #with 22    
        #eRAM[9] = opcodetoram("C1") #POP BC 
        #eRAM[10] = opcodetoram("C5") #PUSH BC
        #eRAM[11] = opcodetoram("76") #Halt

        #EXX
        #qpu.QuantumExecute = "LOAD4"
        #eRAM[0] = opcodetoram("06") #LOAD B,
        #eRAM[1] = opcodetoram("BB") #with BB
        #eRAM[2] = opcodetoram("0e") #LOAD C,
        #eRAM[3] = opcodetoram("CC") #with CC
        #eRAM[4] = opcodetoram("16") #LOAD D,
        #eRAM[5] = opcodetoram("DD") #with DD
        #eRAM[6] = opcodetoram("1e") #LOAD E,
        #eRAM[7] = opcodetoram("EE") #with EE       
        #eRAM[8] = opcodetoram("D9") #EXX
        #eRAM[9] = opcodetoram("06") #LOAD B,
        #eRAM[10] = opcodetoram("22") #with 22
        #eRAM[11] = opcodetoram("0e") #LOAD C,
        #eRAM[12] = opcodetoram("33") #with 33
        #eRAM[13] = opcodetoram("16") #LOAD D,
        #eRAM[14] = opcodetoram("44") #with 44
        #eRAM[15] = opcodetoram("1e") #LOAD E,
        #eRAM[16] = opcodetoram("55") #with 55
        #eRAM[17] = opcodetoram("D9") #EXX
        #eRAM[18] = opcodetoram("c5") #PUSH BC
        #eRAM[19] = opcodetoram("d5") #PUSH DE
        #eRAM[20] = opcodetoram("76") #Halt

        #Res 
        #qpu.QuantumExecute = "SetResBit2"
        #eRAM[0] = opcodetoram("2e") #LOAD L,
        #eRAM[1] = opcodetoram("ff") #with ff
        #eRAM[2] = opcodetoram("cb") #Goto CB opcodes
        #eRAM[3] = opcodetoram("bd") #RES 7,L
        #eRAM[4] = opcodetoram("76") #Halt

        #SET / RES
        #qpu.QuantumExecute = "SetResBit2"
        #eRAM[0] = opcodetoram("06") #LOAD B,
        #eRAM[1] = opcodetoram("FF") #with FF
        #eRAM[2] = opcodetoram("0e") #LOAD C,
        #eRAM[3] = opcodetoram("00") #with 00
        #eRAM[4] = opcodetoram("cb") #Goto CB opcodes
        #eRAM[5] = opcodetoram("80") #RES 0,B
        #eRAM[6] = opcodetoram("cb") #Goto CB opcodes
        #eRAM[7] = opcodetoram("c1") #Set 0,C        
        #eRAM[8] = opcodetoram("C5") #PUSH BC
        #eRAM[9] = opcodetoram("76") #Halt
		
		#Bit
        qpu.QuantumExecute = "SetResBit1"
        eRAM[0] = opcodetoram("3e") #LOAD A,
        eRAM[1] = opcodetoram("ff") #with ff
        eRAM[2] = opcodetoram("cb") #Goto CB opcodes
        eRAM[3] = opcodetoram("87") #BIT A,0
        eRAM[4] = opcodetoram("F5") #PUSH AF
        eRAM[5] = opcodetoram("76") #Halt

        #SET DI
        #qpu.QuantumExecute = "LOAD3"
        #eRAM[0] = opcodetoram("f3") #LOAD A,
        
        #load
        #qpu.QuantumExecute = "LOAD3"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("26") #with 26
        #eRAM[2] = opcodetoram("76") #Halt

 
        #PUSH
        #qpu.QuantumExecute = "AddrBus2" #Or
        #qpu.QuantumExecute = "DataBus2" #Or
        #qpu.QuantumExecute = "DEC2"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("01") #with 01
        #eRAM[2] = opcodetoram("f5") #PUSH AF
        #eRAM[4] = opcodetoram("76") #Halt

        #POP
        #qpu.QuantumExecute = "LOAD2" #Or
        #qpu.QuantumExecute = "INC2"
        #eRAM[1] = opcodetoram("f1") #POP AF
        #eRAM[2] = opcodetoram("76") #Halt

        #Rotate
        #qpu.QuantumExecute = "ROT2"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("7f") #with 7f
        #eRAM[2] = opcodetoram("cb") #Goto CB opcodes
        #eRAM[3] = opcodetoram("27") #SLA A (slew left/rotate)
        #eRAM[4] = opcodetoram("76") #Halt
       
        #DAA
        #qpu.QuantumExecute = "SUB2" #Or
        #qpu.QuantumExecute = "ADD2" #Or
        #qpu.QuantumExecute = "LOAD2"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("01") #with 01
        #eRAM[2] = opcodetoram("3d") #DEC A (to set CNH flags)
        #eRAM[3] = opcodetoram("27") #DAA
        #eRAM[4] = opcodetoram("76") #Halt
          
        #Jump if
        #qpu.QuantumExecute = "LOAD3"
        #eRAM[0] = opcodetoram("37") #SCF
        #eRAM[1] = opcodetoram("da") #JP C,xx
        #eRAM[2] = opcodetoram("0f") #Jump to xx0a
        #eRAM[3] = opcodetoram("00") #Jump to 000a
        #eRAM[4] = opcodetoram("76") #Halt
        #eRAM[15] = opcodetoram("76") #Halt
        
        #CP
        #qpu.QuantumExecute = "CP3"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("07") #with 07
        #eRAM[2] = opcodetoram("06") #LOAD B,
        #eRAM[3] = opcodetoram("07") #with 07
        #eRAM[4] = opcodetoram("b8") #CP A,B
        #eRAM[5] = opcodetoram("F5") #PUSH AF
        #eRAM[6] = opcodetoram("76") #Halt

        #EX af, af1
        #qpu.QuantumExecute = "LOAD4"
        #eRAM[0] = opcodetoram("3e") #LOAD A,
        #eRAM[1] = opcodetoram("07") #with 07
        #eRAM[2] = opcodetoram("08") #EX af, af1
        #eRAM[3] = opcodetoram("76") #Halt 

 
        #CALL
        #qpu.QuantumExecute = "LOAD3"
        #eRAM[0] = opcodetoram("3e") #load A with
        #eRAM[1] = opcodetoram("18") #18
        #eRAM[2] = opcodetoram("CD") #CALL   
        #eRAM[3] = opcodetoram("0A") #0A
        #eRAM[4] = opcodetoram("00") #00
        #eRAM[5] = opcodetoram("F5") #PUSH AF
        #eRAM[6] = opcodetoram("76") #HALT        
        #eRAM[10] = opcodetoram("3c") #INC A
        #eRAM[11] = opcodetoram("c9") #RET
        

        #RLA, SLL, SRA etc
        #qpu.QuantumExecute = "DEC2"
        #eRAM[0] = opcodetoram("3f") #SCF
        #eRAM[1] = opcodetoram("06") #LOAD B,
        #eRAM[2] = opcodetoram("BB") #with BB
        #eRAM[3] = opcodetoram("0e") #LOAD C,
        #eRAM[4] = opcodetoram("CC") #with CC
        #eRAM[5] = opcodetoram("16") #LOAD D,
        #eRAM[6] = opcodetoram("DD") #with DD
        #eRAM[7] = opcodetoram("1e") #LOAD E,
        #eRAM[8] = opcodetoram("EE") #with EE         
        #eRAM[9] = opcodetoram("CB") #xxbitxx
        #eRAM[10] = opcodetoram("00") #rlc B  
        #eRAM[11] = opcodetoram("CB") #xxbitxx
        #eRAM[12] = opcodetoram("09") #rrc C  
        #eRAM[13] = opcodetoram("CB") #xxbitxx
        #eRAM[14] = opcodetoram("22") #sla D  
        #eRAM[15] = opcodetoram("CB") #xxbitxx
        #eRAM[16] = opcodetoram("2b") #sra E      
        #eRAM[17] = opcodetoram("C5") #PUSH BC
        #eRAM[18] = opcodetoram("D5") #PUSH DE
        #eRAM[19] = opcodetoram("76") #Halt




    x = 0
    numberofbytes = 65535 
    while x < numberofbytes:
        qRAM[x] = eRAM[x]
        x = x + 1

resetram()

def bool8str(d7,d6,d5,d4,d3,d2,d1,d0): #checking each bit is a little faster than typecasting to a sting
    line = ""
    if d7 == True: line = line + "1"
    else: line = line + "0"
    if d6 == True: line = line + "1"
    else: line = line + "0"
    if d5 == True: line = line + "1"
    else: line = line + "0"
    if d4 == True: line = line + "1"
    else: line = line + "0"
    if d3 == True: line = line + "1"
    else: line = line + "0"
    if d2 == True: line = line + "1"
    else: line = line + "0"
    if d1 == True: line = line + "1"
    else: line = line + "0"
    if d0 == True: line = line + "1"
    else: line = line + "0"
    return line

def bool16str(a15,a14,a13,a12,a11,a10,a9,a8,a7,a6,a5,a4,a3,a2,a1,a0):
    line = ""
    if a15 == True: line = line + "1"
    else: line = line + "0"
    if a14 == True: line = line + "1"
    else: line = line + "0"
    if a13 == True: line = line + "1"
    else: line = line + "0"
    if a12 == True: line = line + "1"
    else: line = line + "0"
    if a11 == True: line = line + "1"
    else: line = line + "0"
    if a10 == True: line = line + "1"
    else: line = line + "0"
    if a9 == True: line = line + "1"
    else: line = line + "0"
    if a8 == True: line = line + "1"
    else: line = line + "0"
    if a7 == True: line = line + "1"
    else: line = line + "0"
    if a6 == True: line = line + "1"
    else: line = line + "0"
    if a5 == True: line = line + "1"
    else: line = line + "0"
    if a4 == True: line = line + "1"
    else: line = line + "0"
    if a3 == True: line = line + "1"
    else: line = line + "0"
    if a2 == True: line = line + "1"
    else: line = line + "0"
    if a1 == True: line = line + "1"
    else: line = line + "0"
    if a0 == True: line = line + "1"
    else: line = line + "0"
    return line

def notoascii(number):
    letter = ""
   
    if number == 9: letter = "\t"
    #if number == 10: letter = "\r"
    if number == 13: letter = "\n"
    if number == 32: letter = " "
    if number == 33: letter = "!"
    if number == 34: letter = "\""
    if number == 35: letter = "#"
    if number == 36: letter = "$"
    if number == 37: letter = "%"
    if number == 38: letter = "&"
    if number == 39: letter = "'"
    if number == 40: letter = "("
    if number == 41: letter = ")"
    if number == 42: letter = "*"
    if number == 43: letter = "+"
    if number == 44: letter = ","
    if number == 45: letter = "-"
    if number == 46: letter = "."
    if number == 47: letter = "/"
    if number == 48: letter = "0"
    if number == 49: letter = "1"
    if number == 50: letter = "2"
    if number == 51: letter = "3"
    if number == 52: letter = "4"
    if number == 53: letter = "5"
    if number == 54: letter = "6"
    if number == 55: letter = "7"
    if number == 56: letter = "8"
    if number == 57: letter = "9"
    if number == 58: letter = ":"
    if number == 59: letter = ";"
    if number == 60: letter = "<"
    if number == 61: letter = "="
    if number == 62: letter = ">"
    if number == 63: letter = "?"
    if number == 64: letter = "@"
    if number == 65: letter = "A"
    if number == 66: letter = "B"
    if number == 67: letter = "C"
    if number == 68: letter = "D"
    if number == 69: letter = "E"
    if number == 70: letter = "F"
    if number == 71: letter = "G"
    if number == 72: letter = "H"
    if number == 73: letter = "I"
    if number == 74: letter = "J"
    if number == 75: letter = "K"
    if number == 76: letter = "L"
    if number == 77: letter = "M"
    if number == 78: letter = "N"
    if number == 79: letter = "O"
    if number == 80: letter = "P"
    if number == 81: letter = "Q"
    if number == 82: letter = "R"
    if number == 83: letter = "S"
    if number == 84: letter = "T"
    if number == 85: letter = "U"
    if number == 86: letter = "V"
    if number == 87: letter = "W"
    if number == 88: letter = "X"
    if number == 89: letter = "Y"
    if number == 90: letter = "Z"
    if number == 91: letter = "["
    if number == 92: letter = "\\"
    if number == 93: letter = "]"
    if number == 94: letter = "^"
    if number == 95: letter = "_"
    if number == 96: letter = "`"
    if number == 97: letter = "a"
    if number == 98: letter = "b"
    if number == 99: letter = "c"
    if number == 100: letter = "d"
    if number == 101: letter = "e"
    if number == 102: letter = "f"
    if number == 103: letter = "g"
    if number == 104: letter = "h"
    if number == 105: letter = "i"
    if number == 106: letter = "j"
    if number == 107: letter = "k"
    if number == 108: letter = "l"
    if number == 109: letter = "m"
    if number == 110: letter = "n"
    if number == 111: letter = "o"
    if number == 112: letter = "p"
    if number == 113: letter = "q"
    if number == 114: letter = "r"
    if number == 115: letter = "s"
    if number == 116: letter = "t"
    if number == 117: letter = "u"
    if number == 118: letter = "v"
    if number == 119: letter = "w"
    if number == 120: letter = "x"
    if number == 121: letter = "y"
    if number == 122: letter = "z"
    if number == 123: letter = "{"
    if number == 124: letter = "|"
    if number == 125: letter = "}"
    if number == 126: letter = "~"
    return letter

  
#******************************************setup the variables*********************************


updating = False
clock = True
ticks = 0
pause = False
ticklen = 0.001
running = True
elastaddrline = ""
qlastaddrline = ""
debugline = ""
memaddr = 0
viewoffset = 1000
cleanreset = False
syncdelay = 4
resetticks = 0
oldflagline = ""
olddebugline = ""
eoldoutputchar = ""
eConsoleline = []
eConsoleline.append("")
eConsoleline.append("")
eConsoleline.append("")
eConsoleline.append("")
eConsoleline.append("")
qoldoutputchar = ""
qConsoleline = []
qConsoleline.append("")
qConsoleline.append("")
qConsoleline.append("")
qConsoleline.append("")
qConsoleline.append("")
logfile = open("log.txt","w")
logfile.write("Ticks\tE-PC\tQ-PC\tE-OPC\tQ-OPC\tInstruction\n")
tic = ""
toc = ""
freq = "0"
ticcounter = 0
eConsoleno = 0
qConsoleno = 0
frame = 0
rframe = 10 
direction = ""
pwr = True
prd = True
qwr = True
qrd = True
halt = False
startTime = datetime.now()
endTime = "Running"

if sys.argv[1:]:
    frame = 16
    rframe = 20 

else:
    ticklen = 0.1
    rframe = 1
    viewoffset = 0






def getTerminalSize():
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

(screenWidth, screenHeight) = getTerminalSize()






while running == True:

        #*************************************dont render EVERY clock tick*******************************
        frame = frame + 1        
        if frame == rframe: screen.erase()

        #***********************************quick frequency hz counter***********************************
        if tic == "":
            tic = time.perf_counter()
        ticcounter = ticcounter + 1

        if ticcounter == rframe:
            toc = time.perf_counter()
            ticcounter = 0
            freq = str((1/( (toc - tic) / rframe )))
            freq = str(freq.partition('.')[0])
            tic = ""

        #******************check if were paused, if not alternate the clock pin***************************
        if pause == False:
            ticks = ticks + 1

        
        #**********************************Title**********************************************************
        line = "Intel 8080/Z80 - Traditional to Quantum emulation comparison"
        if sys.argv[1:]:
            if sys.argv[1] != "": 
                line = line + " (" + sys.argv[1] + ") (" + endTime + ")" 
           
                if halt == False:
                    if cpu.instructionname == "HALT":
                        halt = True
                        end = datetime.now() - startTime
                        endTime = "Complete " + str(end) + " seconds"

        if frame == rframe: 
            screen.addstr(0,17,line)
            screen.addstr(2,0,"Total clock ticks = " + str(ticks))
            screen.addstr(4,0,"**Traditionally Emuldated Z80**",curses.color_pair(2))
            screen.addstr(4,60,"**Z80 Emulated on a Quantum computer**",curses.color_pair(4))
 

        #********************************check the read write pins ********************************************  
 
 
        erd = int(cpu.RD)
        ewr = int(cpu.WR)
        if frame == rframe: screen.addstr(5,0,"Read = " + str(erd) + " Write = " + str(ewr))
        ebinaddr = bool16str(cpu.a15,cpu.a14,cpu.a13,cpu.a12,cpu.a11,cpu.a10,cpu.a9,cpu.a8,cpu.a7,cpu.a6,cpu.a5,cpu.a4,cpu.a3,cpu.a2,cpu.a1,cpu.a0)
        ehexaddr = format(int(ebinaddr,2),'04X')
        y = int(ehexaddr,16)

        qrd = int(qpu.RD)
        qwr = int(qpu.WR)
        if frame == rframe: screen.addstr(5,60,"Read = " + str(qrd) + " Write = " + str(qwr))
        qbinaddr = bool16str(qpu.a15,qpu.a14,qpu.a13,qpu.a12,qpu.a11,qpu.a10,qpu.a9,qpu.a8,qpu.a7,qpu.a6,qpu.a5,qpu.a4,qpu.a3,qpu.a2,qpu.a1,qpu.a0)
        qhexaddr = format(int(qbinaddr,2),'04X')
        qy = int(qhexaddr,16)

       
       
        
        if ewr == False:
            data = bool8str(cpu.d7,cpu.d6,cpu.d5,cpu.d4,cpu.d3,cpu.d2,cpu.d1,cpu.d0)
            eRAM[y] = [cpu.d0,cpu.d1,cpu.d2,cpu.d3,cpu.d4,cpu.d5,cpu.d6,cpu.d7]

         
        if erd == False:
            cpu.d0 = eRAM[y][0]
            cpu.d1 = eRAM[y][1]
            cpu.d2 = eRAM[y][2]
            cpu.d3 = eRAM[y][3]
            cpu.d4 = eRAM[y][4]
            cpu.d5 = eRAM[y][5]
            cpu.d6 = eRAM[y][6]
            cpu.d7 = eRAM[y][7]

        if qwr == False:
            qdata = bool8str(qpu.d7,qpu.d6,qpu.d5,qpu.d4,qpu.d3,qpu.d2,qpu.d1,qpu.d0)
            qRAM[qy] = [qpu.d0,qpu.d1,qpu.d2,qpu.d3,qpu.d4,qpu.d5,qpu.d6,qpu.d7]

         
        if qrd == False:
            qpu.d0 = qRAM[qy][0]
            qpu.d1 = qRAM[qy][1]
            qpu.d2 = qRAM[qy][2]
            qpu.d3 = qRAM[qy][3]
            qpu.d4 = qRAM[qy][4]
            qpu.d5 = qRAM[qy][5]
            qpu.d6 = qRAM[qy][6]
            qpu.d7 = qRAM[qy][7]


        if pause == False and syncdelay == 0:
            cpu.clock(True)
            qpu.clock(True)
        if syncdelay > 0: syncdelay = syncdelay - 1



        #****************************************Whats on the busses**************************************


       
        #Emulated Z80
        if frame == rframe:
            bindata = bool8str(cpu.d7,cpu.d6,cpu.d5,cpu.d4,cpu.d3,cpu.d2,cpu.d1,cpu.d0)
            hexdata = int(bindata,2)
            hexdata = format(hexdata,'02X')
            hexdata.rjust(4,'0')
            screen.addstr(6,0,"Data bus:" + bindata + " (" + hexdata + ")")
            if erd == False or ewr == False:#we until the emulated cpu is ready
                elastaddrline =  "Address bus:" + bool16str(cpu.a15,cpu.a14,cpu.a13,cpu.a12,cpu.a11,cpu.a10,cpu.a9,cpu.a8,cpu.a7,cpu.a6,cpu.a5,cpu.a4,cpu.a3,cpu.a2,cpu.a1,cpu.a0) + " (" + ehexaddr + ")"      
            screen.addstr(7,0,elastaddrline)

            bindata = bool8str(qpu.d7,qpu.d6,qpu.d5,qpu.d4,qpu.d3,qpu.d2,qpu.d1,qpu.d0)
            hexdata = int(bindata,2)
            hexdata = format(hexdata,'02X')
            hexdata.rjust(4,'0')
            screen.addstr(6,60,"Data bus:" + bindata + " (" + hexdata + ")")
            if qrd == False or qwr == False:#we until the emulated cpu is ready
                qlastaddrline =  "Address bus:" + bool16str(qpu.a15,qpu.a14,qpu.a13,qpu.a12,qpu.a11,qpu.a10,qpu.a9,qpu.a8,qpu.a7,qpu.a6,qpu.a5,qpu.a4,qpu.a3,qpu.a2,qpu.a1,qpu.a0) + " (" + qhexaddr + ")"      
            screen.addstr(7,60,qlastaddrline)




        #********************************************Show RAM********************************************

        if frame == rframe:
            screen.addstr(9,0,"Emulator RAM",curses.color_pair(2))
            screen.addstr(9,60,"Quantum Emulation RAM",curses.color_pair(4))
            x = viewoffset 
        
            while x < (viewoffset +16):

  

                #emulated RAM
                eramstring = bool8str(eRAM[x][7],eRAM[x][6],eRAM[x][5],eRAM[x][4],eRAM[x][3],eRAM[x][2],eRAM[x][1],eRAM[x][0])
                ehexramstring = format(int(eramstring,2),'02X')
                ezero_addr = str(x)
                ezero_addr = ezero_addr.zfill(5)
              
                if cpu.PC == x: screen.addstr((10+x)-viewoffset,29,"<- PC: " + cpu.instructionname ,curses.color_pair(2))
                screen.addstr((10+x)-viewoffset,0,"Address " + ezero_addr + ": " + eramstring + " (" + ehexramstring.upper() + ")")

                #Quantum emulation RAM
                qramstring = bool8str(qRAM[x][7],qRAM[x][6],qRAM[x][5],qRAM[x][4],qRAM[x][3],qRAM[x][2],qRAM[x][1],qRAM[x][0])
                qhexramstring = format(int(qramstring,2),'02X')
                qzero_addr = str(x)
                qzero_addr = qzero_addr.zfill(5)
              
                if qpu.PC == x: screen.addstr((10+x)-viewoffset,89,"<- PC: " + qpu.instructionname ,curses.color_pair(4))
                screen.addstr((10+x)-viewoffset,60,"Address " + qzero_addr + ": " + qramstring + " (" + qhexramstring.upper() + ")")
                x = x + 1


            
        #**********************************show a few lines of the srack************************************    
        if frame == rframe:
         
            y = 65535
            linecount = 28
            if frame == rframe: screen.addstr(27,0,"Emulator stack",curses.color_pair(2))
            while y > 65526:
                eramstring = bool8str(eRAM[y][7],eRAM[y][6],eRAM[y][5],eRAM[y][4],eRAM[y][3],eRAM[y][2],eRAM[y][1],eRAM[y][0])
                ehexramstring = format(int(eramstring,2),'02x')
                screen.addstr(linecount,0,"Address " + str(y) + ": " + eramstring + " (" + ehexramstring.upper() + ")")
                if y == cpu.SP: screen.addstr(linecount,29,"<- SP",curses.color_pair(2))
                y = y - 1
                linecount = linecount + 1

            y = 65535
            linecount = 28
            if frame == rframe: screen.addstr(27,60,"Quantum Emulation stack",curses.color_pair(4))
            while y > 65526:
                qramstring = bool8str(qRAM[y][7],qRAM[y][6],qRAM[y][5],qRAM[y][4],qRAM[y][3],qRAM[y][2],qRAM[y][1],qRAM[y][0])
                qhexramstring = format(int(qramstring,2),'02x')
                screen.addstr(linecount,60,"Address " + str(y) + ": " + qramstring + " (" + qhexramstring.upper() + ")")
                if y == qpu.SP: screen.addstr(linecount,89,"<- SP",curses.color_pair(4))
                y = y - 1
                linecount = linecount + 1


        #***********************************console output****************************************************
        
        echaracter = bool8str(eRAM[32][7],eRAM[32][6],eRAM[32][5],eRAM[32][4],eRAM[32][3],eRAM[32][2],eRAM[32][1],eRAM[32][0])
        
        if eoldoutputchar != echaracter:
            eoldoutputchar = echaracter

            if notoascii(int(echaracter,2)) != "\n": eConsoleline[eConsoleno] = eConsoleline[eConsoleno] + notoascii(int(echaracter,2))
            else:
                eConsoleno = eConsoleno + 1
                if eConsoleno == 5: 
                    eConsoleno = 4

                    eConsoleline[0] = eConsoleline[1]
                    eConsoleline[1] = eConsoleline[2]
                    eConsoleline[2] = eConsoleline[3]
                    eConsoleline[3] = eConsoleline[4]
                    eConsoleline[4] = ""

        if frame == rframe:
            screen.addstr(57,0,"Console output at 20h",curses.color_pair(2))
            screen.addstr(58,2,eConsoleline[0])
            screen.addstr(59,2,eConsoleline[1])
            screen.addstr(60,2,eConsoleline[2])
            screen.addstr(61,2,eConsoleline[3])
            screen.addstr(62,2,eConsoleline[4])
            screen.addstr(58,0,".")
            screen.addstr(59,0,".")
            screen.addstr(60,0,".")
            screen.addstr(61,0,".")
            screen.addstr(62,0,".")
 
        qcharacter = bool8str(qRAM[32][7],qRAM[32][6],qRAM[32][5],qRAM[32][4],qRAM[32][3],qRAM[32][2],qRAM[32][1],qRAM[32][0])
               
        if qoldoutputchar != qcharacter:
            qoldoutputchar = qcharacter

            if notoascii(int(qcharacter,2)) != "\n": qConsoleline[qConsoleno] = qConsoleline[qConsoleno] + notoascii(int(qcharacter,2))
            else:
                qConsoleno = qConsoleno + 1
                if qConsoleno == 5: 
                    qConsoleno = 4

                    qConsoleline[0] = qConsoleline[1]
                    qConsoleline[1] = qConsoleline[2]
                    qConsoleline[2] = qConsoleline[3]
                    qConsoleline[3] = qConsoleline[4]
                    qConsoleline[4] = ""

        if frame == rframe:
            screen.addstr(57,60,"Console output at 20h",curses.color_pair(4))
            screen.addstr(58,62,qConsoleline[0])
            screen.addstr(59,62,qConsoleline[1])
            screen.addstr(60,62,qConsoleline[2])
            screen.addstr(61,62,qConsoleline[3])
            screen.addstr(62,62,qConsoleline[4])
            screen.addstr(58,60,".")
            screen.addstr(59,60,".")
            screen.addstr(60,60,".")
            screen.addstr(61,60,".")
            screen.addstr(62,60,".")
       

        #************************************Emulated CPU details****************************************
        lineoffset = 38
        
        if frame == rframe:
            screen.addstr(lineoffset,0,"**Traditionally emulated Z80 details**",curses.color_pair(2))
            screen.addstr(lineoffset + 2,18,"SZ-H-PNC")
            screen.addstr(lineoffset + 3,0,"A = " + cpu.A + ", F = " + cpu.F)
            screen.addstr(lineoffset + 4,0,"BC = " + cpu.B + ":" + cpu.C)
            screen.addstr(lineoffset + 5,0,"DE = " + cpu.D + ":" + cpu.E)
            screen.addstr(lineoffset + 6,0,"HL = " + cpu.H + ":" + cpu.L)
            screen.addstr(lineoffset + 7,0,"IX = " + cpu.IX)
            screen.addstr(lineoffset + 8,0,"IY = " + cpu.IY)

            screen.addstr(lineoffset + 9,0,"SP = " + str(cpu.SP))
            screen.addstr(lineoffset + 10,0,"RD = " + str(erd) + ", WR = " + str(ewr) + " INT = " + str(int(cpu.interupts)))
            screen.addstr(lineoffset + 11,0,"Instruction = ")
            screen.addstr(lineoffset + 11,14, cpu.instructionname, curses.color_pair(2))
            screen.addstr(lineoffset + 12,0,"Instruction delay = " + str(cpu.delay))
            screen.addstr(lineoffset + 13,0,"Need more bits = " + str(cpu.needmorebits))
            screen.addstr(lineoffset + 14,0,"Ready to execute = " + str(cpu.execute))
            screen.addstr(lineoffset + 17,0,"Debug = ")
 
            screen.addstr(lineoffset + 16,0,"Emulated PC = ")
            screen.addstr(lineoffset + 16,14,str(cpu.PC),curses.color_pair(2))
            screen.addstr(lineoffset + 17,8,cpu.debugline, curses.color_pair(2))
 
            screen.addstr(lineoffset,60,"**Z80 Emulated on a Quantum computer details**",curses.color_pair(4))
            screen.addstr(lineoffset + 2,78,"SZ-H-PNC")
            screen.addstr(lineoffset + 3,60,"A = " + qpu.A + ", F = " + qpu.F)
            screen.addstr(lineoffset + 4,60,"BC = " + qpu.B + ":" + qpu.C)
            screen.addstr(lineoffset + 5,60,"DE = " + qpu.D + ":" + qpu.E)
            screen.addstr(lineoffset + 6,60,"HL = " + qpu.H + ":" + qpu.L)
            screen.addstr(lineoffset + 7,60,"IX = " + qpu.IX)
            screen.addstr(lineoffset + 8,60,"IY = " + qpu.IY)

            screen.addstr(lineoffset + 9,60,"SP = " + str(qpu.SP))
            screen.addstr(lineoffset + 10,60,"RD = " + str(qrd) + ", WR = " + str(qwr) + " INT = " + str(int(qpu.interupts)))
            screen.addstr(lineoffset + 11,60,"Instruction = ")
            screen.addstr(lineoffset + 11,74, qpu.instructionname, curses.color_pair(4))
            screen.addstr(lineoffset + 12,60,"Instruction delay = " + str(qpu.delay))
            screen.addstr(lineoffset + 13,60,"Need more bits = " + str(qpu.needmorebits))
            screen.addstr(lineoffset + 14,60,"Ready to execute = " + str(qpu.execute))
            screen.addstr(lineoffset + 17,60,"Debug = ")
 
            screen.addstr(lineoffset + 16,60,"PC on Quantum computer = ")
            screen.addstr(lineoffset + 16,85,str(qpu.PC),curses.color_pair(4))
            screen.addstr(lineoffset + 17,68,qpu.debugline, curses.color_pair(4))
       


            if cpu.PC != qpu.PC: screen.addstr(lineoffset + 16,132,"(Desynced)",curses.color_pair(3))

 
   

        #******************************************record instructions to log.txt***************************** 
        
       
                        
        if cpu.opcode != "" and qpu.opcode !="":
            newdebugline = str(ticks) + "\t" + str(cpu.PC) + "\t" + str(qpu.PC) + "\t" + format(int(cpu.opcode,2),'02x') + "\t" + format(int(qpu.opcode,2),'02X')   + "\t" + cpu.instructionname + "\n" 
            logfile.write(newdebugline)
       
        
       
        
       #*********************************************UI control*******************************************
        if frame == rframe: 
           input = screen.getch()
           if input == ord('r') or cleanreset == False: #reset must be active for at least 3 clock ticks
                resetticks = 0
                eRAM.clear()
                qRAM.clear()
                resetram()

                cpu.reset() # the emulated cpu doesnt need as much overhead
                cpu.d0 = eRAM[0][0]
                cpu.d1 = eRAM[0][1]
                cpu.d2 = eRAM[0][2]
                cpu.d3 = eRAM[0][3]
                cpu.d4 = eRAM[0][4]
                cpu.d5 = eRAM[0][5]
                cpu.d6 = eRAM[0][6]
                cpu.d7 = eRAM[0][7]

                qpu.reset() # the emulated cpu doesnt need as much overhead
                qpu.d0 = qRAM[0][0]
                qpu.d1 = qRAM[0][1]
                qpu.d2 = qRAM[0][2]
                qpu.d3 = qRAM[0][3]
                qpu.d4 = qRAM[0][4]
                qpu.d5 = qRAM[0][5]
                qpu.d6 = qRAM[0][6]
                qpu.d7 = qRAM[0][7]

                cleanreset = True
                syncdelay = 4
 
           if input == ord('q'): #quit
                curses.nocbreak()
                curses.echo()
                curses.endwin()
                running = False
                exit(0)



           #quick and easy way to scroll through ram
           if input == curses.KEY_DOWN:
                viewoffset = viewoffset + 16
                if viewoffset > 65535: viewoffset = (65535 - 16)

           if input == curses.KEY_UP:
                 viewoffset = viewoffset - 16
                 if viewoffset < 0: viewoffset = 0

           if input == curses.KEY_RIGHT:
                viewoffset = viewoffset + 1000
                if viewoffset > 65535: viewoffset = (65535 - 16)

           if input == curses.KEY_LEFT:
                viewoffset = viewoffset - 1000
                if viewoffset < 0: viewoffset = 0

        
           if input == ord('p'): pause = not pause
        
        
        if frame == rframe:
            if updating == False:
                screen.refresh()
                frame = 0

        #we dont really need a high/low tick delay as the GPIO slows execution down way more that 1hz of 4mhz 
        if not sys.argv[1:]: time.sleep(ticklen)
        cpu.clock(False)
        qpu.clock(False)


 
def exit_handler():#clean up of curses
    curses.endwin()
    os.system('stty sane')
    power.value = False
    logfile.close()
    exit(0)
atexit.register(exit_handler)


