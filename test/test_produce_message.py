from RequestProducer import RequestProducer

test_instance = RequestProducer()

def test_should_send_trade_avro_request():
    test_instance.publish_trade_batch()