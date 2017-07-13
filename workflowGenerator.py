from random import sample
f = ""
def getInputs():
    fileNumber = input("give cluster name: ")
    timeInMins = int(input("Enter time in minutes: "))
    anomalyDuration = int(input("Enter condition for anomaly in seconds: "))
    anomalyCount = int(input("Enter number of anomalies to be produced: "))
    return (fileNumber, timeInMins, anomalyDuration, anomalyCount)

def createFile(fileNumber):
    fileName = "./json-data-generator-1.2.2-SNAPSHOT/conf/cpuUsageWorkflow{}.json".format(fileNumber)
    global f
    f = open(fileName, 'w')

def println(s):
    f.write(s + "\n")

def generateAnomalousTimeSeq(timeInMins, anomalyDuration,anomalyCount):
    time=timeInMins*60
    timeSeq = sample(range(int(time/anomalyDuration)),anomalyCount)
    anomalyStartArray=list(map((lambda x: (x*anomalyDuration, (x+1)*anomalyDuration) if x%2==0 else (x*anomalyDuration, (x+1)*anomalyDuration-1)),timeSeq))
    anomalyStartArray.sort()
    print(anomalyStartArray)
    return anomalyStartArray

def printStepsToFile(time, anomalyStartArray):
    listPos=0
    println("{\n\t\"eventFrequency\": 1000,\n\t\"varyEventFrequency\": false,\n\t\"repeatWorkflow\": true,")
    println("\t\"timeBetweenRepeat\": 0,\n\t\"varyRepeatFrequency\": false,\n\t\"steps\": [{")
    for i in range(time):
        println("\t\t\"config\": [{\n\t\t\t\"nodeID\": 1,\n\t\t\t\"timestamp\":\"now()\",")
        if i>=anomalyStartArray[listPos][0] and i < anomalyStartArray[listPos][1]:
            println("\t\t\t\"cpu\":\"double(81.0,100.0)\"")
            if i == (anomalyStartArray[listPos][1])-1:
                listPos =(listPos + 1)%len(anomalyStartArray)
        else:
            println("\t\t\t\"cpu\":\"double(1.0,80.0)\"")
        println("\t\t}]")
        if i == time-1:
            println("\t}]")
        else:
            println("\t},{")

    println("}")

def execute():
    (fileNumber, timeInMins, anomalyDuration, anomalyCount) = getInputs()
    createFile(fileNumber)
    anomalyStartArray = generateAnomalousTimeSeq(timeInMins, anomalyDuration, anomalyCount)
    printStepsToFile(timeInMins * 60, anomalyStartArray)
    f.close()

if __name__=="__main__":
    execute()
