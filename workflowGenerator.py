from random import randint
fileNumber=input("give cluster name: ")
fileName="./json-data-generator-1.2.2-SNAPSHOT/conf/cpuUsageWorkflow{}.json".format(fileNumber)
f = open(fileName, 'w')

def print_to_file(s):
    f.write(s + "\n")
time = int(input("Enter time in minutes: "))
anomalyMinute=randint(0,time-1)
time=time*60
# combine print statements
print_to_file("{\n\t\"eventFrequency\": 1000,\n\t\"varyEventFrequency\": false,\n\t\"repeatWorkflow\": true,")
print_to_file("\t\"timeBetweenRepeat\": 0,\n\t\"varyRepeatFrequency\": false,\n\t\"steps\": [{")
for i in range(time):
    print_to_file("\t\t\"config\": [{\n\t\t\t\"nodeID\": 1,\n\t\t\t\"timestamp\":\"now()\",")
    if i>=(anomalyMinute*60) and i<((anomalyMinute+1)*60):
        print_to_file("\t\t\t\"cpu\":\"double(81.0,100.0)\"")
    else:
        print_to_file("\t\t\t\"cpu\":\"double(1.0,80.0)\"")
    print_to_file("\t\t}]")
    if i == time-1:
        print_to_file("\t}]")
    else:
        print_to_file("\t},{")

print_to_file("}")
f.close()
