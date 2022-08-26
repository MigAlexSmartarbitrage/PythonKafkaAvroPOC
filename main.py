from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import avro.schema
import avro.io
import io
import sys


def consume_messages():
    conf = {'bootstrap.servers': 'localhost:29092', 'group.id': 'dexilon',
            'default.topic.config': {'auto.offset.reset': 'smallest'}}
    consumer = Consumer(**conf)
    topic = consumer.subscribe(['aggregateResult'])
    schema_path = "models/TradeBatchRequest.avsc"
    schema = avro.schema.parse(open(schema_path).read())

    try:
        running = True
        while running:
            msg = consumer.poll(timeout=60000)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(),
                                      msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))

            message = msg.value()
            bytes_reader = io.BytesIO(message)
            decoder = avro.io.BinaryDecoder(bytes_reader)
            reader = avro.io.DatumReader(schema)
            try:
                decoded_msg = reader.read(decoder)
                print(decoded_msg)
                sys.stdout.flush()
            except AssertionError:
                continue

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    consume_messages()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
