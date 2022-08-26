from decimal import Decimal

from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import avro.schema
import avro.io
import io
import sys


class RequestProducer:

    trade_batch_entry = {
        "batchId": "test_batch_id_1",
        "transactions": [
            {
                "state": {
                    "transactionId": "TEST_TRANSACTION_1",
                    "ask": True,
                    "makerAddress": "TEST_MAKER_ADDRESS",
                    "takerAddress": "TEST_TAKER_ADDRESS",
                    "asset": "SOL_USDC",
                    "amount": Decimal("10.00"),
                    "price": Decimal("20.00"),
                    "fee": Decimal("0.50"),
                    "makerLeverage": 5,
                    "takerLeverage": 1
                }
            }
        ]
    }

    withdraw_batch_entry = {
        "batchId": "test_batch_id_2",
        "transactions": [
            {
                "state": {
                    "transactionId": "TEST_TRANSACTION_2",
                    "address": "TEST_WITHDRAW_ADDRESS_1",
                    "amount": 10.0
                }
            }
        ]
    }

    def publish_trade_batch(self):
        conf = {'bootstrap.servers': 'localhost:29092'}
        producer = Producer(**conf)

        schema_path = "../models/TradeBatchRequest.avsc"
        schema = avro.schema.parse(open(schema_path).read())

        writer = avro.io.DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write(self.trade_batch_entry, encoder)
        raw_bytes = bytes_writer.getvalue()
        producer.produce('aggregateResult', raw_bytes)

        producer.flush()