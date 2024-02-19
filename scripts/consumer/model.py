rom uuid import uuid4

 

class Count(object):

    """

        Count stores the deserialized Avro record for the Kafka value.

    """

    schema = """

        {

            "namespace": "io.confluent.examples.clients.cloud",

            "name": "Count",

            "type": "record",

            "fields": [

                {

                    "name": "count"

                    , "type": "int"

                }

            ]

        }

    """

 

    # Use __slots__ to explicitly declare all data members.

    __slots__ = ["count", "id"]

 

    def __init__(self, count=None):

        self.count = count

        # Unique id used to track produce request success/failures.

        # Do *not* include in the serialized object.

        self.id = uuid4()

 

    @staticmethod

    def dict_to_count(obj, ctx):

        return Count(obj['count'])

 

    @staticmethod

    def count_to_dict(count, ctx):

        return Count.to_dict(count)

 

    def to_dict(self):

        """

            The Avro Python library does not support code generation.

            For this reason we must provide a dict representation of our class for serialization.

        """

        return dict(count=self.count)

 

class Name(object):

    """

        Name stores the deserialized Avro record for the Kafka key.

    """

    schema = """

        {

            "namespace": "io.confluent.examples.clients.cloud",

            "name": "Name",

            "type": "record",

            "fields": [

                {"name": "name", "type": "string"}

            ]

        }

    """

    # Use __slots__ to explicitly declare all data members.

    __slots__ = ["name", "id"]

 

    def __init__(self, name=None):

        self.name = name

        # Unique id used to track produce request success/failures.

        # Do *not* include in the serialized object.

        self.id = uuid4()

 

    @staticmethod

    def dict_to_name(obj, ctx):

        return Name(obj['name'])

 

    @staticmethod

    def name_to_dict(name, ctx):

        return Name.to_dict(name)

 

    def to_dict(self):

        """

            The Avro Python library does not support code generation.

            For this reason we must provide a dict representation of our class for serialization.

        """

        return dict(name=self.name)

 