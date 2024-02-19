from time import sleep

from model import Name, Count

from confluent_kafka.error import KafkaError

from confluent_kafka import DeserializingConsumer

from confluent_kafka.schema_registry import SchemaRegistryClient

from confluent_kafka.schema_registry.avro import AvroDeserializer

from confluent_kafka.serialization import SerializationError

 

def consume():

    print("Consuming records\n")

 

    topics: list[str] = ["TestTopic2"]

 

    # Configure a schema registry client

    sr_config: dict[str, str] = {

        "url": http://localhost:8081,

    }

 

    schema_registry_client = SchemaRegistryClient(sr_config)

 

    # Configure the consumer client

 

    name_avro_deserializer = AvroDeserializer(schema_registry_client=schema_registry_client,

                                              schema_str=Name.schema,

                                              from_dict=Name.dict_to_name)

    count_avro_deserializer = AvroDeserializer(schema_registry_client=schema_registry_client,

                                               schema_str=Count.schema,

                                               from_dict=Count.dict_to_count)

 

    consumer_config: dict[str, object] = {

        "bootstrap.servers": "localhost:9092",

        "key.deserializer": name_avro_deserializer,

        "value.deserializer": count_avro_deserializer,

        "error_cb": error_cb,

        "group.id": "example_consumer",

        "auto.offset.reset": "earliest",

        "partition.assignment.strategy": "roundrobin",

        "client.id": "python_example",

        "session.timeout.ms": "60000",

        "enable.auto.commit": "false",

    }

 

    schema_registry_client = SchemaRegistryClient(sr_config)

 

    consumer = DeserializingConsumer(consumer_config)

 

    consumer.subscribe(topics)

 

    # Process messages

 

    while 1 == 1:

        try:

            msg = consumer.poll(10)

            if msg is None:

                print(f"Waiting for message ...")

                sleep(1)

                continue

            elif msg.error():

                print(f'error: {msg.error()}')

            else:

                ### PROCESSING LOGIC GOES HERE ####

                print(f"Consumed record with key {msg.key().name} and value {msg.value().count}")

                consumer.commit(asynchronous=False)

        except KeyboardInterrupt:

            # Leave group and commit final offsets

            consumer.close()

            break

        except SerializationError as e:

            # Report malformed record, discard results, continue polling

            print(f"Message deserialization failed: {e}")

            consumer.commit(asynchronous=False)

            pass

 

    # Cleanup at the end

    consumer.close()

 

def error_cb(err):

    if err.code() == KafkaError._ALL_BROKERS_DOWN or \

       err.code() == KafkaError._AUTHENTICATION:

        # Any exception raised from this callback will be re-raised from the poll() call.

        print("Unable to connect to Kafka.")

        raise ConnectionRefusedError

 

if __name__ == "__main__":

    consume()

