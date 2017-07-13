from random import sample
class WorkflowGenerator:

    def getInputs(self):
        self.clusterName = input("give cluster name: ")
        self.nodeNumber = input("give node number: ")
        self.time = int(input("Enter time in seconds: "))
        self.anomalyDuration = int(input("Enter condition for anomaly in seconds: "))
        self.anomalyCount = int(input("Enter number of anomalies to be produced: "))

    def createFile(self):
        fileName = "./json-data-generator-1.2.2-SNAPSHOT/conf/cpuUsageWorkflow_{}_{}.json".format(self.clusterName, self.nodeNumber)
        self.f = open(fileName, 'w')

    def println(self,s):
        self.f.write(s + "\n")

    def generateAnomalousTimeSeq(self):
        timeSeq = sample(range(int(self.time/self.anomalyDuration)),self.anomalyCount)
        self.anomalyStartArray=list(map((lambda x: (x*self.anomalyDuration, (x+1)*self.anomalyDuration) if x%2==0 else (x*self.anomalyDuration, (x+1)*self.anomalyDuration-1)),timeSeq))
        self.anomalyStartArray.sort()
        print(self.anomalyStartArray)

    def printStepsToFile(self):
        listPos=0
        self.println("{\n\t\"eventFrequency\": 1000,\n\t\"varyEventFrequency\": false,\n\t\"repeatWorkflow\": true,")
        self.println("\t\"timeBetweenRepeat\": 0,\n\t\"varyRepeatFrequency\": false,\n\t\"steps\": [{")
        for i in range(self.time):
            self.println("\t\t\"config\": [{{\n\t\t\t\"cluster\": \"{}\",\n\t\t\t\"nodeID\": \"{}\",\n\t\t\t\"timestamp\":\"now()\",".format(self.clusterName, self.nodeNumber))
            if i>=self.anomalyStartArray[listPos][0] and i < self.anomalyStartArray[listPos][1]:
                self.println("\t\t\t\"cpu\":\"double(81.0,100.0)\"")
                if i == (self.anomalyStartArray[listPos][1])-1:
                    listPos =(listPos + 1)%len(self.anomalyStartArray)
            else:
                self.println("\t\t\t\"cpu\":\"double(1.0,80.0)\"")
            self.println("\t\t}]")
            if i == self.time-1:
                self.println("\t}]")
            else:
                self.println("\t},{")

        self.println("}")

    def generate(self,arg=[]):
        if len(arg)==0:
            self.getInputs()
        else:
            (self.clusterName, self.nodeNumber, self.time, self.anomalyDuration, self.anomalyCount)=tuple(arg)
        self.createFile()
        self.generateAnomalousTimeSeq()
        self.printStepsToFile()
        self.f.close()

if __name__=="__main__":
    WorkflowGenerator().generate()
