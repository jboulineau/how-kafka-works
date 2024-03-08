---
title: How Kafka Works
author: Jon Boulineau
...

# How Kafka Works

## About Me

### Jon Boulineau

- Emerging Security Technologies Lead, Citizens  

- **Email**: jboulineau@pm.me
- **Blog**: jonboulineau.me
- **Twitter**: @jboulineau
- **GitHub**: jboulineau

## The Problem

``` text
   ┌──────────────┐
   │              │
   │  Application │
   │              │
   └───────┬──────┘
           │
           │
           │
           │
  ┌────────▼─────────┐
  │                  │
  │  Database        │
  │                  │
  └──────────────────┘
```

## The Problem II

``` text
                               ┌──────────────┐
                               │              │
                               │  Application │
                               │              │        ┌─────────────────────┐
                               └───────┬──────┘        │                     │
                                       │               │  File Extract       │
                                       │               │                     │
                                       │               └──────────┬──────────┘
            ┌──────────────┐           │                          │
            │              │           │                          │
            │ Application  │           │                          │
            │              │  ┌────────▼─────────┐                │
            └─────┬────────┘  │                  │                │
                  │           │  Database        ◄────────────────┘
                  └──────────►│                  │
                              └──────▲────▲──────┘
                                     │    │
                                     │    │
                                     │    │
                                     │    │
           ┌─────────────────────┐   │    │      ┌───────────────────┐
           │                     │   │    │      │                   │
           │  Data Mart ETL      ├───┘    └──────┤                   │
           │                     │               │ Data Lake ETL     │
           │                     │               │                   │
           └─────────────────────┘               └───────────────────┘

```

## The Solution

``` text
                                        ┌──────────────────────┐                                                            
                                        │                      │                                                            
                                        │                      │                                                            
                                        │  Database            │                                        ┌───────────────┐   
                                        │                      │                                        │               │   
                                        │                      │                           ┌────────────► Applications  │   
                                        └───────────▲──────────┘                           │            │               │   
                                                    │                                      │            └───────────────┘   
                                                    │                         ┌────────────┴───────┐                        
      ┌─────────────────┐                ┌──────────┴──────────┐              │                    │    ┌───────────────┐   
      │                 │                │                     │              │                    │    │               │   
      │  Application    ├────────────────► API                 ├──────────────►  Kafka             ├────► Datalake ETL  │   
      │                 │                │                     │              │                    │    │               │   
      └─────────────────┘                └──────────▲──────────┘              │                    │    └───────────────┘   
                                                    │                         └────────────┬───────┘                        
                                                    │                                      │            ┌──────────────────┐
                                                    │                                      │            │                  │
                                         ┌──────────┴──────────┐                           └────────────► Stream Analytics │
                                         │                     │                                        │                  │
                                         │ User Interface      │                                        └──────────────────┘
                                         │                     │                                                            
                                         └─────────────────────┘                                                            

```

## What is Kafka?

Kafka is a **_distributed immutable transaction log_** created by engineers at LinkedIn and introduced to the Apache Software Foundation incubator in 2011.

- **Distributed**: Kafka is 'infinitely' horizontally scalable.
- **Immutable**: Once data are stored, they cannot be modified.
- **Transaction Log**: The persistence data structure is an ordered series of state changes.

`**Kafka is not a queue manager**`

## Brokers

- A 'Broker' is an instance of the Kafka service.
- Multiple brokers form a cluster - scales "infinitely"

```text
┌───────────────────────────────┐   ┌───────────────────────────────┐   ┌───────────────────────────────┐
│ Broker 0                      │   │ Broker 1                      │   │ Broker 2                      │
│                               │   │                               │   │                               │
└───────────────────────────────┘   └───────────────────────────────┘   └───────────────────────────────┘
```

## Topics

This diagram represents a three broker cluster hosting a single topic.

- A **topic** is a partitioned immutable transaction log.
- Each partition has a broker leader (indicated by +)

``` text
┌───────────────────────────────┐   ┌───────────────────────────────┐   ┌───────────────────────────────┐
│ Broker 0                      │   │ Broker 1                      │   │ Broker 2                      │
│                               │   │                               │   │                               │
│    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │
│    │                     │    │   │    │                     │    │   │    │                     │    │
│    │ Partition 0 (+)     │    │   │    │ Partition 0         │    │   │    │ Partition 0         │    │
│    └─────────────────────┘    │   │    └─────────────────────┘    │   │    └─────────────────────┘    │
│                               │   │                               │   │                               │
│    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │
│    │                     │    │   │    │                     │    │   │    │                     │    │
│    │ Partition 1         │    │   │    │ Partition 1         │    │   │    │ Partition 1  (+)    │    │
│    └─────────────────────┘    │   │    └─────────────────────┘    │   │    └─────────────────────┘    │
│                               │   │                               │   │                               │
│    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │
│    │                     │    │   │    │                     │    │   │    │                     │    │
│    │ Partition 2         │    │   │    │ Partition 2  (+)    │    │   │    │ Partition 2         │    │
│    └─────────────────────┘    │   │    └─────────────────────┘    │   │    └─────────────────────┘    │
│                               │   │                               │   │                               │
│    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │
│    │                     │    │   │    │                     │    │   │    │                     │    │
│    │ Partition 3 (+)     │    │   │    │ Partition 3         │    │   │    │ Partition 3         │    │
│    └─────────────────────┘    │   │    └─────────────────────┘    │   │    └─────────────────────┘    │
│                               │   │                               │   │                               │
└───────────────────────────────┘   └───────────────────────────────┘   └───────────────────────────────┘
```

## Records

- A **record** is a key value pair persisted to a partition as a Java byte array.
  - **_NOTE_**: By using **Schema Registry**, records are forced to follow a contract defined in JSON, Avro, or Protbuf format.

``` text
                       ┌───────────────────────────────────────────────────────────────────────────┐
                       │ TOPIC <foo>                                                               │
                       │                                                                           │
                       │   ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ │
                       │   │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │
            ┌──────────┼─► │ 0 │ │ 1 │ │ 2 │ │ 3 │ │ 4 │ │ 5 │ │ 6 │ │ 7 │ │ 8 │ │ 9 │ │ . │ │ . │ ├
            │          │   │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │
            │          │   └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ │
            │          │   Partition 1                                                             │
┌───────────┴──┐       │                                                                           │
│              │       │   ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ │
│              │       │   │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │
│ Producer     ├───────┼─► │ 0 │ │ 1 │ │ 2 │ │ 3 │ │ 4 │ │  5│ │ 6 │ │ 7 │ │ 8 │ │ 9 │ │ . │ │ . │ ├
│              │       │   │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │
│              │       │   └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ │
└───────────┬──┘       │    Partition 2                                                            │
            │          │                                                                           │
            │          │   ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ │
            │          │   │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ ├
            └──────────┼─► │ 0 │ │ 1 │ │ 2 │ │ 3 │ │ 4 │ │ 5 │ │ 6 │ │ 7 │ │ 8 │ │ 9 │ │ . │ │ . │ │
                       │   │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │   │ │
                       │   └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ │
                       │   Partition 3                                                             │
                       └───────────────────────────────────────────────────────────────────────────┘
```

## Concept Review

- A 'Broker' is an instance of the Kafka service.
- Multiple brokers form a cluster - scales "infinitely"
- A **topic** is a partitioned immutable transaction log.
- A **partition** is an ordered segment of the transaction log.
- A **record** is a key value pair persisted to a partition as a Java byte array.
  - **_NOTE_**: By using **Schema Registry**, records are forced to follow a contract defined in JSON, Avro, or Protbuf format.
- An **offset** is an ordinal value assigned to each record to identify it on a partition.
  - A record is identified by its topic, partition id, and offset.

## Producers and Consumers

- A **producer** is any application or service that adds records to one or more Kafka topics
- A **consumer** is any application or service that reads records from one or more Kafka topics
- A **consumer instance** is a running application or service process
- A **consumer group** is a collection of consumer instances

`Confluent provides libraries for Java, .Net, Go, C/C++, and Python.`  
`Many other languages, such as Rust and Node.js, have community created libraries.`  

### Producing a Record

1. The producer serializes one or more key/value pairs into a conforming format, then pushes the record(s) to a topic.
2. Kafka assigns each record to a partition based on the value in the key.
3. The broker leader for each partition being assigned a record initiates a replication to the partition replicas.
4. When the configured minimum number of replicas have acknowledged, Kafka confirms writing the record to the producer.

### Consuming Records

1. One or more consumer instances establish persistent connections to a Kafka topic.
2. Kafka assigns each consumer instance to zero or more partitions and establishes connection to the broker leader.
3. The Kafka client library polls the partition for new records continually until closed (implementation varies depending on the library).
4. As records are received the consumer processes the record. Offsets are committed based on the pattern desired by the consumer.

## Producers and Consumers Diagram

``` text
                                      ┌───────────────────────────┐
                                      │         Producer          │
                                      └────────────┬──────────────┘
                                                   ▼
               ┌──────────────────────────----------
               ▼                                   
┌───────────────────────────────┐   ┌───────────────────────────────┐   ┌───────────────────────────────┐
│ Broker 0                      │   │ Broker 1                      │   │ Broker 2                      │
│                               │   │                               │   │                               │
│    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │
│    │ Partition 0 (+)     │    │   │    │ Partition 0         │    │   │    │ Partition 0         │    │
│    └─────────────────────┘    │   │    └─────────────────────┘    │   │    └─────────────────────┘    │
│                               │   │                               │   │                               │
│    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │
│    │ Partition 1         │    │   │    │ Partition 1         │    │   │    │ Partition 1  (+)    │    │
│    └─────────────────────┘    │   │    └─────────────────────┘    │   │    └─────────────────────┘    │
│                               │   │                               │   │                               │
│    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │
│    │ Partition 2         │    │   │    │ Partition 2  (+)    │    │   │    │ Partition 2         │    │
│    └─────────────────────┘    │   │    └─────────────────────┘    │   │    └─────────────────────┘    │
│                               │   │                               │   │                               │
│    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │   │    ┌─────────────────────┐    │
│    │ Partition 3 (+)     │    │   │    │ Partition 3         │    │   │    │ Partition 3         │    │
│    └─────────────────────┘    │   │    └─────────────────────┘    │   │    └─────────────────────┘    │
│                               │   │                               │   │                               │
└───────────────────┬──────┬────┘   └────────────────┬──────────────┘   └──────┬────────────────────────┘
                    │      │                         │                         │
           ┌────────┼──────┼─────────────────────────┼─────────────────────────┼────────────┐
           │        │      │                         │                         │            │
           │    ┌───▼──────▼─────────┐    ┌──────────▼─────────┐     ┌─────────▼──────────┐ │
           │    │   Instance 0       │    │   Instance 1       │     │  Instance 2        │ │
           │    └────────────────────┘    └────────────────────┘     └────────────────────┘ │
           │  Consumer Group <foo>                                                          │
           └────────────────────────────────────────────────────────────────────────────────┘

```

## DEMO TIME

``` text

 (             *        )           (       *           
 )\ )        (  `    ( /(     *   ) )\ )  (  `          
(()/(   (    )\))(   )\())  ` )  /((()/(  )\))(   (     
 /(_))  )\  ((_)()\ ((_)\    ( )(_))/(_))((_)()\  )\    
(_))_  ((_) (_()((_)  ((_)  (_(_())(_))  (_()((_)((_)   
 |   \ | __||  \/  | / _ \  |_   _||_ _| |  \/  || __|  
 | |) || _| | |\/| || (_) |   | |   | |  | |\/| || _|   
 |___/ |___||_|  |_| \___/    |_|  |___| |_|  |_||___|  
                                                        

```

## Closing thoughts

- Kafka is NOT A QUEUE
- Consider your topic design up front
  - Naming conventions are essential at scale
  - Adding partitions is easy, but can break your consumers
- Consider your consuming patterns carefully
  - At-least-once vs. at-most-once vs. exactly-once
  - Topic replay consumer settings
- Schemas (and schema registry) may seem like overhead...use them anyway

GitHub Repo: [https://github.com/jboulineau/how-kafka-works](https://github.com/jboulineau/how-kafka-works)
