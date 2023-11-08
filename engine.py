from __future__ import annotations


# 事件驱动的量化框架

from time import sleep
import logging
from threading import Thread

from model import Event, EventType, Bar, Order, OrderType, Asset, AssetType
from bus_and_engine import EventBus
from strategy import Strategy
from data_feed import DataFeed,DummyBarFeed
from execution import Execution,DummyExecution

# 创建一个日志记录器实例
LOG = logging.getLogger(__name__)
# 控制日志消息的显示方式为：
logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)
# 将日志输出到流的处理器
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logging.getLogger().addHandler(consoleHandler)
LOG.setLevel(logging.DEBUG)

# 创建一个日志记录器实例
LOG = logging.getLogger(__name__)


# 1.  I create engine...
class Engine:
    def __init__(self, bus: EventBus, strategy: Strategy, feed: DataFeed):
        self.bus = bus
        self.strategy = strategy
        self.feed = feed

    def __init__(
        self, bus: EventBus, strategy: Strategy, feed: DataFeed, execution: Execution
    ):
        self.bus = bus
        self.strategy = strategy
        self.feed = feed
        self.execution = execution

    def run(self):
        # subs
        # 订阅事件，并决定事件的回调函数，例如bar事件，回调函数为on bar。
        self.bus.subscribe(EventType.BAR, self.strategy.on_bar)
        self.bus.start()
        self.feed.start()

        while True:
            sleep(0.05)

if __name__ == "__main__":
    LOG.debug("Tesing EventBus")
    bus = EventBus(sample_freq=0.05)
    strat = Strategy(bus)
    execution = DummyExecution(bus)
    feed = DummyBarFeed(bus)
    engine = Engine(bus, strategy=strat, feed=feed,execution=execution)
    

    engine.run()
