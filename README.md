# Kafka Load Generator

### Json data generator to generate log of nodes in a cluster per second with rule based anomalies(>80%)

**kafka_load_generator** can be used to generate stub data of cpu log of multiple nodes in a cluster on a per second basis and send the data to a kafka broker. Learn more about kafka [here](https://kafka.apache.org/).

The data generated does not represent actual cpu usage, but generates data which has some continuous sequences of 9 and 10 seconds of cpu usage of a single node above 80%.
The data generated will contain cpu usage from 1 to 100.
* Some data will be <= 80, which is assumed to be normal data.
* Some data will be > 80, which is considered anomalous.
Anomalous data will be generated in sequences of 9 secs or 10 secs, which might be consecutive as well. The gap between two sequences is random.


[json-data-generator](https://github.com/acesinc/json-data-generator) is used here to generate the json and publish them to a kafka broker.
kafka_load_generator can generate stub cpu logs for multiple nodes of the same cluster. If scaling up the number of nodes creates performance issue on one machine, multiple instances of this generator can be started on various machines after configuring the [clusterConfig.json](/master/clusterConfig.json)'s firstNode and lastNode.

#### Example:
If you want to generate data for 2000 nodes belonging to a same cluster, but the machine you are using can generate only upto 1000 points per second before creating performance issues, two machines can be used to achieve the same. The `clusterConfig` files will look like the following. Notice the `firstNode` and `lastNode`:
##### Machine 1
```javascript
{
  "topic": "cpu-usage",

  "broker": {
    "server": "127.0.0.1",
    "port": 9092
  },

  "cluster": {
    "clusterName": "firstCluster",
    "firstNode": 1,
    "lastNode": 1000
  }
}
```

##### Machine 2
```javascript
{
  "topic": "cpu-usage",

  "broker": {
    "server": "127.0.0.1",
    "port": 9092
  },

  "cluster": {
    "clusterName": "firstCluster",
    "firstNode": 1001,
    "lastNode": 2000
  }
}
```

### Cluster Configuration
[clusterConfig](../master/clusterConfig.json) is the main configuration file which contains:
* `topic` - Name of the Kafka topic to publish to.
* Kafka broker's details:

Variable | Definition
-------- | ----------
`server` | The IP address of the kafka broker server(also referred to as bootstrap server). Currently only one broker server can be given as input.
`port`   | The port of the kafka broker server. This is the port on which the kafka server is listening to. Only one port can be given as input.

* Details of the cluster

Variable | Definition
---------|-----------
`clusterName`| Name of the cluster to which all the nodes belong to. It will be same for all the nodes.
`firstNode`|Identity number of the first node for which data needs to be generated
`lastNode`|Identity number of the last node for which data needs to be generated

## To execute:

1. Edit [clusterConfig.json](../master/clusterConfig.json) accordingly. Details below
2. Run `python3 configGenerator.py` in terminal. If there are no errors, it will generate two types of json files inside [json-data-generator/conf](../../tree/master/json-data-generator-1.2.2-SNAPSHOT/conf).
  * cpuUsageConfig_*clusterName*.json
  * `n` instances of cpuUsageWorkflow_*clusterName*_*nodeNumber*.json where `n` is (`lastNode`-`firstNode`+1) and *nodeNumber* ranges from `firstNode` to `lastNode`.
3. Run `java -jar json-data-generator-1.2.2-SNAPSHOT/json-data-generator-1.2.2-SNAPSHOT.jar cpuUsageConfig_*clusterName*.json`

*Note: Kafka broker should be running before executing the jar.*

#### Prerequisites:
1. [Python3](https://www.python.org/download/releases/3.0/)
2. [Java8](http://www.oracle.com/technetwork/java/javase/overview/java8-2100321.html)

### To do:
* Script to take broker and cluster details as arguments, and start producer.
* Containerize kafka_load_generator.
