import json
from model.producers import WorkflowConfig
from model.producers import Producer
from model.producers import Workflow
from workFlowGenerator import WorkflowGenerator

class ConfigGenerator:

    def __init__(self):
        self.wfg=WorkflowGenerator()

    def printToConfigFile(self,configuration):
        fileName = "./json-data-generator-1.2.2-SNAPSHOT/conf/cpuUsageConfig_{}.json".format(self.clusterName)
        f = open(fileName, 'w')
        f.write(configuration + "\n")
        f.close()

    def generateWorkflows(self,clusterDetails):
        self.clusterName=clusterDetails['clusterName']
        firstNode=clusterDetails['firstNode']
        lastNode=clusterDetails['lastNode']
        workflows=[]
        for nodeNumber in range(firstNode, lastNode + 1):
            self.wfg.generate([self.clusterName, nodeNumber])
            workflowFilename = "cpuUsageWorkflow_{}_{}.json".format(self.clusterName,nodeNumber)
            workflowName = "cpuUsage" + str(nodeNumber)
            workflows.append(Workflow(workflowFilename, 1, workflowName))
        return workflows

    def generateConfig(self):
        clusterConfigFile=open("clusterConfig.json",'r')
        config = json.load(clusterConfigFile)
        producers = [ Producer(config['broker'], config['topic']) ]
        workflows = self.generateWorkflows(config['cluster'])
        workflowConfig = WorkflowConfig(producers,workflows)
        self.printToConfigFile(workflowConfig.toJSON())

if __name__=="__main__":
    ConfigGenerator().generateConfig()
