from time import sleep
from uuid import uuid4
from confluent_kafka.error import KafkaError
from confluent_kafka.serializing_producer import SerializingProducer
from model import Name, Count
from confluent_kafka.error import KeySerializationError
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry.schema_registry_client import SchemaRegistryClient, SchemaRegistryError

def produce():
    print("Producing records")

    topic = "TestTopic"
    # Configure a schema registry client
    sr_config: dict[str, str] = {
        "url": "http://localhost:8081",
    }

    schema_registry_client = SchemaRegistryClient(sr_config)

    # Configure the producer client
    name_avro_serializer = AvroSerializer(schema_registry_client=schema_registry_client,
                                          schema_str=Name.schema,
                                          to_dict=Name.name_to_dict)

    count_avro_serializer = AvroSerializer(schema_registry_client=schema_registry_client,
                                           schema_str=Count.schema,
                                           to_dict=Count.count_to_dict)

    producer_config: dict[str, object] = {
        "bootstrap.servers": "localhost:9092",
        "message.timeout.ms": "0", # milliseconds
        "key.serializer": name_avro_serializer,
        "value.serializer": count_avro_serializer,
        "error_cb": error_cb,
        "on_delivery": callback,
        "batch.size": "1600000",
        "batch.num.messages": "10",
        "linger.ms": "1000",
        "client.id": "python_example",
        "partitioner": "consistent_random",
        "enable.idempotence": "true",
        # Enable idempotence is syntactic sugar for setting the following properties
        #"acks": "all",
        #"retries": 2147483647,
        #"queuing.strategy": "fifo", # deprecated
        #"max.in.flight.requests.per.connection": 5
    }

    producer = SerializingProducer(producer_config)

    # Produce records
    i = 1;

    while 1==1:
        try:
            name_object = Name(name="alice")
            #name = str(uuid4())
            #name_object = Name(name=name)
            count_object = Count(count=i)
            producer.produce(topic=topic, key=name_object, value=count_object)
            producer.flush()
            sleep(1);
            i += 1

        except KeyboardInterrupt:
            # Make sure remaining records are published and receive events
            producer.flush()
            break
        except (ConnectionError, ConnectionRefusedError) as e:
            print(f"Unable to connect to {producer_config['bootstrap.servers']}. Retrying ...")
        except (KeySerializationError) as e:
            print(f"Schema Registry error: {e}")

# Any exception raised from this callback will be re-raised from the triggering flush() or poll() call.

def error_cb(err):
    if err.code() == KafkaError._ALL_BROKERS_DOWN:
        print(f"Unable to connect to Kafka; giving up.")
        raise ConnectionRefusedError

    if err.code() == KafkaError._AUTHENTICATION:
        print(f"Unable to authenticate to Kafka; giving up.")
        raise ConnectionRefusedError

def callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print(
            f"Produced event to topic {msg.topic()}: key = {msg.key()} value = {msg.value()}")

if __name__ == "__main__":
    print ("Producing records. ctrl+c to end")
    produce()
