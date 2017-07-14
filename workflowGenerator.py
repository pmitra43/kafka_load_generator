from random import sample
import json
class WorkflowGenerator:

    def getInputs(self):
        self.clusterName = input("give cluster name: ")
        self.nodeNumber = input("give node number: ")
        self.time = int(input("Enter time in seconds: "))
        self.anomalyDuration = int(input("Enter condition for anomaly in seconds: "))
        self.anomalyCount = int(input("Enter number of anomalies to be produced: "))

    def printToFile(self,s):
        fileName = "./json-data-generator-1.2.2-SNAPSHOT/conf/cpuUsageWorkflow_{}_{}.json".format(self.clusterName, self.nodeNumber)
        f = open(fileName, 'w')
        f.write(s + "\n")
        f.close()

    def generateAnomalousTimeSeq(self):
        timeSeq = sample(range(int(self.time/self.anomalyDuration)),self.anomalyCount)
        self.anomalyStartArray=list(map((lambda x: (x*self.anomalyDuration, (x+1)*self.anomalyDuration) if x%2==0 else (x*self.anomalyDuration, (x+1)*self.anomalyDuration-1)),timeSeq))
        self.anomalyStartArray.sort()
        print(self.anomalyStartArray)

    def generateConfig(self, i):
        config={}
        config['cluster']=self.clusterName
        config['nodeID']=self.nodeNumber
        config['timestamp']="now()"
        if i>=self.anomalyStartArray[self.listPos][0] and i < self.anomalyStartArray[self.listPos][1]:
            config['cpu']="double(81.0,100.0)"
            if i == (self.anomalyStartArray[self.listPos][1])-1:
                self.listPos =(self.listPos + 1)%len(self.anomalyStartArray)
        else:
            config['cpu']="double(1.0,80.0)"
        return config

    def generateSteps(self):
        steps=[]
        for i in range(self.time):
            config=[self.generateConfig(i)]
            dictionary={'config':config}
            steps.append(dictionary)
        return steps

    def printStepsToFile(self):
        self.listPos=0
        jsonData={}
        jsonData['eventFrequency']=1000
        jsonData['varyEventFrequency']=False
        jsonData['repeatWorkflow']=True
        jsonData['timeBetweenRepeat']=0
        jsonData['varyRepeatFrequency']=False
        jsonData['steps']=self.generateSteps()
        self.printToFile(json.dumps(jsonData,indent=1,sort_keys=False))

    def generate(self,arg=[]):
        if len(arg)==0:
            self.getInputs()
        else:
            (self.clusterName, self.nodeNumber, self.time, self.anomalyDuration, self.anomalyCount)=tuple(arg)
        self.generateAnomalousTimeSeq()
        self.printStepsToFile()

if __name__=="__main__":
    WorkflowGenerator().generate()
