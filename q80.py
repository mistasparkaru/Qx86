from z80 import z80
from qiskit import IBMQ,execute,Aer
#IBMQ.save_account('90bbd60a3b41bc1667c13c9fa2aa51579e2e84fe0ed2519b4c7b6668224afa557f98f39854ed06d041330acc367762b2ce01498992c69024e14ca9ad4a053b74')
import qiskit as q
import sys
IBMQ.load_account()
import math

provider = IBMQ.get_provider("ibm-q")
from qiskit.tools.monitor import job_monitor
import qiskit.providers.aer.noise as  noise
#backend = provider.get_backend("ibmq_ourense")

backend = provider.get_backend("ibmq_qasm_simulator")
#backend = provider.get_backend("ibmq_quito")
#backend = provider.get_backend("ibmq_belem")
#backend = provider.get_backend("simulator_extended_stabilizer")


from qiskit.visualization import plot_histogram
from matplotlib import style




class q80(z80):
    circuit0 = ""
    circuit1 = ""
    circuit2 = ""
    circuit3 = ""
    circuit4 = ""
    circuit5 = ""
    circuit6 = ""
    circuit7 = ""

    #QuantumExecute = "AND"
    #QuantumExecute = "XOR"
    #QuantumExecute = "OR"
    QuantumExecute = "INCx"
    #QuantumExecute = "ADD"
    #QuantumExecute = "SetResBit"
    #QuantumExecute = "DEC"
    #QuantumExecute = "SUBii"
    #QuantumExecute = "LOAD"
    #QuantumExecute = "16INC"
    #QuantumExecute = "16dec"
    #QuantumExecute = "addhl"
    #QuantumExecute = "sbchl"
    #QuantumExecute = "adchl"
    #QuantumExecute = "scf"
    #QuantumExecute = "neg"
    #QuantumExecute = "rot"
    #QuantumExecute = "loadhlr"
    #QuantumExecute = "LOAD2" #including PUSH, POP CALL and RET
    #QuantumExecute = "LOAD3"
    #QuantumExecute = "CP"
    #QuantumExecute = "JUMP" 

    def myif(self,inputA):
        inputA = int(inputA) * math.pi

        circuit = q.QuantumCircuit(2,2)
        circuit.ry(inputA,0)
        circuit.cx(0,1)
        circuit.measure(0,0)
        circuit.measure(1,1)
        circuitText = str(circuit)
        self.circuit0 = "Executing a Quantum IF circuit on " + str(backend) + " with the input " + str(inputA)
        self.circuit1 = circuitText

        shots = 2000
        job = q.execute(circuit, backend=backend, shots=shots, memory=True)
        
        f = open("qlog.txt","w")  
        job_monitor(job,output=f)
        f.close()
        
        result = job.result()

        memory = result.get_memory(circuit)
        qubit0 = 0
        qubit1 = 0

        for result in memory:
            qubit0 = qubit0 + int(result[0])
            qubit1 = qubit1 + int(result[1])

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots

        return int(qubit1)

    def setbit(self,bit):
        inputA = bit * math.pi

        circuit = q.QuantumCircuit(1,1)
        circuit.ry(inputA,0)
        circuit.measure(0,0)
        circuitText = str(circuit)
        self.circuit0 = "Executing a Quantum SET/Latch circuit on " + str(backend) + " with the input " + str(bit)
        self.circuit1 = circuitText
   
        shots = 2000
        job = q.execute(circuit, backend=backend, shots=shots, memory=True)
        
        f = open("qlog.txt","w")  
        job_monitor(job, output=f)
        f.close()
 
        result = job.result()

        memory = result.get_memory(circuit)
        qubit0 = 0

        for result in memory:
           qubit0 = qubit0 + int(result[0])

        qubit0 = qubit0/shots

        return int(round(qubit0))

    def fourbitset(self,bits):
        inputA = int(bits[0]) * math.pi
        inputB = int(bits[1]) * math.pi
        inputC = int(bits[2]) * math.pi
        inputD = int(bits[3]) * math.pi

        circuit = q.QuantumCircuit(4,4)
        circuit.ry(inputA,0)
        circuit.ry(inputB,1)
        circuit.ry(inputC,2)
        circuit.ry(inputD,3)
        circuit.measure(0,0)
        circuit.measure(1,1)
        circuit.measure(2,2)
        circuit.measure(3,3)
        circuitText = str(circuit)
        self.circuit0 = "Executing a Quantum 4bit SET/Latch circuit on " + str(backend) + " with the input " + str(bits)
        self.circuit1 = circuitText

        shots = 2000
        job = q.execute(circuit, backend=backend, shots=shots, memory=True)
        
        f = open("qlog.txt","w")  
        job_monitor(job,output=f)
        f.close()

        result = job.result()

        memory = result.get_memory(circuit)
        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0

        for result in memory:
           qubit0 = qubit0 + int(result[0])
           qubit1 = qubit1 + int(result[1])
           qubit2 = qubit2 + int(result[2])
           qubit3 = qubit3 + int(result[3])

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots

        return str(int(round(qubit3))) + str(int(round(qubit2))) + str(int(round(qubit1))) + str(int(round(qubit0))) 

    #def bitset(self,bit):

    #    inputA = bits * math.pi

    #    circuit = q.QuantumCircuit(1,1)
    #    circuit.ry(inputA,0)

    #    circuit.measure(0,0)
 
    #    shots = 2000
    #    job = q.execute(circuit, backend=backend, shots=shots, memory=True)
    #    job_monitor(job)
    #    result = job.result()

    #    memory = result.get_memory(circuit)

    #    qubit0 = 0

    #    for result in memory:
    #       qubit2 = qubit2 + int(result[2])
    #       qubit3 = qubit3 + int(result[3])

    #    qubit0 = qubit0/shots
    #    qubit1 = qubit1/shots
    #    qubit2 = qubit2/shots
    #    qubit3 = qubit3/shots

    #    return str(int(round(qubit3))) + str(int(round(qubit2))) + str(int(round(qubit1))) + str(int(round(qubit0))) 

    def bitset(self,bit):
        inputA = bits * math.pi

        circuit = q.QuantumCircuit(1,1)
        circuit.ry(inputA,0)
        circuit.measure(0,0)
        circuitText = str(circuit)
        self.circuit0 = "Executing a Quantum SET/Latch circuit on " + str(backend) + " with the input " + str(inputA)
        self.circuit1 = circuitText

        shots = 2000
        job = q.execute(circuit, backend=backend, shots=shots, memory=True)
        
        f = open("qlog.txt","w")  
        job_monitor(job,output=f)
        f.close()

       
        
        result = job.result()

        memory = result.get_memory(circuit)
        qubit0 = 0

        for result in memory:
           qubit0 = qubit0 + int(result[0])

        qubit0 = qubit0/shots

        return str(int(round(qubit0)))

    def myand(self,inputA,inputB):

       inputA = inputA * math.pi
       inputB = inputB * math.pi

       circuit = q.QuantumCircuit(3,3)
       circuit.ry(inputA,0)
       circuit.ry(inputB,1)
       circuit.ccx(0,1,2)
       circuit.measure(0,0)
       circuit.measure(1,1)
       circuit.measure(2,2)
       circuitText = str(circuit)
       self.circuit0 = "Executing a Quantum AND circuit on " + str(backend) + " with the input " + str(inputA) + " and " + str(inputB)
       self.circuit1 = circuitText

       shots = 2000
       job = q.execute(circuit, backend=backend, shots=shots, memory=True)
       
       f = open("qlog.txt","w")  
       job_monitor(job,output=f)
       f.close()

      
       result = job.result()

       memory = result.get_memory(circuit)
       qubit0 = 0
       qubit1 = 0
       qubit2 = 0

       for result in memory:
          qubit0 = qubit0 + int(result[0])
          qubit1 = qubit1 + int(result[1])
          qubit2 = qubit2 + int(result[2])

       qubit0 = qubit0/shots
       qubit1 = qubit1/shots
       qubit2 = qubit2/shots

       return int(round(qubit0))
    
    def mynot(self,inputA):
        inputA = inputA * math.pi

        circuit = q.QuantumCircuit(1,1)
        circuit.ry(inputA,0)
        circuit.x(0)
        circuit.measure(0,0)
        circuitText = str(circuit)
        self.circuit0 = "Executing a Quantum NOT circuit on " + str(backend) + " with the input " + str(inputA)
        self.circuit1 = circuitText

        shots = 2000
        job = q.execute(circuit, backend=backend, shots=shots, memory=True)
        
        f = open("qlog.txt","w")  
        job_monitor(job,output=f)
        f.close()

         
        result = job.result()

        memory = result.get_memory(circuit)
        qubit0 = 0

        for result in memory:
            qubit0 = qubit0 + int(result[0])

        qubit0 = qubit0/shots

        return int(round(qubit0))


    def eightbitand(self,register):

        if self.QuantumExecute != "AND":
            self.debugline = "Normal operation"
            A = int(self.A,2)
            andwith = int(register,2)
            anded = bin(A & andwith)[2:].zfill(8)
        else:
            anded = ""
            anded = anded + str(self.myand(int(self.A[0]),int(register[0]))) 
            anded = anded + str(self.myand(int(self.A[1]),int(register[1]))) 
            anded = anded + str(self.myand(int(self.A[2]),int(register[2]))) 
            anded = anded + str(self.myand(int(self.A[3]),int(register[3]))) 
            anded = anded + str(self.myand(int(self.A[4]),int(register[4]))) 
            anded = anded + str(self.myand(int(self.A[5]),int(register[5]))) 
            anded = anded + str(self.myand(int(self.A[6]),int(register[6]))) 
            anded = anded + str(self.myand(int(self.A[7]),int(register[7]))) 

        #set flags
        self.F = anded[0] + self.getZflag(anded) + anded[2] + "1" + anded[4] + self.getparity(anded) + "0" + "0"
        self.clearop()
        self.delay =  1

        return anded

    def singleand(self,register1,register2):
        if self.QuantumExecute != "AND":
            self.debugline = "Normal operation"
            return (register1 & register2)
        else:
            self.debugline = "Quantum operation"
            register1 = str(bin(register1)[2:].zfill(8))
            register2 = str(bin(register2)[2:].zfill(8))
            anded = ""
            anded = anded + str(self.myand(int(register1[0]),int(register2[0]))) 
            anded = anded + str(self.myand(int(register1[1]),int(register2[1]))) 
            anded = anded + str(self.myand(int(register1[2]),int(register2[2]))) 
            anded = anded + str(self.myand(int(register1[3]),int(register2[3]))) 
            anded = anded + str(self.myand(int(register1[4]),int(register2[4]))) 
            anded = anded + str(self.myand(int(register1[5]),int(register2[5]))) 
            anded = anded + str(self.myand(int(register1[6]),int(register2[6]))) 
            anded = anded + str(self.myand(int(register1[7]),int(register2[7]))) 

            return int(anded,2)

    def singleor(self,register1,register2):
        if self.QuantumExecute != "OR":
            self.debugline = "Normal operation"
            return (register1 & register2)
        else:
            self.debugline = "Quantum operation"
            register1 = str(bin(register1)[2:].zfill(8))
            register2 = str(bin(register2)[2:].zfill(8))
            ored = ""
            ored = ored + str(self.myor(int(register1[0]),int(register2[0]))) 
            ored = ored + str(self.myor(int(register1[1]),int(register2[1]))) 
            ored = ored + str(self.myor(int(register1[2]),int(register2[2]))) 
            ored = ored + str(self.myor(int(register1[3]),int(register2[3]))) 
            ored = ored + str(self.myor(int(register1[4]),int(register2[4]))) 
            ored = ored + str(self.myor(int(register1[5]),int(register2[5]))) 
            ored = ored + str(self.myor(int(register1[6]),int(register2[6]))) 
            ored = ored + str(self.myor(int(register1[7]),int(register2[7]))) 

            return int(ored,2)

    def myxor(self,inputA,inputB):

        inputA = inputA * math.pi
        inputB = inputB * math.pi

        circuit = q.QuantumCircuit(2,2)
        circuit.ry(inputA,0)
        circuit.ry(inputB,1)
        circuit.cx(0,1)
        circuit.measure(0,0)
        circuit.measure(1,1)
        circuitText = str(circuit)
        self.circuit0 = "Executing a Quantum XOR circuit on " + str(backend) + " with the input " + str(inputA) + " and " + str(inputB)
        self.circuit1 = circuitText

        shots=2000
        job = q.execute(circuit, backend=backend, shots=shots, memory=True)
        
        f = open("qlog.txt","w")  
        job_monitor(job,output=f)
        f.close()

       
        result = job.result()

        memory = result.get_memory(circuit)
        qubit0 = 0
        qubit1 = 0

        for result in memory:
            qubit0 = qubit0 + int(result[0])
            qubit1 = qubit1 + int(result[1])

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots

        return int(round(qubit0))
             
    def eightbitxor(self,register):

        if self.QuantumExecute != "XOR":
            self.debugline = "Normal operation"
            A = int(self.A,2)
            xorwith = int(register,2)
            xored = bin(A ^ xorwith)[2:].zfill(8)
        else:
            xored = ""
            xored = xored + str(self.myxor(int(self.A[0]),int(register[0])))
            xored = xored + str(self.myxor(int(self.A[1]),int(register[1])))
            xored = xored + str(self.myxor(int(self.A[2]),int(register[2])))
            xored = xored + str(self.myxor(int(self.A[3]),int(register[3])))
            xored = xored + str(self.myxor(int(self.A[4]),int(register[4])))
            xored = xored + str(self.myxor(int(self.A[5]),int(register[5])))
            xored = xored + str(self.myxor(int(self.A[6]),int(register[6])))
            xored = xored + str(self.myxor(int(self.A[7]),int(register[7])))

        #set flags
        self.F = xored[0] + self.getZflag(xored) + xored[2] + "0" + xored[4] + self.getparity(xored) + "0" + "0"
        self.clearop()
        self.delay =  1

        return xored   

    def myor(self,inputA,inputB):

        inputA = inputA * math.pi
        inputB = inputB * math.pi

        circuit = q.QuantumCircuit(4,4)
        circuit.ry(inputA,0)
        circuit.ry(inputB,2)
        circuit.cx(0,1)
        circuit.cx(2,1)
        circuit.cx(2,3)
        circuit.ccx(1,0,3)
        circuit.measure(0,0)
        circuit.measure(1,1)
        circuit.measure(2,2)
        circuit.measure(3,3)
        circuitText = str(circuit)
        self.circuit0 = "Executing a Quantum OR circuit on " + str(backend) + " with the input " + str(inputA) + " and " + str(inputB)
        self.circuit1 = circuitText

        shots = 2000
        job = q.execute(circuit, backend=backend, shots=shots, memory=True)
        
        f = open("qlog.txt","w")  
        job_monitor(job,output=f)
        f.close()

       
        result = job.result()

        memory = result.get_memory(circuit)
        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0

        for result in memory:
            qubit0 = qubit0 + int(result[0])
            qubit1 = qubit1 + int(result[1])
            qubit2 = qubit2 + int(result[2])
            qubit3 = qubit3 + int(result[3])

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots

        return int(round(qubit0))

    def eightbitor(self,register):

        if self.QuantumExecute != "OR":
            self.debugline = "Normal operation"
            A = int(self.A,2)
            oredwith = int(register,2)
            ored = bin(A | oredwith)[2:].zfill(8)
        else:
            ored = ""
            ored = ored + str(self.myor(int(self.A[0]),int(register[0])))
            ored = ored + str(self.myor(int(self.A[1]),int(register[1])))
            ored = ored + str(self.myor(int(self.A[2]),int(register[2])))
            ored = ored + str(self.myor(int(self.A[3]),int(register[3])))
            ored = ored + str(self.myor(int(self.A[4]),int(register[4])))
            ored = ored + str(self.myor(int(self.A[5]),int(register[5])))
            ored = ored + str(self.myor(int(self.A[6]),int(register[6])))
            ored = ored + str(self.myor(int(self.A[7]),int(register[7])))

        #set flags
        self.F = ored[0] + self.getZflag(ored) + ored[2] + "0" + ored[4] + self.getparity(ored) + "0" + "0"
        self.clearop()
        self.delay =  1

        return ored

    def eightbitinc(self,register):
        if self.QuantumExecute != "INC":
            self.debugline = "Normal operation"
            x = int(register,2)
            x = x + 1 

            if x == 256: x = 0
            register = format(x, '08b')
        else:
            inputA = register
            inputA = inputA[::-1]

            temp = ""
            output0 = str(self.myxor(1,int(inputA[0])))
            temp = str(self.myand(1,int(inputA[0])))
            output1 = str(self.myxor(int(temp),int(inputA[1])))
            temp = str(self.myand(int(temp),int(inputA[1])))
            output2 = str(self.myxor(int(temp),int(inputA[2])))
            temp = str(self.myand(int(temp),int(inputA[2])))
            output3 = str(self.myxor(int(temp),int(inputA[3])))
            temp = str(self.myand(int(temp),int(inputA[3])))
            output4 = str(self.myxor(int(temp),int(inputA[4])))
            temp = str(self.myand(int(temp),int(inputA[4])))
            output5 = str(self.myxor(int(temp),int(inputA[5])))
            temp = str(self.myand(int(temp),int(inputA[5])))
            output6 = str(self.myxor(int(temp),int(inputA[6])))
            temp = str(self.myand(int(temp),int(inputA[6])))
            output7 = str(self.myxor(int(temp),int(inputA[7])))
            temp = str(self.myand(int(temp),int(inputA[7])))
            register = output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0

        self.clearop()
        self.delay = 1

        #Set flags
        H = "0"
        P = "0"
        N = self.F[6]
        C = self.F[7]
        if register  == "10000000": P = "1"
        if register[7] == "0" and register[6] == "0" and register[5] == "0" and register[4] == "0": H = "1"
        self.F = register[0] + self.getZflag(register) + register[2] + H + register[4] + P + "0" + C

        return register
     
    def eightBitDecNoFlags(self,register):
        if self.QuantumExecute != "DECi":
            self.debugline = "Normal operation"
            x = register
            x = x - 1
            if x == -1: x = 255
            return x
        else:
            self.debufline = "Quantum opeation"
            inputA = format(register,'08b')
            inputA = inputA[::-1]

            carry = "0"
            xor0 = str(self.myxor(1,int(inputA[0])))
            and0 = str(self.myand(1,int(inputA[0])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output0 = xor1

            xor0 = str(self.myxor(1,int(inputA[1])))
            and0 = str(self.myand(1,int(inputA[1])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output1 = xor1

            xor0 = str(self.myxor(1,int(inputA[2])))
            and0 = str(self.myand(1,int(inputA[2])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output2 = xor1

            xor0 = str(self.myxor(1,int(inputA[3])))
            and0 = str(self.myand(1,int(inputA[3])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output3 = xor1

            xor0 = str(self.myxor(1,int(inputA[4])))
            and0 = str(self.myand(1,int(inputA[4])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output4 = xor1

            xor0 = str(self.myxor(1,int(inputA[5])))
            and0 = str(self.myand(1,int(inputA[5])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output5 = xor1

            xor0 = str(self.myxor(1,int(inputA[6])))
            and0 = str(self.myand(1,int(inputA[6])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output6 = xor1

            xor0 = str(self.myxor(1,int(inputA[7])))
            and0 = str(self.myand(1,int(inputA[7])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output7 = xor1

            register = output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0
            return int(register,2)


    def eightBitIncNoFlags(self,register):
        if self.QuantumExecute != "INCi":
            self.debugline = "Normal operation"
            x = register
            x = x + 1 

            if x == 256: x = 0
            return x 
        else:
            inputA = format(register,'08b')
            inputA = inputA[::-1]

            temp = ""
            output0 = str(self.myxor(1,int(inputA[0])))
            temp = str(self.myand(1,int(inputA[0])))
            output1 = str(self.myxor(int(temp),int(inputA[1])))
            temp = str(self.myand(int(temp),int(inputA[1])))
            output2 = str(self.myxor(int(temp),int(inputA[2])))
            temp = str(self.myand(int(temp),int(inputA[2])))
            output3 = str(self.myxor(int(temp),int(inputA[3])))
            temp = str(self.myand(int(temp),int(inputA[3])))
            output4 = str(self.myxor(int(temp),int(inputA[4])))
            temp = str(self.myand(int(temp),int(inputA[4])))
            output5 = str(self.myxor(int(temp),int(inputA[5])))
            temp = str(self.myand(int(temp),int(inputA[5])))
            output6 = str(self.myxor(int(temp),int(inputA[6])))
            temp = str(self.myand(int(temp),int(inputA[6])))
            output7 = str(self.myxor(int(temp),int(inputA[7])))
            temp = str(self.myand(int(temp),int(inputA[7])))
            register = output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0
            return int(register,2)


    def sixteenbitinc(self,register1,register2):
        if self.opcode == "00110011":
            rr = int(format(self.SP,'016b'),2)
        else:
            rr = int(register1 + register2,2)
        if self.opcode == "00100011" and self.preopcode == "11011101":
            rr = int(self.IX,2)
        if self.opcode == "00100011" and self.preopcode == "11111101":
            rr = int(self.IY,2)

        if self.QuantumExecute != "16INC":
            self.debugline = "Normal operation"
            rr = rr + 1
            if rr > 65535:
                rr = rr - 65536
            total = format(rr, '016b')
        else:
            self.debugline = "Quantum operation"
            inputA = format(rr, '016b')
            inputA = inputA[::-1]

            temp = ""

            output0 = str(self.myxor(1,int(inputA[0])))
            temp = str(self.myand(1,int(inputA[0])))
            output1 = str(self.myxor(int(temp),int(inputA[1])))
            temp = str(self.myand(int(temp),int(inputA[1])))
            output2 = str(self.myxor(int(temp),int(inputA[2])))
            temp = str(self.myand(int(temp),int(inputA[2])))
            output3 = str(self.myxor(int(temp),int(inputA[3])))
            temp = str(self.myand(int(temp),int(inputA[3])))
            output4 = str(self.myxor(int(temp),int(inputA[4])))
            temp = str(self.myand(int(temp),int(inputA[4])))
            output5 = str(self.myxor(int(temp),int(inputA[5])))
            temp = str(self.myand(int(temp),int(inputA[5])))
            output6 = str(self.myxor(int(temp),int(inputA[6])))
            temp = str(self.myand(int(temp),int(inputA[6])))
            output7 = str(self.myxor(int(temp),int(inputA[7])))
            temp = str(self.myand(int(temp),int(inputA[7])))
            output8 = str(self.myxor(int(temp),int(inputA[8])))
            temp = str(self.myand(int(temp),int(inputA[8])))
            output9 = str(self.myxor(int(temp),int(inputA[9])))
            temp = str(self.myand(int(temp),int(inputA[9])))
            output10 = str(self.myxor(int(temp),int(inputA[10])))
            temp = str(self.myand(int(temp),int(inputA[10])))
            output11 = str(self.myxor(int(temp),int(inputA[11])))
            temp = str(self.myand(int(temp),int(inputA[11])))
            output12 = str(self.myxor(int(temp),int(inputA[12])))
            temp = str(self.myand(int(temp),int(inputA[12])))
            output13 = str(self.myxor(int(temp),int(inputA[13])))
            temp = str(self.myand(int(temp),int(inputA[13])))
            output14 = str(self.myxor(int(temp),int(inputA[14])))
            temp = str(self.myand(int(temp),int(inputA[14])))
            output15 = str(self.myxor(int(temp),int(inputA[15])))
            temp = str(self.myand(int(temp),int(inputA[15])))

            register = output15 + output14 + output13 + output12 + output11 + output10 + output9 + output8 + output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0

            total = register

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
            self.SP = str(int(total,2))

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

        if self.QuantumExecute != "16dec":
            self.debugline = "Normal operation"
            rr = rr - 1
            if rr < 0:
               rr = rr + 65536
            total = format(rr, '016b')
        else:
            self.debugline = "Quantum operation"
            inputA = format(rr, '016b')
            inputA = inputA[::-1]

            temp = ""

            carry = "0"
            xor0 = str(self.myxor(1,int(inputA[0])))
            and0 = str(self.myand(1,int(inputA[0])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output0 = xor1

            xor0 = str(self.myxor(1,int(inputA[1])))
            and0 = str(self.myand(1,int(inputA[1])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output1 = xor1

            xor0 = str(self.myxor(1,int(inputA[2])))
            and0 = str(self.myand(1,int(inputA[2])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output2 = xor1

            xor0 = str(self.myxor(1,int(inputA[3])))
            and0 = str(self.myand(1,int(inputA[3])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output3 = xor1

            xor0 = str(self.myxor(1,int(inputA[4])))
            and0 = str(self.myand(1,int(inputA[4])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output4 = xor1

            xor0 = str(self.myxor(1,int(inputA[5])))
            and0 = str(self.myand(1,int(inputA[5])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output5 = xor1

            xor0 = str(self.myxor(1,int(inputA[6])))
            and0 = str(self.myand(1,int(inputA[6])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output6 = xor1

            xor0 = str(self.myxor(1,int(inputA[7])))
            and0 = str(self.myand(1,int(inputA[7])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output7 = xor1

            xor0 = str(self.myxor(1,int(inputA[8])))
            and0 = str(self.myand(1,int(inputA[8])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output8 = xor1

            xor0 = str(self.myxor(1,int(inputA[9])))
            and0 = str(self.myand(1,int(inputA[9])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output9 = xor1

            xor0 = str(self.myxor(1,int(inputA[10])))
            and0 = str(self.myand(1,int(inputA[10])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output10 = xor1

            xor0 = str(self.myxor(1,int(inputA[11])))
            and0 = str(self.myand(1,int(inputA[11])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output11 = xor1

            xor0 = str(self.myxor(1,int(inputA[12])))
            and0 = str(self.myand(1,int(inputA[12])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output12 = xor1

            xor0 = str(self.myxor(1,int(inputA[13])))
            and0 = str(self.myand(1,int(inputA[13])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output13 = xor1

            xor0 = str(self.myxor(1,int(inputA[14])))
            and0 = str(self.myand(1,int(inputA[14])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output14 = xor1

            xor0 = str(self.myxor(1,int(inputA[15])))
            and0 = str(self.myand(1,int(inputA[15])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output15 = xor1

            register = output15 + output14 + output13 + output12 + output11 + output10 + output9 + output8 + output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0
            total = register

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
            self.SP = str(int(total,2))
        if self.opcode == "00101011" and self.preopcode == "11011101":
            self.IX = r1 + r2
        if self.opcode == "00101011" and self.preopcode == "11111101":
            self.IY = r1 + r2

        self.clearop()
        self.delay = 1

    def eightbitdec(self,register):
        if self.QuantumExecute != "DEC":
            self.debugline = "Normal operation"
            x = int(register,2)
            x = x - 1
            if x == -1: x = 255
            register = format(x, '08b')
        else:
            self.debufline = "Quantum opeation"
            inputA = register[::-1]

            carry = "0"
            xor0 = str(self.myxor(1,int(inputA[0])))
            and0 = str(self.myand(1,int(inputA[0])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output0 = xor1

            xor0 = str(self.myxor(1,int(inputA[1])))
            and0 = str(self.myand(1,int(inputA[1])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output1 = xor1

            xor0 = str(self.myxor(1,int(inputA[2])))
            and0 = str(self.myand(1,int(inputA[2])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output2 = xor1

            xor0 = str(self.myxor(1,int(inputA[3])))
            and0 = str(self.myand(1,int(inputA[3])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output3 = xor1

            xor0 = str(self.myxor(1,int(inputA[4])))
            and0 = str(self.myand(1,int(inputA[4])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output4 = xor1

            xor0 = str(self.myxor(1,int(inputA[5])))
            and0 = str(self.myand(1,int(inputA[5])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output5 = xor1

            xor0 = str(self.myxor(1,int(inputA[6])))
            and0 = str(self.myand(1,int(inputA[6])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output6 = xor1

            xor0 = str(self.myxor(1,int(inputA[7])))
            and0 = str(self.myand(1,int(inputA[7])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output7 = xor1

            register = output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0

        self.clearop()
        self.delay = 1

        #set flags
        H = "0"
        if register[7] == "1" and register[6] == "1" and register[5] == "1" and register[4] == "1": H = "1"
        P = "0"
        if register == "01111111": P = "1"
        self.F = register[0] + self.getZflag(register) + register[2] + H + register[4] + P + "1" + self.F[7]

        return register


    def eightbitsub(self,register):
        A = int(self.A,2)
        B = int(register,2)

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

        if self.QuantumExecute != "SUB":
            sub = (A - B) - minus
            self.debugline = "Normal operation"
            C = "0"
            P = "0"
            if sub < 0:
                sub = sub  + 256
                C = "1"
            sub = format(sub, '08b')
        
        else:
            self.debugline = "Quantum operation"
            inputA = self.A
            inputB = register
            inputA = inputA[::-1]
            inputB = inputB[::-1]

            temp = ""
            borrow = str(minus)

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            not1 = str(self.mynot(int(inputA[0])))
            and1 = str(self.myand(int(not1),int(inputB[0])))
            output0 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            not1 = str(self.mynot(int(inputA[1])))
            and1 = str(self.myand(int(not1),int(inputB[1])))
            output1 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            not1 = str(self.mynot(int(inputA[2])))
            and1 = str(self.myand(int(not1),int(inputB[2])))
            output2 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            not1 = str(self.mynot(int(inputA[3])))
            and1 = str(self.myand(int(not1),int(inputB[3])))
            output3 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            not1 = str(self.mynot(int(inputA[4])))
            and1 = str(self.myand(int(not1),int(inputB[4])))
            output4 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            not1 = str(self.mynot(int(inputA[5])))
            and1 = str(self.myand(int(not1),int(inputB[5])))
            output5 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            not1 = str(self.mynot(int(inputA[6])))
            and1 = str(self.myand(int(not1),int(inputB[6])))
            output6 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            not1 = str(self.mynot(int(inputA[7])))
            and1 = str(self.myand(int(not1),int(inputB[7])))
            output7 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
 
            sub = int(output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)

            C = borrow
            P = "0"
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
 
        C = "0"
        
        if self.QuantumExecute != "ADD":
            total = A + (B + addition)
            self.debugline = "Normal operation"
            if total > 255:
                total = total - 256
                C = "1"

           
        else:
            inputA = self.A
            inputB = register
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            

            carry = str(addition) 

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            and1 = str(self.myand(int(inputB[0]),int(inputA[0])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output0 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            and1 = str(self.myand(int(inputB[1]),int(inputA[1])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output1 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            and1 = str(self.myand(int(inputB[2]),int(inputA[2])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output2 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            and1 = str(self.myand(int(inputB[3]),int(inputA[3])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output3 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            and1 = str(self.myand(int(inputB[4]),int(inputA[4])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output4 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            and1 = str(self.myand(int(inputB[5]),int(inputA[5])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output5 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            and1 = str(self.myand(int(inputB[6]),int(inputA[6])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output6 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            and1 = str(self.myand(int(inputB[7]),int(inputA[7])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output7 = xor2
            carry = or1

            total = int(output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)
            
            #total = 5 
            self.debugline = "carry = " + str(addition)  +  "pre opcode = " + self.preopcode + " opcode = " + self.opcode + " opernad1 = " + self.operand1
            C = carry
 
        P = "0"

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


    def xxbitxx(self,register):
        if self.QuantumExecute != "SetResBit":
            self.debugline = "Normal operation"
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
                    register = self.rotate(register[1] , register[2] , register[3] , register[4] , register[5] , register[6] , register[7] , "1")
                    X = int(temp,2)
                    Y = int(register,2)
                    C = "0"
                    if X >= Y: C = "1"
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 2:
                    C = register[0]
                    register = self.rotate(register[1] , register[2] , register[3] , register[4] , register[5] , register[6] , register[7] , "0")
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 1:
                    temp = register
                    C = register[0]
                    register = self.rotate(register[1] , register[2] , register[3] , register[4] , register[5] , register[6] , register[7] , self.F[7])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 0:
                    temp = register
                    C = register[0]
                    register = self.rotate(register[1] , register[2] , register[3] , register[4] , register[5] , register[6] , register[7] , register[0])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C
                    
        
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
                    register = self.rotate("0" , register[0] , register[1] , register[2] , register[3] , register[4] , register[5] , register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 2:
                    C = register[7]
                    register = self.rotate(register[0] , register[0] , register[1] , register[2] , register[3] , register[4] , register[5] , register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 1:
                    temp = register
                    C = register[7]
                    register = self.rotate(self.F[7] , register[0] , register[1] , register[2] , register[3] , register[4] , register[5] , register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 0:
                    temp = register
                    C = register[7]
                    register = self.rotate(register[7] ,  register[0] , register[1] , register[2] , register[3] , register[4] , register[5] , register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

            return register
        else:

            self.debugline = "Quantum operation"
            if self.opy < 8: #left side of table
                bit = 0
                if self.opx == 4: bit = 0
                if self.opx == 5: bit = 2
                if self.opx == 6: bit = 4
                if self.opx == 7: bit = 6

                if self.opx > 3 and self.opx < 8:
                    #notbit = not bool(int(register[7 - bit]))
                    notbit = self.mynot(int(register[7-bit]))
                    notbit = str(int(notbit))
                    self.F = "0" + notbit + self.F[2] + "1" + self.F[4] + "0"  + "0" + self.F[7]

                if self.opx == 8:  register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + str(self.mysetbit(0))
                if self.opx == 9:  register = register[0] + register[1] + register[2] + register[3] + register[4] + str(self.mysetbit(0)) + register[6] + register[7]
                if self.opx == 10: register = register[0] + register[1] + register[2] + str(self.mysetbit(0)) + register[4] + register[5] + register[6] + register[7]
                if self.opx == 11: register = register[0] + str(self.mysetbit(0)) + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 12: register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + str(self.mysetbit(1))
                if self.opx == 13: register = register[0] + register[1] + register[2] + register[3] + register[4] + str(self.mysetbit(1)) + register[6] + register[7]
                if self.opx == 14: register = register[0] + register[1] + register[2] + str(self.mysetbit(1)) + register[4] + register[5] + register[6] + register[7]
                if self.opx == 15: register = register[0] + str(self.mysetbit(1)) + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]

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
                    register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + register[0]
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C
        
            if self.opy > 7: #right side of table
                bit = 0
                if self.opx == 4: bit = 1
                if self.opx == 5: bit = 3
                if self.opx == 6: bit = 5
                if self.opx == 7: bit = 7

                if self.opx > 3 and self.opx < 8:
                    #notbit = not bool(int(register[7 - bit]))
                    notbit = self.mynot(int(register[7 - bit]))
                    notbit = str(int(notbit))
                    self.F = "0" + notbit + self.F[2] + "1" + self.F[4] + "0"  + "0" + self.F[7]

                if self.opx == 8:  register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + str(self.mysetbit(0)) + register[7]
                if self.opx == 9:  register = register[0] + register[1] + register[2] + register[3] + str(self.mysetbit(0)) + register[5] + register[6] + register[7]
                if self.opx == 10: register = register[0] + register[1] + str(self.mysetbit(0)) + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 11: register = str(self.mysetbit(0)) + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 12: register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + str(self.mysetbit(1)) + register[7]
                if self.opx == 13: register = register[0] + register[1] + register[2] + register[3] + str(self.mysetbit(1)) + register[5] + register[6] + register[7]
                if self.opx == 14: register = register[0] + register[1] + str(self.mysetbit(1)) + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 15: register = str(self.mysetbit(1)) + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]

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
 


    def eightbitld(self,register1,register2):


        if self.QuantumExecute != "LOAD":
            self.debugline = "Normal operation"

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
        else:
            self.debugline = "Quantum operation"
            if self.preopcode == "11011101" and self.opcode == "01100000": self.IX = register2 + self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100000": self.IY = register2 + self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100001": self.IX = register2 + self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100001": self.IY = register2 + self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100010": self.IX = register2 + self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100010": self.IY = register2 + self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100011": self.IX = register2 + self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100011": self.IY = register2 + self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100111": self.IX = register2 + self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100111": self.IY = register2 + self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01101000": self.IX = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101000": self.IY = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101001": self.IX = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101001": self.IY = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101010": self.IX = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101010": self.IY = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101011": self.IX = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101011": self.IY = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101111": self.IX = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101111": self.IY = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) + register2

            if self.preopcode == "11011101" and self.opcode == "01000100": self.B = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000100": self.B = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01000101": self.B = self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01000101": self.B = self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16]) 

            if self.preopcode == "11011101" and self.opcode == "01010100": self.D = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010100": self.D = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01010101": self.D = self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01010101": self.D = self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01001100": self.C = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001100": self.C = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01001101": self.C = self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01001101": self.C = self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01111100": self.A = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111100": self.A = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8])#self.IY[0:8]
            if self.preopcode == "11011101" and self.opcode == "01111101": self.A = self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])#self.IX[8:16]
            if self.preopcode == "11111101" and self.opcode == "01111101": self.A = self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16])#self.IY[8:16]

            if self.preopcode == "11011101" and self.opcode == "01011100": self.E = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8]) 
            if self.preopcode == "11111101" and self.opcode == "01011100": self.E = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01011101": self.E = self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16]) 
            if self.preopcode == "11111101" and self.opcode == "01011101": self.E = self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16]) 

            if self.preopcode == "11011101" and self.opcode == "01101100": self.IX = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8]) +  self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01101100": self.IY = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) +  self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8])

            if self.preopcode == "11011101" and self.opcode == "01100101": self.IX = self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16]) +  self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100101": self.IY = self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16]) +  self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01000000": register1 = self.fourbitset(self.B[0:4]) + self.fourbitset(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000000": register1 = self.fourbitset(self.B[0:4]) + self.fourbitset(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01000001": register1 = self.fourbitset(self.C[0:4]) + self.fourbitset(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000001": register1 = self.fourbitset(self.C[0:4]) + self.fourbitset(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01000010": register1 = self.fourbitset(self.D[0:4]) + self.fourbitset(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000010": register1 = self.fourbitset(self.D[0:4]) + self.fourbitset(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01000011": register1 = self.fourbitset(self.E[0:4]) + self.fourbitset(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000011": register1 = self.fourbitset(self.E[0:4]) + self.fourbitset(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01010000": register1 = self.fourbitset(self.B[0:4]) + self.fourbitset(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010000": register1 = self.fourbitset(self.B[0:4]) + self.fourbitset(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01010001": register1 = self.fourbitset(self.C[0:4]) + self.fourbitset(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010001": register1 = self.fourbitset(self.C[0:4]) + self.fourbitset(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01010010": register1 = self.fourbitset(self.D[0:4]) + self.fourbitset(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010010": register1 = self.fourbitset(self.D[0:4]) + self.fourbitset(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01010011": register1 = self.fourbitset(self.E[0:4]) + self.fourbitset(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010011": register1 = self.fourbitset(self.E[0:4]) + self.fourbitset(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01000111": register1 = self.fourbitset(self.A[0:4]) + self.fourbitset(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000111": register1 = self.fourbitset(self.A[0:4]) + self.fourbitset(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01001000": register1 = self.fourbitset(self.B[0:4]) + self.fourbitset(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001000": register1 = self.fourbitset(self.B[0:4]) + self.fourbitset(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01001001": register1 = self.fourbitset(self.C[0:4]) + self.fourbitset(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001001": register1 = self.fourbitset(self.C[0:4]) + self.fourbitset(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01001010": register1 = self.fourbitset(self.D[0:4]) + self.fourbitset(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001010": register1 = self.fourbitset(self.D[0:4]) + self.fourbitset(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01001011": register1 = self.fourbitset(self.E[0:4]) + self.fourbitset(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001011": register1 = self.fourbitset(self.E[0:4]) + self.fourbitset(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01001111": register1 = self.fourbitset(self.A[0:4]) + self.fourbitset(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001111": register1 = self.fourbitset(self.A[0:4]) + self.fourbitset(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01010111": register1 = self.fourbitset(self.A[0:4]) + self.fourbitset(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010111": register1 = self.fourbitset(self.A[0:4]) + self.fourbitset(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01011000": register1 = self.fourbitset(self.B[0:4]) + self.fourbitset(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011000": register1 = self.fourbitset(self.B[0:4]) + self.fourbitset(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01011001": register1 = self.fourbitset(self.C[0:4]) + self.fourbitset(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011001": register1 = self.fourbitset(self.C[0:4]) + self.fourbitset(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01011010": register1 = self.fourbitset(self.D[0:4]) + self.fourbitset(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011010": register1 = self.fourbitset(self.D[0:4]) + self.fourbitset(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01011011": register1 = self.fourbitset(self.E[0:4]) + self.fourbitset(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011011": register1 = self.fourbitset(self.E[0:4]) + self.fourbitset(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01011111": register1 = self.fourbitset(self.A[0:4]) + self.fourbitset(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011111": register1 = self.fourbitset(self.A[0:4]) + self.fourbitset(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01111000": register1 = self.fourbitset(self.B[0:4]) + self.fourbitset(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111000": register1 = self.fourbitset(self.B[0:4]) + self.fourbitset(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01111001": register1 = self.fourbitset(self.C[0:4]) + self.fourbitset(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111001": register1 = self.fourbitset(self.C[0:4]) + self.fourbitset(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01111010": register1 = self.fourbitset(self.D[0:4]) + self.fourbitset(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111010": register1 = self.fourbitset(self.D[0:4]) + self.fourbitset(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01111011": register1 = self.fourbitset(self.E[0:4]) + self.fourbitset(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111011": register1 = self.fourbitset(self.E[0:4]) + self.fourbitset(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01111111": register1 = self.fourbitset(self.A[0:4]) + self.fourbitset(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111111": register1 = self.fourbitset(self.A[0:4]) + self.fourbitset(self.A[4:8])
 
            if self.preopcode == "11011101" and self.opcode == "01100100": self.IX = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8]) +  self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100100": self.IY = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) +  self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01101101": self.IX = self.fourbitset(self.IX[0:4]) + self.fourbitset(self.IX[4:8]) +  self.fourbitset(self.IX[8:12]) + self.fourbitset(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01101101": self.IY = self.fourbitset(self.IY[0:4]) + self.fourbitset(self.IY[4:8]) +  self.fourbitset(self.IY[8:12]) + self.fourbitset(self.IY[12:16])


            if self.preopcode == "":
                register1 = self.fourbitset(register2[0:4]) + self.fourbitset(register2[4:8])


            self.clearop()
            self.delay = 1
            #No flags effected
            return register1

    def hladd(self,register):
        hl12 = int((self.H + self.L)[-12:],2)
        add12 = int(register[-12:],2)

        if self.preopcode == "": A = int(self.H  + self.L,2)
        if self.preopcode == "11011101": A = int(self.IX,2)
        if self.preopcode == "11111101": A = int(self.IY,2)

        B = int(register,2)

        C = "0"
        P = "0"
 
        if self.QuantumExecute != "addhl":
            self.debugline = "Normal operation"
            total = A + B

            if total > 65535:
                total = total - 65536
                C = "1"
        else:   
            self.debugline = "Quantum operation"
    
            inputA = format(A, '016b')
            inputB = format(B, '016b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]

            carry = "0" 

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            and1 = str(self.myand(int(inputB[0]),int(inputA[0])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output0 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            and1 = str(self.myand(int(inputB[1]),int(inputA[1])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output1 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            and1 = str(self.myand(int(inputB[2]),int(inputA[2])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output2 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            and1 = str(self.myand(int(inputB[3]),int(inputA[3])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output3 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            and1 = str(self.myand(int(inputB[4]),int(inputA[4])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output4 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            and1 = str(self.myand(int(inputB[5]),int(inputA[5])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output5 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            and1 = str(self.myand(int(inputB[6]),int(inputA[6])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output6 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            and1 = str(self.myand(int(inputB[7]),int(inputA[7])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output7 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[8]),int(inputB[8])))
            and1 = str(self.myand(int(inputB[8]),int(inputA[8])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output8 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[9]),int(inputB[9])))
            and1 = str(self.myand(int(inputB[9]),int(inputA[9])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output9 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[10]),int(inputB[10])))
            and1 = str(self.myand(int(inputB[10]),int(inputA[10])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output10 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[11]),int(inputB[11])))
            and1 = str(self.myand(int(inputB[11]),int(inputA[11])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output11 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[12]),int(inputB[12])))
            and1 = str(self.myand(int(inputB[12]),int(inputA[12])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output12 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[13]),int(inputB[13])))
            and1 = str(self.myand(int(inputB[13]),int(inputA[13])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output13 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[14]),int(inputB[14])))
            and1 = str(self.myand(int(inputB[14]),int(inputA[14])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output14 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[15]),int(inputB[15])))
            and1 = str(self.myand(int(inputB[15]),int(inputA[15])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output15 = xor2
            carry = or1

            C = carry

            total = int(output15 + output14 + output13 + output12 + output11 + output10 + output9 + output8 + output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)

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

    def hlsbc(self,register):
        hl12 = int((self.H + self.L)[-12:],2)
        sub12 = int(register[-12:],2) - int(self.F[7])

        A = int(self.H + self.L,2)
        B = int(register,2)
        C = "0"
        Z = "0"

        if self.QuantumExecute != "sbchl":
            self.debugline = "Normal operation"
            total = A - B - int(self.F[7])
            
            if total < 0:
                total = total + 65536
                C = "1"
        else:
            self.debugline = "Quantum operation"
            inputA = self.H + self.L
            inputB = register
            inputA = inputA[::-1]
            inputB = inputB[::-1]

            temp = ""
            borrow = self.F[7]

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            not1 = str(self.mynot(int(inputA[0])))
            and1 = str(self.myand(int(not1),int(inputB[0])))
            output0 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            not1 = str(self.mynot(int(inputA[1])))
            and1 = str(self.myand(int(not1),int(inputB[1])))
            output1 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            not1 = str(self.mynot(int(inputA[2])))
            and1 = str(self.myand(int(not1),int(inputB[2])))
            output2 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            not1 = str(self.mynot(int(inputA[3])))
            and1 = str(self.myand(int(not1),int(inputB[3])))
            output3 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            not1 = str(self.mynot(int(inputA[4])))
            and1 = str(self.myand(int(not1),int(inputB[4])))
            output4 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            not1 = str(self.mynot(int(inputA[5])))
            and1 = str(self.myand(int(not1),int(inputB[5])))
            output5 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            not1 = str(self.mynot(int(inputA[6])))
            and1 = str(self.myand(int(not1),int(inputB[6])))
            output6 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            not1 = str(self.mynot(int(inputA[7])))
            and1 = str(self.myand(int(not1),int(inputB[7])))
            output7 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
 
            xor1 = str(self.myxor(int(inputA[8]),int(inputB[8])))
            not1 = str(self.mynot(int(inputA[8])))
            and1 = str(self.myand(int(not1),int(inputB[8])))
            output8 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            xor1 = str(self.myxor(int(inputA[9]),int(inputB[9])))
            not1 = str(self.mynot(int(inputA[9])))
            and1 = str(self.myand(int(not1),int(inputB[9])))
            output9 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            xor1 = str(self.myxor(int(inputA[10]),int(inputB[10])))
            not1 = str(self.mynot(int(inputA[10])))
            and1 = str(self.myand(int(not1),int(inputB[10])))
            output10 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[11]),int(inputB[11])))
            not1 = str(self.mynot(int(inputA[11])))
            and1 = str(self.myand(int(not1),int(inputB[11])))
            output11 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[12]),int(inputB[12])))
            not1 = str(self.mynot(int(inputA[12])))
            and1 = str(self.myand(int(not1),int(inputB[12])))
            output12 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[13]),int(inputB[13])))
            not1 = str(self.mynot(int(inputA[13])))
            and1 = str(self.myand(int(not1),int(inputB[13])))
            output13 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[14]),int(inputB[14])))
            not1 = str(self.mynot(int(inputA[14])))
            and1 = str(self.myand(int(not1),int(inputB[14])))
            output14 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[15]),int(inputB[15])))
            not1 = str(self.mynot(int(inputA[15])))
            and1 = str(self.myand(int(not1),int(inputB[15])))
            output15 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
 
            sub = int(output15 + output14 + output13 + output12 + output11 + output10 + output9 + output8 + output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)

            total = sub
        
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



    def hladc(self,register):
        hl12 = int((self.H + self.L)[-12:],2)
        add12 = int(register[-12:],2) + int(self.F[7])

        A = int(self.H + self.L,2)
        B = int(register,2)
        C = "0"

        if self.QuantumExecute != "adchl":
            self.debugline = "Normal operation"
            total = A + B + int(self.F[7])
     
            if total > 65535:
                total = total - 65536
                C = "1"
        else:
            self.debugline = "Quantum operation"

            inputA = format(A, '016b')
            inputB = format(B, '016b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]

            carry = self.F[7] 

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            and1 = str(self.myand(int(inputB[0]),int(inputA[0])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output0 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            and1 = str(self.myand(int(inputB[1]),int(inputA[1])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output1 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            and1 = str(self.myand(int(inputB[2]),int(inputA[2])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output2 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            and1 = str(self.myand(int(inputB[3]),int(inputA[3])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output3 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            and1 = str(self.myand(int(inputB[4]),int(inputA[4])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output4 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            and1 = str(self.myand(int(inputB[5]),int(inputA[5])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output5 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            and1 = str(self.myand(int(inputB[6]),int(inputA[6])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output6 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            and1 = str(self.myand(int(inputB[7]),int(inputA[7])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output7 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[8]),int(inputB[8])))
            and1 = str(self.myand(int(inputB[8]),int(inputA[8])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output8 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[9]),int(inputB[9])))
            and1 = str(self.myand(int(inputB[9]),int(inputA[9])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output9 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[10]),int(inputB[10])))
            and1 = str(self.myand(int(inputB[10]),int(inputA[10])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output10 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[11]),int(inputB[11])))
            and1 = str(self.myand(int(inputB[11]),int(inputA[11])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output11 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[12]),int(inputB[12])))
            and1 = str(self.myand(int(inputB[12]),int(inputA[12])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output12 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[13]),int(inputB[13])))
            and1 = str(self.myand(int(inputB[13]),int(inputA[13])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output13 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[14]),int(inputB[14])))
            and1 = str(self.myand(int(inputB[14]),int(inputA[14])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output14 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[15]),int(inputB[15])))
            and1 = str(self.myand(int(inputB[15]),int(inputA[15])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output15 = xor2
            carry = or1

            C = carry

            total = int(output15 + output14 + output13 + output12 + output11 + output10 + output9 + output8 + output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)

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



    def scf(self):
        if self.QuantumExecute != "scf":
            self.debugline = "Normal operation"
            self.F = self.F[0] + self.F[1] + self.F[2] + "0" + self.F[4] + self.F[5] + "0" + "1"   
        else:
            self.debugline = "Quantum operation"
            self.F = self.F[0] + self.F[1] + self.F[2] + "0" + self.F[4] + self.F[5] + "0" + str(self.setbit(1))
 
    def neg(self,register):
        if self.QuantumExecute != "neg":
            self.debugline = "Normal operation"
            return 0 - register
        else:
            self.debugline = "Quantum operation"
            
            inputA = "00000000"
            inputB = format(register,'08b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]

            temp = ""
            borrow = "0"

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            not1 = str(self.mynot(int(inputA[0])))
            and1 = str(self.myand(int(not1),int(inputB[0])))
            output0 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            not1 = str(self.mynot(int(inputA[1])))
            and1 = str(self.myand(int(not1),int(inputB[1])))
            output1 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            not1 = str(self.mynot(int(inputA[2])))
            and1 = str(self.myand(int(not1),int(inputB[2])))
            output2 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            not1 = str(self.mynot(int(inputA[3])))
            and1 = str(self.myand(int(not1),int(inputB[3])))
            output3 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            not1 = str(self.mynot(int(inputA[4])))
            and1 = str(self.myand(int(not1),int(inputB[4])))
            output4 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            not1 = str(self.mynot(int(inputA[5])))
            and1 = str(self.myand(int(not1),int(inputB[5])))
            output5 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            not1 = str(self.mynot(int(inputA[6])))
            and1 = str(self.myand(int(not1),int(inputB[6])))
            output6 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            not1 = str(self.mynot(int(inputA[7])))
            and1 = str(self.myand(int(not1),int(inputB[7])))
            output7 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
 
            sub = int(output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)

            return int(sub)


    def rotate(self,bit0,bit1,bit2,bit3,bit4,bit5,bit6,bit7):
        if self.QuantumExecute != "rot":
            self.debugline = "Normal operation"
            return bit0 + bit1 + bit2 + bit3 + bit4 + bit5 + bit6 + bit7
        else:
            self.debugline = "Quantum operation"
            return  self.fourbitset(bit0 + bit1 + bit2 + bit3) + self.fourbitset(bit4 + bit5 + bit6 + bit7)

    def singleload(self,bit0,bit1,bit2,bit3,bit4,bit5,bit6,bit7):
        if self.QuantumExecute != "LOAD3i":
            self.debugline = "Normal operation"
            return bit0 + bit1 + bit2 + bit3 + bit4 + bit5 + bit6 + bit7
        else:
            self.debugline = "Quantum operation"
            return  self.fourbitset(bit0 + bit1 + bit2 + bit3) + self.fourbitset(bit4 + bit5 + bit6 + bit7)

    def loadhlr(self,data,original):
        if self.QuantumExecute != "loadhlr":
            self.debugline = "Normal operation"
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
        else:
            self.debugline = "Quantum operation"
            if self.preopcode == "":
                if self.stage == "1":
                    stage = ""
                    self.delay = 1
                    self.needmorebits = False
                    self.execute = True
                    #register = data
                    register = self.fourbitset(data[0] + data[1] + data[2] + data[3]) + self.fourbitset(data[4] + data[5] + data[6] + data[7])

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
                    register = self.fourbitset(data[0] + data[1] + data[2] + data[3]) + self.fourbitset(data[4] + data[5] + data[6] + data[7])
                    return register

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

    def regtodatabus(self,register):
        if self.QuantumExecute != "LOAD3i":#was load2
            self.debugline = "Normal operation"
 
            self.d7 = bool(int(register[0]))
            self.d6 = bool(int(register[1]))
            self.d5 = bool(int(register[2]))
            self.d4 = bool(int(register[3]))
            self.d3 = bool(int(register[4]))
            self.d2 = bool(int(register[5]))
            self.d1 = bool(int(register[6]))
            self.d0 = bool(int(register[7]))
        else:
            self.debugline = "Quantum operation"

            output = self.fourbitset(register[0] + register[1] + register[2] + register[3]) + self.fourbitset(register[4] + register[5] + register[6] + register[7])

            self.d7 = bool(int(output[0]))
            self.d6 = bool(int(output[1]))
            self.d5 = bool(int(output[2]))
            self.d4 = bool(int(output[3]))
            self.d3 = bool(int(output[4]))
            self.d2 = bool(int(output[5]))
            self.d1 = bool(int(output[6]))
            self.d0 = bool(int(output[7]))

    def regtoaddrbus(self,register):
        if self.QuantumExecute != "LOAD3i":#was load2
            self.debugline = "Normal operation"
 
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
        else:
            self.debugline = "Quantum operation"

            output = self.fourbitset(register[0] + register[1] + register[2] + register[3]) + self.fourbitset(register[4] + register[5] + register[6] + register[7]) + self.fourbitset(register[8] + register[9] + register[10] + register[11]) + self.fourbitset(register[12] + register[13] + register[14] + register[15])


            self.a15 = bool(int(output[0]))
            self.a14 = bool(int(output[1]))
            self.a13 = bool(int(output[2]))
            self.a12 = bool(int(output[3]))
            self.a11 = bool(int(output[4]))
            self.a10 = bool(int(output[5]))
            self.a9 = bool(int(output[6]))
            self.a8 = bool(int(output[7]))
            self.a7 = bool(int(output[8]))
            self.a6 = bool(int(output[9]))
            self.a5 = bool(int(output[10]))
            self.a4 = bool(int(output[11]))
            self.a3 = bool(int(output[12]))
            self.a2 = bool(int(output[13]))
            self.a1 = bool(int(output[14]))
            self.a0 = bool(int(output[15]))


    def incNoFlags(self,number):
        if self.QuantumExecute != "LOAD3":
            self.debugline = "Normal operation"
            number = number + 1
            if number == 65536: number = 0
            return number

        else:
            self.debugline = "Quantum operation"

            inputA = format(number, '016b')
            inputA = inputA[::-1]

            temp = ""

            output0 = str(self.myxor(1,int(inputA[0])))
            temp = str(self.myand(1,int(inputA[0])))
            output1 = str(self.myxor(int(temp),int(inputA[1])))
            temp = str(self.myand(int(temp),int(inputA[1])))
            output2 = str(self.myxor(int(temp),int(inputA[2])))
            temp = str(self.myand(int(temp),int(inputA[2])))
            output3 = str(self.myxor(int(temp),int(inputA[3])))
            temp = str(self.myand(int(temp),int(inputA[3])))
            output4 = str(self.myxor(int(temp),int(inputA[4])))
            temp = str(self.myand(int(temp),int(inputA[4])))
            output5 = str(self.myxor(int(temp),int(inputA[5])))
            temp = str(self.myand(int(temp),int(inputA[5])))
            output6 = str(self.myxor(int(temp),int(inputA[6])))
            temp = str(self.myand(int(temp),int(inputA[6])))
            output7 = str(self.myxor(int(temp),int(inputA[7])))
            temp = str(self.myand(int(temp),int(inputA[7])))
            output8 = str(self.myxor(int(temp),int(inputA[8])))
            temp = str(self.myand(int(temp),int(inputA[8])))
            output9 = str(self.myxor(int(temp),int(inputA[9])))
            temp = str(self.myand(int(temp),int(inputA[9])))
            output10 = str(self.myxor(int(temp),int(inputA[10])))
            temp = str(self.myand(int(temp),int(inputA[10])))
            output11 = str(self.myxor(int(temp),int(inputA[11])))
            temp = str(self.myand(int(temp),int(inputA[11])))
            output12 = str(self.myxor(int(temp),int(inputA[12])))
            temp = str(self.myand(int(temp),int(inputA[12])))
            output13 = str(self.myxor(int(temp),int(inputA[13])))
            temp = str(self.myand(int(temp),int(inputA[13])))
            output14 = str(self.myxor(int(temp),int(inputA[14])))
            temp = str(self.myand(int(temp),int(inputA[14])))
            output15 = str(self.myxor(int(temp),int(inputA[15])))
            temp = str(self.myand(int(temp),int(inputA[15])))

            register = output15 + output14 + output13 + output12 + output11 + output10 + output9 + output8 + output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0
            
            return int(register,2)


    def decNoFlags(self,number):
        if self.QuantumExecute != "LOAD3i":#was LOAD2
            self.debugline = "Normal operation"
            number = number - 1
            if number < 0: number = number + 65536
            return number

        else:
            self.debugline = "Quantum operation"

            inputA = format(number, '016b')
            inputA = inputA[::-1]

            temp = ""

            carry = "0"
            xor0 = str(self.myxor(1,int(inputA[0])))
            and0 = str(self.myand(1,int(inputA[0])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output0 = xor1

            xor0 = str(self.myxor(1,int(inputA[1])))
            and0 = str(self.myand(1,int(inputA[1])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output1 = xor1

            xor0 = str(self.myxor(1,int(inputA[2])))
            and0 = str(self.myand(1,int(inputA[2])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output2 = xor1

            xor0 = str(self.myxor(1,int(inputA[3])))
            and0 = str(self.myand(1,int(inputA[3])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output3 = xor1

            xor0 = str(self.myxor(1,int(inputA[4])))
            and0 = str(self.myand(1,int(inputA[4])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output4 = xor1

            xor0 = str(self.myxor(1,int(inputA[5])))
            and0 = str(self.myand(1,int(inputA[5])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output5 = xor1

            xor0 = str(self.myxor(1,int(inputA[6])))
            and0 = str(self.myand(1,int(inputA[6])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output6 = xor1

            xor0 = str(self.myxor(1,int(inputA[7])))
            and0 = str(self.myand(1,int(inputA[7])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output7 = xor1

            xor0 = str(self.myxor(1,int(inputA[8])))
            and0 = str(self.myand(1,int(inputA[8])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output8 = xor1

            xor0 = str(self.myxor(1,int(inputA[9])))
            and0 = str(self.myand(1,int(inputA[9])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output9 = xor1

            xor0 = str(self.myxor(1,int(inputA[10])))
            and0 = str(self.myand(1,int(inputA[10])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output10 = xor1

            xor0 = str(self.myxor(1,int(inputA[11])))
            and0 = str(self.myand(1,int(inputA[11])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output11 = xor1

            xor0 = str(self.myxor(1,int(inputA[12])))
            and0 = str(self.myand(1,int(inputA[12])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output12 = xor1

            xor0 = str(self.myxor(1,int(inputA[13])))
            and0 = str(self.myand(1,int(inputA[13])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output13 = xor1

            xor0 = str(self.myxor(1,int(inputA[14])))
            and0 = str(self.myand(1,int(inputA[14])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output14 = xor1

            xor0 = str(self.myxor(1,int(inputA[15])))
            and0 = str(self.myand(1,int(inputA[15])))
            xor1 = str(self.myxor(int(xor0),int(carry)))
            and1 = str(self.myand(int(carry),int(xor0)))
            carry = str(self.myor(int(and1),int(and0)))
            output15 = xor1

            register = output15 + output14 + output13 + output12 + output11 + output10 + output9 + output8 + output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0
            
            return int(register,2)


    def eightbitcp(self,register):
        if self.QuantumExecute != "CP":
            self.debugline = "Normal operation"
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
        else:
            self.debugline = "Quantum operation"
            A = int(self.A,2)
            N = int(register,2)

            #***** Z *****
            Z = "0"
            if A == N: Z = "1"

            #result = A - N


            inputA = self.A
            inputB = register
            inputA = inputA[::-1]
            inputB = inputB[::-1]

            temp = ""
            borrow = "0" 

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            not1 = str(self.mynot(int(inputA[0])))
            and1 = str(self.myand(int(not1),int(inputB[0])))
            output0 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            not1 = str(self.mynot(int(inputA[1])))
            and1 = str(self.myand(int(not1),int(inputB[1])))
            output1 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            not1 = str(self.mynot(int(inputA[2])))
            and1 = str(self.myand(int(not1),int(inputB[2])))
            output2 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            output6 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            not1 = str(self.mynot(int(inputA[7])))
            and1 = str(self.myand(int(not1),int(inputB[7])))
            output7 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
 
            result = int(output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)

            C = borrow
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
     
    def setPC(self,addr):
        if self.QuantumExecute != "LOAD3i":#was JUMP
            self.debugline = "Normal operation"
            return addr
        else:
            self.debugline = "Quantum operation"
            return  self.fourbitset(addr[0] + addr[1] + addr[2] + addr[3]) + self.fourbitset(addr[4] + addr[5] + addr[6] + addr[7]) + self.fourbitset(addr[8] + addr[9] + addr[10] + addr[11]) + self.fourbitset(addr[12] + addr[13] + addr[14] + addr[15])


    def conditionalSetPC(self,addr,condition):
        if self.QuantumExecute != "LOAD3":#was JUMP
            self.debugline = "Normal operation"
            if condition == "1": return addr
            else: return False
        else:
            self.debugline = "Quantum operation"
            if self.myif(condition) == 1: return self.fourbitset(addr[0] + addr[1] + addr[2] + addr[3]) + self.fourbitset(addr[4] + addr[5] + addr[6] + addr[7]) + self.fourbitset(addr[8] + addr[9] + addr[10] + addr[11]) + self.fourbitset(addr[12] + addr[13] + addr[14] + addr[15])
            else: return False

    def checkFlag(self,condition):
        if self.QuantumExecute != "LOAD3":#was JUMP
            self.debugline = "Normal operation"
            if condition == "1": return "1"
            else: return "0"
        else:
            self.debugline = "Quantum operation"
            return str(self.myif(int(condition)))





    def eightBitSubNoFlags(self,number1,number2):
        if self.QuantumExecute != "LOAD3":
            self.debugline = "Normal operation"
            output = number1 - number2
            return output
        else:
            self.debugline = "Quantum operation"
            inputA = format(number1,'08b')
            inputB = format(number2,'08b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]

            temp = ""
            borrow = "1" 

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            not1 = str(self.mynot(int(inputA[0])))
            and1 = str(self.myand(int(not1),int(inputB[0])))
            output0 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            not1 = str(self.mynot(int(inputA[1])))
            and1 = str(self.myand(int(not1),int(inputB[1])))
            output1 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            not1 = str(self.mynot(int(inputA[2])))
            and1 = str(self.myand(int(not1),int(inputB[2])))
            output2 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            not1 = str(self.mynot(int(inputA[3])))
            and1 = str(self.myand(int(not1),int(inputB[3])))
            output3 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            not1 = str(self.mynot(int(inputA[4])))
            and1 = str(self.myand(int(not1),int(inputB[4])))
            output4 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            not1 = str(self.mynot(int(inputA[5])))
            and1 = str(self.myand(int(not1),int(inputB[5])))
            output5 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            not1 = str(self.mynot(int(inputA[6])))
            and1 = str(self.myand(int(not1),int(inputB[6])))
            output6 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            not1 = str(self.mynot(int(inputA[7])))
            and1 = str(self.myand(int(not1),int(inputB[7])))
            output7 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            
            sub = int(output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)
            temp = sub
            if output7 == "1":# covert to singed

                if output6 == "1":
                    output6 = "0"
                else:
                    output6 = "1"
           
                if output5 == "1":
                    output5 = "0"
                else:
                    output5 = "1"

                if output4 == "1":
                    output4 = "0"
                else:
                    output4 = "1"

                if output3 == "1":
                    output3 = "0"
                else:
                    output3 = "1"

                if output2 == "1":
                    output2 = "0"
                else:
                    output2 = "1"

                if output1 == "1":
                    output1 = "0"
                else:
                    output1 = "1"

                if output0 == "1":
                    output0 = "0"
                else:
                    output0 = "1"



                sub = 0 - int(output6 + output5 + output4 + output3 + output2 + output1 + output0,2)
                self.debugline = "A = " + inputA + " B = " + inputB + " binary = " + output6 + output5 + output4 + output3 + output2 + output1 + output0 + " singed = " + str(sub) + " sum = " + str(temp)
            
            return sub


    def eightBitSubNoFlagsUnsigned(self,number1,number2):
        if self.QuantumExecute != "LOAD3i":
            self.debugline = "Normal operation"
            output = number1 - number2
            self.debugline = "number 1 " + str(number1) + " - number2 " + str(number2) + " = " + str(output)
            return output
        else:
            self.debugline = "Quantum operation"
            inputA = format(number1,'08b')
            inputB = format(number2,'08b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]

            temp = ""
            borrow = "0" 

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            not1 = str(self.mynot(int(inputA[0])))
            and1 = str(self.myand(int(not1),int(inputB[0])))
            output0 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            not1 = str(self.mynot(int(inputA[1])))
            and1 = str(self.myand(int(not1),int(inputB[1])))
            output1 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            not1 = str(self.mynot(int(inputA[2])))
            and1 = str(self.myand(int(not1),int(inputB[2])))
            output2 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            not1 = str(self.mynot(int(inputA[3])))
            and1 = str(self.myand(int(not1),int(inputB[3])))
            output3 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            not1 = str(self.mynot(int(inputA[4])))
            and1 = str(self.myand(int(not1),int(inputB[4])))
            output4 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            not1 = str(self.mynot(int(inputA[5])))
            and1 = str(self.myand(int(not1),int(inputB[5])))
            output5 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            not1 = str(self.mynot(int(inputA[6])))
            and1 = str(self.myand(int(not1),int(inputB[6])))
            output6 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            not1 = str(self.mynot(int(inputA[7])))
            and1 = str(self.myand(int(not1),int(inputB[7])))
            output7 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            
            sub = int(output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)
            self.debugline = "A = " + inputA + " B = " + inputB + " binary = " + output6 + output5 + output4 + output3 + output2 + output1 + output0 + " singed = " + str(sub) + " sum = " + str(temp)
            
            return sub



    def sixteenBitAddNoFlags(self,number1,number2):
        if self.QuantumExecute != "load3i":
            self.debugline = "normal operation"
            output = number1 + number2
            if output < 0: output = output + 65536
            if output > 65535: output = output - 65536
            return output
        else:
            self.debugline = "quantum operation"

            if number1 < 0: number1 = number1 + 65536 #fix for the potential of adding a signed number to a non signed 16 bit number
            if number2 < 0: number2 = number2 + 65536

            inputA = format(number1, '016b')
            inputB = format(number2, '016b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            
            #self.debugline = str(number1) + " " + str(number2)



            carry = "0" 

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            and1 = str(self.myand(int(inputB[0]),int(inputA[0])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output0 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            and1 = str(self.myand(int(inputB[1]),int(inputA[1])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output1 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            and1 = str(self.myand(int(inputB[2]),int(inputA[2])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output2 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            and1 = str(self.myand(int(inputB[3]),int(inputA[3])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output3 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            and1 = str(self.myand(int(inputB[4]),int(inputA[4])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output4 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            and1 = str(self.myand(int(inputB[5]),int(inputA[5])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output5 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            and1 = str(self.myand(int(inputB[6]),int(inputA[6])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output6 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            and1 = str(self.myand(int(inputB[7]),int(inputA[7])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output7 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[8]),int(inputB[8])))
            and1 = str(self.myand(int(inputB[8]),int(inputA[8])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output8 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[9]),int(inputB[9])))
            and1 = str(self.myand(int(inputB[9]),int(inputA[9])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output9 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[10]),int(inputB[10])))
            and1 = str(self.myand(int(inputB[10]),int(inputA[10])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output10 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[11]),int(inputB[11])))
            and1 = str(self.myand(int(inputB[11]),int(inputA[11])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output11 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[12]),int(inputB[12])))
            and1 = str(self.myand(int(inputB[12]),int(inputA[12])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output12 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[13]),int(inputB[13])))
            and1 = str(self.myand(int(inputB[13]),int(inputA[13])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output13 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[14]),int(inputB[14])))
            and1 = str(self.myand(int(inputB[14]),int(inputA[14])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output14 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[15]),int(inputB[15])))
            and1 = str(self.myand(int(inputB[15]),int(inputA[15])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output15 = xor2
            carry = or1

            C = carry

            total = int(output15 + output14 + output13 + output12 + output11 + output10 + output9 + output8 + output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)

            return total

    def setBoolValue(self,value):
        if self.QuantumExecute != "LOAD3":
            self.debugline = "normal operation"
            return value
        else:
            self.debugline = "qunatum operation"
            return bool(self.setbit(int(value)))




    def eightBitAddNoFlagsNotSigned(self,number1,number2):
        if self.QuantumExecute != "ADDi":
            output = number1 + number2
            if output < 0: output = output + 256
            if output > 255: output = output - 256
            return output
        else:
            self.debugline = "Quantum operation"
            inputA = format(number1, '016b')
            inputB = format(number2, '016b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            
            carry = "0" 

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            and1 = str(self.myand(int(inputB[0]),int(inputA[0])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output0 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            and1 = str(self.myand(int(inputB[1]),int(inputA[1])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output1 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            and1 = str(self.myand(int(inputB[2]),int(inputA[2])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output2 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            and1 = str(self.myand(int(inputB[3]),int(inputA[3])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output3 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            and1 = str(self.myand(int(inputB[4]),int(inputA[4])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output4 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            and1 = str(self.myand(int(inputB[5]),int(inputA[5])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output5 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            and1 = str(self.myand(int(inputB[6]),int(inputA[6])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output6 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            and1 = str(self.myand(int(inputB[7]),int(inputA[7])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output7 = xor2
            carry = or1

            C = carry

            total = int(output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)

            return total


    def eightBitSubNoFlagsNotSigned(self,number1,number2):
        if self.QuantumExecute != "SUB":
            output = number1 - number2
            if output < 0: output = output + 256
            if output > 255: output = output - 256
            return output
        else:
            self.debugline = "Quantum operation"
            inputA = format(number1,'08b')
            inputB = format(number2,'08b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]

            temp = ""
            borrow = "0" 

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            not1 = str(self.mynot(int(inputA[0])))
            and1 = str(self.myand(int(not1),int(inputB[0])))
            output0 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            not1 = str(self.mynot(int(inputA[1])))
            and1 = str(self.myand(int(not1),int(inputB[1])))
            output1 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            not1 = str(self.mynot(int(inputA[2])))
            and1 = str(self.myand(int(not1),int(inputB[2])))
            output2 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
                
            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            not1 = str(self.mynot(int(inputA[3])))
            and1 = str(self.myand(int(not1),int(inputB[3])))
            output3 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            not1 = str(self.mynot(int(inputA[4])))
            and1 = str(self.myand(int(not1),int(inputB[4])))
            output4 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            not1 = str(self.mynot(int(inputA[5])))
            and1 = str(self.myand(int(not1),int(inputB[5])))
            output5 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            not1 = str(self.mynot(int(inputA[6])))
            and1 = str(self.myand(int(not1),int(inputB[6])))
            output6 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))
            
            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            not1 = str(self.mynot(int(inputA[7])))
            and1 = str(self.myand(int(not1),int(inputB[7])))
            output7 = str(self.myxor(int(xor1),int(borrow)))
            not2 = str(self.mynot(int(xor1)))
            and2 = str(self.myand(int(not2),int(borrow)))
            borrow = str(self.myor(int(and2),int(and1)))

            
            sub = int(output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)
            self.debugline = "A = " + inputA + " B = " + inputB + " binary = " + output6 + output5 + output4 + output3 + output2 + output1 + output0 + " singed = " + str(sub) + " sum = " + str(temp)
            
            return sub

    def sixteenBitAddNoFlags(self,number1,number2):
        if self.QuantumExecute != "ADDii":
            self.debugline = "Normal operation"
            output = number1 - number2
            output = number1 + number2
            if output < 0: output = output + 65536
            if output > 65535: output = output - 65536
            return output
        else:
            self.debugline = "quantum operation"

            inputA = format(number1, '016b')
            inputB = format(number2, '016b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            
            carry = "0" 

            xor1 = str(self.myxor(int(inputA[0]),int(inputB[0])))
            and1 = str(self.myand(int(inputB[0]),int(inputA[0])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output0 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[1]),int(inputB[1])))
            and1 = str(self.myand(int(inputB[1]),int(inputA[1])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output1 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[2]),int(inputB[2])))
            and1 = str(self.myand(int(inputB[2]),int(inputA[2])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output2 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[3]),int(inputB[3])))
            and1 = str(self.myand(int(inputB[3]),int(inputA[3])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output3 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[4]),int(inputB[4])))
            and1 = str(self.myand(int(inputB[4]),int(inputA[4])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output4 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[5]),int(inputB[5])))
            and1 = str(self.myand(int(inputB[5]),int(inputA[5])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output5 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[6]),int(inputB[6])))
            and1 = str(self.myand(int(inputB[6]),int(inputA[6])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output6 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[7]),int(inputB[7])))
            and1 = str(self.myand(int(inputB[7]),int(inputA[7])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output7 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[8]),int(inputB[8])))
            and1 = str(self.myand(int(inputB[8]),int(inputA[8])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output8 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[9]),int(inputB[9])))
            and1 = str(self.myand(int(inputB[9]),int(inputA[9])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output9 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[10]),int(inputB[10])))
            and1 = str(self.myand(int(inputB[10]),int(inputA[10])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output10 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[11]),int(inputB[11])))
            and1 = str(self.myand(int(inputB[11]),int(inputA[11])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output11 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[12]),int(inputB[12])))
            and1 = str(self.myand(int(inputB[12]),int(inputA[12])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output12 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[13]),int(inputB[13])))
            and1 = str(self.myand(int(inputB[13]),int(inputA[13])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output13 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[14]),int(inputB[14])))
            and1 = str(self.myand(int(inputB[14]),int(inputA[14])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output14 = xor2
            carry = or1

            xor1 = str(self.myxor(int(inputA[15]),int(inputB[15])))
            and1 = str(self.myand(int(inputB[15]),int(inputA[15])))
            xor2 = str(self.myxor(int(xor1),int(carry)))
            and2 = str(self.myand(int(xor1),int(carry)))
            or1 = str(self.myor(int(and2),int(and1)))
            output15 = xor2
            carry = or1

            C = carry

            total = int(output15 + output14 + output13 + output12 + output11 + output10 + output9 + output8 + output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)

            return total

       

