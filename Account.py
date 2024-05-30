from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(channel="ibm_quantum", token="XXXXXXXXXX", overwrite= True)
 
service = QiskitRuntimeService() 