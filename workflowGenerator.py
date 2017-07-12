from random import sample
fileNumber=input("give cluster name: ")
fileName="./json-data-generator-1.2.2-SNAPSHOT/conf/cpuUsageWorkflow{}.json".format(fileNumber)
f = open(fileName, 'w')

def print_to_file(s):
    f.write(s + "\n")

time = int(input("Enter time in minutes: "))
anomalyDuration = int(input("Enter condition for anomaly in seconds: "))
anomalyCount = int(input("Enter number of anomalies to be produced: "))
time=time*60
listPos=0;

anomalyStartArray=list(map((lambda x: (x*anomalyDuration, (x+1)*anomalyDuration)),sample(range(int(time/anomalyDuration)),anomalyCount)))
anomalyStartArray.sort()
print(anomalyStartArray)
# combine print statements
print_to_file("{\n\t\"eventFrequency\": 1000,\n\t\"varyEventFrequency\": false,\n\t\"repeatWorkflow\": true,")
print_to_file("\t\"timeBetweenRepeat\": 0,\n\t\"varyRepeatFrequency\": false,\n\t\"steps\": [{")
for i in range(time):
    print_to_file("\t\t\"config\": [{\n\t\t\t\"nodeID\": 1,\n\t\t\t\"timestamp\":\"now()\",")
    if i>=anomalyStartArray[listPos][0] and i < anomalyStartArray[listPos][1]:
        print_to_file("\t\t\t\"cpu\":\"double(81.0,100.0)\"")
        if i == (anomalyStartArray[listPos][1])-1:
            listPos =(listPos + 1)%len(anomalyStartArray)
    else:
        print_to_file("\t\t\t\"cpu\":\"double(1.0,80.0)\"")
    print_to_file("\t\t}]")
    if i == time-1:
        print_to_file("\t}]")
    else:
        print_to_file("\t},{")

print_to_file("}")
f.close()
