import json

class Producer:

    def __init__(self, broker, topic):
        self.server = broker['server']
        self.sync = False
        self.topic = topic
        self.port = broker['port']
        self.flatten = False
        self.type = 'kafka'

class Workflow:
    def __init__(self, workflowFilename, instances, workflowName):
        self.workflowFilename = workflowFilename
        self.instances = instances
        self.workflowName = workflowName

class WorkflowConfig:
    def __init__(self, producers, workflows):
        self.producers = producers
        self.workflows = workflows

    def toJSON(self):
        config = self.__dict__
        data = config["producers"][0].__dict__
        data["broker.server"] = data.pop("server")
        data["broker.port"] = data.pop("port")
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=False, indent=1)
