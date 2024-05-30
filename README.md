# Qx86

Welcome to the Github repository for Qx86. 
Qx86 is an intel 8080/Z80 emulator which executes all salient points of intel 8080/Z80 execution on IBMs quantum computers.

## Background
One of the major obstacles to the adoption of quantum computing is the requirement to define quantum circuits at the quantum gate level. Many programmers are familiar with high-level or low-level programming languages but not quantum gates nor the low-level quantum logic required to derive useful results from quantum computers. The steep learning curve involved when progressing from quantum gates to complex simulations such as Shor’s algorithm has proven too much for many developers. This software addresses this challenge by providing a Software Development Kit (SDK), translation layer, emulator and a framework of techniques for executing Intel 8080/Z80 assembler on a quantum computer, i.e. all salient points of CPU execution, logic, arithmetic and bitwise manipulation will be executed on the quantum computer using quantum circuits. Developers and researchers can use the SDK to write code in Intel 8080/Z80 assembler which is executed locally via traditional emulation and remotely on a quantum computer in parallel. The emulator features side-by-side code execution with visibility of the running quantum circuit and re-usable/overridable methods. This enables programmers to learn, reuse and contrast techniques for performing any traditional CPU based technique/instruction on a quantum computer; e.g. a programmer may know how to multiply and perform checks on a classical CPU but is not able to perform the same tasks in a quantum implementation, this SDK allows the programmer to pick and choose the methods they would like to use to fulfil their requirements.



## Installation and use
Due to the nature of this work, you will need a basic understanding of development, assembler and quantum computers.
Note - The code included in this repository has been tested with Python version 3.7 to 3.12 on Windows 10.

1. Download and install the latest version of Python
```
https://www.python.org/downloads/windows/
```

2. Install the Microsoft Visual C++ run time 
```
https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170
```

3. Install IBMs Qiskit using the following commands
```
python -m pip install qiskit
python -m pip install qiskit-ibm-runtime
python -m pip install qiskit-aer
```

4. Install matplotlib and curses 
```
python -m pip install matplot-lib
python -m pip install pylatexenc
python -m pip install windows-curses
```

5. Sign up for IBMs quantum experience at
```
https://quantum-computing.ibm.com/
```

6. Copy your API token, which can be found in your IBM account settings on the IBM quantum page.

![image](https://user-images.githubusercontent.com/66572228/199702656-c9708def-971a-4ca1-a053-3e8de32f2ef7.png)


7. Download the following files from this repository
```
Account.py  - A script which connects you to your IBM account
cpu3.py     - The orchestration scripts
z80.py      - The intel 8080/Z80 emulator
q80.py      - The intel 8080/z80 emulator with its instructions overridden for execution on IBMs quantum computer
```

8. Edit the Account.py file, paste in your API token and execute it with
```
Python.exe Acccount.py
```

9. Run the emulator with 
```
Python.exe cpu3.py
```
Note – Make your command prompt window full screen as curses may error if it cannot fit the entire screen in your window.
This will run the traditional emulator and emulator for execution on a quantum computer in parallel. Note the emulators pseudo RAM contains an example program which loads the A register, increments A then halts.

![image](https://user-images.githubusercontent.com/66572228/199703390-af98205e-d405-4c52-92bf-154daf02605d.png)

To exit the emulator, press the Q key.<br>

10. The next step is to tell the emulator which instructions to execute on the quantum computer. This is done by editing the cpu3.py file and scrolling down until you get to the Example program section. This section contains a number of sample programs, in this example un-comment the line #qpu.QuantumExecute = "INC1" 

![image](https://user-images.githubusercontent.com/66572228/199703594-21d78f1e-a9b6-44c6-be81-bdf6e7841f28.png)

11. Execute the emulator again, but note when the program counter gets to the INC instruction (3C) execution pauses, this is the emulator joining the queue for execution on one of IBMs quantum computers. (or setting up a local quantum simulator) After roughly 30 seconds the results will be returned from IBMs quantum computer and we can see that the A register has incremented.

![image](https://user-images.githubusercontent.com/66572228/199703816-66f6fc91-3521-4a6a-b134-af0d646c28ba.png)

12. All the quantum circuits used to execute the instruction will be displayed when we exit the emulator.

![image](https://user-images.githubusercontent.com/66572228/199703991-298904eb-b147-4de0-9e4b-002be4ee2446.png)

13. You can also execute user supplied binaries on the command line with the following command
```
Python.exe cpu3.py myprogram.bin
```


## FAQ
- Why does it take so long to execute, I thought quantum computers were fast?<br>
The majority of the delay is due to the queuing mechanism we have to join for execution, but other delays include the latency of the API call and the fact that quantum computers are not designed to perform traditional logic operations.

- Why can’t I run the entire binary on the quantum computer?<br>
As you would have to join a queue for each instruction it would be extremely slow. You may edit the methods in q80.py to do this but each instruction will take circa 30 seconds to call and execute.

- Why do the example specify a INC2, DEC2 etc?<br>
I have included multiple methods for each instruction, method 1 (INC1) calls each gate separately whereas method 2 (INC2) implements a quantum circuit for the entire (where possible) instruction so is much faster.

- Why call it Qx86 when you only have intel 8080/Z80 compatibility?<br>
Artistic license! Also q80 is a television set and a qx80 is a car so those names were already taken. Intel x86 compatibility is planned but will require more qubits due to the larger internal registers.

- I get an error when I choose a real Quantum computer.<br>
You must choose a quantum computer that meets the minimum requirements, all instructions executed using method 1 require upto 5 qubits whereas all instructions using method 2 require upto 32 qubits.

- Why turn a $1,000,000 quantum computer into a 40 year old CPU?<br>
The motivation for this SDK is to provide a learning tool and re-useable reference framework, a framework that will help bridge the steep learning curve and enable developers to drive useful results from quantum computers. The framework will show developers that quantum computers can do anything a traditional computer can, just in a different manner. The SDK also prepares the groundwork (via the delivery of the emulators and translation layer) for a possible scenario where the overhead for performing classical computations on a quantum computer is not so large. This is not to say that the value of the SDK is purely theoretical, as even with today’s capability many quantum-based simulations require aspects of traditional logic which are included as re-usable methods within the framework. 
Emulating a CPU was chosen as a goal for this SDK as it provides a provable mechanism for delivering every logic/arithmetic/bitwise function needed in a traditional computer. It was not my aim to reduce a quantum computer to a device only capable of traditional logic-based calculations but describe, prove and demonstrate how to perform those calculations. The logic calculations can be used to form parts of many quantum-based calculations and are found in a framework which developers are familiar with and can readily re-use.


