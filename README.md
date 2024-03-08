# How Kafka Works

This repo contains materials for 'How Kafka Works', a presentation delivered to conferences and user groups.

## Repo Structure

## Running Kafka

``` bash
cd docker/
docker-compose up
```

## Kafka Commands

``` bash
#Get a shell on the Kafka broker
docker exec -it broker /bin/bash

# Inspect a consumer group
    kafka-consumer-groups --bootstrap-server localhost:9092 --group example_consumer --describe

# Inspect a topic
kafka-topics --bootstrap-server localhost:9092 --topic TestTopic --describe

```

## More Resources

- [The Log: What Every Software Engineer Should know About Real-Time Data's Unifying Abstraction](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)
