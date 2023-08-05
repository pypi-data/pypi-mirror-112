from contextlib import contextmanager
from functools import lru_cache
from multiprocessing import Process, Event as event
from multiprocessing.synchronize import Event
from os import get_terminal_size
from pathlib import Path
from typing import Optional, Callable, Tuple, Any
from pprint import pformat

import click
from legion_utils import Priority
from robotnikmq import RobotnikConfig, Subscriber, Message
from termcolor import colored
from typeguard import typechecked

DEFAULT_CONFIG = Path.cwd() / 'config.yaml'


@contextmanager
def timeout_process(target=Callable, args=Tuple[Any], timeout: int = 10):
    proc = Process(target=target, args=args)
    proc.start()
    yield
    proc.terminate()
    proc.join(timeout=timeout)
    proc.kill()
    proc.join()


class MessagePrinter:
    def __init__(self,
                 msg_limit_received: Optional[Event] = None,
                 num_msgs: Optional[int] = None):
        self.msg_limit_received = msg_limit_received
        self.num_msgs = num_msgs

    @property
    def term_width(self) -> int:
        return get_terminal_size().columns

    def _priority_color(self, msg: Message) -> Optional[str]:
        if msg.contents['priority'] == 1:
            return 'blue'
        if msg.contents['priority'] == 2:
            return 'yellow'
        if msg.contents['priority'] == 3:
            return 'red'
        if msg.contents['priority'] == 4:
            return 'magenta'
        return None

    @lru_cache
    def _label(self, msg: Message) -> str:
        return f"{Priority(msg.contents['priority']).name}: {msg.timestamp.format()}"

    def _header(self, msg: Message) -> str:
        width = self.term_width
        untrimmed_header = f"{'=' * ((width - 2 - len(self._label(msg))) // 2 + 1)} {self._label(msg)} {'=' * ((width - 2 - len(self._label(msg))) // 2)}"
        return untrimmed_header[:width]

    def _route(self, msg: Message) -> str:
        width = self.term_width
        untrimmed_route = f"{'-' * ((width - 2 - len(msg.routing_key)) // 2 + 1)} {msg.routing_key} {'-' * ((width - 2 - len(msg.routing_key)) // 2)}"
        return untrimmed_route[:width]

    @typechecked
    def watch(self, msg: Message) -> None:
        print(colored(self._header(msg), self._priority_color(msg)))
        print(colored(self._route(msg), self._priority_color(msg)))
        print(colored(pformat(msg.contents), self._priority_color(msg)))
        print(colored('=' * self.term_width, self._priority_color(msg)))
        if self.num_msgs is not None:  # pragma: no cover
            self.num_msgs -= 1
            if self.num_msgs <= 0 and self.msg_limit_received is not None:
                self.msg_limit_received.set()


@typechecked
def _watch_process(exchange: str,
                   routing_key: str,
                   msg_limit_received: Optional[Event] = None,
                   config: Optional[RobotnikConfig] = None,
                   num_msgs: Optional[int] = None):
    watcher = MessagePrinter(msg_limit_received, num_msgs)
    sub = Subscriber(exchange=exchange, binding_key=routing_key, config=config)
    sub.register_listener(watcher.watch)
    sub.run()


@typechecked
def _watch(exchange: str, routing_key: str,
           num_msgs: Optional[int] = None,
           config: Optional[RobotnikConfig] = None):
    msg_limit_received = event()
    with timeout_process(target=_watch_process, args=(exchange,
                                                      routing_key,
                                                      msg_limit_received,
                                                      config,
                                                      num_msgs)):
        msg_limit_received.wait()


@click.group()
def cli():
    """A set of utilities for working with legion on the commandline"""


@cli.command()  # @cli, not @click!
@click.argument('exchange')
@click.option('-r', '--routing-key', default='#',
              help='The routing key which is used to filter messages on RobotnikMQ '
                   '(RabbitMQ) Topic exchanges. By default, will be set to # which'
                   ' will output all messages on the exchange.')
@click.option('-n', '--msg-limit', default=None, type=int,
              help='If set, this will cause the script to finish after a given number of messages '
                   'has been received.')
def watch(exchange: str, routing_key: str, msg_limit):
    """Given an exchange name, this utility will monitor all messages going through said
       exchange (subject to optional filters) and output them to STDOUT."""
    _watch(exchange, routing_key, msg_limit)
