from random import randint
from workflowGenerator import WorkflowGenerator

wfg = WorkflowGenerator()
clusterName=input("Enter cluster name: ")
nodeCount = int(input("Enter number of nodes required: "))

for nodeNumber in range(1, nodeCount+1):
    timeInMins=randint(1,10)
    anomalyCount=timeInMins*randint(1,3)
    wfg.generate([clusterName, nodeNumber, timeInMins * 60, 10, anomalyCount])
