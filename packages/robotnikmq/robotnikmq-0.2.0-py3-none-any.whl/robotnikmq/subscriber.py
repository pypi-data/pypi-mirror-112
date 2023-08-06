from collections import namedtuple
from typing import Optional, Callable, List

from pika.exceptions import AMQPConnectionError
from retry import retry
from typeguard import typechecked

from robotnikmq.config import RobotnikConfig
from robotnikmq.core import Robotnik, ConnErrorCallback, Message

OnMessageCallback = Callable[[Message], None]

ExchangeBinding = namedtuple('ExchangeBinding', ['exchange', 'binding_key'])


class Subscriber(Robotnik):
    @typechecked
    def __init__(self,
                 exchange_bindings: Optional[List[ExchangeBinding]] = None,
                 config: Optional[RobotnikConfig] = None,
                 on_conn_error: ConnErrorCallback = None):
        super().__init__(config=config, on_conn_error=on_conn_error)
        self.exchange_bindings = exchange_bindings or []

    @typechecked
    def _bind(self, exchange_binding: ExchangeBinding) -> 'Subscriber':
        self.exchange_bindings.append(exchange_binding)
        return self

    @typechecked
    def bind(self, exchange: str, binding_key: str = '#') -> 'Subscriber':
        return self._bind(ExchangeBinding(exchange, binding_key))

    @retry(AMQPConnectionError, delay=2, jitter=1)
    @typechecked
    def run(self, callback: OnMessageCallback) -> None:
        while 42:
            with self.open_channel() as channel:
                @typechecked
                def meta_callback(_, method, ___, body: bytes):
                    callback(Message.of(body.decode()))
                    channel.basic_ack(delivery_tag=method.delivery_tag)
                queue_name = channel.queue_declare(queue='', exclusive=True).method.queue
                for ex_b in self.exchange_bindings:
                    channel.exchange_declare(exchange=ex_b.exchange,
                                             exchange_type='topic',
                                             auto_delete=True)
                    channel.queue_bind(exchange=ex_b.exchange,
                                       queue=queue_name,
                                       routing_key=ex_b.binding_key)
                channel.basic_consume(queue=queue_name,
                                      on_message_callback=meta_callback,
                                      auto_ack=False)
                channel.start_consuming()
