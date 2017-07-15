from random import randint
import yaml
import json
from workflowGenerator import WorkflowGenerator

class ConfigGenerator:

    def __init__(self):
        self.wfg=WorkflowGenerator()

    def getProducer(self,brokerDetails,topic):
        kafkaProducer = {}
        kafkaProducer['type']='kafka'
        kafkaProducer['broker.server']=brokerDetails['server']
        kafkaProducer['broker.port']=brokerDetails['port']
        kafkaProducer['topic']=topic
        kafkaProducer['flatten']=False
        kafkaProducer['sync']=False
        return kafkaProducer

    def printToFile(self,s):
        fileName = "./json-data-generator-1.2.2-SNAPSHOT/conf/cpuUsageConfig_{}.json".format(self.clusterName)
        f = open(fileName, 'w')
        f.write(s + "\n")
        f.close()

    def generateWorkflows(self,clusterDetails):
        self.clusterName=clusterDetails['clusterName']
        firstNode=clusterDetails['firstNode']
        lastNode=clusterDetails['lastNode']
        workflows=[]
        for nodeNumber in range(firstNode, lastNode):
            timeInMins=randint(1,10)
            anomalyCount=timeInMins*randint(1,4)
            self.wfg.generate([self.clusterName, nodeNumber, timeInMins * 60, 10, anomalyCount])
            workflows.append(self.generateWorkflowDetails(nodeNumber))
        return workflows

    def generateWorkflowDetails(self,nodeNumber):
        workflow={}
        workflow['workflowName']="cpuUsage" + str(nodeNumber)
        workflow['workflowFilename']="cpuUsageWorkflow_{}_{}.json".format(self.clusterName,nodeNumber)
        workflow['instances']=1
        return workflow

    def generateConfig(self):
        jsonfile=open("clusterConfig.json",'r')
        cfg = json.load(jsonfile)

        jsonData={}
        jsonData['producers']=[self.getProducer(cfg['broker'], cfg['topic'])]
        jsonData['workflows']=self.generateWorkflows(cfg['cluster'])

        self.printToFile(json.dumps(jsonData,indent=1,sort_keys=False))

if __name__=="__main__":
    ConfigGenerator().generateConfig()
