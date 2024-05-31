from z80 import z80
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.circuit.library.standard_gates import C4XGate
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
import sys
import math
from qiskit.visualization import plot_histogram
from matplotlib import style




class q80(z80):
    
    QuantumExecute = "None"
    QuantumComputer = AerSimulator(method='matrix_product_state')
    shots = 2000
    #QuantumExecute = "INC1" #Quantum method 1 - In silicon method (Very slow)
    #QuantumExecute = "INC2" #Quantum method 2 - Entirely in the quantum domain
    #QuantumExecute = "INC3" #Quantum method 3 - Entirely in the quantum domain, including the F register
    #QuantumExecute = "DEC1" #Quantum method 1 - In silicon method (Very slow)
    #QuantumExecute = "DEC2" #Quantum method 2 - Entirely in the quantum domain
    #QuantumExecute = "XOR1" #Quantum method 1 - In silicon method (Very slow)
    #QuantumExecute = "XOR2" #Quantum method 2 - Entirely in the quantum domain
    #QuantumExecute = "AND1" #Quantum method 1 - In silicon method (Very slow)
    #QuantumExecute = "AND2" #Quantum method 2 - Entirely in the quantum domain
    #QuantumExecute = "OR1" #Quantum method 1 - In silicon method (Very slow)
    #QuantumExecute = "OR2" #Quantum method 2 - Entirely in the quantum domain
    #QuantumExecute = "LOAD1" #Quantum method 1 - Direct load from Qubits (Note, loading is included as parts of PUSH, POP, CALL,RET, etc... INCLUDING ***HALT***)
    #QuantumExecute = "LOAD2" #Quantum method 2 - In silicon method (Note, loading is included as parts of PUSH, POP, CALL,RET, etc... INCLUDING ***HALT***) 
    #QuantumExecute = "LOAD3" #Quantum method 3 - Load using Hadamard gates to entanlgle the source and destination bits (Note, loading is included as parts of PUSH, POP, CALL,RET, etc... INCLUDING ***HALT***) 
    #QuantumExecute = "LOAD4" #Quantum method 4 - Load using quantum swap gates (Note, this is not safe for all load instructions and is intended for EX instructions)
    #QuantumExecute = "ADD1" #Quantum method 1 - In silicon method (Very slow)
    #QuantumExecute = "ADD2" #Quantum method 2 - Entirely in the quantum domain
    #QuantumExecute = "ADD3" #Quantum method 3 - Ry rotation method
    #QuantumExecute = "SUB1" #Quantum method 1 - In silicon method (Very slow)
    #QuantumExecute = "SUB2" #Quantum method 2 - Entirely in the quantum domain
    #QuantumExecute = "SetResBit1" #Quantum method 1 - In silicon method 
    #QuantumExecute = "SetResBit2" #Quantum method 2 - Entirely in the quantum domain
    #QuantumExecute = "NEG1" #Quantum method 1 - In silicon method (Very slow)
    #QuantumExecute = "NEG2" #Quantum method 2 - Entirely in the quantum domain
    #QuantumExecute = "ROT1" #Quantum method 1 - Direct load from Qubits
    #QuantumExecute = "ROT2" #Quantum method 2 - In silicon method 
    #QuantumExecute = "ROT3" #Quantum method 3 - Quantum swap gate method 
    #QuantumExecute = "SCF1" #Quantum method 1 - Direct load from Qubits
    #QuantumExecute = "SCF2" #Quantum method 2 - In silicon method 
    #QuantumExecute = "CP1" #Quantum method 1 - In silicon method (Very slow)
    #QuantumExecute = "CP2" #Quantum method 2 - Entirely in the quantum domain
    #QuantumExecute = "CP3" #Quantum method 3 - XOR based method entirly in the quantum domain
    #QuantumExecute = "SetPC1" #Quantum method 1 - Direct load from Qubits
    #QuantumExecute = "SetPC2" #Quantum method 2 - In silicon method
    #QuantumExecute = "DataBus1" #Quantum method 1 - Direct load from Qubits
    #QuantumExecute = "DataBus2" #Quantum method 2 - In silicon method
    #QuantumExecute = "AddrBus1" #Quantum method 1 - Direct load from Qubits
    #QuantumExecute = "AddrBus2" #Quantum method 2 - In silicon method


#****************************************************************************************************************************************************************************
#****************************************************************************************************************************************************************************
#************************************************************************* Quantum Gates ************************************************************************************
#****************************************************************************************************************************************************************************
#****************************************************************************************************************************************************************************
    def myand(self,inputA,inputB):
        """
      ┌───────┐     ┌─┐
 q_0: ┤ Ry(π) ├──■──┤M├───────
      ├───────┤  │  └╥┘┌─┐
 q_1: ┤ Ry(0) ├──■───╫─┤M├────
      └───────┘┌─┴─┐ ║ └╥┘┌─┐
 q_2: ─────────┤ X ├─╫──╫─┤M├─
               └───┘ ║  ║ └╥┘
c:  3/═══════════════╩══╩══╩══
                     0  1  2  
        """
        inputA = inputA * math.pi
        inputB = inputB * math.pi

        circuit = QuantumCircuit(3,3)
        circuit.ry(inputA,0)
        circuit.ry(inputB,1)
        circuit.ccx(0,1,2)
        circuit.measure_all()
        print("Quantum AND circuit")
        print(circuit)
  
        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
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
        """
      ┌───────┐┌───┐┌─┐
 q_0: ┤ Ry(π) ├┤ X ├┤M├─
      └───────┘└───┘└╥┘
 c: 1/═══════════════╩══
                     0  
        """
        inputA = inputA * math.pi

        circuit = QuantumCircuit(1,1)
        circuit.ry(inputA,0)
        circuit.x(0)
        circuit.measure_all()
        print("Quantum NOT circuit")        
        print(circuit)
    
        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)
            
        qubit0 = 0

        for result in memory:
            qubit0 = qubit0 + int(result[0])

        qubit0 = qubit0/shots

        return int(round(qubit0))

    def myxor(self,inputA,inputB):
        """
      ┌───────┐     ┌─┐
 q_0: ┤ Ry(π) ├──■──┤M├────
      ├───────┤┌─┴─┐└╥┘┌─┐
 q_1: ┤ Ry(0) ├┤ X ├─╫─┤M├─
      └───────┘└───┘ ║ └╥┘
c:  2/═══════════════╩══╩══
                     0  1    
        """                           
        inputA = inputA * math.pi
        inputB = inputB * math.pi

        circuit = QuantumCircuit(2,2)
        circuit.ry(inputA,0)
        circuit.ry(inputB,1)
        circuit.cx(0,1)
        circuit.measure_all()
        print("Quantum XOR circuit")
        print(circuit)
 
        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)
        
        qubit0 = 0
        qubit1 = 0

        for result in memory:
            qubit0 = qubit0 + int(result[0])
            qubit1 = qubit1 + int(result[1])

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots

        return int(round(qubit0))

    def myor(self,inputA,inputB):
        """
      ┌───────┐                     ░ ┌─┐
 q_0: ┤ Ry(0) ├──■──────────────■───░─┤M├──────────
      └───────┘┌─┴─┐┌───┐       │   ░ └╥┘┌─┐
 q_1: ─────────┤ X ├┤ X ├───────■───░──╫─┤M├───────
      ┌───────┐└───┘└─┬─┘       │   ░  ║ └╥┘┌─┐
 q_2: ┤ Ry(0) ├───────■────■────┼───░──╫──╫─┤M├────
      └───────┘          ┌─┴─┐┌─┴─┐ ░  ║  ║ └╥┘┌─┐
 q_3: ───────────────────┤ X ├┤ X ├─░──╫──╫──╫─┤M├─
                         └───┘└───┘ ░  ║  ║  ║ └╥┘       
c:  4/═════════════════════════════════╩══╩══╩══╩══
                     0  1  2  3
        """
        inputA = inputA * math.pi
        inputB = inputB * math.pi

        circuit = QuantumCircuit(4,4)
        circuit.ry(inputA,0)
        circuit.ry(inputB,2)
        circuit.cx(0,1)
        circuit.cx(2,1)
        circuit.cx(2,3)
        circuit.ccx(1,0,3)
        circuit.measure_all()
        print("Quantum OR circuit")
        print(circuit)
 
        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
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

    def myif(self,inputA):
        """
      ┌───────┐     ┌─┐
 q_0: ┤ Ry(π) ├──■──┤M├────
      └───────┘┌─┴─┐└╥┘┌─┐
 q_1: ─────────┤ X ├─╫─┤M├─
               └───┘ ║ └╥┘
c:  2/═══════════════╩══╩══
                     0  1    
        """        
        inputA = int(inputA) * math.pi

        circuit = QuantumCircuit(2,2)
        circuit.ry(inputA,0)
        circuit.cx(0,1)
        circuit.measure_all()
        print("Quantum if circuit")
        print(circuit)
  
        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)
            
        qubit0 = 0
        qubit1 = 0

        for result in memory:
            qubit0 = qubit0 + int(result[0])
            qubit1 = qubit1 + int(result[1])

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots

        return round(qubit1)

#****************************************************************************************************************************************************************************
#****************************************************************************************************************************************************************************
#************************************************************************* Quantum circuits *********************************************************************************
#****************************************************************************************************************************************************************************
#****************************************************************************************************************************************************************************
    
    def myQuantum8BitInc(self,input7,input6,input5,input4,input3,input2,input1,input0,carry):
            """
      ┌───────┐           ░                     ░                     ░                     ░                     ░                     ░                     ░                     ░ ┌─┐
 q_0: ┤ Ry(π) ├──■────■───░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─┤M├────────────────────────────────────────────────
      ├───────┤  │  ┌─┴─┐ ░                     ░                     ░                     ░                     ░                     ░                     ░                     ░ └╥┘┌─┐
 q_1: ┤ Ry(π) ├──■──┤ X ├─░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░──╫─┤M├─────────────────────────────────────────────
      └───────┘┌─┴─┐└───┘ ░                     ░                     ░                     ░                     ░                     ░                     ░                     ░  ║ └╥┘┌─┐
 q_2: ─────────┤ X ├──────░────────────■────■───░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░──╫──╫─┤M├──────────────────────────────────────────
               └───┘      ░ ┌───────┐  │  ┌─┴─┐ ░                     ░                     ░                     ░                     ░                     ░                     ░  ║  ║ └╥┘┌─┐
 q_3: ────────────────────░─┤ Ry(π) ├──■──┤ X ├─░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░──╫──╫──╫─┤M├───────────────────────────────────────
                          ░ └───────┘┌─┴─┐└───┘ ░                     ░                     ░                     ░                     ░                     ░                     ░  ║  ║  ║ └╥┘┌─┐
 q_4: ────────────────────░──────────┤ X ├──────░────────────■────■───░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░──╫──╫──╫──╫─┤M├────────────────────────────────────
                          ░          └───┘      ░ ┌───────┐  │  ┌─┴─┐ ░                     ░                     ░                     ░                     ░                     ░  ║  ║  ║  ║ └╥┘┌─┐
 q_5: ────────────────────░─────────────────────░─┤ Ry(π) ├──■──┤ X ├─░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░──╫──╫──╫──╫──╫─┤M├─────────────────────────────────
                          ░                     ░ └───────┘┌─┴─┐└───┘ ░                     ░                     ░                     ░                     ░                     ░  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ────────────────────░─────────────────────░──────────┤ X ├──────░────────────■────■───░─────────────────────░─────────────────────░─────────────────────░─────────────────────░──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────
                          ░                     ░          └───┘      ░ ┌───────┐  │  ┌─┴─┐ ░                     ░                     ░                     ░                     ░  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ────────────────────░─────────────────────░─────────────────────░─┤ Ry(0) ├──■──┤ X ├─░─────────────────────░─────────────────────░─────────────────────░─────────────────────░──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────
                          ░                     ░                     ░ └───────┘┌─┴─┐└───┘ ░                     ░                     ░                     ░                     ░  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_8: ────────────────────░─────────────────────░─────────────────────░──────────┤ X ├──────░────────────■────■───░─────────────────────░─────────────────────░─────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────
                          ░                     ░                     ░          └───┘      ░ ┌───────┐  │  ┌─┴─┐ ░                     ░                     ░                     ░  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_9: ────────────────────░─────────────────────░─────────────────────░─────────────────────░─┤ Ry(0) ├──■──┤ X ├─░─────────────────────░─────────────────────░─────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────
                          ░                     ░                     ░                     ░ └───────┘┌─┴─┐└───┘ ░                     ░                     ░                     ░  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_10: ────────────────────░─────────────────────░─────────────────────░─────────────────────░──────────┤ X ├──────░────────────■────■───░─────────────────────░─────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────
                          ░                     ░                     ░                     ░          └───┘      ░ ┌───────┐  │  ┌─┴─┐ ░                     ░                     ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_11: ────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─┤ Ry(0) ├──■──┤ X ├─░─────────────────────░─────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────
                          ░                     ░                     ░                     ░                     ░ └───────┘┌─┴─┐└───┘ ░                     ░                     ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_12: ────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░──────────┤ X ├──────░────────────■────■───░─────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────
                          ░                     ░                     ░                     ░                     ░          └───┘      ░ ┌───────┐  │  ┌─┴─┐ ░                     ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_13: ────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─┤ Ry(π) ├──■──┤ X ├─░─────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────
                          ░                     ░                     ░                     ░                     ░                     ░ └───────┘┌─┴─┐└───┘ ░                     ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_14: ────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░──────────┤ X ├──────░────────────■────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
                          ░                     ░                     ░                     ░                     ░                     ░          └───┘      ░ ┌───────┐  │  ┌─┴─┐ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_15: ────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─┤ Ry(0) ├──■──┤ X ├─░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
                          ░                     ░                     ░                     ░                     ░                     ░                     ░ └───────┘┌─┴─┐└───┘ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_16: ────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░─────────────────────░──────────┤ X ├──────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
                          ░                     ░                     ░                     ░                     ░                     ░                     ░          └───┘      ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 17/═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
                                                                                                                                                                                       0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16
            """         
            incrementbit = int(carry) * math.pi
            input0 = int(input0) * math.pi
            input1 = int(input1) * math.pi
            input2 = int(input2) * math.pi
            input3 = int(input3) * math.pi
            input4 = int(input4) * math.pi
            input5 = int(input5) * math.pi
            input6 = int(input6) * math.pi
            input7 = int(input7) * math.pi

             
            circuit = QuantumCircuit(17,17)

            #Bit 0
            circuit.ry(incrementbit,0)
            circuit.ry(input0,1)
            #AND 
            circuit.ccx(1,0,2)
            #XOR
            circuit.cx(0,1)
            circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
             
            #bit 1
            circuit.ry(input1,3)
            #AND 
            circuit.ccx(3,2,4)
            #xor
            circuit.cx(2,3)
            # AND1 
            circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)

            #bit 2
            circuit.ry(input2,5)
            #AND 
            circuit.ccx(5,4,6)
            #xor
            circuit.cx(4,5)
            # AND1 
            circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)

            #bit 3
            circuit.ry(input3,7)
            #AND 
            circuit.ccx(7,6,8)
            #xor
            circuit.cx(6,7)
            # AND1 
            circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)

            #bit 4
            circuit.ry(input4,9)
            #AND 
            circuit.ccx(9,8,10)
            #xor
            circuit.cx(8,9)
            # AND1 
            circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)

            #bit 5
            circuit.ry(input5,11)
            #AND 
            circuit.ccx(11,10,12)
            #xor
            circuit.cx(10,11)
            # AND1 
            circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)

            #bit 6
            circuit.ry(input6,13)
            #AND 
            circuit.ccx(13,12,14)
            #xor
            circuit.cx(12,13)
            # AND1 
            circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)

            #bit 7
            circuit.ry(input7,15)
            #AND 
            circuit.ccx(15,14,16)
            #xor
            circuit.cx(14,15)
            # AND1 
            circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)


            circuit.measure_all()
            
            
            print("Quantum increment circuit")
            print(circuit)

            shots = self.shots
            QuantumComputer = self.QuantumComputer
            circuit = transpile(circuit, QuantumComputer)
            result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
            memory = result.get_memory(circuit)


            qubit0 = 0
            qubit1 = 0
            qubit2 = 0
            qubit3 = 0
            qubit4 = 0
            qubit5 = 0
            qubit6 = 0
            qubit7 = 0
            qubit8 = 0
            qubit9 = 0
            qubit10 = 0
            qubit11 = 0
            qubit12 = 0
            qubit13 = 0
            qubit14 = 0
            qubit15 = 0
            qubit16 = 0
 
            for result in memory:

                        qubit0 = qubit0 + int(result[16])
                        qubit1 = qubit1 + int(result[15])
                        qubit2 = qubit2 + int(result[14])
                        qubit3 = qubit3 + int(result[13])
                        qubit4 = qubit4 + int(result[12])
                        qubit5 = qubit5 + int(result[11])
                        qubit6 = qubit6 + int(result[10])
                        qubit7 = qubit7 + int(result[9])
                        qubit8 = qubit8 + int(result[8])
                        qubit9 = qubit9 + int(result[7])
                        qubit10 = qubit10 + int(result[6])
                        qubit11 = qubit11 + int(result[5])
                        qubit12 = qubit12 + int(result[4])
                        qubit13 = qubit13 + int(result[3])
                        qubit14 = qubit14 + int(result[2])
                        qubit15 = qubit15 + int(result[1])
                        qubit16 = qubit16 + int(result[0])
 
            qubit0 = qubit0/shots
            qubit1 = qubit1/shots
            qubit2 = qubit2/shots
            qubit3 = qubit3/shots
            qubit4 = qubit4/shots
            qubit5 = qubit5/shots
            qubit6 = qubit6/shots
            qubit7 = qubit7/shots
            qubit8 = qubit8/shots
            qubit9 = qubit9/shots
            qubit10 = qubit10/shots
            qubit11 = qubit11/shots
            qubit12 = qubit12/shots
            qubit13 = qubit13/shots
            qubit14 = qubit14/shots
            qubit15 = qubit15/shots
            qubit16 = qubit16/shots


            #print(" qubit 0 = " + str(int(qubit0)) + " qubit 1 = " + str(int(qubit1)) + " qubit 2 = " + str(int(qubit2)) + " qubit 3 = " + str(int(qubit3)) + " qubit 4 = " + str(int(qubit4)) + " qubit 5 = " + str(int(qubit5)) + " qubit 6 = " + str(int(qubit6)) + " qubit 7 = " + str(int(qubit7)))

            return str(round(qubit16)) + str(round(qubit15)) + str(round(qubit13)) + str(round(qubit11)) + str(round(qubit9)) + str(round(qubit7)) + str(round(qubit5)) + str(round(qubit3)) + str(round(qubit1))

    def myQuantum8BitIncWithFlags(self,input7,input6,input5,input4,input3,input2,input1,input0):
   
        incrementbit = math.pi
        input0 = int(input0) * math.pi
        input1 = int(input1) * math.pi
        input2 = int(input2) * math.pi
        input3 = int(input3) * math.pi
        input4 = int(input4) * math.pi
        input5 = int(input5) * math.pi
        input6 = int(input6) * math.pi
        input7 = int(input7) * math.pi
         
        circuit = QuantumCircuit(31,31)

        #Bit 0
        circuit.ry(incrementbit,0)
        circuit.ry(input0,1)
        #AND 
        circuit.ccx(1,0,2)
        #XOR
        circuit.cx(0,1)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)
         
        #bit 1
        circuit.ry(input1,3)
        #AND 
        circuit.ccx(3,2,4)
        #xor
        circuit.cx(2,3)
        # AND1 
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)

        #bit 2
        circuit.ry(input2,5)
        #AND 
        circuit.ccx(5,4,6)
        #xor
        circuit.cx(4,5)
        # AND1 
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)

        #bit 3
        circuit.ry(input3,7)
        #AND 
        circuit.ccx(7,6,8)
        #xor
        circuit.cx(6,7)
        # AND1 
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)

        #bit 4
        circuit.ry(input4,9)
        #AND 
        circuit.ccx(9,8,10)
        #xor
        circuit.cx(8,9)
        # AND1 
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)

        #bit 5
        circuit.ry(input5,11)
        #AND 
        circuit.ccx(11,10,12)
        #xor
        circuit.cx(10,11)
        # AND1 
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)

        #bit 6
        circuit.ry(input6,13)
        #AND 
        circuit.ccx(13,12,14)
        #xor
        circuit.cx(12,13)
        # AND1 
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)

        #bit 7
        circuit.ry(input7,15)
        #AND 
        circuit.ccx(15,14,16)
        #xor
        circuit.cx(14,15)
        # AND1 
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)
        
        #F register
        #N flag
        circuit.ry(0,17)

        
        circuit.cx(1,18)
        circuit.cx(3,19)
        circuit.cx(5,20)
        circuit.cx(7,21)            
        circuit.cx(9,22)
        circuit.cx(11,23)
        circuit.cx(13,24)
        circuit.cx(15,25) 
        
        circuit.x(18)
        circuit.x(19)
        circuit.x(20)
        circuit.x(21)
        circuit.x(22)
        circuit.x(23)
        circuit.x(24)
        circuit.x(25)
        
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)
        
        circuit.append(C4XGate(), [18,19,20,21,26])

        circuit.append(C4XGate(), [22,23,24,25,27])
        
        circuit.ccx(26,27,28)

        circuit.x(25)
        circuit.append(C4XGate(), [22,23,24,25,29])            
        circuit.x(25)
        circuit.ccx(26,29,30)
        
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)            


        circuit.measure_all()
        

        print(circuit)
  

        shots = self.shots
        
        circuit.measure_all()

        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)


        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0
        qubit8 = 0
        qubit9 = 0
        qubit10 = 0
        qubit11 = 0
        qubit12 = 0
        qubit13 = 0
        qubit14 = 0
        qubit15 = 0
        qubit16 = 0
        qubit17 = 0
        qubit18 = 0
        qubit19 = 0
        qubit20 = 0
        qubit21 = 0
        qubit22 = 0
        qubit23 = 0
        qubit24 = 0
        qubit25 = 0
        qubit26 = 0
        qubit27 = 0
        qubit28 = 0
        qubit29 = 0
        qubit30 = 0
        
        for result in memory:



                    qubit0 = qubit0 + int(result[30])
                    qubit1 = qubit1 + int(result[29])
                    qubit2 = qubit2 + int(result[28])
                    qubit3 = qubit3 + int(result[27])
                    qubit4 = qubit4 + int(result[26])
                    qubit5 = qubit5 + int(result[25])
                    qubit6 = qubit6 + int(result[24])
                    qubit7 = qubit7 + int(result[23])
                    qubit8 = qubit8 + int(result[22])
                    qubit9 = qubit9 + int(result[21])
                    qubit10 = qubit10 + int(result[20])
                    qubit11 = qubit11 + int(result[19])
                    qubit12 = qubit12 + int(result[18])
                    qubit13 = qubit13 + int(result[17])
                    qubit14 = qubit14 + int(result[16])
                    qubit15 = qubit15 + int(result[15])
                    qubit16 = qubit16 + int(result[14])
                    qubit17 = qubit17 + int(result[13])
                    qubit18 = qubit18 + int(result[12])
                    qubit19 = qubit19 + int(result[11])
                    qubit20 = qubit20 + int(result[10])
                    qubit21 = qubit21 + int(result[9])
                    qubit22 = qubit22 + int(result[8])
                    qubit23 = qubit23 + int(result[7]) 
                    qubit24 = qubit24 + int(result[6])
                    qubit25 = qubit25 + int(result[5])
                    qubit26 = qubit26 + int(result[4])
                    qubit27 = qubit27 + int(result[3])
                    qubit28 = qubit28 + int(result[2])
                    qubit29 = qubit29 + int(result[1])
                    qubit30 = qubit30 + int(result[0])                        

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots
        qubit8 = qubit8/shots
        qubit9 = qubit9/shots
        qubit10 = qubit10/shots
        qubit11 = qubit11/shots
        qubit12 = qubit12/shots
        qubit13 = qubit13/shots
        qubit14 = qubit14/shots
        qubit15 = qubit15/shots
        qubit16 = qubit16/shots
        qubit17 = qubit17/shots
        qubit18 = qubit18/shots
        qubit19 = qubit19/shots
        qubit20 = qubit20/shots
        qubit21 = qubit21/shots
        qubit22 = qubit22/shots
        qubit23 = qubit23/shots
        qubit24 = qubit24/shots
        qubit25 = qubit25/shots
        qubit26 = qubit26/shots
        qubit27 = qubit27/shots
        qubit28 = qubit28/shots
        qubit29 = qubit29/shots
        qubit30 = qubit30/shots

        return str(round(qubit15)) + str(round(qubit13)) + str(round(qubit11)) + str(round(qubit9)) + str(round(qubit7)) + str(round(qubit5)) + str(round(qubit3)) + str(round(qubit1)) + ":"  + str(round(qubit15)) + str(round(qubit28)) + str(round(qubit26)) + str(round(qubit30)) + str(round(qubit17)) + str(round(qubit16))

    def myQuantum4BitDec(self,inputA3,inputA2,inputA1,inputA0,borrow):
        """
      ┌───────┐                                    ░                                              ░                                              ░                                              ░ ┌─┐
 q_0: ┤ Ry(π) ├──■────■────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░─┤M├────────────────────────────────────────────────────────────────────────
      ├───────┤  │  ┌─┴─┐                          ░                                              ░                                              ░                                              ░ └╥┘┌─┐
 q_1: ┤ Ry(0) ├──■──┤ X ├──■────■──────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫─┤M├─────────────────────────────────────────────────────────────────────
      └───────┘┌─┴─┐└───┘  │    │                  ░                                              ░                                              ░                                              ░  ║ └╥┘┌─┐
 q_2: ─────────┤ X ├───────┼────┼────■────■────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫─┤M├──────────────────────────────────────────────────────────────────
      ┌───────┐└───┘       │  ┌─┴─┐  │    │        ░                                              ░                                              ░                                              ░  ║  ║ └╥┘┌─┐
 q_3: ┤ Ry(0) ├────────────■──┤ X ├──┼────┼────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫─┤M├───────────────────────────────────────────────────────────────
      └───────┘          ┌─┴─┐└───┘  │    │        ░                                              ░                                              ░                                              ░  ║  ║  ║ └╥┘┌─┐
 q_4: ───────────────────┤ X ├──■────┼────┼────■───░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫─┤M├────────────────────────────────────────────────────────────
                         └───┘┌─┴─┐┌─┴─┐  │    │   ░                                              ░                                              ░                                              ░  ║  ║  ║  ║ └╥┘┌─┐
 q_5: ────────────────────────┤ X ├┤ X ├──┼────■───░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────────────────
                              └───┘└───┘┌─┴─┐┌─┴─┐ ░                         ┌───┐                ░                                              ░                                              ░  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ──────────────────────────────────┤ X ├┤ X ├─░──────────────────────■──┤ X ├────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────────────────
                                        └───┘└───┘ ░ ┌───────┐            │  └─┬─┘                ░                                              ░                                              ░  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ─────────────────────────────────────────────░─┤ Ry(π) ├──■────■────┼────┼──────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────────────────
                                                   ░ ├───────┤  │  ┌─┴─┐  │    │                  ░                                              ░                                              ░  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_8: ─────────────────────────────────────────────░─┤ Ry(0) ├──■──┤ X ├──■────■──────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────────────────
                                                   ░ └───────┘┌─┴─┐└───┘  │                       ░                                              ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_9: ─────────────────────────────────────────────░──────────┤ X ├───────┼─────────■────■────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────
                                                   ░          └───┘     ┌─┴─┐       │    │        ░                                              ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_10: ─────────────────────────────────────────────░────────────────────┤ X ├──■────┼────┼────■───░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────
                                                   ░                    └───┘┌─┴─┐┌─┴─┐  │    │   ░                                              ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_11: ─────────────────────────────────────────────░─────────────────────────┤ X ├┤ X ├──┼────■───░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────
                                                   ░                         └───┘└───┘┌─┴─┐┌─┴─┐ ░                         ┌───┐                ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_12: ─────────────────────────────────────────────░───────────────────────────────────┤ X ├┤ X ├─░──────────────────────■──┤ X ├────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────
                                                   ░                                   └───┘└───┘ ░ ┌───────┐            │  └─┬─┘                ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_13: ─────────────────────────────────────────────░──────────────────────────────────────────────░─┤ Ry(π) ├──■────■────┼────┼──────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────
                                                   ░                                              ░ ├───────┤  │  ┌─┴─┐  │    │                  ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_14: ─────────────────────────────────────────────░──────────────────────────────────────────────░─┤ Ry(0) ├──■──┤ X ├──■────■──────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────
                                                   ░                                              ░ └───────┘┌─┴─┐└───┘  │                       ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_15: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────┤ X ├───────┼─────────■────■────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────
                                                   ░                                              ░          └───┘     ┌─┴─┐       │    │        ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_16: ─────────────────────────────────────────────░──────────────────────────────────────────────░────────────────────┤ X ├──■────┼────┼────■───░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────
                                                   ░                                              ░                    └───┘┌─┴─┐┌─┴─┐  │    │   ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_17: ─────────────────────────────────────────────░──────────────────────────────────────────────░─────────────────────────┤ X ├┤ X ├──┼────■───░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────
                                                   ░                                              ░                         └───┘└───┘┌─┴─┐┌─┴─┐ ░                         ┌───┐                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_18: ─────────────────────────────────────────────░──────────────────────────────────────────────░───────────────────────────────────┤ X ├┤ X ├─░──────────────────────■──┤ X ├────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────
                                                   ░                                              ░                                   └───┘└───┘ ░ ┌───────┐            │  └─┬─┘                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_19: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░─┤ Ry(π) ├──■────■────┼────┼──────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────
                                                   ░                                              ░                                              ░ ├───────┤  │  ┌─┴─┐  │    │                  ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_20: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░─┤ Ry(π) ├──■──┤ X ├──■────■──────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────
                                                   ░                                              ░                                              ░ └───────┘┌─┴─┐└───┘  │                       ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_21: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────┤ X ├───────┼─────────■────■────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────
                                                   ░                                              ░                                              ░          └───┘     ┌─┴─┐       │    │        ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_22: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░────────────────────┤ X ├──■────┼────┼────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
                                                   ░                                              ░                                              ░                    └───┘┌─┴─┐┌─┴─┐  │    │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_23: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░─────────────────────────┤ X ├┤ X ├──┼────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
                                                   ░                                              ░                                              ░                         └───┘└───┘┌─┴─┐┌─┴─┐ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_24: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░───────────────────────────────────┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
                                                   ░                                              ░                                              ░                                   └───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 25/═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
                                                                                                                                                                                                   0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
    """ 
        carrybit = int(borrow) * math.pi
        inputA0 = int(inputA0) * math.pi
        inputA1 = int(inputA1) * math.pi
        inputA2 = int(inputA2) * math.pi
        inputA3 = int(inputA3) * math.pi
    
        
        
        circuit = QuantumCircuit(25,25)
        #Bit 0
        circuit.ry(math.pi,0)
        circuit.ry(inputA0,1)
        circuit.ry(carrybit,3)

        #AND1
        circuit.ccx(1,0,2)
        #XOR1
        circuit.cx(0,1)
        #AND2
        circuit.ccx(3,1,4)
        #XOR2
        circuit.cx(1,3)
        #OR1
        circuit.cx(4,5)
        circuit.cx(2,5)
        circuit.cx(2,6)
        circuit.ccx(4,5,6)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
        
        
        #Bit 1
        circuit.ry(math.pi,7)
        circuit.ry(inputA1,8)

        #AND1
        circuit.ccx(8,7,9)
        #XOR1
        circuit.cx(7,8)
        #AND2
        circuit.ccx(6,8,10)
        #XOR2
        circuit.cx(8,6)
        #OR1
        circuit.cx(10,11)
        circuit.cx(9,11)
        circuit.cx(9,12)
        circuit.ccx(10,11,12)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
    
        
        #Bit 2
        circuit.ry(math.pi,13)
        circuit.ry(inputA2,14)
        
        #AND1
        circuit.ccx(14,13,15)  
        #XOR1
        circuit.cx(13,14)
        #AND2
        circuit.ccx(12,14,16)
        #XOR2
        circuit.cx(14,12)
        #OR1
        circuit.cx(16,17)
        circuit.cx(15,17)
        circuit.cx(15,18)
        circuit.ccx(16,17,18)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
        
        #Bit 3
        circuit.ry(math.pi,19)
        circuit.ry(inputA3,20)
        
        #AND1
        circuit.ccx(20,19,21)  
        #XOR1
        circuit.cx(19,20)
        #AND2
        circuit.ccx(18,20,22)
        #XOR2
        circuit.cx(20,18)
        #OR1
        circuit.cx(22,23)
        circuit.cx(21,23)
        circuit.cx(21,24)
        circuit.ccx(22,23,24)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)

        circuit.measure_all()
        
        print("Quantum decrement circuit")    
        print(circuit)
    
        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0
        qubit8 = 0
        qubit9 = 0
        qubit10 = 0
        qubit11 = 0
        qubit12 = 0
        qubit13 = 0
        qubit14 = 0
        qubit15 = 0
        qubit16 = 0
        qubit17 = 0
        qubit18 = 0
        qubit19 = 0
        qubit20 = 0
        qubit21 = 0
        qubit22 = 0
        qubit23 = 0
        qubit24 = 0

    
        for result in memory:

            qubit0 = qubit0 + int(result[24])
            qubit1 = qubit1 + int(result[23])
            qubit2 = qubit2 + int(result[22])
            qubit3 = qubit3 + int(result[21])
            qubit4 = qubit4 + int(result[20])
            qubit5 = qubit5 + int(result[19])
            qubit6 = qubit6 + int(result[18])
            qubit7 = qubit7 + int(result[17])
            qubit8 = qubit8 + int(result[16])
            qubit9 = qubit9 + int(result[15])
            qubit10 = qubit10 + int(result[14])
            qubit11 = qubit11 + int(result[13])
            qubit12 = qubit12 + int(result[12])
            qubit13 = qubit13 + int(result[11])
            qubit14 = qubit14 + int(result[10])
            qubit15 = qubit15 + int(result[9])
            qubit16 = qubit16 + int(result[8])
            qubit17 = qubit17 + int(result[7])
            qubit18 = qubit18 + int(result[6])
            qubit19 = qubit19 + int(result[5])
            qubit20 = qubit20 + int(result[4])
            qubit21 = qubit21 + int(result[3])
            qubit22 = qubit22 + int(result[2])
            qubit23 = qubit23 + int(result[1])
            qubit24 = qubit24 + int(result[0])

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots
        qubit8 = qubit8/shots
        qubit9 = qubit9/shots
        qubit10 = qubit10/shots
        qubit11 = qubit11/shots
        qubit12 = qubit12/shots
        qubit13 = qubit13/shots
        qubit14 = qubit14/shots
        qubit15 = qubit15/shots
        qubit16 = qubit16/shots
        qubit17 = qubit17/shots
        qubit18 = qubit18/shots
        qubit19 = qubit19/shots
        qubit20 = qubit20/shots
        qubit21 = qubit21/shots
        qubit22 = qubit22/shots
        qubit23 = qubit23/shots
        qubit24 = qubit24/shots

        #4 bit + borrow bit on qubit 24
        return str(round(qubit24)) + str(round(qubit18)) + str(round(qubit12)) + str(round(qubit6)) + str(round(qubit3))

    def myQuantum8BitXor(self,inputA7,inputA6,inputA5,inputA4,inputA3,inputA2,inputA1,inputA0,inputB7,inputB6,inputB5,inputB4,inputB3,inputB2,inputB1,inputB0):
        """
      ┌───────┐     ┌─┐
 q_0: ┤ Ry(π) ├──■──┤M├─────────────────────────────────────────────
      ├───────┤┌─┴─┐└╥┘┌─┐
 q_1: ┤ Ry(0) ├┤ X ├─╫─┤M├──────────────────────────────────────────
      ├───────┤└───┘ ║ └╥┘┌─┐
 q_2: ┤ Ry(0) ├──■───╫──╫─┤M├───────────────────────────────────────
      ├───────┤┌─┴─┐ ║  ║ └╥┘┌─┐
 q_3: ┤ Ry(0) ├┤ X ├─╫──╫──╫─┤M├────────────────────────────────────
      ├───────┤└───┘ ║  ║  ║ └╥┘┌─┐
 q_4: ┤ Ry(π) ├──■───╫──╫──╫──╫─┤M├─────────────────────────────────
      ├───────┤┌─┴─┐ ║  ║  ║  ║ └╥┘┌─┐
 q_5: ┤ Ry(0) ├┤ X ├─╫──╫──╫──╫──╫─┤M├──────────────────────────────
      ├───────┤└───┘ ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ┤ Ry(0) ├──■───╫──╫──╫──╫──╫──╫─┤M├───────────────────────────
      ├───────┤┌─┴─┐ ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ┤ Ry(0) ├┤ X ├─╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────
      ├───────┤└───┘ ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_8: ┤ Ry(π) ├──■───╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────
      ├───────┤┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_9: ┤ Ry(π) ├┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────
      ├───────┤└───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_10: ┤ Ry(0) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────
      ├───────┤┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_11: ┤ Ry(π) ├┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────
      ├───────┤└───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_12: ┤ Ry(π) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────
      ├───────┤┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_13: ┤ Ry(π) ├┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
      ├───────┤└───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_14: ┤ Ry(0) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
      ├───────┤┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_15: ┤ Ry(π) ├┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
      └───────┘└───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 16/═══════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
                     0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
        """    
        inputA0 = int(inputA0) * math.pi
        inputA1 = int(inputA1) * math.pi
        inputA2 = int(inputA2) * math.pi
        inputA3 = int(inputA3) * math.pi
        inputA4 = int(inputA4) * math.pi
        inputA5 = int(inputA5) * math.pi
        inputA6 = int(inputA6) * math.pi
        inputA7 = int(inputA7) * math.pi

        inputB0 = int(inputB0) * math.pi
        inputB1 = int(inputB1) * math.pi
        inputB2 = int(inputB2) * math.pi
        inputB3 = int(inputB3) * math.pi
        inputB4 = int(inputB4) * math.pi
        inputB5 = int(inputB5) * math.pi
        inputB6 = int(inputB6) * math.pi
        inputB7 = int(inputB7) * math.pi

         
        circuit = QuantumCircuit(16,16)

        #Bit 0
        circuit.ry(inputA0,0)
        circuit.ry(inputB0,1)
        #XOR 
        circuit.cx(0,1)
        
        #Bit 1
        circuit.ry(inputA1,2)
        circuit.ry(inputB1,3)
        #XOR
        circuit.cx(2,3)
        
        #Bit 2
        circuit.ry(inputA2,4)
        circuit.ry(inputB2,5)
        #XOR
        circuit.cx(4,5)
        
        #Bit 3
        circuit.ry(inputA3,6)
        circuit.ry(inputB3,7)
        #XOR 
        circuit.cx(6,7)

        #Bit 4
        circuit.ry(inputA4,8)
        circuit.ry(inputB4,9)
        #XOR 
        circuit.cx(8,9)
        
        #Bit 5
        circuit.ry(inputA5,10)
        circuit.ry(inputB5,11)
        #XOR 
        circuit.cx(10,11)
        
        #Bit 6
        circuit.ry(inputA6,12)
        circuit.ry(inputB6,13)
        #XOR 
        circuit.cx(12,13)
        
        #Bit 7
        circuit.ry(inputA7,14)
        circuit.ry(inputB7,15)
        #XOR 
        circuit.cx(14,15)
            
            
        circuit.measure_all()
        print("Quantum XOR circuit")
        print(circuit)

        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)
        
        #print(memory)
        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0
        qubit8 = 0
        qubit9 = 0
        qubit10 = 0
        qubit11 = 0
        qubit12 = 0
        qubit13 = 0
        qubit14 = 0
        qubit15 = 0
        
        for result in memory:

            qubit0 = qubit0 + int(result[15])
            qubit1 = qubit1 + int(result[14])
            qubit2 = qubit2 + int(result[13])
            qubit3 = qubit3 + int(result[12])
            qubit4 = qubit4 + int(result[11])
            qubit5 = qubit5 + int(result[10])
            qubit6 = qubit6 + int(result[9])
            qubit7 = qubit7 + int(result[8])
            qubit8 = qubit8 + int(result[7])
            qubit9 = qubit9 + int(result[6])
            qubit10 = qubit10 + int(result[5])
            qubit11 = qubit11 + int(result[4])
            qubit12 = qubit12 + int(result[3])
            qubit13 = qubit13 + int(result[2])
            qubit14 = qubit14 + int(result[1])
            qubit15 = qubit15 + int(result[0])

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots
        qubit8 = qubit8/shots
        qubit9 = qubit9/shots
        qubit10 = qubit10/shots
        qubit11 = qubit11/shots
        qubit12 = qubit12/shots
        qubit13 = qubit13/shots
        qubit14 = qubit14/shots
        qubit15 = qubit15/shots
        
            
          
        return str(round(qubit15)) + str(round(qubit13)) + str(round(qubit11)) + str(round(qubit9)) + str(round(qubit7)) + str(round(qubit5)) + str(round(qubit3)) + str(round(qubit1))

    def myQuantum8BitAnd(self,inputA7,inputA6,inputA5,inputA4,inputA3,inputA2,inputA1,inputA0,inputB7,inputB6,inputB5,inputB4,inputB3,inputB2,inputB1,inputB0):
        """
      ┌───────┐     ┌─┐
 q_0: ┤ Ry(π) ├──■──┤M├─────────────────────────────────────────────────────────────────────
      ├───────┤  │  └╥┘┌─┐
 q_1: ┤ Ry(0) ├──■───╫─┤M├──────────────────────────────────────────────────────────────────
      └───────┘┌─┴─┐ ║ └╥┘┌─┐
 q_2: ─────────┤ X ├─╫──╫─┤M├───────────────────────────────────────────────────────────────
      ┌───────┐└───┘ ║  ║ └╥┘┌─┐
 q_3: ┤ Ry(0) ├──■───╫──╫──╫─┤M├────────────────────────────────────────────────────────────
      ├───────┤  │   ║  ║  ║ └╥┘┌─┐
 q_4: ┤ Ry(0) ├──■───╫──╫──╫──╫─┤M├─────────────────────────────────────────────────────────
      └───────┘┌─┴─┐ ║  ║  ║  ║ └╥┘┌─┐
 q_5: ─────────┤ X ├─╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────────────────
      ┌───────┐└───┘ ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ┤ Ry(π) ├──■───╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────────────────
      ├───────┤  │   ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ┤ Ry(0) ├──■───╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────────────────
      └───────┘┌─┴─┐ ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_8: ─────────┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────
      ┌───────┐└───┘ ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_9: ┤ Ry(0) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────
      ├───────┤  │   ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_10: ┤ Ry(0) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────
      └───────┘┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_11: ─────────┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────
      ┌───────┐└───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_12: ┤ Ry(π) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────
      ├───────┤  │   ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_13: ┤ Ry(π) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────
      └───────┘┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_14: ─────────┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────
      ┌───────┐└───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_15: ┤ Ry(0) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────
      ├───────┤  │   ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_16: ┤ Ry(π) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────
      └───────┘┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_17: ─────────┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────
      ┌───────┐└───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_18: ┤ Ry(π) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────
      ├───────┤  │   ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_19: ┤ Ry(π) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────
      └───────┘┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_20: ─────────┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────
      ┌───────┐└───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_21: ┤ Ry(0) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
      ├───────┤  │   ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_22: ┤ Ry(π) ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
      └───────┘┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_23: ─────────┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
               └───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 24/═══════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
                     0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 17 18 19
        """
        inputA0 = int(inputA0) * math.pi
        inputA1 = int(inputA1) * math.pi
        inputA2 = int(inputA2) * math.pi
        inputA3 = int(inputA3) * math.pi
        inputA4 = int(inputA4) * math.pi
        inputA5 = int(inputA5) * math.pi
        inputA6 = int(inputA6) * math.pi
        inputA7 = int(inputA7) * math.pi

        inputB0 = int(inputB0) * math.pi
        inputB1 = int(inputB1) * math.pi
        inputB2 = int(inputB2) * math.pi
        inputB3 = int(inputB3) * math.pi
        inputB4 = int(inputB4) * math.pi
        inputB5 = int(inputB5) * math.pi
        inputB6 = int(inputB6) * math.pi
        inputB7 = int(inputB7) * math.pi

         
        circuit = QuantumCircuit(24,24)

        #Bit 0
        circuit.ry(inputA0,0)
        circuit.ry(inputB0,1)
        #AND 
        circuit.ccx(0,1,2)
        
        #Bit 1
        circuit.ry(inputA1,3)
        circuit.ry(inputB1,4)
        #AND 
        circuit.ccx(3,4,5)
        
        #Bit 2
        circuit.ry(inputA2,6)
        circuit.ry(inputB2,7)
        #AND 
        circuit.ccx(6,7,8)
        
        #Bit 3
        circuit.ry(inputA3,9)
        circuit.ry(inputB3,10)
        #AND 
        circuit.ccx(9,10,11)

        #Bit 4
        circuit.ry(inputA4,12)
        circuit.ry(inputB4,13)
        #AND 
        circuit.ccx(12,13,14)
        
        #Bit 5
        circuit.ry(inputA5,15)
        circuit.ry(inputB6,16)
        #AND 
        circuit.ccx(15,16,17)
        
        #Bit 6
        circuit.ry(inputA6,18)
        circuit.ry(inputB6,19)
        #AND 
        circuit.ccx(18,19,20)
        
        #Bit 7
        circuit.ry(inputA7,21)
        circuit.ry(inputB7,22)
        #AND 
        circuit.ccx(21,22,23)
        

        circuit.measure_all()
        print("Quantum AND circuit")            
        print(circuit)

        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0
        qubit8 = 0
        qubit9 = 0
        qubit10 = 0
        qubit11 = 0
        qubit12 = 0
        qubit13 = 0
        qubit14 = 0
        qubit15 = 0
        qubit16 = 0
        qubit17 = 0
        qubit18 = 0
        qubit19 = 0
        qubit20 = 0
        qubit21 = 0
        qubit22 = 0
        qubit23 = 0
        
        for result in memory:



                qubit0 = qubit0 + int(result[23])
                qubit1 = qubit1 + int(result[22])
                qubit2 = qubit2 + int(result[21])
                qubit3 = qubit3 + int(result[20])
                qubit4 = qubit4 + int(result[19])
                qubit5 = qubit5 + int(result[18])
                qubit6 = qubit6 + int(result[17])
                qubit7 = qubit7 + int(result[16])
                qubit8 = qubit8 + int(result[15])
                qubit9 = qubit9 + int(result[14])
                qubit10 = qubit10 + int(result[13])
                qubit11 = qubit11 + int(result[12])
                qubit12 = qubit12 + int(result[11])
                qubit13 = qubit13 + int(result[10])
                qubit14 = qubit14 + int(result[9])
                qubit15 = qubit15 + int(result[8])
                qubit16 = qubit16 + int(result[7])
                qubit17 = qubit17 + int(result[6])
                qubit18 = qubit18 + int(result[5])
                qubit19 = qubit19 + int(result[4])
                qubit20 = qubit20 + int(result[3])
                qubit21 = qubit21 + int(result[2])
                qubit22 = qubit22 + int(result[1])
                qubit23 = qubit23 + int(result[0])
                

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots
        qubit8 = qubit8/shots
        qubit9 = qubit9/shots
        qubit10 = qubit10/shots
        qubit11 = qubit11/shots
        qubit12 = qubit12/shots
        qubit13 = qubit13/shots
        qubit14 = qubit14/shots
        qubit15 = qubit15/shots
        qubit16 = qubit16/shots
        qubit17 = qubit17/shots
        qubit18 = qubit18/shots
        qubit19 = qubit19/shots
        qubit20 = qubit20/shots
        qubit21 = qubit21/shots
        qubit22 = qubit22/shots
        qubit23 = qubit23/shots

     

        return str(round(qubit23)) + str(round(qubit20)) + str(round(qubit17)) + str(round(qubit14)) + str(round(qubit11)) + str(round(qubit8)) + str(round(qubit5)) + str(round(qubit2))

    def myQuantum8BitOr(self,inputA7,inputA6,inputA5,inputA4,inputA3,inputA2,inputA1,inputA0,inputB7,inputB6,inputB5,inputB4,inputB3,inputB2,inputB1,inputB0):
        """
      ┌───────┐                     ░ ┌─┐
 q_0: ┤ Ry(0) ├──■──────────────■───░─┤M├─────────────────────────────────────────────────────────────────────────────────────────────
      └───────┘┌─┴─┐┌───┐       │   ░ └╥┘┌─┐
 q_1: ─────────┤ X ├┤ X ├───────■───░──╫─┤M├──────────────────────────────────────────────────────────────────────────────────────────
      ┌───────┐└───┘└─┬─┘       │   ░  ║ └╥┘┌─┐
 q_2: ┤ Ry(0) ├───────■────■────┼───░──╫──╫─┤M├───────────────────────────────────────────────────────────────────────────────────────
      └───────┘          ┌─┴─┐┌─┴─┐ ░  ║  ║ └╥┘┌─┐
 q_3: ───────────────────┤ X ├┤ X ├─░──╫──╫──╫─┤M├────────────────────────────────────────────────────────────────────────────────────
      ┌───────┐          └───┘└───┘ ░  ║  ║  ║ └╥┘┌─┐
 q_4: ┤ Ry(π) ├──■──────────────■───░──╫──╫──╫──╫─┤M├─────────────────────────────────────────────────────────────────────────────────
      └───────┘┌─┴─┐┌───┐       │   ░  ║  ║  ║  ║ └╥┘┌─┐
 q_5: ─────────┤ X ├┤ X ├───────■───░──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────────────────────────────────────────
      ┌───────┐└───┘└─┬─┘       │   ░  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ┤ Ry(0) ├───────■────■────┼───░──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────────────────────────────────────────
      └───────┘          ┌─┴─┐┌─┴─┐ ░  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ───────────────────┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────────────────────────────────────────
      ┌───────┐          └───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_8: ┤ Ry(0) ├──■──────────────■───░──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────────────────────────────
      └───────┘┌─┴─┐┌───┐       │   ░  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_9: ─────────┤ X ├┤ X ├───────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────────────────────────────
      ┌───────┐└───┘└─┬─┘       │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_10: ┤ Ry(0) ├───────■────■────┼───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────────────────────────────
      └───────┘          ┌─┴─┐┌─┴─┐ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_11: ───────────────────┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────────────────────────────
      ┌───────┐          └───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_12: ┤ Ry(π) ├──■──────────────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────────────────
      └───────┘┌─┴─┐┌───┐       │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_13: ─────────┤ X ├┤ X ├───────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────────────────
      ┌───────┐└───┘└─┬─┘       │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_14: ┤ Ry(0) ├───────■────■────┼───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────────────────
      └───────┘          ┌─┴─┐┌─┴─┐ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_15: ───────────────────┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────────────────
      ┌───────┐          └───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_16: ┤ Ry(0) ├──■──────────────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────
      └───────┘┌─┴─┐┌───┐       │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_17: ─────────┤ X ├┤ X ├───────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────
      ┌───────┐└───┘└─┬─┘       │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_18: ┤ Ry(1) ├───────■────■────┼───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────
      └───────┘          ┌─┴─┐┌─┴─┐ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_19: ───────────────────┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────
      ┌───────┐          └───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_20: ┤ Ry(1) ├──■──────────────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────
      └───────┘┌─┴─┐┌───┐       │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_21: ─────────┤ X ├┤ X ├───────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────
      ┌───────┐└───┘└─┬─┘       │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_22: ┤ Ry(1) ├───────■────■────┼───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────
      └───────┘          ┌─┴─┐┌─┴─┐ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_23: ───────────────────┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────
      ┌───────┐          └───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_24: ┤ Ry(0) ├──■──────────────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────
      └───────┘┌─┴─┐┌───┐       │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_25: ─────────┤ X ├┤ X ├───────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────
      ┌───────┐└───┘└─┬─┘       │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_26: ┤ Ry(1) ├───────■────■────┼───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────
      └───────┘          ┌─┴─┐┌─┴─┐ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_27: ───────────────────┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────
      ┌───────┐          └───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_28: ┤ Ry(1) ├──■──────────────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────
      └───────┘┌─┴─┐┌───┐       │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_29: ─────────┤ X ├┤ X ├───────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
      ┌───────┐└───┘└─┬─┘       │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_30: ┤ Ry(1) ├───────■────■────┼───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
      └───────┘          ┌─┴─┐┌─┴─┐ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_31: ───────────────────┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
                         └───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 32/═════════════════════════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
                           0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
        """
        inputA0 = int(inputA0) * math.pi
        inputA1 = int(inputA1) * math.pi
        inputA2 = int(inputA2) * math.pi
        inputA3 = int(inputA3) * math.pi
        inputA4 = int(inputA4) * math.pi
        inputA5 = int(inputA5) * math.pi
        inputA6 = int(inputA6) * math.pi
        inputA7 = int(inputA7) * math.pi

        inputB0 = int(inputB0) * math.pi
        inputB1 = int(inputB1) * math.pi
        inputB2 = int(inputB2) * math.pi
        inputB3 = int(inputB3) * math.pi
        inputB4 = int(inputB4) * math.pi
        inputB5 = int(inputB5) * math.pi
        inputB6 = int(inputB6) * math.pi
        inputB7 = int(inputB7) * math.pi
         
        circuit = QuantumCircuit(32,32)

        #Bit 0
        circuit.ry(inputA0,0)
        circuit.ry(inputB0,2)
        #OR 
        circuit.cx(0,1)
        circuit.cx(2,1)
        circuit.cx(2,3)
        circuit.ccx(0,1,3)
    
        #Bit 1
        circuit.ry(inputA1,4)
        circuit.ry(inputB1,6)
        #OR 
        circuit.cx(4,5)
        circuit.cx(6,5)
        circuit.cx(6,7)
        circuit.ccx(4,5,7)

        #Bit 2
        circuit.ry(inputA2,8)
        circuit.ry(inputB2,10)
        #OR 
        circuit.cx(8,9)
        circuit.cx(10,9)
        circuit.cx(10,11)
        circuit.ccx(8,9,11)

        #Bit 3
        circuit.ry(inputA3,12)
        circuit.ry(inputB3,14)
        #OR 
        circuit.cx(12,13)
        circuit.cx(14,13)
        circuit.cx(14,15)
        circuit.ccx(12,13,15)

            
        #Bit 4
        circuit.ry(inputA4,16)
        circuit.ry(inputB4,18)
        #OR 
        circuit.cx(16,17)
        circuit.cx(18,17)
        circuit.cx(18,19)
        circuit.ccx(16,17,19)
    
        #Bit 5
        circuit.ry(inputA5,20)
        circuit.ry(inputB5,22)
        #OR 
        circuit.cx(20,21)
        circuit.cx(22,21)
        circuit.cx(22,23)
        circuit.ccx(20,21,23)

        #Bit 6
        circuit.ry(inputA6,24)
        circuit.ry(inputB6,26)
        #OR 
        circuit.cx(24,25)
        circuit.cx(26,25)
        circuit.cx(26,27)
        circuit.ccx(24,25,27)

        #Bit 7
        circuit.ry(inputA7,28)
        circuit.ry(inputB7,30)
        #OR 
        circuit.cx(28,29)
        circuit.cx(30,29)
        circuit.cx(30,31)
        circuit.ccx(28,29,31)
            
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)        
            
        circuit.measure_all()
        print("Quantum OR circuit")
        print(circuit)
 
        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0
        qubit8 = 0
        qubit9 = 0
        qubit10 = 0
        qubit11 = 0
        qubit12 = 0
        qubit13 = 0
        qubit14 = 0
        qubit15 = 0
        qubit16 = 0
        qubit17 = 0
        qubit18 = 0
        qubit19 = 0
        qubit20 = 0
        qubit21 = 0
        qubit22 = 0
        qubit23 = 0
        qubit24 = 0
        qubit25 = 0
        qubit26 = 0
        qubit27 = 0
        qubit28 = 0
        qubit29 = 0
        qubit30 = 0
        qubit31 = 0

        
        for result in memory:

                qubit0 = qubit0 + int(result[31])
                qubit1 = qubit1 + int(result[30])
                qubit2 = qubit2 + int(result[29])
                qubit3 = qubit3 + int(result[28])
                qubit4 = qubit4 + int(result[27])
                qubit5 = qubit5 + int(result[26])
                qubit6 = qubit6 + int(result[25])
                qubit7 = qubit7 + int(result[24])
                qubit8 = qubit8 + int(result[23])
                qubit9 = qubit9 + int(result[22])
                qubit10 = qubit10 + int(result[21])
                qubit11 = qubit11 + int(result[20])
                qubit12 = qubit12 + int(result[19])
                qubit13 = qubit13 + int(result[18])
                qubit14 = qubit14 + int(result[17])
                qubit15 = qubit15 + int(result[16])
                qubit16 = qubit16 + int(result[15])
                qubit17 = qubit17 + int(result[14])
                qubit18 = qubit18 + int(result[13])
                qubit19 = qubit19 + int(result[12])
                qubit20 = qubit20 + int(result[11])
                qubit21 = qubit21 + int(result[10])
                qubit22 = qubit22 + int(result[9])
                qubit23 = qubit23 + int(result[8])
                qubit24 = qubit24 + int(result[7])
                qubit25 = qubit25 + int(result[6])
                qubit26 = qubit26 + int(result[5])
                qubit27 = qubit27 + int(result[4])
                qubit28 = qubit28 + int(result[3])
                qubit29 = qubit29 + int(result[2])
                qubit30 = qubit30 + int(result[1])
                qubit31 = qubit31 + int(result[0])

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots
        qubit8 = qubit8/shots
        qubit9 = qubit9/shots
        qubit10 = qubit10/shots
        qubit11 = qubit11/shots
        qubit12 = qubit12/shots
        qubit13 = qubit13/shots
        qubit14 = qubit14/shots
        qubit15 = qubit15/shots
        qubit16 = qubit16/shots
        qubit17 = qubit17/shots
        qubit18 = qubit18/shots
        qubit19 = qubit19/shots
        qubit20 = qubit20/shots
        qubit21 = qubit21/shots
        qubit22 = qubit22/shots
        qubit23 = qubit23/shots
        qubit24 = qubit24/shots
        qubit25 = qubit25/shots
        qubit26 = qubit26/shots
        qubit27 = qubit27/shots
        qubit28 = qubit28/shots
        qubit29 = qubit29/shots
        qubit30 = qubit30/shots
        qubit31 = qubit31/shots     

        return str(round(qubit31)) + str(round(qubit27)) + str(round(qubit23)) + str(round(qubit19)) + str(round(qubit15)) + str(round(qubit11)) + str(round(qubit7)) + str(round(qubit3))

    def myQuantum4BitLatch(self,input):
        """
      ┌───────┐     ┌───┐     ┌───┐                                                                                                                                            ░ ┌─┐
 q_0: ┤ Ry(0) ├──■──┤ X ├──■──┤ X ├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────░─┤M├────────────────────────────────────────────────────────────────────────────────────
      ├───────┤  │  └───┘  │  └───┘                                                                                                                                            ░ └╥┘┌─┐
 q_1: ┤ Ry(π) ├──■─────────■─────────■──────────────■─────────────────────────────────■──────────────■─────────■──────────────■────────────────────────────────────────────────░──╫─┤M├─────────────────────────────────────────────────────────────────────────────────
      └───────┘  │       ┌─┴─┐       │              │                                 │              │         │              │                                                ░  ║ └╥┘┌─┐
 q_2: ───────────┼───────┤ X ├──■────┼──────────────┼────■────────────────────────────┼──────────────┼─────────┼──────────────┼────────────────────────────────────────────────░──╫──╫─┤M├──────────────────────────────────────────────────────────────────────────────
               ┌─┴─┐     └───┘  │    │              │    │                            │              │         │              │                                                ░  ║  ║ └╥┘┌─┐
 q_3: ─────────┤ X ├────────────┼────┼──────────────┼────┼────────────────■──────■────┼──────────────┼─────────┼──────────────┼────────────────────────────────────────────────░──╫──╫──╫─┤M├───────────────────────────────────────────────────────────────────────────
               └───┘          ┌─┴─┐  │  ┌───┐       │    │                │      │    │              │         │              │                                                ░  ║  ║  ║ └╥┘┌─┐
 q_4: ────────────────────────┤ X ├──┼──┤ X ├───────┼────■────────────────┼──────┼────┼──────────────┼─────────┼──────────────┼────────────────────────────────────────────────░──╫──╫──╫──╫─┤M├────────────────────────────────────────────────────────────────────────
                              └───┘  │  └─┬─┘┌───┐  │  ┌─┴─┐┌───┐         │      │    │              │         │              │                                                ░  ║  ║  ║  ║ └╥┘┌─┐
 q_5: ───────────────────────────────┼────┼──┤ X ├──┼──┤ X ├┤ X ├──■──────┼──────┼────┼────■─────────┼─────────┼──────────────┼────────────────────────────────────────────────░──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────────────────────────────
                                     │    │  └─┬─┘  │  └───┘└───┘┌─┴─┐  ┌─┴─┐    │    │    │         │         │              │                                                ░  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ───────────────────────────────┼────┼────┼────┼────────────┤ X ├──┤ X ├────┼────┼────■─────────┼─────────┼──────────────┼────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────────────────────────────
                                     │    │    │    │            └───┘  └───┘  ┌─┴─┐  │  ┌─┴─┐┌───┐  │         │              │                                                ░  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ───────────────────────────────┼────■────■────┼──────────────────────────┤ X ├──┼──┤ X ├┤ X ├──┼─────────┼──────────────┼────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────────────────────────────
      ┌───────┐                      │  ┌───┐       │  ┌───┐                   └───┘  │  └───┘└───┘  │         │              │                                                ░  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_8: ┤ Ry(0) ├──────────────────────■──┤ X ├───────■──┤ X ├──────────────────────────┼──────────────┼─────────┼──────────────┼────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────────────────────────────
      └───────┘                      │  └───┘     ┌─┴─┐└───┘                          │              │         │              │                                                ░  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_9: ───────────────────────────────┼────────────┤ X ├──■────────────────■───────────┼──────────────┼─────────┼──────────────┼────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────────────────
                                   ┌─┴─┐          └───┘  │                │           │              │         │              │                                                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_10: ─────────────────────────────┤ X ├─────────────────┼────────────────┼───────────┼─────────■────┼────■────┼──────────────┼────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────────────────
                                   └───┘               ┌─┴─┐┌───┐         │           │         │    │    │    │              │                                                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_11: ─────────────────────────────────────────────────┤ X ├┤ X ├─────────■───────────┼─────────┼────┼────┼────┼──────────────┼────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────────────────
                                                       └───┘└─┬─┘┌───┐  ┌─┴─┐  ┌───┐  │         │    │    │    │              │                                                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_12: ────────────────────────────────────────────────────────┼──┤ X ├──┤ X ├──┤ X ├──┼────■────┼────┼────┼────┼────■─────────┼────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────────────────
                                                              │  └─┬─┘  └───┘  └───┘  │  ┌─┴─┐┌─┴─┐  │    │    │    │         │                                                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_13: ────────────────────────────────────────────────────────┼────┼──────────────────┼──┤ X ├┤ X ├──┼────┼────┼────■─────────┼────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────
                                                              │    │                  │  └───┘└───┘  │  ┌─┴─┐  │  ┌─┴─┐┌───┐  │                                                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_14: ────────────────────────────────────────────────────────┼────┼──────────────────┼──────────────┼──┤ X ├──┼──┤ X ├┤ X ├──┼────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────
       ┌───────┐                                              │    │                  │  ┌───┐       │  ├───┤  │  └───┘└───┘  │                                                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_15: ─┤ Ry(π) ├──────────────────────────────────────────────■────■───────────────■──┤──┤ X ├───────■──┤ X ├──┼──────────────┼────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────
       └───────┘                                                                      │  └───┘     ┌─┴─┐└───┘  │              │                                                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_16: ────────────────────────────────────────────────────────────────────────────────┼────────────┤ X ├──■────┼──────────────┼────■───────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────
                                                                                    ┌─┴─┐          └───┘  │    │              │    │                                           ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_17: ──────────────────────────────────────────────────────────────────────────────┤ X ├─────────────────┼────┼──────────────┼────┼──────────────■────■───────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────
                                                                                    └───┘               ┌─┴─┐  │  ┌───┐       │    │              │    │                       ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_18: ──────────────────────────────────────────────────────────────────────────────────────────────────┤ X ├──┼──┤ X ├───────┼────■──────────────┼────┼───────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────
                                                                                                        └───┘  │  └─┬─┘┌───┐  │  ┌─┴─┐┌───┐       │    │                       ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_19: ─────────────────────────────────────────────────────────────────────────────────────────────────────────┼────┼──┤ X ├──┼──┤ X ├┤ X ├──■────┼────┼────■──────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────
                                                                                                               │    │  └─┬─┘  │  └───┘└───┘┌─┴─┐┌─┴─┐  │    │                  ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_20: ─────────────────────────────────────────────────────────────────────────────────────────────────────────┼────┼────┼────┼────────────┤ X ├┤ X ├──┼────■──────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────
                                                                                                               │    │    │    │            └───┘└───┘┌─┴─┐┌─┴─┐┌───┐┌───┐      ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_21: ─────────────────────────────────────────────────────────────────────────────────────────────────────────┼────■────■────┼──────────────────────┤ X ├┤ X ├┤ X ├┤ X ├──────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────
      ┌───────┐                                                                                                │  ┌───┐       │  ┌───┐               └───┘└───┘└───┘└───┘      ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_22: ┤ Ry(0) ├────────────────────────────────────────────────────────────────────────────────────────────────■──┤ X ├───────■──┤ X ├─────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────
      └───────┘                                                                                                │  └───┘     ┌─┴─┐└───┘                                         ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_23: ─────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────┤ X ├──■──────────────■────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────
                                                                                                             ┌─┴─┐          └───┘  │              │                            ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_24: ───────────────────────────────────────────────────────────────────────────────────────────────────────┤ X ├─────────────────┼──────────────┼──────────────■────■────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────
                                                                                                             └───┘               ┌─┴─┐┌───┐       │              │    │        ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_25: ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ X ├┤ X ├───────■──────────────┼────┼────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────
                                                                                                                                 └───┘└─┬─┘┌───┐┌─┴─┐┌───┐       │    │        ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_26: ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──┤ X ├┤ X ├┤ X ├──■────┼────┼────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
                                                                                                                                        │  └─┬─┘└───┘└───┘┌─┴─┐┌─┴─┐  │    │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_27: ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────┼────────────┤ X ├┤ X ├──┼────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
                                                                                                                                        │    │            └───┘└───┘┌─┴─┐┌─┴─┐ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_28: ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────■────■──────────────────────┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
                                                                                                                                                                    └───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 29/════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
                                                                                                                                                                                  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
        """

        enable = 1 * math.pi
        inputA0 = int(input[3]) * math.pi
        inputA1 = int(input[2]) * math.pi
        inputA2 = int(input[1]) * math.pi
        inputA3 = int(input[0]) * math.pi
 

        circuit = QuantumCircuit(29,29)
        #Bit 0
        circuit.ry(inputA0,0)
        circuit.ry(enable,1)

        #Bottom AND
        circuit.ccx(1,0,3)

        #Top AND
        circuit.x(0)
        circuit.ccx(0,1,2)
        circuit.x(0)        
    
        #Top NOR
        circuit.cx(2,4)
        circuit.cx(7,4)
        circuit.cx(7,5)
        circuit.ccx(2,4,5)
        circuit.x(5)

        #Bottom NOR
        circuit.cx(5,6)
        circuit.cx(3,6)
        circuit.cx(3,7)
        circuit.ccx(5,6,7)
        circuit.x(7)
    
    
        #Bit 1
        circuit.ry(inputA1,8)
        #Bottom AND
        circuit.ccx(1,8,10)
        #Top AND
        circuit.x(8)
        circuit.ccx(8,1,9)
        circuit.x(8)        
        #Top NOR
        circuit.cx(9,11)
        circuit.cx(15,11)
        circuit.cx(15,12)
        circuit.ccx(9,11,12)
        circuit.x(12)
        #Bottom NOR
        circuit.cx(12,13)
        circuit.cx(10,13)
        circuit.cx(10,14)
        circuit.ccx(12,13,14)
        circuit.x(14)
    
        #Bit 2
        circuit.ry(inputA2,15)
        #Bottom AND
        circuit.ccx(1,15,17)
        #Top AND
        circuit.x(15)
        circuit.ccx(15,1,16)
        circuit.x(15)        
        #Top NOR
        circuit.cx(16,18)
        circuit.cx(21,18)
        circuit.cx(21,19)
        circuit.ccx(16,18,19)
        circuit.x(19)
        #Bottom NOR
        circuit.cx(19,20)
        circuit.cx(17,20)
        circuit.cx(17,21)
        circuit.ccx(19,20,21)
        circuit.x(21)

        #Bit 3
        circuit.ry(inputA3,22)
        #Bottom AND
        circuit.ccx(1,22,24)
        #Top AND
        circuit.x(22)
        circuit.ccx(22,1,23)
        circuit.x(22)        
        #Top NOR
        circuit.cx(23,25)
        circuit.cx(28,25)
        circuit.cx(28,26)
        circuit.ccx(23,25,26)
        circuit.x(26)
        #Bottom NOR
        circuit.cx(26,27)
        circuit.cx(24,27)
        circuit.cx(24,28)
        circuit.ccx(26,27,28)
        circuit.x(21)
    
    
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28)
        
        circuit.measure_all()
        
        print("Quantum lacth circuit")
        print(circuit)

        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0
        qubit8 = 0
        qubit9 = 0
        qubit10 = 0
        qubit11 = 0
        qubit12 = 0
        qubit13 = 0
        qubit14 = 0
        qubit15 = 0
        qubit16 = 0
        qubit17 = 0
        qubit18 = 0
        qubit19 = 0
        qubit20 = 0
        qubit21 = 0
        qubit22 = 0
        qubit23 = 0
        qubit24 = 0
        qubit25 = 0
        qubit26 = 0
        qubit27 = 0
        qubit28 = 0
    
        for result in memory:

                qubit0 = qubit0 + int(result[28])
                qubit1 = qubit1 + int(result[27])
                qubit2 = qubit2 + int(result[26])
                qubit3 = qubit3 + int(result[25])
                qubit4 = qubit4 + int(result[24])
                qubit5 = qubit5 + int(result[23])
                qubit6 = qubit6 + int(result[22])
                qubit7 = qubit7 + int(result[21])
                qubit8 = qubit8 + int(result[20])
                qubit9 = qubit9 + int(result[19])
                qubit10 = qubit10 + int(result[18])
                qubit11 = qubit11 + int(result[17])
                qubit12 = qubit12 + int(result[16])
                qubit13 = qubit13 + int(result[15])
                qubit14 = qubit14 + int(result[14])
                qubit15 = qubit15 + int(result[13])
                qubit16 = qubit16 + int(result[12])
                qubit17 = qubit17 + int(result[11])
                qubit18 = qubit18 + int(result[10])
                qubit19 = qubit19 + int(result[9])
                qubit20 = qubit20 + int(result[8])
                qubit21 = qubit21 + int(result[7])
                qubit22 = qubit22 + int(result[6])
                qubit23 = qubit23 + int(result[5])
                qubit24 = qubit24 + int(result[4])
                qubit25 = qubit25 + int(result[3])
                qubit26 = qubit26 + int(result[2])
                qubit27 = qubit27 + int(result[1])
                qubit28 = qubit28 + int(result[0])
        
        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots
        qubit8 = qubit8/shots
        qubit9 = qubit9/shots
        qubit10 = qubit10/shots
        qubit11 = qubit11/shots
        qubit12 = qubit12/shots
        qubit13 = qubit13/shots
        qubit14 = qubit14/shots
        qubit15 = qubit15/shots
        qubit16 = qubit16/shots
        qubit17 = qubit17/shots
        qubit18 = qubit18/shots
        qubit19 = qubit19/shots
        qubit20 = qubit20/shots
        qubit21 = qubit21/shots
        qubit22 = qubit22/shots
        qubit23 = qubit23/shots
        qubit24 = qubit24/shots
        qubit25 = qubit25/shots
        qubit26 = qubit26/shots
        qubit27 = qubit27/shots
        qubit28 = qubit28/shots

        return str(round(qubit26)) + str(round(qubit19)) + str(round(qubit12)) + str(round(qubit5))

    def myQuantum1BitHadamardLatch(self,input):
        """
      ┌───────┐┌───┐     ┌─┐
 q_0: ┤ Ry(0) ├┤ H ├──■──┤M├────
      ├───────┤└───┘┌─┴─┐└╥┘┌─┐
 q_1: ┤ Ry(0) ├─────┤ X ├─╫─┤M├─
      └───────┘     └───┘ ║ └╥┘  
c: 2/ ════════════════════╩══╩══
        """    
        inputA0 = int(input) * math.pi
        
      
        circuit = QuantumCircuit(2,2)
        
        
        #Bit 0
        circuit.ry(inputA0,0)
        circuit.ry(inputA0,1)
        circuit.h(0)
        circuit.cx(0,1)

        
        circuit.measure_all()
        
        print(circuit)
        print("1 bit Hadamard latch")

        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        
        output0 = 0
       
        for result in memory:
        
        
                output0 = output0 + int(bool(int(result[1])) ^ bool(int(result[0])))


        output0 = output0/shots        
     

        return str(round(output0))

    def myQuantum4BitHadamardLatch(self,input):
        """
      ┌───────┐┌───┐     ┌─┐
 q_0: ┤ Ry(0) ├┤ H ├──■──┤M├─────────────────────
      ├───────┤└───┘┌─┴─┐└╥┘┌─┐
 q_1: ┤ Ry(0) ├─────┤ X ├─╫─┤M├──────────────────
      ├───────┤┌───┐└───┘ ║ └╥┘┌─┐
 q_2: ┤ Ry(π) ├┤ H ├──■───╫──╫─┤M├───────────────
      ├───────┤└───┘┌─┴─┐ ║  ║ └╥┘┌─┐
 q_3: ┤ Ry(π) ├─────┤ X ├─╫──╫──╫─┤M├────────────
      ├───────┤┌───┐└───┘ ║  ║  ║ └╥┘┌─┐
 q_4: ┤ Ry(0) ├┤ H ├──■───╫──╫──╫──╫─┤M├─────────
      ├───────┤└───┘┌─┴─┐ ║  ║  ║  ║ └╥┘┌─┐
 q_5: ┤ Ry(0) ├─────┤ X ├─╫──╫──╫──╫──╫─┤M├──────
      ├───────┤┌───┐└───┘ ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ┤ Ry(π) ├┤ H ├──■───╫──╫──╫──╫──╫──╫─┤M├───
      ├───────┤└───┘┌─┴─┐ ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ┤ Ry(π) ├─────┤ X ├─╫──╫──╫──╫──╫──╫──╫─┤M├
      └───────┘     └───┘ ║  ║  ║  ║  ║  ║  ║ └╥┘  
c: 8/ ════════════════════╩══╩══╩══╩══╩══╩══╩══╩═
        """    
        reset = 0
        inputA0 = int(input[3]) * math.pi
        inputA1 = int(input[2]) * math.pi
        inputA2 = int(input[1]) * math.pi
        inputA3 = int(input[0]) * math.pi

        
        
        circuit = QuantumCircuit(8,8)
        
        
        #Bit 0
        circuit.ry(inputA0,0)
        circuit.ry(inputA0,1)
        circuit.h(0)
        circuit.cx(0,1)

        #Bit 1
        circuit.ry(inputA1,2)
        circuit.ry(inputA1,3)
        circuit.h(2)
        circuit.cx(2,3)

        #Bit 2
        circuit.ry(inputA2,4)
        circuit.ry(inputA2,5)
        circuit.h(4)
        circuit.cx(4,5)

        #Bit 3
        circuit.ry(inputA3,6)
        circuit.ry(inputA3,7)
        circuit.h(6)
        circuit.cx(6,7)


  

        circuit.measure_all()


        
        print("4 bit Hadamard Latch")
        print(circuit)


        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        
        output0 = 0
        output1 = 0
        output2 = 0
        output3 = 0



        
        for result in memory:
        
        
                output0 = output0 + int(bool(int(result[7])) ^ bool(int(result[6])))
                output1 = output1 + int(bool(int(result[5])) ^ bool(int(result[4])))
                output2 = output2 + int(bool(int(result[3])) ^ bool(int(result[2])))
                output3 = output3 + int(bool(int(result[1])) ^ bool(int(result[0])))

        output0 = output0/shots        
        output1 = output1/shots        
        output2 = output2/shots        
        output3 = output3/shots        

        return str(round(output3)) + str(round(output2)) + str(round(output1)) + str(round(output0))

    def myQuantum8BitHadamardLatch(self,inputA7,inputA6,inputA5,inputA4,inputA3,inputA2,inputA1,inputA0):
        """
      ┌───────┐┌───┐     ┌─┐
 q_0: ┤ Ry(0) ├┤ H ├──■──┤M├─────────────────────────────────────────────
      ├───────┤└───┘┌─┴─┐└╥┘┌─┐
 q_1: ┤ Ry(0) ├─────┤ X ├─╫─┤M├──────────────────────────────────────────
      ├───────┤┌───┐└───┘ ║ └╥┘┌─┐
 q_2: ┤ Ry(π) ├┤ H ├──■───╫──╫─┤M├───────────────────────────────────────
      ├───────┤└───┘┌─┴─┐ ║  ║ └╥┘┌─┐
 q_3: ┤ Ry(π) ├─────┤ X ├─╫──╫──╫─┤M├────────────────────────────────────
      ├───────┤┌───┐└───┘ ║  ║  ║ └╥┘┌─┐
 q_4: ┤ Ry(0) ├┤ H ├──■───╫──╫──╫──╫─┤M├─────────────────────────────────
      ├───────┤└───┘┌─┴─┐ ║  ║  ║  ║ └╥┘┌─┐
 q_5: ┤ Ry(0) ├─────┤ X ├─╫──╫──╫──╫──╫─┤M├──────────────────────────────
      ├───────┤┌───┐└───┘ ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ┤ Ry(π) ├┤ H ├──■───╫──╫──╫──╫──╫──╫─┤M├───────────────────────────
      ├───────┤└───┘┌─┴─┐ ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ┤ Ry(π) ├─────┤ X ├─╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────
      ├───────┤┌───┐└───┘ ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_8: ┤ Ry(0) ├┤ H ├──■───╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────
      ├───────┤└───┘┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_9: ┤ Ry(0) ├─────┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────
      ├───────┤┌───┐└───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_10: ┤ Ry(π) ├┤ H ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────
      ├───────┤└───┘┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_11: ┤ Ry(π) ├─────┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────
      ├───────┤┌───┐└───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_12: ┤ Ry(0) ├┤ H ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────
      ├───────┤└───┘┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_13: ┤ Ry(0) ├─────┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
      ├───────┤┌───┐└───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_14: ┤ Ry(π) ├┤ H ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
      ├───────┤└───┘┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_15: ┤ Ry(π) ├─────┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
      └───────┘     └───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 16/════════════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
        """    
        reset = 0
        inputA0 = int(inputA0) * math.pi
        inputA1 = int(inputA1) * math.pi
        inputA2 = int(inputA2) * math.pi
        inputA3 = int(inputA3) * math.pi
        inputA4 = int(inputA4) * math.pi
        inputA5 = int(inputA5) * math.pi
        inputA6 = int(inputA6) * math.pi
        inputA7 = int(inputA7) * math.pi
        
        
        circuit = QuantumCircuit(16,16)
        
        
        #Bit 0
        circuit.ry(inputA0,0)
        circuit.ry(inputA0,1)
        circuit.h(0)
        circuit.cx(0,1)

        #Bit 1
        circuit.ry(inputA1,2)
        circuit.ry(inputA1,3)
        circuit.h(2)
        circuit.cx(2,3)

        #Bit 2
        circuit.ry(inputA2,4)
        circuit.ry(inputA2,5)
        circuit.h(4)
        circuit.cx(4,5)

        #Bit 3
        circuit.ry(inputA3,6)
        circuit.ry(inputA3,7)
        circuit.h(6)
        circuit.cx(6,7)

        #Bit 4
        circuit.ry(inputA4,8)
        circuit.ry(inputA4,9)
        circuit.h(8)
        circuit.cx(8,9)

        #Bit 5
        circuit.ry(inputA5,10)
        circuit.ry(inputA5,11)
        circuit.h(10)
        circuit.cx(10,11)

        #Bit 6
        circuit.ry(inputA6,12)
        circuit.ry(inputA6,13)
        circuit.h(12)
        circuit.cx(12,13)

        #Bit 7
        circuit.ry(inputA7,14)
        circuit.ry(inputA7,15)        
        circuit.h(14)
        circuit.cx(14,15)
  

        circuit.measure_all()

        
        print("Quantum 8 Bit Hadamard Latch")
        print(circuit)
        
        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)
        
        output0 = 0
        output1 = 0
        output2 = 0
        output3 = 0
        output4 = 0
        output5 = 0
        output6 = 0
        output7 = 0


        
        for result in memory:
        
        
                output0 = output0 + int(bool(int(result[15])) ^ bool(int(result[14])))
                output1 = output1 + int(bool(int(result[13])) ^ bool(int(result[12])))
                output2 = output2 + int(bool(int(result[11])) ^ bool(int(result[10])))
                output3 = output3 + int(bool(int(result[9])) ^ bool(int(result[8])))
                output4 = output4 + int(bool(int(result[7])) ^ bool(int(result[6])))
                output5 = output5 + int(bool(int(result[5])) ^ bool(int(result[4])))
                output6 = output6 + int(bool(int(result[3])) ^ bool(int(result[2])))
                output7 = output7 + int(bool(int(result[1])) ^ bool(int(result[0])))
                
                

        

        output0 = output0/shots        
        output1 = output1/shots        
        output2 = output2/shots        
        output3 = output3/shots        
        output4 = output4/shots        
        output5 = output5/shots        
        output6 = output6/shots        
        output7 = output7/shots        

 
        return str(round(output7)) + str(round(output6)) + str(round(output5)) + str(round(output4)) + str(round(output3)) + str(round(output2)) + str(round(output1)) + str(round(output0))

    def myQuantum1BitLatch(self,input):
        """
     ┌───────┐     ┌───┐     ┌───┐                                              ░ ┌─┐
q_0: ┤ Ry(π) ├──■──┤ X ├──■──┤ X ├──────────────────────────────────────────────░─┤M├─────────────────────
     ├───────┤  │  └───┘  │  └───┘                                              ░ └╥┘┌─┐
q_1: ┤ Ry(π) ├──■─────────■─────────────────────────────────────────────────────░──╫─┤M├──────────────────
     └───────┘  │       ┌─┴─┐                                                   ░  ║ └╥┘┌─┐
q_2: ───────────┼───────┤ X ├──■──────────────■─────────────────────────────────░──╫──╫─┤M├───────────────
              ┌─┴─┐     └───┘  │              │                                 ░  ║  ║ └╥┘┌─┐
q_3: ─────────┤ X ├────────────┼──────────────┼──────────────■────■─────────────░──╫──╫──╫─┤M├────────────
              └───┘          ┌─┴─┐┌───┐       │              │    │             ░  ║  ║  ║ └╥┘┌─┐
q_4: ────────────────────────┤ X ├┤ X ├───────■──────────────┼────┼─────────────░──╫──╫──╫──╫─┤M├─────────
                             └───┘└─┬─┘┌───┐┌─┴─┐┌───┐       │    │             ░  ║  ║  ║  ║ └╥┘┌─┐
q_5: ───────────────────────────────┼──┤ X ├┤ X ├┤ X ├──■────┼────┼────■────────░──╫──╫──╫──╫──╫─┤M├──────
                                    │  └─┬─┘└───┘└───┘┌─┴─┐┌─┴─┐  │    │        ░  ║  ║  ║  ║  ║ └╥┘┌─┐
q_6: ───────────────────────────────┼────┼────────────┤ X ├┤ X ├──┼────■────────░──╫──╫──╫──╫──╫──╫─┤M├───
                                    │    │            └───┘└───┘┌─┴─┐┌─┴─┐┌───┐ ░  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_7: ───────────────────────────────■────■──────────────────────┤ X ├┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫─┤M├
                                                                └───┘└───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 8/══════════════════════════════════════════════════════════════════════════════╩══╩══╩══╩══╩══╩══╩══╩═
                                                                                   0  1  2  3  4  5  6  7
        """
        enable = 1 * math.pi
        input = int(input) * math.pi


        circuit = QuantumCircuit(8,8)
        #Bit 0
        circuit.ry(input,0)
        circuit.ry(enable,1)

        #Bottom AND
        circuit.ccx(1,0,3)

        #Top AND
        circuit.x(0)
        circuit.ccx(0,1,2)
        circuit.x(0)        
    
        #Top NOR
        circuit.cx(2,4)
        circuit.cx(7,4)
        circuit.cx(7,5)
        circuit.ccx(2,4,5)
        circuit.x(5)

        #Bottom NOR
        circuit.cx(5,6)
        circuit.cx(3,6)
        circuit.cx(3,7)
        circuit.ccx(5,6,7)
        circuit.x(7)
    

        circuit.barrier(0,1,2,3,4,5,6,7)
        
 

        circuit.measure_all()
        
        print("Quantum latch circuit")
        print(circuit)

        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0

    
        for result in memory:

            qubit0 = qubit0 + int(result[7])
            qubit1 = qubit1 + int(result[6])
            qubit2 = qubit2 + int(result[5])
            qubit3 = qubit3 + int(result[4])
            qubit4 = qubit4 + int(result[3])
            qubit5 = qubit5 + int(result[2])
            qubit6 = qubit6 + int(result[1])
            qubit7 = qubit7 + int(result[0])

        
        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots


        return str(int(qubit5))

    def myQuantum4BitAdder(self,inputA3,inputA2,inputA1,inputA0,inputB3,inputB2,inputB1,inputB0,carry):
        """
      ┌───────┐                                    ░                                              ░                                              ░                                              ░ ┌─┐
 q_0: ┤ Ry(π) ├──■────■────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░─┤M├────────────────────────────────────────────────────────────────────────
      ├───────┤  │  ┌─┴─┐                          ░                                              ░                                              ░                                              ░ └╥┘┌─┐
 q_1: ┤ Ry(π) ├──■──┤ X ├──■────■──────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫─┤M├─────────────────────────────────────────────────────────────────────
      └───────┘┌─┴─┐└───┘  │    │                  ░                                              ░                                              ░                                              ░  ║ └╥┘┌─┐
 q_2: ─────────┤ X ├───────┼────┼────■────■────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫─┤M├──────────────────────────────────────────────────────────────────
      ┌───────┐└───┘       │  ┌─┴─┐  │    │        ░                                              ░                                              ░                                              ░  ║  ║ └╥┘┌─┐
 q_3: ┤ Ry(0) ├────────────■──┤ X ├──┼────┼────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫─┤M├───────────────────────────────────────────────────────────────
      └───────┘          ┌─┴─┐└───┘  │    │        ░                                              ░                                              ░                                              ░  ║  ║  ║ └╥┘┌─┐
 q_4: ───────────────────┤ X ├──■────┼────┼────■───░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫─┤M├────────────────────────────────────────────────────────────
                         └───┘┌─┴─┐┌─┴─┐  │    │   ░                                              ░                                              ░                                              ░  ║  ║  ║  ║ └╥┘┌─┐
 q_5: ────────────────────────┤ X ├┤ X ├──┼────■───░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────────────────
                              └───┘└───┘┌─┴─┐┌─┴─┐ ░                         ┌───┐                ░                                              ░                                              ░  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ──────────────────────────────────┤ X ├┤ X ├─░──────────────────────■──┤ X ├────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────────────────
                                        └───┘└───┘ ░ ┌───────┐            │  └─┬─┘                ░                                              ░                                              ░  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ─────────────────────────────────────────────░─┤ Ry(0) ├──■────■────┼────┼──────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────────────────
                                                   ░ ├───────┤  │  ┌─┴─┐  │    │                  ░                                              ░                                              ░  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_8: ─────────────────────────────────────────────░─┤ Ry(0) ├──■──┤ X ├──■────■──────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────────────────
                                                   ░ └───────┘┌─┴─┐└───┘  │                       ░                                              ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_9: ─────────────────────────────────────────────░──────────┤ X ├───────┼─────────■────■────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────
                                                   ░          └───┘     ┌─┴─┐       │    │        ░                                              ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_10: ─────────────────────────────────────────────░────────────────────┤ X ├──■────┼────┼────■───░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────
                                                   ░                    └───┘┌─┴─┐┌─┴─┐  │    │   ░                                              ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_11: ─────────────────────────────────────────────░─────────────────────────┤ X ├┤ X ├──┼────■───░──────────────────────────────────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────
                                                   ░                         └───┘└───┘┌─┴─┐┌─┴─┐ ░                         ┌───┐                ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_12: ─────────────────────────────────────────────░───────────────────────────────────┤ X ├┤ X ├─░──────────────────────■──┤ X ├────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────
                                                   ░                                   └───┘└───┘ ░ ┌───────┐            │  └─┬─┘                ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_13: ─────────────────────────────────────────────░──────────────────────────────────────────────░─┤ Ry(0) ├──■────■────┼────┼──────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────
                                                   ░                                              ░ ├───────┤  │  ┌─┴─┐  │    │                  ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_14: ─────────────────────────────────────────────░──────────────────────────────────────────────░─┤ Ry(π) ├──■──┤ X ├──■────■──────────────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────
                                                   ░                                              ░ └───────┘┌─┴─┐└───┘  │                       ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_15: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────┤ X ├───────┼─────────■────■────────░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────
                                                   ░                                              ░          └───┘     ┌─┴─┐       │    │        ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_16: ─────────────────────────────────────────────░──────────────────────────────────────────────░────────────────────┤ X ├──■────┼────┼────■───░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────
                                                   ░                                              ░                    └───┘┌─┴─┐┌─┴─┐  │    │   ░                                              ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_17: ─────────────────────────────────────────────░──────────────────────────────────────────────░─────────────────────────┤ X ├┤ X ├──┼────■───░──────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────
                                                   ░                                              ░                         └───┘└───┘┌─┴─┐┌─┴─┐ ░                         ┌───┐                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_18: ─────────────────────────────────────────────░──────────────────────────────────────────────░───────────────────────────────────┤ X ├┤ X ├─░──────────────────────■──┤ X ├────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────
                                                   ░                                              ░                                   └───┘└───┘ ░ ┌───────┐            │  └─┬─┘                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_19: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░─┤ Ry(π) ├──■────■────┼────┼──────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────
                                                   ░                                              ░                                              ░ ├───────┤  │  ┌─┴─┐  │    │                  ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_20: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░─┤ Ry(π) ├──■──┤ X ├──■────■──────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────
                                                   ░                                              ░                                              ░ └───────┘┌─┴─┐└───┘  │                       ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_21: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░──────────┤ X ├───────┼─────────■────■────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────
                                                   ░                                              ░                                              ░          └───┘     ┌─┴─┐       │    │        ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_22: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░────────────────────┤ X ├──■────┼────┼────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
                                                   ░                                              ░                                              ░                    └───┘┌─┴─┐┌─┴─┐  │    │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_23: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░─────────────────────────┤ X ├┤ X ├──┼────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
                                                   ░                                              ░                                              ░                         └───┘└───┘┌─┴─┐┌─┴─┐ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_24: ─────────────────────────────────────────────░──────────────────────────────────────────────░──────────────────────────────────────────────░───────────────────────────────────┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
                                                   ░                                              ░                                              ░                                   └───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 25/═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
                                                                                                                                                                                                   0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 
        """      
        carrybit = int(carry) * math.pi
        inputA0 = int(inputA0) * math.pi
        inputA1 = int(inputA1) * math.pi
        inputA2 = int(inputA2) * math.pi
        inputA3 = int(inputA3) * math.pi
    
        inputB0 = int(inputB0) * math.pi
        inputB1 = int(inputB1) * math.pi
        inputB2 = int(inputB2) * math.pi
        inputB3 = int(inputB3) * math.pi
        
        
        circuit = QuantumCircuit(25,25)
        #Bit 0
        circuit.ry(inputA0,0)
        circuit.ry(inputB0,1)
        circuit.ry(carrybit,3)

        #AND1
        circuit.ccx(1,0,2)
        #XOR1
        circuit.cx(0,1)
        #AND2
        circuit.ccx(3,1,4)
        #XOR2
        circuit.cx(1,3)
        #OR1
        circuit.cx(4,5)
        circuit.cx(2,5)
        circuit.cx(2,6)
        circuit.ccx(4,5,6)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
        
        
        #Bit 1
        circuit.ry(inputA1,7)
        circuit.ry(inputB1,8)

        #AND1
        circuit.ccx(8,7,9)
        #XOR1
        circuit.cx(7,8)
        #AND2
        circuit.ccx(6,8,10)
        #XOR2
        circuit.cx(8,6)
        #OR1
        circuit.cx(10,11)
        circuit.cx(9,11)
        circuit.cx(9,12)
        circuit.ccx(10,11,12)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
    
        
        #Bit 2
        circuit.ry(inputA2,13)
        circuit.ry(inputB2,14)
        
        #AND1
        circuit.ccx(14,13,15)  
        #XOR1
        circuit.cx(13,14)
        #AND2
        circuit.ccx(12,14,16)
        #XOR2
        circuit.cx(14,12)
        #OR1
        circuit.cx(16,17)
        circuit.cx(15,17)
        circuit.cx(15,18)
        circuit.ccx(16,17,18)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
        
        #Bit 3
        circuit.ry(inputA3,19)
        circuit.ry(inputB3,20)
        
        #AND1
        circuit.ccx(20,19,21)  
        #XOR1
        circuit.cx(19,20)
        #AND2
        circuit.ccx(18,20,22)
        #XOR2
        circuit.cx(20,18)
        #OR1
        circuit.cx(22,23)
        circuit.cx(21,23)
        circuit.cx(21,24)
        circuit.ccx(22,23,24)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)

        circuit.measure_all()
        
        print("Quantum adder circuit")        
        print(circuit)
        
        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0
        qubit8 = 0
        qubit9 = 0
        qubit10 = 0
        qubit11 = 0
        qubit12 = 0
        qubit13 = 0
        qubit14 = 0
        qubit15 = 0
        qubit16 = 0
        qubit17 = 0
        qubit18 = 0
        qubit19 = 0
        qubit20 = 0
        qubit21 = 0
        qubit22 = 0
        qubit23 = 0
        qubit24 = 0
    
        for result in memory:

                qubit0 = qubit0 + int(result[24])
                qubit1 = qubit1 + int(result[23])
                qubit2 = qubit2 + int(result[22])
                qubit3 = qubit3 + int(result[21])
                qubit4 = qubit4 + int(result[20])
                qubit5 = qubit5 + int(result[19])
                qubit6 = qubit6 + int(result[18])
                qubit7 = qubit7 + int(result[17])
                qubit8 = qubit8 + int(result[16])
                qubit9 = qubit9 + int(result[15])
                qubit10 = qubit10 + int(result[14])
                qubit11 = qubit11 + int(result[13])
                qubit12 = qubit12 + int(result[12])
                qubit13 = qubit13 + int(result[11])
                qubit14 = qubit14 + int(result[10])
                qubit15 = qubit15 + int(result[9])
                qubit16 = qubit16 + int(result[8])
                qubit17 = qubit17 + int(result[7])
                qubit18 = qubit18 + int(result[6])
                qubit19 = qubit19 + int(result[5])
                qubit20 = qubit20 + int(result[4])
                qubit21 = qubit21 + int(result[3])
                qubit22 = qubit22 + int(result[2])
                qubit23 = qubit23 + int(result[1])
                qubit24 = qubit24 + int(result[0])
        
        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots
        qubit8 = qubit8/shots
        qubit9 = qubit9/shots
        qubit10 = qubit10/shots
        qubit11 = qubit11/shots
        qubit12 = qubit12/shots
        qubit13 = qubit13/shots
        qubit14 = qubit14/shots
        qubit15 = qubit15/shots
        qubit16 = qubit16/shots
        qubit17 = qubit17/shots
        qubit18 = qubit18/shots
        qubit19 = qubit19/shots
        qubit20 = qubit20/shots
        qubit21 = qubit21/shots
        qubit22 = qubit22/shots
        qubit23 = qubit23/shots
        qubit24 = qubit24/shots

 
        #4bit + carry bit on qubit 24
        return str(round(qubit24)) + str(round(qubit18)) + str(round(qubit12)) + str(round(qubit6)) + str(round(qubit3))

    def myQuantum4BitSubtractor(self,inputA3,inputA2,inputA1,inputA0,inputB3,inputB2,inputB1,inputB0,borrow):
        """
      ┌───────┐┌───┐     ┌───┐                                         ░                                                             ░                                                             ░                                                             ░ ┌─┐
 q_0: ┤ Ry(π) ├┤ X ├──■──┤ X ├──■──────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─┤M├────────────────────────────────────────────────────────────────────────
      ├───────┤└───┘  │  └───┘┌─┴─┐┌───┐     ┌───┐                     ░                                                             ░                                                             ░                                                             ░ └╥┘┌─┐
 q_1: ┤ Ry(π) ├───────■───────┤ X ├┤ X ├──■──┤ X ├──■──────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──╫─┤M├─────────────────────────────────────────────────────────────────────
      └───────┘     ┌─┴─┐     └───┘└───┘  │  └───┘  │                  ░                                                             ░                                                             ░                                                             ░  ║ └╥┘┌─┐
 q_2: ──────────────┤ X ├─────────────────┼─────────┼────■────■────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──╫──╫─┤M├──────────────────────────────────────────────────────────────────
      ┌───────┐     └───┘                 │       ┌─┴─┐  │    │        ░                                                             ░                                                             ░                                                             ░  ║  ║ └╥┘┌─┐
 q_3: ┤ Ry(0) ├───────────────────────────■───────┤ X ├──┼────┼────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──╫──╫──╫─┤M├───────────────────────────────────────────────────────────────
      └───────┘                         ┌─┴─┐     └───┘  │    │        ░                                                             ░                                                             ░                                                             ░  ║  ║  ║ └╥┘┌─┐
 q_4: ──────────────────────────────────┤ X ├──■─────────┼────┼────■───░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫─┤M├────────────────────────────────────────────────────────────
                                        └───┘┌─┴─┐     ┌─┴─┐  │    │   ░                                                             ░                                                             ░                                                             ░  ║  ║  ║  ║ └╥┘┌─┐
 q_5: ───────────────────────────────────────┤ X ├─────┤ X ├──┼────■───░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────────────────
                                             └───┘     └───┘┌─┴─┐┌─┴─┐ ░                                             ┌───┐           ░                                                             ░                                                             ░  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ──────────────────────────────────────────────────────┤ X ├┤ X ├─░─────────────────────────────────────■───────┤ X ├───────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────────────────
                                                            └───┘└───┘ ░ ┌───────┐┌───┐     ┌───┐            │       └─┬─┘           ░                                                             ░                                                             ░  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ─────────────────────────────────────────────────────────────────░─┤ Ry(π) ├┤ X ├──■──┤ X ├──■─────────┼─────────┼─────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────────────────
                                                                       ░ ├───────┤└───┘  │  └───┘┌─┴─┐┌───┐  │  ┌───┐  │             ░                                                             ░                                                             ░  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_8: ─────────────────────────────────────────────────────────────────░─┤ Ry(π) ├───────■───────┤ X ├┤ X ├──■──┤ X ├──■─────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────────────────
                                                                       ░ └───────┘     ┌─┴─┐     └───┘└───┘  │  └───┘                ░                                                             ░                                                             ░  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_9: ─────────────────────────────────────────────────────────────────░───────────────┤ X ├─────────────────┼─────────■────■────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────────────────
                                                                       ░               └───┘               ┌─┴─┐       │    │        ░                                                             ░                                                             ░  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_10: ─────────────────────────────────────────────────────────────────░───────────────────────────────────┤ X ├──■────┼────┼────■───░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────────────────
                                                                       ░                                   └───┘┌─┴─┐┌─┴─┐  │    │   ░                                                             ░                                                             ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_11: ─────────────────────────────────────────────────────────────────░────────────────────────────────────────┤ X ├┤ X ├──┼────■───░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────────────────
                                                                       ░                                        └───┘└───┘┌─┴─┐┌─┴─┐ ░                                             ┌───┐           ░                                                             ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_12: ─────────────────────────────────────────────────────────────────░──────────────────────────────────────────────────┤ X ├┤ X ├─░─────────────────────────────────────■───────┤ X ├───────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────
                                                                       ░                                                  └───┘└───┘ ░ ┌───────┐┌───┐     ┌───┐            │       └─┬─┘           ░                                                             ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_13: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─┤ Ry(π) ├┤ X ├──■──┤ X ├──■─────────┼─────────┼─────────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────
                                                                       ░                                                             ░ ├───────┤└───┘  │  └───┘┌─┴─┐┌───┐  │  ┌───┐  │             ░                                                             ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_14: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─┤ Ry(0) ├───────■───────┤ X ├┤ X ├──■──┤ X ├──■─────────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────
                                                                       ░                                                             ░ └───────┘     ┌─┴─┐     └───┘└───┘  │  └───┘                ░                                                             ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_15: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░───────────────┤ X ├─────────────────┼─────────■────■────────░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────
                                                                       ░                                                             ░               └───┘               ┌─┴─┐       │    │        ░                                                             ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_16: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░───────────────────────────────────┤ X ├──■────┼────┼────■───░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────
                                                                       ░                                                             ░                                   └───┘┌─┴─┐┌─┴─┐  │    │   ░                                                             ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_17: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░────────────────────────────────────────┤ X ├┤ X ├──┼────■───░─────────────────────────────────────────────────────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────
                                                                       ░                                                             ░                                        └───┘└───┘┌─┴─┐┌─┴─┐ ░                                             ┌───┐           ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_18: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──────────────────────────────────────────────────┤ X ├┤ X ├─░─────────────────────────────────────■───────┤ X ├───────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────
                                                                       ░                                                             ░                                                  └───┘└───┘ ░ ┌───────┐┌───┐     ┌───┐            │       └─┬─┘           ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_19: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─┤ Ry(0) ├┤ X ├──■──┤ X ├──■─────────┼─────────┼─────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────
                                                                       ░                                                             ░                                                             ░ ├───────┤└───┘  │  └───┘┌─┴─┐┌───┐  │  ┌───┐  │             ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_20: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─┤ Ry(π) ├───────■───────┤ X ├┤ X ├──■──┤ X ├──■─────────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────
                                                                       ░                                                             ░                                                             ░ └───────┘     ┌─┴─┐     └───┘└───┘  │  └───┘                ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_21: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░───────────────┤ X ├─────────────────┼─────────■────■────────░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────
                                                                       ░                                                             ░                                                             ░               └───┘               ┌─┴─┐       │    │        ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_22: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░───────────────────────────────────┤ X ├──■────┼────┼────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
                                                                       ░                                                             ░                                                             ░                                   └───┘┌─┴─┐┌─┴─┐  │    │   ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_23: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░────────────────────────────────────────┤ X ├┤ X ├──┼────■───░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
                                                                       ░                                                             ░                                                             ░                                        └───┘└───┘┌─┴─┐┌─┴─┐ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_24: ─────────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░─────────────────────────────────────────────────────────────░──────────────────────────────────────────────────┤ X ├┤ X ├─░──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
                                                                       ░                                                             ░                                                             ░                                                  └───┘└───┘ ░  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 25/══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
                                                                                                                                                                                                                                                                    0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
        """  
        carrybit = int(borrow) * math.pi
        inputA0 = int(inputA0) * math.pi
        inputA1 = int(inputA1) * math.pi
        inputA2 = int(inputA2) * math.pi
        inputA3 = int(inputA3) * math.pi
    
        inputB0 = int(inputB0) * math.pi
        inputB1 = int(inputB1) * math.pi
        inputB2 = int(inputB2) * math.pi
        inputB3 = int(inputB3) * math.pi
        
        
        circuit = QuantumCircuit(25,25)
        #Bit 0
        circuit.ry(inputA0,0)
        circuit.ry(inputB0,1)
        circuit.ry(carrybit,3)

        #AND1
        circuit.x(0)
        circuit.ccx(1,0,2)
        circuit.x(0)
        #XOR1
        circuit.cx(0,1)
        #AND2
        circuit.x(1)
        circuit.ccx(3,1,4)
        circuit.x(1)
        #XOR2
        circuit.cx(1,3)
        #OR1
        circuit.cx(4,5)
        circuit.cx(2,5)
        circuit.cx(2,6)
        circuit.ccx(4,5,6)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
        
        
        #Bit 1
        circuit.ry(inputA1,7)
        circuit.ry(inputB1,8)

        #AND1
        circuit.x(7)
        circuit.ccx(8,7,9)
        circuit.x(7)
        #XOR1
        circuit.cx(7,8)
        #AND2
        circuit.x(8)
        circuit.ccx(6,8,10)
        circuit.x(8)
        #XOR2
        circuit.cx(8,6)
        #OR1
        circuit.cx(10,11)
        circuit.cx(9,11)
        circuit.cx(9,12)
        circuit.ccx(10,11,12)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
    
        
        #Bit 2
        circuit.ry(inputA2,13)
        circuit.ry(inputB2,14)
        
        #AND1
        circuit.x(13)
        circuit.ccx(14,13,15)  
        circuit.x(13)
        #XOR1
        circuit.cx(13,14)
        #AND2
        circuit.x(14)
        circuit.ccx(12,14,16)
        circuit.x(14)
        #XOR2
        circuit.cx(14,12)
        #OR1
        circuit.cx(16,17)
        circuit.cx(15,17)
        circuit.cx(15,18)
        circuit.ccx(16,17,18)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
        
        #Bit 3
        circuit.ry(inputA3,19)
        circuit.ry(inputB3,20)
        
        #AND1
        circuit.x(19)
        circuit.ccx(20,19,21)  
        circuit.x(19)
        #XOR1
        circuit.cx(19,20)
        #AND2
        circuit.x(20)
        circuit.ccx(18,20,22)
        circuit.x(20)
        #XOR2
        circuit.cx(20,18)
        #OR1
        circuit.cx(22,23)
        circuit.cx(21,23)
        circuit.cx(21,24)
        circuit.ccx(22,23,24)
        circuit.barrier(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)

        circuit.measure_all()
        
        print("Quantum subtractor circuit")
        print(circuit)        

        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0
        qubit8 = 0
        qubit9 = 0
        qubit10 = 0
        qubit11 = 0
        qubit12 = 0
        qubit13 = 0
        qubit14 = 0
        qubit15 = 0
        qubit16 = 0
        qubit17 = 0
        qubit18 = 0
        qubit19 = 0
        qubit20 = 0
        qubit21 = 0
        qubit22 = 0
        qubit23 = 0
        qubit24 = 0

    
        for result in memory:

                qubit0 = qubit0 + int(result[24])
                qubit1 = qubit1 + int(result[23])
                qubit2 = qubit2 + int(result[22])
                qubit3 = qubit3 + int(result[21])
                qubit4 = qubit4 + int(result[20])
                qubit5 = qubit5 + int(result[19])
                qubit6 = qubit6 + int(result[18])
                qubit7 = qubit7 + int(result[17])
                qubit8 = qubit8 + int(result[16])
                qubit9 = qubit9 + int(result[15])
                qubit10 = qubit10 + int(result[14])
                qubit11 = qubit11 + int(result[13])
                qubit12 = qubit12 + int(result[12])
                qubit13 = qubit13 + int(result[11])
                qubit14 = qubit14 + int(result[10])
                qubit15 = qubit15 + int(result[9])
                qubit16 = qubit16 + int(result[8])
                qubit17 = qubit17 + int(result[7])
                qubit18 = qubit18 + int(result[6])
                qubit19 = qubit19 + int(result[5])
                qubit20 = qubit20 + int(result[4])
                qubit21 = qubit21 + int(result[3])
                qubit22 = qubit22 + int(result[2])
                qubit23 = qubit23 + int(result[1])
                qubit24 = qubit24 + int(result[0])

        
        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots
        qubit8 = qubit8/shots
        qubit9 = qubit9/shots
        qubit10 = qubit10/shots
        qubit11 = qubit11/shots
        qubit12 = qubit12/shots
        qubit13 = qubit13/shots
        qubit14 = qubit14/shots
        qubit15 = qubit15/shots
        qubit16 = qubit16/shots
        qubit17 = qubit17/shots
        qubit18 = qubit18/shots
        qubit19 = qubit19/shots
        qubit20 = qubit20/shots
        qubit21 = qubit21/shots
        qubit22 = qubit22/shots
        qubit23 = qubit23/shots
        qubit24 = qubit24/shots

 
        return str(round(qubit24)) + str(round(qubit18)) + str(round(qubit12)) + str(round(qubit6)) + str(round(qubit3))

    def myQuantumRyAdd(self,inputA,inputB):
        """
      ┌──────────┐┌──────────┐┌─┐
 q_0: ┤ Ry(1.68) ├┤ Ry(1.47) ├┤M├──────────────────────────────────────────────────────
      ├──────────┤├──────────┤└╥┘┌─┐
 q_1: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫─┤M├───────────────────────────────────────────────────
      ├──────────┤├──────────┤ ║ └╥┘┌─┐
 q_2: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫─┤M├────────────────────────────────────────────────
      ├──────────┤├──────────┤ ║  ║ └╥┘┌─┐
 q_3: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫─┤M├─────────────────────────────────────────────
      ├──────────┤├──────────┤ ║  ║  ║ └╥┘┌─┐
 q_4: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫─┤M├──────────────────────────────────────────
      ├──────────┤├──────────┤ ║  ║  ║  ║ └╥┘┌─┐
 q_5: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫──╫─┤M├───────────────────────────────────────
      ├──────────┤├──────────┤ ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫─┤M├────────────────────────────────────
      ├──────────┤├──────────┤ ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────────────────
      ├──────────┤├──────────┤ ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_8: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────────────────
      ├──────────┤├──────────┤ ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_9: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────────────────
      ├──────────┤├──────────┤ ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_10: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────
      ├──────────┤├──────────┤ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_11: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────
      ├──────────┤├──────────┤ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_12: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────
      ├──────────┤├──────────┤ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_13: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────
      ├──────────┤├──────────┤ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_14: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────
      ├──────────┤├──────────┤ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_15: ┤ Ry(1.68) ├┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────
      └┬───────┬─┘├──────────┤ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_16: ─┤ Ry(0) ├──┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
       ├───────┤  ├──────────┤ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_17: ─┤ Ry(0) ├──┤ Ry(1.47) ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
       ├───────┤  ├──────────┤ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_18: ─┤ Ry(0) ├──┤ Ry(0.21) ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
       └───────┘  └──────────┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 19/═════════════════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
                               0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
        """
        #print(str(inputA) + " + "  + str(inputB))                               
        if inputA > 128: intpuA = 128
        if inputB > 128: intpuB = 128


        mA = inputA % 8
        fA = inputA // 8	

        mB = inputB % 7
        fB = inputB // 7	

        circuit = QuantumCircuit(19,19)
        
        
        x = 0
        while (x < 19):
            a = 0
            b = 0
            
            
            if x < fA: a = 8
            if x == fA: a = mA
            if x > fA: a = 0
        

            if x < fB: b = 7
            if x == fB: b = mB
            if x > fB: b = 0
            
            aRy = self.numberToRyRotation(a)
            bRy = self.numberToRyRotation(b)
            
            #3 = 0.6284 and 6 =  1.2568
            #print("aRY = " + str(aRy) + " bRY = " + str(bRy))
            
            circuit.ry(aRy,x)
            circuit.ry(bRy,x)

        
            x = x + 1
            
        circuit.measure_all()
        
        print("Quantum Ry based adder circuit")
        print(circuit)

        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        test = 0
        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0
        qubit8 = 0
        qubit9 = 0
        qubit10 = 0
        qubit11 = 0
        qubit12 = 0
        qubit13 = 0
        qubit14 = 0
        qubit15 = 0
        qubit16 = 0
        qubit17 = 0
        qubit18 = 0

        
        for result in memory:

            qubit0 = qubit0 + int(result[18])
            qubit1 = qubit1 + int(result[17])
            qubit2 = qubit2 + int(result[16])
            qubit3 = qubit3 + int(result[15])
            qubit4 = qubit4 + int(result[14])
            qubit5 = qubit5 + int(result[13])
            qubit6 = qubit6 + int(result[12])
            qubit7 = qubit7 + int(result[11])
            qubit8 = qubit8 + int(result[10])
            qubit9 = qubit9 + int(result[9])
            qubit10 = qubit10 + int(result[8])
            qubit11 = qubit11 + int(result[7])
            qubit12 = qubit12 + int(result[6])
            qubit13 = qubit13 + int(result[5])
            qubit14 = qubit14 + int(result[4])
            qubit15 = qubit15 + int(result[3])
            qubit16 = qubit16 + int(result[2])
            qubit17 = qubit17 + int(result[1])
            qubit18 = qubit18 + int(result[0])
           
            
        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots
        qubit8 = qubit8/shots
        qubit9 = qubit9/shots
        qubit10 = qubit10/shots
        qubit11 = qubit11/shots
        qubit12 = qubit12/shots
        qubit13 = qubit13/shots
        qubit14 = qubit14/shots
        qubit15 = qubit15/shots
        qubit16 = qubit16/shots
        qubit17 = qubit17/shots
        qubit18 = qubit18/shots



        
        total = self.probabilityToNumber((1 - qubit0) * 100) + self.probabilityToNumber((1 - qubit1) * 100) + self.probabilityToNumber((1 - qubit2) * 100) + self.probabilityToNumber((1 - qubit3) * 100) + self.probabilityToNumber((1 - qubit4) * 100) + self.probabilityToNumber((1 - qubit5) * 100) + self.probabilityToNumber((1 - qubit6) * 100) + self.probabilityToNumber((1 - qubit7) * 100) + self.probabilityToNumber((1 - qubit8) * 100) + self.probabilityToNumber((1 - qubit9) * 100) + self.probabilityToNumber((1 - qubit10) * 100) + self.probabilityToNumber((1 - qubit11) * 100) + self.probabilityToNumber((1 - qubit12) * 100) + self.probabilityToNumber((1 - qubit13) * 100) + self.probabilityToNumber((1 - qubit14) * 100) + self.probabilityToNumber((1 - qubit15) * 100) + self.probabilityToNumber((1 - qubit16) * 100) + self.probabilityToNumber((1 - qubit17) * 100) + self.probabilityToNumber((1 - qubit18) * 100)
        
      


        return int(total)

    def myQuantumCP(self,inputA7,inputA6,inputA5,inputA4,inputA3,inputA2,inputA1,inputA0,inputB7,inputB6,inputB5,inputB4,inputB3,inputB2,inputB1,inputB0):
        """
      ┌───────┐          ┌─┐
 q_0: ┤ Ry(0) ├──■───────┤M├─────────────────────────────────────────────────────────────────────
      ├───────┤┌─┴─┐┌───┐└╥┘                                    ┌─┐
 q_1: ┤ Ry(0) ├┤ X ├┤ X ├─╫────────────────────────■────────────┤M├──────────────────────────────
      ├───────┤└───┘└───┘ ║ ┌─┐                    │            └╥┘
 q_2: ┤ Ry(0) ├──■────────╫─┤M├────────────────────┼─────────────╫───────────────────────────────
      ├───────┤┌─┴─┐┌───┐ ║ └╥┘                    │             ║ ┌─┐
 q_3: ┤ Ry(0) ├┤ X ├┤ X ├─╫──╫─────────────────────■─────────────╫─┤M├───────────────────────────
      ├───────┤└───┘└───┘ ║  ║ ┌─┐                 │             ║ └╥┘
 q_4: ┤ Ry(0) ├──■────────╫──╫─┤M├─────────────────┼─────────────╫──╫────────────────────────────
      ├───────┤┌─┴─┐┌───┐ ║  ║ └╥┘                 │             ║  ║ ┌─┐
 q_5: ┤ Ry(0) ├┤ X ├┤ X ├─╫──╫──╫──────────────────■─────────────╫──╫─┤M├────────────────────────
      ├───────┤└───┘└───┘ ║  ║  ║ ┌─┐              │             ║  ║ └╥┘
 q_6: ┤ Ry(0) ├──■────────╫──╫──╫─┤M├──────────────┼─────────────╫──╫──╫─────────────────────────
      ├───────┤┌─┴─┐┌───┐ ║  ║  ║ └╥┘              │             ║  ║  ║ ┌─┐
 q_7: ┤ Ry(0) ├┤ X ├┤ X ├─╫──╫──╫──╫───────────────■─────────────╫──╫──╫─┤M├─────────────────────
      ├───────┤└───┘└───┘ ║  ║  ║  ║ ┌─┐           │             ║  ║  ║ └╥┘
 q_8: ┤ Ry(0) ├──■────────╫──╫──╫──╫─┤M├───────────┼─────────────╫──╫──╫──╫──────────────────────
      ├───────┤┌─┴─┐┌───┐ ║  ║  ║  ║ └╥┘           │             ║  ║  ║  ║ ┌─┐
 q_9: ┤ Ry(0) ├┤ X ├┤ X ├─╫──╫──╫──╫──╫────────────┼────■────────╫──╫──╫──╫─┤M├──────────────────
      ├───────┤└───┘└───┘ ║  ║  ║  ║  ║ ┌─┐        │    │        ║  ║  ║  ║ └╥┘
q_10: ┤ Ry(0) ├──■────────╫──╫──╫──╫──╫─┤M├────────┼────┼────────╫──╫──╫──╫──╫───────────────────
      ├───────┤┌─┴─┐┌───┐ ║  ║  ║  ║  ║ └╥┘        │    │        ║  ║  ║  ║  ║ ┌─┐
q_11: ┤ Ry(0) ├┤ X ├┤ X ├─╫──╫──╫──╫──╫──╫─────────┼────■────────╫──╫──╫──╫──╫─┤M├───────────────
      ├───────┤└───┘└───┘ ║  ║  ║  ║  ║  ║ ┌─┐     │    │        ║  ║  ║  ║  ║ └╥┘
q_12: ┤ Ry(0) ├──■────────╫──╫──╫──╫──╫──╫─┤M├─────┼────┼────────╫──╫──╫──╫──╫──╫────────────────
      ├───────┤┌─┴─┐┌───┐ ║  ║  ║  ║  ║  ║ └╥┘     │    │        ║  ║  ║  ║  ║  ║ ┌─┐
q_13: ┤ Ry(0) ├┤ X ├┤ X ├─╫──╫──╫──╫──╫──╫──╫──────┼────■────────╫──╫──╫──╫──╫──╫─┤M├────────────
      ├───────┤└───┘└───┘ ║  ║  ║  ║  ║  ║  ║ ┌─┐  │    │        ║  ║  ║  ║  ║  ║ └╥┘
q_14: ┤ Ry(0) ├──■────────╫──╫──╫──╫──╫──╫──╫─┤M├──┼────┼────────╫──╫──╫──╫──╫──╫──╫─────────────
      ├───────┤┌─┴─┐┌───┐ ║  ║  ║  ║  ║  ║  ║ └╥┘  │    │        ║  ║  ║  ║  ║  ║  ║ ┌─┐
q_15: ┤ Ry(0) ├┤ X ├┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫───┼────■────────╫──╫──╫──╫──╫──╫──╫─┤M├─────────
      └───────┘└───┘└───┘ ║  ║  ║  ║  ║  ║  ║  ║ ┌─┴─┐  │        ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_16: ────────────────────╫──╫──╫──╫──╫──╫──╫──╫─┤ X ├──┼────■───╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
                          ║  ║  ║  ║  ║  ║  ║  ║ └───┘┌─┴─┐  │   ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_17: ────────────────────╫──╫──╫──╫──╫──╫──╫──╫──────┤ X ├──■───╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
                          ║  ║  ║  ║  ║  ║  ║  ║      └───┘┌─┴─┐ ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_18: ────────────────────╫──╫──╫──╫──╫──╫──╫──╫───────────┤ X ├─╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
                          ║  ║  ║  ║  ║  ║  ║  ║           └───┘ ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 19/════════════════════╩══╩══╩══╩══╩══╩══╩══╩═════════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
                          0  2  4  6  8  10 12 14                1  3  5  7  9  11 13 15 16 17 18
        """
        print("The methods sees input A = " + str(inputA7) + str(inputA6) + str(inputA5) + str(inputA4) + str(inputA3) + str(inputA2) + str(inputA1) + str(inputA0) + " and input B = " + str(inputB7) + str(inputB6) + str(inputB5) + str(inputB4) + str(inputB3) + str(inputB2) + str(inputB1) + str(inputB0))

        inputA0 = int(inputA0) * math.pi
        inputA1 = int(inputA1) * math.pi
        inputA2 = int(inputA2) * math.pi
        inputA3 = int(inputA3) * math.pi
        inputA4 = int(inputA4) * math.pi
        inputA5 = int(inputA5) * math.pi
        inputA6 = int(inputA6) * math.pi
        inputA7 = int(inputA7) * math.pi

        inputB0 = int(inputB0) * math.pi
        inputB1 = int(inputB1) * math.pi
        inputB2 = int(inputB2) * math.pi
        inputB3 = int(inputB3) * math.pi
        inputB4 = int(inputB4) * math.pi
        inputB5 = int(inputB5) * math.pi
        inputB6 = int(inputB6) * math.pi
        inputB7 = int(inputB7) * math.pi

         
        circuit = QuantumCircuit(19,19)

        #Bit 0
        circuit.ry(inputA0,0)
        circuit.ry(inputB0,1)
        #XOR 
        circuit.cx(0,1)
        circuit.x(1)            
        
        #Bit 1
        circuit.ry(inputA1,2)
        circuit.ry(inputB1,3)
        #XOR
        circuit.cx(2,3)
        circuit.x(3)            
        
        #Bit 2
        circuit.ry(inputA2,4)
        circuit.ry(inputB2,5)
        #XOR
        circuit.cx(4,5)
        circuit.x(5)            
        
        #Bit 3
        circuit.ry(inputA3,6)
        circuit.ry(inputB3,7)
        #XOR 
        circuit.cx(6,7)
        circuit.x(7)            
        
        #Bit 4
        circuit.ry(inputA4,8)
        circuit.ry(inputB4,9)
        #XOR 
        circuit.cx(8,9)
        circuit.x(9)            
        
        #Bit 5
        circuit.ry(inputA5,10)
        circuit.ry(inputB5,11)
        #XOR 
        circuit.cx(10,11)
        circuit.x(11)            
        
        #Bit 6
        circuit.ry(inputA6,12)
        circuit.ry(inputB6,13)
        #XOR 
        circuit.cx(12,13)
        circuit.x(13)            
        
        #Bit 7
        circuit.ry(inputA7,14)
        circuit.ry(inputB7,15)
        #XOR 
        circuit.cx(14,15)
        circuit.x(15)                        

        circuit.append(C4XGate(), [1,3,5,7, 16])
        circuit.append(C4XGate(), [9,11,13,15, 17])
        circuit.ccx(16,17,18)

        circuit.measure_all()

        print(circuit)

        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0
        qubit8 = 0
        qubit9 = 0
        qubit10 = 0
        qubit11 = 0
        qubit12 = 0
        qubit13 = 0
        qubit14 = 0
        qubit15 = 0
        qubit16 = 0
        qubit17 = 0
        qubit18 = 0
        
        for result in memory:

                    qubit0 = qubit0 + int(result[18])
                    qubit1 = qubit1 + int(result[17])
                    qubit2 = qubit2 + int(result[16])
                    qubit3 = qubit3 + int(result[15])
                    qubit4 = qubit4 + int(result[14])
                    qubit5 = qubit5 + int(result[13])
                    qubit6 = qubit6 + int(result[12])
                    qubit7 = qubit7 + int(result[11])
                    qubit8 = qubit8 + int(result[10])
                    qubit9 = qubit9 + int(result[9])
                    qubit10 = qubit10 + int(result[8])
                    qubit11 = qubit11 + int(result[7])
                    qubit12 = qubit12 + int(result[6])
                    qubit13 = qubit13 + int(result[5])
                    qubit14 = qubit14 + int(result[4])
                    qubit15 = qubit15 + int(result[3])
                    qubit16 = qubit16 + int(result[2])
                    qubit17 = qubit17 + int(result[1])
                    qubit18 = qubit18 + int(result[0])

                   
        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots
        qubit8 = qubit8/shots
        qubit9 = qubit9/shots
        qubit10 = qubit10/shots
        qubit11 = qubit11/shots
        qubit12 = qubit12/shots
        qubit13 = qubit13/shots
        qubit14 = qubit14/shots
        qubit15 = qubit15/shots
        qubit16 = qubit16/shots
        qubit17 = qubit17/shots
        qubit18 = qubit18/shots

        return str(round(qubit18)) 

    def myQuantumSwap(self,inputA0,inputA1,inputA2,inputA3,inputA4,inputA5,inputA6,inputA7,inputB0,inputB1,inputB2,inputB3,inputB4,inputB5,inputB6,inputB7):
        """
      ┌───────┐                        ┌─┐
 q_0: ┤ Ry(π) ├─X──────────────────────┤M├─────────────────────────────────────────────
      ├───────┤ │                      └╥┘┌─┐
 q_1: ┤ Ry(π) ├─┼──X────────────────────╫─┤M├──────────────────────────────────────────
      ├───────┤ │  │                    ║ └╥┘┌─┐
 q_2: ┤ Ry(π) ├─┼──┼──X─────────────────╫──╫─┤M├───────────────────────────────────────
      ├───────┤ │  │  │                 ║  ║ └╥┘┌─┐
 q_3: ┤ Ry(π) ├─┼──┼──┼──X──────────────╫──╫──╫─┤M├────────────────────────────────────
      ├───────┤ │  │  │  │              ║  ║  ║ └╥┘┌─┐
 q_4: ┤ Ry(π) ├─┼──┼──┼──┼──X───────────╫──╫──╫──╫─┤M├─────────────────────────────────
      ├───────┤ │  │  │  │  │           ║  ║  ║  ║ └╥┘┌─┐
 q_5: ┤ Ry(π) ├─┼──┼──┼──┼──┼──X────────╫──╫──╫──╫──╫─┤M├──────────────────────────────
      ├───────┤ │  │  │  │  │  │        ║  ║  ║  ║  ║ └╥┘┌─┐
 q_6: ┤ Ry(π) ├─┼──┼──┼──┼──┼──┼──X─────╫──╫──╫──╫──╫──╫─┤M├───────────────────────────
      ├───────┤ │  │  │  │  │  │  │     ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_7: ┤ Ry(π) ├─┼──┼──┼──┼──┼──┼──┼──X──╫──╫──╫──╫──╫──╫──╫─┤M├────────────────────────
      ├───────┤ │  │  │  │  │  │  │  │  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_8: ┤ Ry(0) ├─X──┼──┼──┼──┼──┼──┼──┼──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────────────────
      ├───────┤    │  │  │  │  │  │  │  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
 q_9: ┤ Ry(0) ├────X──┼──┼──┼──┼──┼──┼──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────────────────
      ├───────┤       │  │  │  │  │  │  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_10: ┤ Ry(0) ├───────X──┼──┼──┼──┼──┼──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───────────────
      ├───────┤          │  │  │  │  │  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_11: ┤ Ry(0) ├──────────X──┼──┼──┼──┼──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├────────────
      ├───────┤             │  │  │  │  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_12: ┤ Ry(0) ├─────────────X──┼──┼──┼──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├─────────
      ├───────┤                │  │  │  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_13: ┤ Ry(0) ├────────────────X──┼──┼──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├──────
      ├───────┤                   │  │  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_14: ┤ Ry(0) ├───────────────────X──┼──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├───
      ├───────┤                      │  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘┌─┐
q_15: ┤ Ry(0) ├──────────────────────X──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫──╫─┤M├
      └───────┘                         ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║  ║ └╥┘
c: 16/══════════════════════════════════╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩══╩═
                                        0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
        """
        print("The methods sees input A = " + str(inputA0) + str(inputA1) + str(inputA2) + str(inputA3) + str(inputA4) + str(inputA5) + str(inputA6) + str(inputA7) + " And input B = " + str(inputB0) + str(inputB1) + str(inputB2) + str(inputB3) + str(inputB4) + str(inputB5) + str(inputB6) + str(inputB7))

        inputA0 = int(inputA0) * math.pi
        inputA1 = int(inputA1) * math.pi
        inputA2 = int(inputA2) * math.pi
        inputA3 = int(inputA3) * math.pi
        inputA4 = int(inputA4) * math.pi
        inputA5 = int(inputA5) * math.pi
        inputA6 = int(inputA6) * math.pi
        inputA7 = int(inputA7) * math.pi

        inputB0 = int(inputB0) * math.pi
        inputB1 = int(inputB1) * math.pi
        inputB2 = int(inputB2) * math.pi
        inputB3 = int(inputB3) * math.pi
        inputB4 = int(inputB4) * math.pi
        inputB5 = int(inputB5) * math.pi
        inputB6 = int(inputB6) * math.pi
        inputB7 = int(inputB7) * math.pi


         
        circuit = QuantumCircuit(16,16)

        #Bit 0
        circuit.ry(inputA0,0)
        circuit.ry(inputB0,8)
        circuit.swap(0,8)

        #Bit 1
        circuit.ry(inputA1,1)
        circuit.ry(inputB1,9)
        circuit.swap(1,9)
        
        #Bit 2
        circuit.ry(inputA2,2)
        circuit.ry(inputB2,10)
        circuit.swap(2,10)
        
        #Bit 3
        circuit.ry(inputA3,3)
        circuit.ry(inputB3,11)
        circuit.swap(3,11)

        #Bit 4
        circuit.ry(inputA4,4)
        circuit.ry(inputB4,12)
        circuit.swap(4,12)
        
        #Bit 5
        circuit.ry(inputA5,5)
        circuit.ry(inputB5,13)
        circuit.swap(5,13)
        
        #Bit 6
        circuit.ry(inputA6,6)
        circuit.ry(inputB6,14)
        circuit.swap(6,14)
        
        #Bit 7
        circuit.ry(inputA7,7)
        circuit.ry(inputB7,15)
        circuit.swap(7,15)
                    

        circuit.measure_all() 


        print(circuit)
        

        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

        qubit0 = 0
        qubit1 = 0
        qubit2 = 0
        qubit3 = 0
        qubit4 = 0
        qubit5 = 0
        qubit6 = 0
        qubit7 = 0
        qubit8 = 0
        qubit9 = 0
        qubit10 = 0
        qubit11 = 0
        qubit12 = 0
        qubit13 = 0
        qubit14 = 0
        qubit15 = 0

        for result in memory:

                    qubit0 = qubit0 + int(result[15])
                    qubit1 = qubit1 + int(result[14])
                    qubit2 = qubit2 + int(result[13])
                    qubit3 = qubit3 + int(result[12])
                    qubit4 = qubit4 + int(result[11])
                    qubit5 = qubit5 + int(result[10])
                    qubit6 = qubit6 + int(result[9])
                    qubit7 = qubit7 + int(result[8])
                    qubit8 = qubit8 + int(result[7])
                    qubit9 = qubit9 + int(result[6])
                    qubit10 = qubit10 + int(result[5])
                    qubit11 = qubit11 + int(result[4])
                    qubit12 = qubit12 + int(result[3])
                    qubit13 = qubit13 + int(result[2])
                    qubit14 = qubit14 + int(result[1])
                    qubit15 = qubit15 + int(result[0])

        qubit0 = qubit0/shots
        qubit1 = qubit1/shots
        qubit2 = qubit2/shots
        qubit3 = qubit3/shots
        qubit4 = qubit4/shots
        qubit5 = qubit5/shots
        qubit6 = qubit6/shots
        qubit7 = qubit7/shots
        qubit8 = qubit8/shots
        qubit9 = qubit9/shots
        qubit10 = qubit10/shots
        qubit11 = qubit11/shots
        qubit12 = qubit12/shots
        qubit13 = qubit13/shots
        qubit14 = qubit14/shots
        qubit15 = qubit15/shots


        return str(round(qubit0)) + str(round(qubit1)) + str(round(qubit2)) + str(round(qubit3)) + str(round(qubit4)) + str(round(qubit5)) + str(round(qubit6)) + str(round(qubit7)) + str(round(qubit8)) + str(round(qubit9)) + str(round(qubit10)) + str(round(qubit11)) + str(round(qubit12)) + str(round(qubit13)) + str(round(qubit14)) + str(round(qubit15))



#****************************************************************************************************************************************************************************
#****************************************************************************************************************************************************************************
#************************************************************* CPU Instructions with 2+ Quantum Methods **********************************************************************
#****************************************************************************************************************************************************************************
#****************************************************************************************************************************************************************************

    def eightbitinc(self,register):
        if self.QuantumExecute != "INC1" and self.QuantumExecute != "INC2" and self.QuantumExecute != "INC3":

            x = int(register,2)
            x = x + 1 
            if x == 256: x = 0
            register = format(x, '08b')
            
            #Set flags
            H = "0"
            P = "0"
            N = "0"
            C = self.F[7]
            if register  == "10000000": P = "1"
            if register[7] == "0" and register[6] == "0" and register[5] == "0" and register[4] == "0": H = "1"
            self.F = register[0] + self.getZflag(register) + register[2] + H + register[4] + P + "0" + C
            
        if self.QuantumExecute == "INC1":
            self.debugline = "Quantum method 1"
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

            #Set flags
            H = "0"
            P = "0"
            N = "0"
            C = self.F[7]
            if register  == "10000000": P = "1"
            if register[7] == "0" and register[6] == "0" and register[5] == "0" and register[4] == "0": H = "1"
            self.F = register[0] + self.getZflag(register) + register[2] + H + register[4] + P + "0" + C

            
        if self.QuantumExecute == "INC2":
            self.debugline = "Quantum method 2"
            inputA = register            
            register = self.myQuantum8BitInc(inputA[0],inputA[1],inputA[2],inputA[3],inputA[4],inputA[5],inputA[6],inputA[7],"1")
            register = register[-8:]

            #Set flags
            H = "0"
            P = "0"
            N = "0"
            C = self.F[7]
            if register  == "10000000": P = "1"
            if register[7] == "0" and register[6] == "0" and register[5] == "0" and register[4] == "0": H = "1"
            self.F = register[0] + self.getZflag(register) + register[2] + H + register[4] + P + "0" + C

        if self.QuantumExecute == "INC3":
            self.debugline = "Quantum method 3"
            inputA = register            
            temp = self.myQuantum8BitIncWithFlags(inputA[0],inputA[1],inputA[2],inputA[3],inputA[4],inputA[5],inputA[6],inputA[7])
            register = temp[0] + temp[1] + temp[2] + temp[3] + temp[4] + temp[5] + temp[6] + temp[7]
            register = register[-8:]

            #Set flags
            S = temp[9]
            Z = temp[10]
            H = temp[11]
            P = temp[12]
            N = temp[13]
            C = self.F[7]

            self.F = S + Z + register[2] + H + register[4] + P + N + C            
        
        self.clearop()
        self.delay = 1



        return register

    def sixteenbitinc(self,register1,register2):
        if self.opcode == "00110011":
            rr = int(format(self.SP,'016b'),2)
        else:
            rr = int(register1 + register2,2)
        if self.opcode == "00100011" and self.preopcode == "11011101":
            rr = int(self.IX,2)
        if self.opcode == "00100011" and self.preopcode == "11111101":
            rr = int(self.IY,2)

        if self.QuantumExecute != "INC1" and self.QuantumExecute != "INC2":

            rr = rr + 1
            if rr > 65535:
                rr = rr - 65536
            total = format(rr, '016b')
        if self.QuantumExecute == "INC1":
            self.debugline = "Quantum method 1"

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
            
        if self.QuantumExecute == "INC2":
            self.debugline = "Quantum method 2"
            
            inputA = format(rr, '016b')
            inputA = inputA[::-1]    
            
            lsbAndCarry = self.myQuantum8BitInc(inputA[7],inputA[6],inputA[5],inputA[4],inputA[3],inputA[2],inputA[1],inputA[0],"1")
            carry = lsbAndCarry[0]
            lsbAndCarry = lsbAndCarry[-8:]            

            msbAndCarry = self.myQuantum8BitInc(inputA[15],inputA[14],inputA[13],inputA[12],inputA[11],inputA[10],inputA[9],inputA[8],carry)
            msbAndCarry = msbAndCarry[-8:]            
                        
            register = int(msbAndCarry + lsbAndCarry,2)
            total = format(register, '016b')
            
            

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

    def incNoFlags(self,number):
        if self.QuantumExecute != "INC1" and self.QuantumExecute != "INC2":

            number = number + 1
            if number == 65536: number = 0
            return number

        if self.QuantumExecute == "INC1":
            self.debugline = "Quantum method 1"


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

        if self.QuantumExecute == "INC2":
            self.debugline = "Quantum method 2"
            
            inputA = format(number, '016b')
            inputA = inputA[::-1]    
            
            lsbAndCarry = self.myQuantum8BitInc(inputA[7],inputA[6],inputA[5],inputA[4],inputA[3],inputA[2],inputA[1],inputA[0],"1")
            carry = lsbAndCarry[0]
            lsbAndCarry = lsbAndCarry[-8:]            

            msbAndCarry = self.myQuantum8BitInc(inputA[15],inputA[14],inputA[13],inputA[12],inputA[11],inputA[10],inputA[9],inputA[8],carry)
            msbAndCarry = msbAndCarry[-8:]            
                        
            register = msbAndCarry + lsbAndCarry
            return int(register,2)
 
    def eightbitdec(self,register):
        if self.QuantumExecute != "DEC1" and self.QuantumExecute != "DEC2":

            x = int(register,2)
            x = x - 1
            if x == -1: x = 255
            register = format(x, '08b')
        if self.QuantumExecute == "DEC1":
            self.debufline = "Quantum method 1"
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
        if self.QuantumExecute == "DEC2":
            self.debugline = "Quantum method 2"
            inputA = register   
                    
            
            lsbAndBorrow = self.myQuantum4BitDec(inputA[4],inputA[5],inputA[6],inputA[7],"0")
            borrow1 = lsbAndBorrow[0]
            lsbAndBorrow = lsbAndBorrow[-4:]            
            
            msbAndBorrow = self.myQuantum4BitDec(inputA[0],inputA[1],inputA[2],inputA[3],borrow1)
            borrow2 = msbAndBorrow[0]
            msbAndBorrow = msbAndBorrow[-4:]
            
            
            register = msbAndBorrow + lsbAndBorrow            
            
  
           
            
        self.clearop()
        self.delay = 1

        #set flags
        H = "0"
        if register[7] == "1" and register[6] == "1" and register[5] == "1" and register[4] == "1": H = "1"
        P = "0"
        if register == "01111111": P = "1"
        self.F = register[0] + self.getZflag(register) + register[2] + H + register[4] + P + "1" + self.F[7]

        return register

    def decNoFlags(self,number):
        if self.QuantumExecute != "DEC1" and self.QuantumExecute != "DEC2":

            number = number - 1
            if number < 0: number = number + 65536
            return number

        if self.QuantumExecute == "DEC1":
            self.debufline = "Quantum method 1"

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
            
        if self.QuantumExecute == "DEC2":
            self.debugline = "Quantum method 2"
            
            inputA = format(number, '016b')

            lllsbAndBorrow = self.myQuantum4BitDec(inputA[12],inputA[13],inputA[14],inputA[15],"0")
            borrow = lllsbAndBorrow[0]
            lllsbAndBorrow = lllsbAndBorrow[-4:]
            
            llsbAndBorrow = self.myQuantum4BitDec(inputA[8],inputA[9],inputA[10],inputA[11],borrow)
            borrow0 = llsbAndBorrow[0]
            llsbAndBorrow = llsbAndBorrow[-4:]
            
            lsbAndBorrow = self.myQuantum4BitDec(inputA[4],inputA[5],inputA[6],inputA[7],borrow0)
            borrow1 = lsbAndBorrow[0]
            lsbAndBorrow = lsbAndBorrow[-4:]            
            
            msbAndBorrow = self.myQuantum4BitDec(inputA[0],inputA[1],inputA[2],inputA[3],borrow1)
            borrow2 = msbAndBorrow[0]
            msbAndBorrow = msbAndBorrow[-4:]
            
            
            register = msbAndBorrow + lsbAndBorrow + llsbAndBorrow + lllsbAndBorrow    
            return int(register,2)
  
    def sixteenbitdec(self,register1,register2):
        if self.opcode == "00111011":
            rr = int(format(self.SP,'016b'),2)
        else:
            rr = int(register1 + register2,2)

        if self.opcode == "00101011" and self.preopcode == "11011101":
            rr = int(self.IX,2)
        if self.opcode == "00101011" and self.preopcode == "11111101":
            rr = int(self.IY,2)

        if self.QuantumExecute != "DEC1" and self.QuantumExecute != "DEC2":

            rr = rr - 1
            if rr < 0:
               rr = rr + 65536
            total = format(rr, '016b')
        if self.QuantumExecute == "DEC1":
            self.debufline = "Quantum method 1"
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
            
        if self.QuantumExecute == "DEC2":
            self.debugline = "Quantum method 2"
            inputA = format(rr, '016b')

            lllsbAndBorrow = self.myQuantum4BitDec(inputA[12],inputA[13],inputA[14],inputA[15],"0")
            borrow = lllsbAndBorrow[0]
            lllsbAndBorrow = lllsbAndBorrow[-4:]
            
            llsbAndBorrow = self.myQuantum4BitDec(inputA[8],inputA[9],inputA[10],inputA[11],borrow)
            borrow0 = llsbAndBorrow[0]
            llsbAndBorrow = llsbAndBorrow[-4:]
            
            lsbAndBorrow = self.myQuantum4BitDec(inputA[4],inputA[5],inputA[6],inputA[7],borrow0)
            borrow1 = lsbAndBorrow[0]
            lsbAndBorrow = lsbAndBorrow[-4:]            
            
            msbAndBorrow = self.myQuantum4BitDec(inputA[0],inputA[1],inputA[2],inputA[3],borrow1)
            borrow2 = msbAndBorrow[0]
            msbAndBorrow = msbAndBorrow[-4:]
            
            
            register = msbAndBorrow + lsbAndBorrow + llsbAndBorrow + lllsbAndBorrow    
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
    
    def eightBitDecNoFlags(self,register):
        if self.QuantumExecute != "DEC1" and self.QuantumExecute != "DEC2":

            x = register
            x = x - 1
            if x == -1: x = 255
            return x
        if self.QuantumExecute == "DEC1":
            self.debufline = "Quantum method 1"
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
        if self.QuantumExecute == "DEC2":
            self.debugline = "Quantum method 2"
            inputA = format(register,'08b')
                   
            
            lsbAndBorrow = self.myQuantum4BitDec(inputA[4],inputA[5],inputA[6],inputA[7],"0")
            borrow1 = lsbAndBorrow[0]
            lsbAndBorrow = lsbAndBorrow[-4:]            
            
            msbAndBorrow = self.myQuantum4BitDec(inputA[0],inputA[1],inputA[2],inputA[3],borrow1)
            borrow2 = msbAndBorrow[0]
            msbAndBorrow = msbAndBorrow[-4:]
            
            
            register = msbAndBorrow + lsbAndBorrow    
            return int(register,2)                    
            
    def eightbitxor(self,register):

        if self.QuantumExecute != "XOR1" and self.QuantumExecute != "XOR2":

            A = int(self.A,2)
            xorwith = int(register,2)
            xored = bin(A ^ xorwith)[2:].zfill(8)
            
        if self.QuantumExecute == "XOR1":
            self.debugline = "Quantum method 1"
            xored = ""
            xored = xored + str(self.myxor(int(self.A[0]),int(register[0])))
            xored = xored + str(self.myxor(int(self.A[1]),int(register[1])))
            xored = xored + str(self.myxor(int(self.A[2]),int(register[2])))
            xored = xored + str(self.myxor(int(self.A[3]),int(register[3])))
            xored = xored + str(self.myxor(int(self.A[4]),int(register[4])))
            xored = xored + str(self.myxor(int(self.A[5]),int(register[5])))
            xored = xored + str(self.myxor(int(self.A[6]),int(register[6])))
            xored = xored + str(self.myxor(int(self.A[7]),int(register[7])))
            
        if self.QuantumExecute == "XOR2":
            self.debugline = "Quantum method 2"
            xored = self.myQuantum8BitXor(self.A[0],self.A[1],self.A[2],self.A[3],self.A[4],self.A[5],self.A[6],self.A[7],register[0],register[1],register[2],register[3],register[4],register[5],register[6],register[7])
        
        #set flags
        self.F = xored[0] + self.getZflag(xored) + xored[2] + "0" + xored[4] + self.getparity(xored) + "0" + "0"
        self.clearop()
        self.delay =  1

        return xored   

    def eightbitand(self,register):

        if self.QuantumExecute != "AND1" and self.QuantumExecute != "AND2":

            A = int(self.A,2)
            andwith = int(register,2)
            anded = bin(A & andwith)[2:].zfill(8)
            
        if self.QuantumExecute == "AND1":
            self.debugline = "Quantum method 1"
            anded = ""
            anded = anded + str(self.myand(int(self.A[0]),int(register[0]))) 
            anded = anded + str(self.myand(int(self.A[1]),int(register[1]))) 
            anded = anded + str(self.myand(int(self.A[2]),int(register[2]))) 
            anded = anded + str(self.myand(int(self.A[3]),int(register[3]))) 
            anded = anded + str(self.myand(int(self.A[4]),int(register[4]))) 
            anded = anded + str(self.myand(int(self.A[5]),int(register[5]))) 
            anded = anded + str(self.myand(int(self.A[6]),int(register[6]))) 
            anded = anded + str(self.myand(int(self.A[7]),int(register[7]))) 

        if self.QuantumExecute == "AND2":
            self.debugline = "Quantum method 2"
            anded = self.myQuantum8BitAnd(self.A[0],self.A[1],self.A[2],self.A[3],self.A[4],self.A[5],self.A[6],self.A[7],register[0],register[1],register[2],register[3],register[4],register[5],register[6],register[7])

        #set flags
        self.F = anded[0] + self.getZflag(anded) + anded[2] + "1" + anded[4] + self.getparity(anded) + "0" + "0"
        self.clearop()
        self.delay =  1

        return anded

    def singleand(self,register1,register2):
        if self.QuantumExecute != "AND1" and self.QuantumExecute != "AND2":

            return (register1 & register2)
        if self.QuantumExecute == "AND1":
            self.debugline = "Quantum method 1"
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
            
        if self.QuantumExecute == "AND2":
            self.debugline = "Quantum method 2"
            register1 = str(bin(register1)[2:].zfill(8))
            register2 = str(bin(register2)[2:].zfill(8))
            anded = self.myQuantum8BitAnd(register1[0],register1[1],register1[2],register1[3],register1[4],register1[5],register1[6],register1[7],register2[0],register2[1],register2[2],register2[3],register2[4],register2[5],register2[6],register2[7])
            return int(anded,2)

    def eightbitor(self,register):

        if self.QuantumExecute != "OR1" and self.QuantumExecute != "OR2":

            A = int(self.A,2)
            oredwith = int(register,2)
            ored = bin(A | oredwith)[2:].zfill(8)

        if self.QuantumExecute == "OR1":
            ored = ""
            ored = ored + str(self.myor(int(self.A[0]),int(register[0])))
            ored = ored + str(self.myor(int(self.A[1]),int(register[1])))
            ored = ored + str(self.myor(int(self.A[2]),int(register[2])))
            ored = ored + str(self.myor(int(self.A[3]),int(register[3])))
            ored = ored + str(self.myor(int(self.A[4]),int(register[4])))
            ored = ored + str(self.myor(int(self.A[5]),int(register[5])))
            ored = ored + str(self.myor(int(self.A[6]),int(register[6])))
            ored = ored + str(self.myor(int(self.A[7]),int(register[7])))

        if self.QuantumExecute == "OR2":
            ored = self.myQuantum8BitOr(self.A[0],self.A[1],self.A[2],self.A[3],self.A[4],self.A[5],self.A[6],self.A[7],register[0],register[1],register[2],register[3],register[4],register[5],register[6],register[7])

        #set flags
        self.F = ored[0] + self.getZflag(ored) + ored[2] + "0" + ored[4] + self.getparity(ored) + "0" + "0"
        self.clearop()
        self.delay =  1

        return ored

    def singleor(self,register1,register2):
        if self.QuantumExecute != "OR1" and self.QuantumExecute != "OR2":

            return (register1 | register2)
            

        if self.QuantumExecute == "OR1":
            self.debugline = "Quantum method 1"
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
            
        if self.QuantumExecute == "OR2":
            self.debugline = "Quantum method 2"
            register1 = str(bin(register1)[2:].zfill(8))
            register2 = str(bin(register2)[2:].zfill(8))
            ored = self.myQuantum8BitOr(register1[0],register1[1],register1[2],register1[3],register1[4],register1[5],register1[6],register1[7],register2[0],register2[1],register2[2],register2[3],register2[4],register2[5],register2[6],register2[7])  
            return int(ored,2)

    def eightbitld(self,register1,register2):


        if self.QuantumExecute != "LOAD1" and self.QuantumExecute != "LOAD2" and self.QuantumExecute != "LOAD3":


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
            
        if self.QuantumExecute == "LOAD1":
            self.debugline = "Quantum method 1"
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

        if self.QuantumExecute == "LOAD2":
            self.debugline = "Quantum method 2"
            if self.preopcode == "11011101" and self.opcode == "01100000": self.IX = register2 + self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100000": self.IY = register2 + self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100001": self.IX = register2 + self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100001": self.IY = register2 + self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100010": self.IX = register2 + self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100010": self.IY = register2 + self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100011": self.IX = register2 + self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100011": self.IY = register2 + self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100111": self.IX = register2 + self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100111": self.IY = register2 + self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01101000": self.IX = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101000": self.IY = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101001": self.IX = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101001": self.IY = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101010": self.IX = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101010": self.IY = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101011": self.IX = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101011": self.IY = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101111": self.IX = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101111": self.IY = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) + register2

            if self.preopcode == "11011101" and self.opcode == "01000100": self.B = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000100": self.B = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01000101": self.B = self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01000101": self.B = self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16]) 

            if self.preopcode == "11011101" and self.opcode == "01010100": self.D = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010100": self.D = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01010101": self.D = self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01010101": self.D = self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01001100": self.C = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001100": self.C = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01001101": self.C = self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01001101": self.C = self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01111100": self.A = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111100": self.A = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8])#self.IY[0:8]
            if self.preopcode == "11011101" and self.opcode == "01111101": self.A = self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])#self.IX[8:16]
            if self.preopcode == "11111101" and self.opcode == "01111101": self.A = self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16])#self.IY[8:16]

            if self.preopcode == "11011101" and self.opcode == "01011100": self.E = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8]) 
            if self.preopcode == "11111101" and self.opcode == "01011100": self.E = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01011101": self.E = self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16]) 
            if self.preopcode == "11111101" and self.opcode == "01011101": self.E = self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16]) 

            if self.preopcode == "11011101" and self.opcode == "01101100": self.IX = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8]) +  self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01101100": self.IY = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) +  self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8])

            if self.preopcode == "11011101" and self.opcode == "01100101": self.IX = self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16]) +  self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100101": self.IY = self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16]) +  self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01000000": register1 = self.myQuantum4BitLatch(self.B[0:4]) + self.myQuantum4BitLatch(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000000": register1 = self.myQuantum4BitLatch(self.B[0:4]) + self.myQuantum4BitLatch(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01000001": register1 = self.myQuantum4BitLatch(self.C[0:4]) + self.myQuantum4BitLatch(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000001": register1 = self.myQuantum4BitLatch(self.C[0:4]) + self.myQuantum4BitLatch(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01000010": register1 = self.myQuantum4BitLatch(self.D[0:4]) + self.myQuantum4BitLatch(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000010": register1 = self.myQuantum4BitLatch(self.D[0:4]) + self.myQuantum4BitLatch(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01000011": register1 = self.myQuantum4BitLatch(self.E[0:4]) + self.myQuantum4BitLatch(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000011": register1 = self.myQuantum4BitLatch(self.E[0:4]) + self.myQuantum4BitLatch(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01010000": register1 = self.myQuantum4BitLatch(self.B[0:4]) + self.myQuantum4BitLatch(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010000": register1 = self.myQuantum4BitLatch(self.B[0:4]) + self.myQuantum4BitLatch(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01010001": register1 = self.myQuantum4BitLatch(self.C[0:4]) + self.myQuantum4BitLatch(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010001": register1 = self.myQuantum4BitLatch(self.C[0:4]) + self.myQuantum4BitLatch(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01010010": register1 = self.myQuantum4BitLatch(self.D[0:4]) + self.myQuantum4BitLatch(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010010": register1 = self.myQuantum4BitLatch(self.D[0:4]) + self.myQuantum4BitLatch(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01010011": register1 = self.myQuantum4BitLatch(self.E[0:4]) + self.myQuantum4BitLatch(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010011": register1 = self.myQuantum4BitLatch(self.E[0:4]) + self.myQuantum4BitLatch(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01000111": register1 = self.myQuantum4BitLatch(self.A[0:4]) + self.myQuantum4BitLatch(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000111": register1 = self.myQuantum4BitLatch(self.A[0:4]) + self.myQuantum4BitLatch(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01001000": register1 = self.myQuantum4BitLatch(self.B[0:4]) + self.myQuantum4BitLatch(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001000": register1 = self.myQuantum4BitLatch(self.B[0:4]) + self.myQuantum4BitLatch(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01001001": register1 = self.myQuantum4BitLatch(self.C[0:4]) + self.myQuantum4BitLatch(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001001": register1 = self.myQuantum4BitLatch(self.C[0:4]) + self.myQuantum4BitLatch(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01001010": register1 = self.myQuantum4BitLatch(self.D[0:4]) + self.myQuantum4BitLatch(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001010": register1 = self.myQuantum4BitLatch(self.D[0:4]) + self.myQuantum4BitLatch(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01001011": register1 = self.myQuantum4BitLatch(self.E[0:4]) + self.myQuantum4BitLatch(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001011": register1 = self.myQuantum4BitLatch(self.E[0:4]) + self.myQuantum4BitLatch(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01001111": register1 = self.myQuantum4BitLatch(self.A[0:4]) + self.myQuantum4BitLatch(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001111": register1 = self.myQuantum4BitLatch(self.A[0:4]) + self.myQuantum4BitLatch(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01010111": register1 = self.myQuantum4BitLatch(self.A[0:4]) + self.myQuantum4BitLatch(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010111": register1 = self.myQuantum4BitLatch(self.A[0:4]) + self.myQuantum4BitLatch(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01011000": register1 = self.myQuantum4BitLatch(self.B[0:4]) + self.myQuantum4BitLatch(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011000": register1 = self.myQuantum4BitLatch(self.B[0:4]) + self.myQuantum4BitLatch(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01011001": register1 = self.myQuantum4BitLatch(self.C[0:4]) + self.myQuantum4BitLatch(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011001": register1 = self.myQuantum4BitLatch(self.C[0:4]) + self.myQuantum4BitLatch(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01011010": register1 = self.myQuantum4BitLatch(self.D[0:4]) + self.myQuantum4BitLatch(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011010": register1 = self.myQuantum4BitLatch(self.D[0:4]) + self.myQuantum4BitLatch(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01011011": register1 = self.myQuantum4BitLatch(self.E[0:4]) + self.myQuantum4BitLatch(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011011": register1 = self.myQuantum4BitLatch(self.E[0:4]) + self.myQuantum4BitLatch(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01011111": register1 = self.myQuantum4BitLatch(self.A[0:4]) + self.myQuantum4BitLatch(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011111": register1 = self.myQuantum4BitLatch(self.A[0:4]) + self.myQuantum4BitLatch(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01111000": register1 = self.myQuantum4BitLatch(self.B[0:4]) + self.myQuantum4BitLatch(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111000": register1 = self.myQuantum4BitLatch(self.B[0:4]) + self.myQuantum4BitLatch(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01111001": register1 = self.myQuantum4BitLatch(self.C[0:4]) + self.myQuantum4BitLatch(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111001": register1 = self.myQuantum4BitLatch(self.C[0:4]) + self.myQuantum4BitLatch(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01111010": register1 = self.myQuantum4BitLatch(self.D[0:4]) + self.myQuantum4BitLatch(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111010": register1 = self.myQuantum4BitLatch(self.D[0:4]) + self.myQuantum4BitLatch(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01111011": register1 = self.myQuantum4BitLatch(self.E[0:4]) + self.myQuantum4BitLatch(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111011": register1 = self.myQuantum4BitLatch(self.E[0:4]) + self.myQuantum4BitLatch(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01111111": register1 = self.myQuantum4BitLatch(self.A[0:4]) + self.myQuantum4BitLatch(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111111": register1 = self.myQuantum4BitLatch(self.A[0:4]) + self.myQuantum4BitLatch(self.A[4:8])
 
            if self.preopcode == "11011101" and self.opcode == "01100100": self.IX = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8]) +  self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100100": self.IY = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) +  self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01101101": self.IX = self.myQuantum4BitLatch(self.IX[0:4]) + self.myQuantum4BitLatch(self.IX[4:8]) +  self.myQuantum4BitLatch(self.IX[8:12]) + self.myQuantum4BitLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01101101": self.IY = self.myQuantum4BitLatch(self.IY[0:4]) + self.myQuantum4BitLatch(self.IY[4:8]) +  self.myQuantum4BitLatch(self.IY[8:12]) + self.myQuantum4BitLatch(self.IY[12:16])

            if self.preopcode == "":
                register1 = self.myQuantum4BitLatch(register2[0:4]) + self.myQuantum4BitLatch(register2[4:8])

            self.clearop()
            self.delay = 1
            #No flags effected
            return register1

        if self.QuantumExecute == "LOAD3":
            self.debugline = "Quantum method 3"
            if self.preopcode == "11011101" and self.opcode == "01100000": self.IX = register2 + self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100000": self.IY = register2 + self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100001": self.IX = register2 + self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100001": self.IY = register2 + self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100010": self.IX = register2 + self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100010": self.IY = register2 + self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100011": self.IX = register2 + self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100011": self.IY = register2 + self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01100111": self.IX = register2 + self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100111": self.IY = register2 + self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01101000": self.IX = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101000": self.IY = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101001": self.IX = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101001": self.IY = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101010": self.IX = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101010": self.IY = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101011": self.IX = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101011": self.IY = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) + register2
            if self.preopcode == "11011101" and self.opcode == "01101111": self.IX = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8]) + register2
            if self.preopcode == "11111101" and self.opcode == "01101111": self.IY = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) + register2

            if self.preopcode == "11011101" and self.opcode == "01000100": self.B = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000100": self.B = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01000101": self.B = self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01000101": self.B = self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16]) 

            if self.preopcode == "11011101" and self.opcode == "01010100": self.D = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010100": self.D = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01010101": self.D = self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01010101": self.D = self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01001100": self.C = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001100": self.C = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01001101": self.C = self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01001101": self.C = self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01111100": self.A = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111100": self.A = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8])#self.IY[0:8]
            if self.preopcode == "11011101" and self.opcode == "01111101": self.A = self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])#self.IX[8:16]
            if self.preopcode == "11111101" and self.opcode == "01111101": self.A = self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16])#self.IY[8:16]

            if self.preopcode == "11011101" and self.opcode == "01011100": self.E = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8]) 
            if self.preopcode == "11111101" and self.opcode == "01011100": self.E = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) 
            if self.preopcode == "11011101" and self.opcode == "01011101": self.E = self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16]) 
            if self.preopcode == "11111101" and self.opcode == "01011101": self.E = self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16]) 

            if self.preopcode == "11011101" and self.opcode == "01101100": self.IX = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8]) +  self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8])
            if self.preopcode == "11111101" and self.opcode == "01101100": self.IY = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) +  self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8])

            if self.preopcode == "11011101" and self.opcode == "01100101": self.IX = self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16]) +  self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100101": self.IY = self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16]) +  self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16])

            if self.preopcode == "11011101" and self.opcode == "01000000": register1 = self.myQuantum4BitHadamardLatch(self.B[0:4]) + self.myQuantum4BitHadamardLatch(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000000": register1 = self.myQuantum4BitHadamardLatch(self.B[0:4]) + self.myQuantum4BitHadamardLatch(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01000001": register1 = self.myQuantum4BitHadamardLatch(self.C[0:4]) + self.myQuantum4BitHadamardLatch(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000001": register1 = self.myQuantum4BitHadamardLatch(self.C[0:4]) + self.myQuantum4BitHadamardLatch(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01000010": register1 = self.myQuantum4BitHadamardLatch(self.D[0:4]) + self.myQuantum4BitHadamardLatch(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000010": register1 = self.myQuantum4BitHadamardLatch(self.D[0:4]) + self.myQuantum4BitHadamardLatch(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01000011": register1 = self.myQuantum4BitHadamardLatch(self.E[0:4]) + self.myQuantum4BitHadamardLatch(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000011": register1 = self.myQuantum4BitHadamardLatch(self.E[0:4]) + self.myQuantum4BitHadamardLatch(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01010000": register1 = self.myQuantum4BitHadamardLatch(self.B[0:4]) + self.myQuantum4BitHadamardLatch(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010000": register1 = self.myQuantum4BitHadamardLatch(self.B[0:4]) + self.myQuantum4BitHadamardLatch(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01010001": register1 = self.myQuantum4BitHadamardLatch(self.C[0:4]) + self.myQuantum4BitHadamardLatch(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010001": register1 = self.myQuantum4BitHadamardLatch(self.C[0:4]) + self.myQuantum4BitHadamardLatch(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01010010": register1 = self.myQuantum4BitHadamardLatch(self.D[0:4]) + self.myQuantum4BitHadamardLatch(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010010": register1 = self.myQuantum4BitHadamardLatch(self.D[0:4]) + self.myQuantum4BitHadamardLatch(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01010011": register1 = self.myQuantum4BitHadamardLatch(self.E[0:4]) + self.myQuantum4BitHadamardLatch(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010011": register1 = self.myQuantum4BitHadamardLatch(self.E[0:4]) + self.myQuantum4BitHadamardLatch(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01000111": register1 = self.myQuantum4BitHadamardLatch(self.A[0:4]) + self.myQuantum4BitHadamardLatch(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01000111": register1 = self.myQuantum4BitHadamardLatch(self.A[0:4]) + self.myQuantum4BitHadamardLatch(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01001000": register1 = self.myQuantum4BitHadamardLatch(self.B[0:4]) + self.myQuantum4BitHadamardLatch(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001000": register1 = self.myQuantum4BitHadamardLatch(self.B[0:4]) + self.myQuantum4BitHadamardLatch(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01001001": register1 = self.myQuantum4BitHadamardLatch(self.C[0:4]) + self.myQuantum4BitHadamardLatch(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001001": register1 = self.myQuantum4BitHadamardLatch(self.C[0:4]) + self.myQuantum4BitHadamardLatch(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01001010": register1 = self.myQuantum4BitHadamardLatch(self.D[0:4]) + self.myQuantum4BitHadamardLatch(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001010": register1 = self.myQuantum4BitHadamardLatch(self.D[0:4]) + self.myQuantum4BitHadamardLatch(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01001011": register1 = self.myQuantum4BitHadamardLatch(self.E[0:4]) + self.myQuantum4BitHadamardLatch(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001011": register1 = self.myQuantum4BitHadamardLatch(self.E[0:4]) + self.myQuantum4BitHadamardLatch(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01001111": register1 = self.myQuantum4BitHadamardLatch(self.A[0:4]) + self.myQuantum4BitHadamardLatch(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01001111": register1 = self.myQuantum4BitHadamardLatch(self.A[0:4]) + self.myQuantum4BitHadamardLatch(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01010111": register1 = self.myQuantum4BitHadamardLatch(self.A[0:4]) + self.myQuantum4BitHadamardLatch(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01010111": register1 = self.myQuantum4BitHadamardLatch(self.A[0:4]) + self.myQuantum4BitHadamardLatch(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01011000": register1 = self.myQuantum4BitHadamardLatch(self.B[0:4]) + self.myQuantum4BitHadamardLatch(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011000": register1 = self.myQuantum4BitHadamardLatch(self.B[0:4]) + self.myQuantum4BitHadamardLatch(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01011001": register1 = self.myQuantum4BitHadamardLatch(self.C[0:4]) + self.myQuantum4BitHadamardLatch(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011001": register1 = self.myQuantum4BitHadamardLatch(self.C[0:4]) + self.myQuantum4BitHadamardLatch(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01011010": register1 = self.myQuantum4BitHadamardLatch(self.D[0:4]) + self.myQuantum4BitHadamardLatch(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011010": register1 = self.myQuantum4BitHadamardLatch(self.D[0:4]) + self.myQuantum4BitHadamardLatch(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01011011": register1 = self.myQuantum4BitHadamardLatch(self.E[0:4]) + self.myQuantum4BitHadamardLatch(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011011": register1 = self.myQuantum4BitHadamardLatch(self.E[0:4]) + self.myQuantum4BitHadamardLatch(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01011111": register1 = self.myQuantum4BitHadamardLatch(self.A[0:4]) + self.myQuantum4BitHadamardLatch(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01011111": register1 = self.myQuantum4BitHadamardLatch(self.A[0:4]) + self.myQuantum4BitHadamardLatch(self.A[4:8])

            if self.preopcode == "11011101" and self.opcode == "01111000": register1 = self.myQuantum4BitHadamardLatch(self.B[0:4]) + self.myQuantum4BitHadamardLatch(self.B[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111000": register1 = self.myQuantum4BitHadamardLatch(self.B[0:4]) + self.myQuantum4BitHadamardLatch(self.B[4:8])
            if self.preopcode == "11011101" and self.opcode == "01111001": register1 = self.myQuantum4BitHadamardLatch(self.C[0:4]) + self.myQuantum4BitHadamardLatch(self.C[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111001": register1 = self.myQuantum4BitHadamardLatch(self.C[0:4]) + self.myQuantum4BitHadamardLatch(self.C[4:8])
            if self.preopcode == "11011101" and self.opcode == "01111010": register1 = self.myQuantum4BitHadamardLatch(self.D[0:4]) + self.myQuantum4BitHadamardLatch(self.D[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111010": register1 = self.myQuantum4BitHadamardLatch(self.D[0:4]) + self.myQuantum4BitHadamardLatch(self.D[4:8])
            if self.preopcode == "11011101" and self.opcode == "01111011": register1 = self.myQuantum4BitHadamardLatch(self.E[0:4]) + self.myQuantum4BitHadamardLatch(self.E[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111011": register1 = self.myQuantum4BitHadamardLatch(self.E[0:4]) + self.myQuantum4BitHadamardLatch(self.E[4:8])

            if self.preopcode == "11011101" and self.opcode == "01111111": register1 = self.myQuantum4BitHadamardLatch(self.A[0:4]) + self.myQuantum4BitHadamardLatch(self.A[4:8])
            if self.preopcode == "11111101" and self.opcode == "01111111": register1 = self.myQuantum4BitHadamardLatch(self.A[0:4]) + self.myQuantum4BitHadamardLatch(self.A[4:8])
 
            if self.preopcode == "11011101" and self.opcode == "01100100": self.IX = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8]) +  self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01100100": self.IY = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) +  self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16])
            if self.preopcode == "11011101" and self.opcode == "01101101": self.IX = self.myQuantum4BitHadamardLatch(self.IX[0:4]) + self.myQuantum4BitHadamardLatch(self.IX[4:8]) +  self.myQuantum4BitHadamardLatch(self.IX[8:12]) + self.myQuantum4BitHadamardLatch(self.IX[12:16])
            if self.preopcode == "11111101" and self.opcode == "01101101": self.IY = self.myQuantum4BitHadamardLatch(self.IY[0:4]) + self.myQuantum4BitHadamardLatch(self.IY[4:8]) +  self.myQuantum4BitHadamardLatch(self.IY[8:12]) + self.myQuantum4BitHadamardLatch(self.IY[12:16])

            if self.preopcode == "":
                register1 = self.myQuantum4BitHadamardLatch(register2[0:4]) + self.myQuantum4BitHadamardLatch(register2[4:8])

            self.clearop()
            self.delay = 1
            #No flags effected
            return register1

    def conditionalSetPC(self,addr,condition):
        if self.QuantumExecute != "LOAD1" and self.QuantumExecute != "LOAD2" and self.QuantumExecute != "LOAD3":

            if condition == "1": return addr
            else: return False
        if self.QuantumExecute == "LOAD1":
            self.debugline = "Quantum method 1"
            if self.myif(condition) == 1: return self.fourbitset(addr[0] + addr[1] + addr[2] + addr[3]) + self.fourbitset(addr[4] + addr[5] + addr[6] + addr[7]) + self.fourbitset(addr[8] + addr[9] + addr[10] + addr[11]) + self.fourbitset(addr[12] + addr[13] + addr[14] + addr[15])
            else: return False
        if self.QuantumExecute == "LOAD2":
            self.debugline = "Quantum method 2"
            if self.myif(condition) == 1: return self.myQuantum4BitLatch(addr[0] + addr[1] + addr[2] + addr[3]) + self.myQuantum4BitLatch(addr[4] + addr[5] + addr[6] + addr[7]) + self.myQuantum4BitLatch(addr[8] + addr[9] + addr[10] + addr[11]) + self.myQuantum4BitLatch(addr[12] + addr[13] + addr[14] + addr[15])
            else: return False
        if self.QuantumExecute == "LOAD3":
            self.debugline = "Quantum method 3"
            if self.myif(condition) == 1: return self.myQuantum8BitHadamardLatch(addr[0],addr[1],addr[2],addr[3],addr[4],addr[5],addr[6],addr[7]) + self.myQuantum8BitHadamardLatch(addr[8],addr[9],addr[10],addr[11],addr[12],addr[13],addr[14],addr[15])
            else: return False 
			
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
        
        if self.QuantumExecute != "ADD1" and self.QuantumExecute != "ADD2" and self.QuantumExecute != "ADD3":

            total = A + (B + addition)
            if total > 255:
                total = total - 256
                C = "1"
   
        if self.QuantumExecute == "ADD1":
            self.debugline = "Quantum method 1"
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
            

            C = carry
        if self.QuantumExecute == "ADD2":
            self.debugline = "Quantum method 2"
            inputA = self.A
            inputB = register
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            
            carry = str(addition)            
            lsbAndCarry = self.myQuantum4BitAdder(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitAdder(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            

            total = int(msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
            C = msbAndCarry[0]            

        if self.QuantumExecute == "ADD3":
            self.debugline = "Quantum method 3"
            inputA = int(self.A,2)
            inputB = int(register,2)
            
            mA = inputA % 128
            fA = inputA // 128	

            mB = inputB % 128
            fB = inputB // 128	

            total = addition
        
            x = 0
            while (x < 2):
                a = 0
                b = 0
                
                
                if x < fA: a = 128
                if x == fA: a = mA
                if x > fA: a = 0
            

                if x < fB: b = 128
                if x == fB: b = mB
                if x > fB: b = 0
                

                total = total + self.myQuantumRyAdd(a,b)
     
                x = x + 1
       
            
            if total > 255:
                total = total - 256
                C = "1"
            
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

    def eightBitAddNoFlagsNotSigned(self,number1,number2):
        if self.QuantumExecute != "ADD1" and self.QuantumExecute != "ADD2":

            output = number1 + number2
            if output < 0: output = output + 256
            if output > 255: output = output - 256
            return output
        if self.QuantumExecute == "ADD1":
            self.debugline = "Quantum method 1"
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
        if self.QuantumExecute == "ADD2":
            self.debugline = "Quantum method 2"
            
            inputA = format(number1, '016b')
            inputB = format(number2, '016b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            
            carry = "0"            
            lsbAndCarry = self.myQuantum4BitAdder(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitAdder(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            

            total = int(msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
            
            return total            
     
    def sixteenBitAddNoFlags(self,number1,number2):

        if self.QuantumExecute != "ADD1" and self.QuantumExecute != "ADD2":

            self.debugline = "normal operation"
            output = number1 + number2
            if output < 0: output = output + 65536
            if output > 65535: output = output - 65536
            return output
        if self.QuantumExecute == "ADD1":
            self.debugline = "Quantum method 1"

            if number1 < 0: number1 = number1 + 65536 #fix for the potential of adding a signed number to a non signed 16 bit number
            if number2 < 0: number2 = number2 + 65536

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
            
        if self.QuantumExecute == "ADD2":
            self.debugline = "Quantum method 2"
            
            inputA = format(number1, '016b')
            inputB = format(number2, '016b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            
            carry = "0"            
            lsbAndCarry = self.myQuantum4BitAdder(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            
            carry1 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitAdder(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry1)            

            carry2 = str(msbAndCarry[0])
            mmsbAndCarry = self.myQuantum4BitAdder(inputA[11],inputA[10],inputA[9],inputA[8],inputB[11],inputB[10],inputB[9],inputB[8],carry2)            

            carry3 = str(mmsbAndCarry[0])
            mmmsbAndCarry = self.myQuantum4BitAdder(inputA[15],inputA[14],inputA[13],inputA[12],inputB[15],inputB[14],inputB[13],inputB[12],carry3)            

            total = int(mmmsbAndCarry[1] + mmmsbAndCarry[2] + mmmsbAndCarry[3] + mmmsbAndCarry[4] + mmsbAndCarry[1] + mmsbAndCarry[2] + mmsbAndCarry[3] + mmsbAndCarry[4] + msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
            
            return total            
            
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

        if self.QuantumExecute != "SUB1" and self.QuantumExecute != "SUB2":
            sub = (A - B) - minus

            C = "0"
            if sub < 0:
                sub = sub  + 256
                C = "1"
            sub = format(sub, '08b')
        
        if self.QuantumExecute == "SUB1":
            self.debugline = "Quantum method 1"
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
            sub = format(sub, '08b')
            
        if self.QuantumExecute == "SUB2":
            self.debugline = "Quantum method 2"

            inputA = self.A
            inputB = register
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            
            carry = str(minus)            
            lsbAndCarry = self.myQuantum4BitSubtractor(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitSubtractor(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            

            sub = int(msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
            C = msbAndCarry[0]    
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

    def eightBitSubNoFlags(self,number1,number2):
        if self.QuantumExecute != "SUB1" and self.QuantumExecute != "SUB2":

            output = number1 - number2
            return output
        if self.QuantumExecute == "SUB1":
            self.debugline = "Quantum method 1"
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
               
            return sub
        if self.QuantumExecute == "SUB2":
            self.debugline = "Quantum method 2"
            inputA = format(number1,'08b')
            inputB = format(number2,'08b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            
            carry = "1"        
            lsbAndCarry = self.myQuantum4BitSubtractor(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitSubtractor(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            

            output7 = msbAndCarry[1]
            output6 = msbAndCarry[2]
            output5 = msbAndCarry[3]
            output4 = msbAndCarry[4]
            output3 = lsbAndCarry[1]
            output2 = lsbAndCarry[2]
            output1 = lsbAndCarry[3]
            output0 = lsbAndCarry[4]
            
            
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
               
            return sub        

    def eightBitSubNoFlagsNotSigned(self,number1,number2):
        if self.QuantumExecute != "SUB1" and self.QuantumExecute != "SUB2":

            output = number1 - number2
            if output < 0: output = output + 256
            if output > 255: output = output - 256
            return output
        if self.QuantumExecute == "SUB1":
            self.debugline = "Quantum method 1"

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
           
            return sub

        if self.QuantumExecute == "SUB2":
            self.debugline = "Quantum method 2"            

            inputA = format(number1,'08b')
            inputB = format(number2,'08b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]
    
            carry = "0"        
            lsbAndCarry = self.myQuantum4BitSubtractor(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitSubtractor(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            

            sub = int(msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
                        
            return sub

    def eightBitSubNoFlagsUnsigned(self,number1,number2):
        if self.QuantumExecute != "SUB1" and self.QuantumExecute != "SUB2":

            output = number1 - number2
            self.debugline = "number 1 " + str(number1) + " - number2 " + str(number2) + " = " + str(output)
            return output
        if self.QuantumExecute == "SUB1":
            self.debugline = "Quantum method 1"
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
           
            return sub
        if self.QuantumExecute == "SUB2":
            self.debugline = "Quantum method 2"  

            inputA = format(number1,'08b')
            inputB = format(number2,'08b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]
    
            carry = "0"        
            lsbAndCarry = self.myQuantum4BitSubtractor(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitSubtractor(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            

            sub = int(msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
                        
            return sub

    def xxbitxx(self,register):
        if self.QuantumExecute != "SetResBit1" and self.QuantumExecute != "SetResBit2":

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
        if self.QuantumExecute == "SetResBit1":
            self.debugline = "Quantum method 1"

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

                if self.opx == 8:  register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + str(self.setbit(0))
                if self.opx == 9:  register = register[0] + register[1] + register[2] + register[3] + register[4] + str(self.setbit(0)) + register[6] + register[7]
                if self.opx == 10: register = register[0] + register[1] + register[2] + str(self.setbit(0)) + register[4] + register[5] + register[6] + register[7]
                if self.opx == 11: register = register[0] + str(self.setbit(0)) + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 12: register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + str(self.setbit(1))
                if self.opx == 13: register = register[0] + register[1] + register[2] + register[3] + register[4] + str(self.setbit(1)) + register[6] + register[7]
                if self.opx == 14: register = register[0] + register[1] + register[2] + str(self.setbit(1)) + register[4] + register[5] + register[6] + register[7]
                if self.opx == 15: register = register[0] + str(self.setbit(1)) + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]

                if self.opx == 3:
                    temp = register
                    #register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + "1"
                    register = self.fourbitset(register[1] + register[2] + register[3] + register[4]) + self.fourbitset(register[5] + register[6] + register[7] + "1")
                    X = int(temp,2)
                    Y = int(register,2)
                    C = "0"
                    if X >= Y: C = "1"
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 2:
                    C = register[0]
                    #register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + "0"
                    register = self.fourbitset(register[1] + register[2] + register[3] + register[4]) + self.fourbitset(register[5] + register[6] + register[7] + "0")
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 1:
                    temp = register
                    C = register[0]
                    #register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + self.F[7]
                    register = self.fourbitset(register[1] + register[2] + register[3] + register[4]) + self.fourbitset(register[5] + register[6] + register[7] + self.F[7])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 0:
                    temp = register
                    C = register[0]
                    #register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + register[0]
                    register = self.fourbitset(register[1] + register[2] + register[3] + register[4]) + self.fourbitset(register[5] + register[6] + register[7] + register[0])
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

                if self.opx == 8:  register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + str(self.setbit(0)) + register[7]
                if self.opx == 9:  register = register[0] + register[1] + register[2] + register[3] + str(self.setbit(0)) + register[5] + register[6] + register[7]
                if self.opx == 10: register = register[0] + register[1] + str(self.setbit(0)) + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 11: register = str(self.setbit(0)) + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 12: register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + str(self.setbit(1)) + register[7]
                if self.opx == 13: register = register[0] + register[1] + register[2] + register[3] + str(self.setbit(1)) + register[5] + register[6] + register[7]
                if self.opx == 14: register = register[0] + register[1] + str(self.setbit(1)) + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 15: register = str(self.setbit(1)) + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]

                if self.opx == 3:
                    C = register[7]
                    #register = "0" + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6]
                    register = self.fourbitset("0" + register[0] + register[1] + register[2]) + self.fourbitset(register[3] + register[4] + register[5] + register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 2:
                    C = register[7]
                    #register = register[0] + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6]
                    register = self.fourbitset(register[0] + register[0] + register[1] + register[2]) + self.fourbitset(register[3] + register[4] + register[5] + register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 1:
                    temp = register
                    C = register[7]
                    #register = self.F[7] + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6]
                    register = self.fourbitset(self.F[7] + register[0] + register[1] + register[2]) + self.fourbitset(register[3] + register[4] + register[5] + register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 0:
                    temp = register
                    C = register[7]
                    #register = register[7] + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6]
                    register = self.fourbitset(register[7] + register[0] + register[1] + register[2]) + self.fourbitset(register[3] + register[4] + register[5] + register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

            return register
            
        if self.QuantumExecute == "SetResBit2":
            self.debugline = "Quantum method 2"

            #opx = going down table
            #opy = going accross

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

                if self.opx == 8:  register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + str(self.myQuantum1BitLatch(0))
                if self.opx == 9:  register = register[0] + register[1] + register[2] + register[3] + register[4] + str(self.myQuantum1BitLatch(0)) + register[6] + register[7]
                if self.opx == 10: register = register[0] + register[1] + register[2] + str(self.myQuantum1BitLatch(0)) + register[4] + register[5] + register[6] + register[7]
                if self.opx == 11: register = register[0] + str(self.myQuantum1BitLatch(0)) + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 12: register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + str(self.myQuantum1BitLatch(1))
                if self.opx == 13: register = register[0] + register[1] + register[2] + register[3] + register[4] + str(self.myQuantum1BitLatch(1)) + register[6] + register[7]
                if self.opx == 14: register = register[0] + register[1] + register[2] + str(self.myQuantum1BitLatch(1)) + register[4] + register[5] + register[6] + register[7]
                if self.opx == 15: register = register[0] + str(self.myQuantum1BitLatch(1)) + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]

                if self.opx == 3:
                    temp = register
                    #register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + "1"
                    register = self.myQuantum4BitLatch(register[1] + register[2] + register[3] + register[4]) + self.myQuantum4BitLatch(register[5] + register[6] + register[7] + "1")
                    X = int(temp,2)
                    Y = int(register,2)
                    C = "0"
                    if X >= Y: C = "1"
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 2:
                    C = register[0]
                    #register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + "0"
                    register = self.myQuantum4BitLatch(register[1] + register[2] + register[3] + register[4]) + self.myQuantum4BitLatch(register[5] + register[6] + register[7] + "0")
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 1:
                    temp = register
                    C = register[0]
                    #register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + self.F[7]
                    register = self.myQuantum4BitLatch(register[1] + register[2] + register[3] + register[4]) + self.myQuantum4BitLatch(register[5] + register[6] + register[7] + self.F[7])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 0:
                    temp = register
                    C = register[0]
                    #register = register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7] + register[0]
                    register = self.myQuantum4BitLatch(register[1] + register[2] + register[3] + register[4]) + self.myQuantum4BitLatch(register[5] + register[6] + register[7] + register[0])
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

                if self.opx == 8:  register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + str(self.myQuantum1BitLatch(0)) + register[7]
                if self.opx == 9:  register = register[0] + register[1] + register[2] + register[3] + str(self.myQuantum1BitLatch(0)) + register[5] + register[6] + register[7]
                if self.opx == 10: register = register[0] + register[1] + str(self.myQuantum1BitLatch(0)) + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 11: register = str(self.myQuantum1BitLatch(0)) + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 12: register = register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + str(self.myQuantum1BitLatch(1)) + register[7]
                if self.opx == 13: register = register[0] + register[1] + register[2] + register[3] + str(self.myQuantum1BitLatch(1)) + register[5] + register[6] + register[7]
                if self.opx == 14: register = register[0] + register[1] + str(self.myQuantum1BitLatch(1)) + register[3] + register[4] + register[5] + register[6] + register[7]
                if self.opx == 15: register = str(self.myQuantum1BitLatch(1)) + register[1] + register[2] + register[3] + register[4] + register[5] + register[6] + register[7]

                if self.opx == 3:
                    C = register[7]
                    #register = "0" + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6]
                    register = self.myQuantum4BitLatch("0" + register[0] + register[1] + register[2]) + self.myQuantum4BitLatch(register[3] + register[4] + register[5] + register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 2:
                    C = register[7]
                    #register = register[0] + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6]
                    register = self.myQuantum4BitLatch(register[0] + register[0] + register[1] + register[2]) + self.myQuantum4BitLatch(register[3] + register[4] + register[5] + register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 1:
                    temp = register
                    C = register[7]
                    #register = self.F[7] + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6]
                    register = self.myQuantum4BitLatch(self.F[7] + register[0] + register[1] + register[2]) + self.myQuantum4BitLatch(register[3] + register[4] + register[5] + register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

                if self.opx == 0:
                    temp = register
                    C = register[7]
                    #register = register[7] + register[0] + register[1] + register[2] + register[3] + register[4] + register[5] + register[6]
                    register = self.myQuantum4BitLatch(register[7] + register[0] + register[1] + register[2]) + self.myQuantum4BitLatch(register[3] + register[4] + register[5] + register[6])
                    self.F = register[0] + self.getZflag(register) + register[2] + "0" + register[4] + self.getparity(register)   + "0" + C

            return register

    def hladd(self,register):
        hl12 = int((self.H + self.L)[-12:],2)
        add12 = int(register[-12:],2)

        if self.preopcode == "": A = int(self.H  + self.L,2)
        if self.preopcode == "11011101": A = int(self.IX,2)
        if self.preopcode == "11111101": A = int(self.IY,2)

        B = int(register,2)

        C = "0"
        P = "0"
 
        if self.QuantumExecute != "ADD1" and self.QuantumExecute != "ADD2":

            total = A + B

            if total > 65535:
                total = total - 65536
                C = "1"
        if self.QuantumExecute == "ADD1":
            self.debugline = "Quantum method 1"
    
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
            
        if self.QuantumExecute == "ADD2":
            self.debugline = "Quantum method 2"
            inputA = format(A, '016b')
            inputB = format(B, '016b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            
            carry = str(0)            
            lsbAndCarry = self.myQuantum4BitAdder(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitAdder(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            
            
            carry3 = str(msbAndCarry[0])
            mmsbAndCarry = self.myQuantum4BitAdder(inputA[11],inputA[10],inputA[9],inputA[8],inputB[11],inputB[10],inputB[9],inputB[8],carry3)        
            
            carry4 = str(mmsbAndCarry[0])
            mmmsbAndCarry = self.myQuantum4BitAdder(inputA[15],inputA[14],inputA[13],inputA[12],inputB[15],inputB[14],inputB[13],inputB[12],carry4)        
            
            
            
            total = int(mmmsbAndCarry[1] + mmmsbAndCarry[2] + mmmsbAndCarry[3] + mmmsbAndCarry[4] + mmsbAndCarry[1] + mmsbAndCarry[2] + mmsbAndCarry[3] + mmsbAndCarry[4] + msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
            C = mmmsbAndCarry[0]            

            
            

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

    def hladc(self,register):
        hl12 = int((self.H + self.L)[-12:],2)
        add12 = int(register[-12:],2) + int(self.F[7])

        A = int(self.H + self.L,2)
        B = int(register,2)
        C = "0"

        if self.QuantumExecute != "ADD1" and self.QuantumExecute != "ADD2":

            total = A + B + int(self.F[7])
     
            if total > 65535:
                total = total - 65536
                C = "1"

        if self.QuantumExecute == "ADD1":
            self.debugline = "Quantum method 1"

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


        if self.QuantumExecute == "ADD2":
            self.debugline = "Quantum method 2"
            inputA = format(A, '016b')
            inputB = format(B, '016b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            
            carry = self.F[7]             
            lsbAndCarry = self.myQuantum4BitAdder(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitAdder(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            
            
            carry3 = str(msbAndCarry[0])
            mmsbAndCarry = self.myQuantum4BitAdder(inputA[11],inputA[10],inputA[9],inputA[8],inputB[11],inputB[10],inputB[9],inputB[8],carry3)        
            
            carry4 = str(mmsbAndCarry[0])
            mmmsbAndCarry = self.myQuantum4BitAdder(inputA[15],inputA[14],inputA[13],inputA[12],inputB[15],inputB[14],inputB[13],inputB[12],carry4)            
            
            total = int(mmmsbAndCarry[1] + mmmsbAndCarry[2] + mmmsbAndCarry[3] + mmmsbAndCarry[4] + mmsbAndCarry[1] + mmsbAndCarry[2] + mmsbAndCarry[3] + mmsbAndCarry[4] + msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
            C = mmmsbAndCarry[0]    


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
        C = "0"
        Z = "0"

        if self.QuantumExecute != "SUB1" and self.QuantumExecute != "SUB2":

            total = A - B - int(self.F[7])
            
            if total < 0:
                total = total + 65536
                C = "1"
        if self.QuantumExecute == "SUB1":
            self.debugline = "Quantum method 1"
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
        if self.QuantumExecute == "SUB2":
            self.debugline = "Quantum method 2"
  
            inputA = self.H + self.L
            inputB = register
            inputA = inputA[::-1]
            inputB = inputB[::-1]

                
            carry = self.F[7]            
            lsbAndCarry = self.myQuantum4BitSubtractor(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitSubtractor(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            
            
            carry3 = str(msbAndCarry[0])
            mmsbAndCarry = self.myQuantum4BitSubtractor(inputA[11],inputA[10],inputA[9],inputA[8],inputB[11],inputB[10],inputB[9],inputB[8],carry3)        
            
            carry4 = str(mmsbAndCarry[0])
            mmmsbAndCarry = self.myQuantum4BitSubtractor(inputA[15],inputA[14],inputA[13],inputA[12],inputB[15],inputB[14],inputB[13],inputB[12],carry4)        
            
            
            sub = int(mmmsbAndCarry[1] + mmmsbAndCarry[2] + mmmsbAndCarry[3] + mmmsbAndCarry[4] + mmsbAndCarry[1] + mmsbAndCarry[2] + mmsbAndCarry[3] + mmsbAndCarry[4] + msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
            C = msbAndCarry[0]    
            
            
            
                
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
 
    def neg(self,register):
        if self.QuantumExecute != "NEG1" and self.QuantumExecute != "NEG2":

            return 0 - register
        if self.QuantumExecute == "NEG1":
            self.debugline = "Quantum method 1"
            
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
        if self.QuantumExecute == "NEG2":
            self.debugline = "Quantum method 2"
            
            inputA = "00000000"
            inputB = format(register,'08b')
            inputA = inputA[::-1]
            inputB = inputB[::-1]

            
            carry = str(0)            
            lsbAndCarry = self.myQuantum4BitSubtractor(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitSubtractor(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            

            sub = int(msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
            
            return int(sub)
    
    def rotate(self,bit0,bit1,bit2,bit3,bit4,bit5,bit6,bit7):
        if self.QuantumExecute != "ROT1" and self.QuantumExecute != "ROT2" and self.QuantumExecute != "ROT3":

            return bit0 + bit1 + bit2 + bit3 + bit4 + bit5 + bit6 + bit7
            
        if self.QuantumExecute == "ROT1":
            self.debugline = "Quantum method 1"
            return  self.fourbitset(bit0 + bit1 + bit2 + bit3) + self.fourbitset(bit4 + bit5 + bit6 + bit7)
            
        if self.QuantumExecute == "ROT2":
            self.debugline = "Quantum method 2"
            return self.myQuantum4BitLatch(bit0 + bit1 + bit2 + bit3) + self.myQuantum4BitLatch(bit4 + bit5 + bit6 + bit7)

        if self.QuantumExecute == "ROT3":
            self.debugline = "Quantum method 3"
            temp =  self.myQuantumSwap(bit0, bit1, bit2, bit3, bit4, bit5, bit6, bit7,0,0,0,0,0,0,0,0)
            
            return temp[8] + temp[9] + temp[10] + temp[11] + temp[12] + temp[13] + temp[14] + temp[15]
    
    def scf(self):
        if self.QuantumExecute != "SCF1" and self.QuantumExecute != "SCF2":

            self.F = self.F[0] + self.F[1] + self.F[2] + "0" + self.F[4] + self.F[5] + "0" + "1"   
            
        if self.QuantumExecute == "SCF1":
            self.debugline = "Quantum method 1"
            self.F = self.F[0] + self.F[1] + self.F[2] + "0" + self.F[4] + self.F[5] + "0" + str(self.setbit(1))    
            
        if self.QuantumExecute == "SCF2":
            self.debugline = "Quantum method 2"
            self.F = self.F[0] + self.F[1] + self.F[2] + "0" + self.F[4] + self.F[5] + "0" + str(self.myQuantum1BitLatch(1))

    def singleload(self,bit0,bit1,bit2,bit3,bit4,bit5,bit6,bit7):
        if self.QuantumExecute != "LOAD1" and self.QuantumExecute != "LOAD2" and self.QuantumExecute != "LOAD3" and self.QuantumExecute != "LOAD4":

            return bit0 + bit1 + bit2 + bit3 + bit4 + bit5 + bit6 + bit7
            
        if self.QuantumExecute == "LOAD1":
            self.debugline = "Quantum method 1"
            return  self.fourbitset(bit0 + bit1 + bit2 + bit3) + self.fourbitset(bit4 + bit5 + bit6 + bit7)
            
        if self.QuantumExecute == "LOAD2":
            self.debugline = "Quantum method 2"
            return self.myQuantum4BitLatch(bit0 + bit1 + bit2 + bit3) + self.myQuantum4BitLatch(bit4 + bit5 + bit6 + bit7)            

        if self.QuantumExecute == "LOAD3":
            self.debugline = "Quantum method 3"
            return self.myQuantum8BitHadamardLatch(bit0, bit1, bit2, bit3, bit4, bit5, bit6, bit7)            
        
        if self.QuantumExecute == "LOAD4":
            self.debugline = "Quantum method 4"
            temp = self.myQuantumSwap(bit0, bit1, bit2, bit3, bit4, bit5, bit6, bit7,0,0,0,0,0,0,0,0)   
            
            return temp[8] + temp[9] + temp[10] + temp[11] + temp[12] + temp[13] + temp[14] + temp[15]

    def loadhlr(self,data,original):
        if self.QuantumExecute != "LOAD1" and self.QuantumExecute != "LOAD2" and self.QuantumExecute != "LOAD3":

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
        if self.QuantumExecute == "LOAD1":
            self.debugline = "Quantum method 1"
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
        if self.QuantumExecute == "LOAD2":
            self.debugline = "Quantum method 2"
            
            if self.preopcode == "":
                if self.stage == "1":
                    stage = ""
                    self.delay = 1
                    self.needmorebits = False
                    self.execute = True
                    #register = data
                    register = self.myQuantum4BitLatch(data[0] + data[1] + data[2] + data[3]) + self.myQuantum4BitLatch(data[4] + data[5] + data[6] + data[7])

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
                    register = self.myQuantum4BitLatch(data[0] + data[1] + data[2] + data[3]) + self.myQuantum4BitLatch(data[4] + data[5] + data[6] + data[7])
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
					
        if self.QuantumExecute == "LOAD3":
            self.debugline = "Quantum method 3"
            
            if self.preopcode == "":
                if self.stage == "1":
                    stage = ""
                    self.delay = 1
                    self.needmorebits = False
                    self.execute = True
                    #register = data
                    register = self.myQuantum4BitHadamardLatch(data[0] + data[1] + data[2] + data[3]) + self.myQuantum4BitHadamardLatch(data[4] + data[5] + data[6] + data[7])

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
                    register = self.myQuantum4BitHadamardLatch(data[0] + data[1] + data[2] + data[3]) + self.myQuantum4BitHadamardLatch(data[4] + data[5] + data[6] + data[7])
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

    def eightbitcp(self,register):
        if self.QuantumExecute != "CP1" and self.QuantumExecute != "CP2" and self.QuantumExecute != "CP3":

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
        if self.QuantumExecute == "CP1":
            self.debugline = "Quantum method 1"
            A = int(self.A,2)
            N = int(register,2)

            #***** Z *****
            Z = "0"

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
 
            result = int(output7 + output6 + output5 + output4 + output3 + output2 + output1 + output0,2)

            C = borrow
            result = format(result,'08b')
            if result == "00000000": Z = "1"

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
        if self.QuantumExecute == "CP2":
            self.debugline = "Quantum method 2"
            A = int(self.A,2)
            N = int(register,2)

            #***** Z *****
            Z = "0"
            


            inputA = self.A
            inputB = register
            inputA = inputA[::-1]
            inputB = inputB[::-1]

            carry = str(0)            
            lsbAndCarry = self.myQuantum4BitSubtractor(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitSubtractor(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            

            result = int(msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
            
            C = str(msbAndCarry[0])
            result = format(result,'08b')
            if result == "00000000": Z = "1"

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
        if self.QuantumExecute == "CP3":
            self.debugline = "Quantum method 3"
            A = int(self.A,2)
            N = int(register,2)



            inputA = self.A
            inputB = register
            inputA = inputA[::-1]
            inputB = inputB[::-1]
            
            #XOR based compare
            #***** Z *****
            Z = self.myQuantumCP(inputA[7],inputA[6],inputA[5],inputA[4],inputA[3],inputA[2],inputA[1],inputA[0],inputB[7],inputB[6],inputB[5],inputB[4],inputB[3],inputB[2],inputB[1],inputB[0])

            carry = str(0)            
            lsbAndCarry = self.myQuantum4BitSubtractor(inputA[3],inputA[2],inputA[1],inputA[0],inputB[3],inputB[2],inputB[1],inputB[0],carry)        
            carry2 = str(lsbAndCarry[0])
            msbAndCarry = self.myQuantum4BitSubtractor(inputA[7],inputA[6],inputA[5],inputA[4],inputB[7],inputB[6],inputB[5],inputB[4],carry2)            

            result = int(msbAndCarry[1] + msbAndCarry[2] + msbAndCarry[3] + msbAndCarry[4] + lsbAndCarry[1] + lsbAndCarry[2] + lsbAndCarry[3] + lsbAndCarry[4],2)
            
            C = str(msbAndCarry[0])
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

    def setBoolValue(self,value):
        if self.QuantumExecute != "LOAD1" and self.QuantumExecute != "LOAD2" and self.QuantumExecute != "LOAD3":

            return value
        if self.QuantumExecute == "LOAD1":
            self.debugline = "Quantum method 1"
            return bool(self.setbit(int(value)))
        if self.QuantumExecute == "LOAD2":
            self.debugline = "Quantum method 2"
            return bool(int(self.myQuantum1BitLatch(value)))
        if self.QuantumExecute == "LOAD3":
            self.debugline = "Quantum method 3"
            return bool(int(self.myQuantum1BitHadamardLatch(value)))   
            
    def setPC(self,addr):
        if self.QuantumExecute != "SetPC1" and self.QuantumExecute != "SetPC2":

            return addr
        if self.QuantumExecute == "SetPC1":
            self.debugline = "Quantum method 1"
            return  self.fourbitset(addr[0] + addr[1] + addr[2] + addr[3]) + self.fourbitset(addr[4] + addr[5] + addr[6] + addr[7]) + self.fourbitset(addr[8] + addr[9] + addr[10] + addr[11]) + self.fourbitset(addr[12] + addr[13] + addr[14] + addr[15])
        if self.QuantumExecute == "SetPC2":
            self.debugline = "Quantum method 2"  
            return  self.myQuantum4BitLatch(addr[0] + addr[1] + addr[2] + addr[3]) + self.myQuantum4BitLatch(addr[4] + addr[5] + addr[6] + addr[7]) + self.myQuantum4BitLatch(addr[8] + addr[9] + addr[10] + addr[11]) + self.myQuantum4BitLatch(addr[12] + addr[13] + addr[14] + addr[15])
    
    def regtodatabus(self,register):
        if self.QuantumExecute != "DataBus1" and self.QuantumExecute != "DataBus2":
 
            self.d7 = bool(int(register[0]))
            self.d6 = bool(int(register[1]))
            self.d5 = bool(int(register[2]))
            self.d4 = bool(int(register[3]))
            self.d3 = bool(int(register[4]))
            self.d2 = bool(int(register[5]))
            self.d1 = bool(int(register[6]))
            self.d0 = bool(int(register[7]))
        if self.QuantumExecute == "DataBus1":
            self.debugline = "Quantum method 1"

            output = self.fourbitset(register[0] + register[1] + register[2] + register[3]) + self.fourbitset(register[4] + register[5] + register[6] + register[7])

            self.d7 = bool(int(output[0]))
            self.d6 = bool(int(output[1]))
            self.d5 = bool(int(output[2]))
            self.d4 = bool(int(output[3]))
            self.d3 = bool(int(output[4]))
            self.d2 = bool(int(output[5]))
            self.d1 = bool(int(output[6]))
            self.d0 = bool(int(output[7]))
        if self.QuantumExecute == "DataBus2":
            self.debugline = "Quantum method 2"             
			
            output = self.myQuantum4BitLatch(register[0] + register[1] + register[2] + register[3]) + self.myQuantum4BitLatch(register[4] + register[5] + register[6] + register[7])

            self.d7 = bool(int(output[0]))
            self.d6 = bool(int(output[1]))
            self.d5 = bool(int(output[2]))
            self.d4 = bool(int(output[3]))
            self.d3 = bool(int(output[4]))
            self.d2 = bool(int(output[5]))
            self.d1 = bool(int(output[6]))
            self.d0 = bool(int(output[7]))

    def regtoaddrbus(self,register):
        if self.QuantumExecute != "AddrBus1" and self.QuantumExecute != "AddrBus2":


 
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
        if self.QuantumExecute == "AddrBus1":
            self.debugline = "Quantum method 1"

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
			
        if self.QuantumExecute == "AddrBus2":
            self.debugline = "Quantum method 2"   
            output = self.myQuantum4BitLatch(register[0] + register[1] + register[2] + register[3]) + self.myQuantum4BitLatch(register[4] + register[5] + register[6] + register[7]) + self.myQuantum4BitLatch(register[8] + register[9] + register[10] + register[11]) + self.myQuantum4BitLatch(register[12] + register[13] + register[14] + register[15])

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
			
#****************************************************************************************************************************************************************************
#****************************************************************************************************************************************************************************
#************************************************************* CPU Instructions with 1 Quantum Method ***********************************************************************
#****************************************************************************************************************************************************************************
#****************************************************************************************************************************************************************************
  
    def checkFlag(self,condition):
        if self.QuantumExecute != "JUMP":
            self.debugline = "Normal operation"
            if condition == "1": return "1"
            else: return "0"
        else:
            self.debugline = "Quantum operation"
            return str(self.myif(int(condition)))    

#****************************************************************************************************************************************************************************
#****************************************************************************************************************************************************************************
#*************************************************************************** Helper methods *********************************************************************************
#****************************************************************************************************************************************************************************
#****************************************************************************************************************************************************************************

    def setbit(self,bit):
        inputA = bit * math.pi

        circuit = QuantumCircuit(1,1)
        circuit.ry(inputA,0)
        circuit.measure_all()
   
        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
        memory = result.get_memory(circuit)

            
        print(circuit)
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

        circuit = QuantumCircuit(4,4)
        circuit.ry(inputA,0)
        circuit.ry(inputB,1)
        circuit.ry(inputC,2)
        circuit.ry(inputD,3)
        circuit.measure_all()
  
        shots = self.shots
        QuantumComputer = self.QuantumComputer
        circuit = transpile(circuit, QuantumComputer)
        result = QuantumComputer.run(circuit, shots=shots, memory=True).result()
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

    def numberToRyRotation(self,x):
        output = x * (math.pi /15)
        return round(output,2)

    def probabilityToNumber(self,x):

        output = math.acos((x-50)/100 * 2)
        output = round((output/math.pi) * 15,0)
        return output