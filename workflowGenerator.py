from random import sample
from random import randint
import json
from model.workflow import ConfigDetail
from model.workflow import Config
from model.workflow import Workflow

class WorkflowGenerator:

    def printToFile(self,s):
        fileName = "./json-data-generator-1.2.2-SNAPSHOT/conf/cpuUsageWorkflow_{}_{}.json".format(self.clusterName, self.nodeNumber)
        f = open(fileName, 'w')
        f.write(s + "\n")
        f.close()

    def getAnaomalusRangeForEvenTimeSeq(self, timeSeq):
        return (timeSeq * self.anomalyDuration, (timeSeq+1) * self.anomalyDuration)

    def getAnaomalusRangeForOddTimeSeq(self, timeSeq):
        return (timeSeq * self.anomalyDuration, (timeSeq+1) * self.anomalyDuration-1)

    def generateAnomalousTimeSeq(self):
        timeSeq = sample(range(int(self.totalWorkflowDuration/self.anomalyDuration)),self.anomalyCount)
        calculateRange = lambda x: self.getAnaomalusRangeForEvenTimeSeq(x) if x%2==0 else self.getAnaomalusRangeForOddTimeSeq(x)
        self.anomalyStartArray=list(map(calculateRange,timeSeq))
        self.anomalyStartArray.sort()
        print(self.anomalyStartArray)

    def generateSteps(self):
        steps=[]
        for i in range(self.totalWorkflowDuration):
            if i>=self.anomalyStartArray[self.listPos][0] and i < self.anomalyStartArray[self.listPos][1]:
                cpu = "double(81.0,100.0)"
                if i == (self.anomalyStartArray[self.listPos][1])-1:
                    self.listPos =(self.listPos + 1)%len(self.anomalyStartArray)
            else:
                cpu = "double(1.0,80.0)"
            config = Config(ConfigDetail(self.clusterName, "now()", cpu, self.nodeNumber ))
            steps.append(config)
        return steps


    def printStepsToFile(self):
        self.listPos=0
        workflow = Workflow(0, False, False, 1000, True, self.generateSteps())

        self.printToFile(workflow.toJSON())

    def generate(self,arg=[]):
        timeInMins=randint(1,10)
        self.anomalyCount=timeInMins*randint(1,4)
        self.totalWorkflowDuration = timeInMins * 60
        self.anomalyDuration = 10

        (self.clusterName, self.nodeNumber)=tuple(arg)

        self.generateAnomalousTimeSeq()
        self.printStepsToFile()

if __name__=="__main__":
    WorkflowGenerator().generate()
