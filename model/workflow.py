import json

class Config:
    def __init__(self, configDetail):
        self.config = [configDetail]

class ConfigDetail:
    def __init__(self,  cluster, cpu, nodeID, timestamp, timeCounter):
        self.cluster = cluster
        self.timestamp = timestamp
        self.cpu = cpu
        self.nodeID = nodeID
        self.timeCounter = timeCounter

class Workflow:
    def __init__(self, timeBetweenRepeat, varyRepeatFrequency, varyEventFrequency, eventFrequency, repeatWorkflow, configList):
        self.timeBetweenRepeat = timeBetweenRepeat
        self.varyRepeatFrequency = varyRepeatFrequency
        self.varyEventFrequency = varyEventFrequency
        self.eventFrequency = eventFrequency
        self.repeatWorkflow = repeatWorkflow
        self.steps = configList

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=False, indent=1)
