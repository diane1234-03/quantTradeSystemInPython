# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 10:57:31 2023

@author: 11347
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor
 
This is a temporary script file.
"""
# 事件驱动的量化框架
from __future__ import annotations  # the FUTURE of annotation...hah 
from collections import defaultdict
from typing import Any, Dict, List, Callable
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from time import sleep
import logging
from threading import Thread

# 创建一个日志记录器实例
LOG = logging.getLogger(__name__)
# 控制日志消息的显示方式为：
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# 将日志输出到流的处理器
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logging.getLogger().addHandler(consoleHandler)
LOG.setLevel(logging.DEBUG)

# 事件类型
# Basic Data Types
class EventType(Enum):
    BAR = "BAR"
    #提交订单事件
    ORDER_CREATE = "ORDER_CREATE"
    #执行订单后的返回事件。
    TRADE = "TRADE"


@dataclass(frozen=True)
class Event:
    type: EventType
    # payload：时间载荷。
    payload: Any  # this could be a enum as well

# 3. I need a Bar, so I wrote a Bar dataclasses? 
# Why dataclass?
@dataclass(frozen=True)
class Bar:
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: datetime


# 1.  I create engine...
class Engine:

    def __init__(self, bus: EventBus, strategy: Strategy, feed: DataFeed):
        self.bus = bus
        self.strategy = strategy
        self.feed = feed

    def run(self):
        # subs
        bus.subscribe(EventType.BAR, self.strategy.on_bar)
        self.bus.start()
        self.feed.start()
        
        while True:
            sleep(0.05)


class EventBus:

    def __init__(self, sample_freq: float=0.2):
        # TODO: Could be a priority queue
        self.topics: Dict[EventType, List[Callable]] = defaultdict(list)  
        # 用于缓存推到总线的事件。
        self.events: List[Event] = list()
        self.sample_freq = sample_freq
        # 多线程：内部有自己的线程。线程内运行的函数为blocking_run方法。
        self.thread = Thread(target=self.blocking_run)
    
    # 订阅
    def subscribe(self, event_type: EventType, callback: Callable):
        LOG.debug(f"Subscribe {event_type} with {callback}")
        self.topics[event_type].append(callback)  # TODO: could be duplicated callbacks.
    # 将事件推送给事件总线。
    def push(self, event: Event):
        self.events.append(event)

    def blocking_run(self):
        """ blocking run """
        while True:
            while self.events:
                # 当存在事件时就处理。
                event = self.events.pop()
                _callables = self.topics[event.type]
                for _callable in _callables:
                    _callable(event.payload)
            
            sleep(self.sample_freq)  # sample frequency to avoid throttling the CPU.

    def start(self):
        """ Async run """
        LOG.info(f"EventBus thread starting...")
        self.thread.start()

    def stop(self):
        self.thread.join()


class DataFeed(ABC):

    # a interface
    @abstractmethod
    def start(self):
        ...



# push a bar to the event bus every 2 seconds
class DummyBarFeed(DataFeed):
    # Does Bar feed needs to know EventBus?

    def __init__(self, bus: EventBus) -> None:
        self.bus = bus
        # 线程内运行的即为run函数。
        self.thread = Thread(target=self._run)

    def start(self):
        # 添加日志
        LOG.info(f"{self} thread starting...")
        # 开始运行该线程
        self.thread.start()
    # 运行逻辑：每隔两秒钟生成一个bar数据，并作为载荷生成一个事件实例。
    # 最后将实例推送给事件总线。
    def _run(self):
        while True:
            sleep(2)
            bar = Bar(
                open=100,
                high=200,
                low=100,
                close=100,
                volume=20000,
                timestamp=datetime.now()
            )
            event = Event(
                type=EventType.BAR,
                payload=bar
            )
            LOG.debug(f"DummyBarFeed pushed {event}")
            self.bus.push(event)


# 2. I write down strategy class
class Strategy:

    def on_bar(self, bar: Bar):
        latency = datetime.now() - bar.timestamp
        LOG.info(f"Strategy reveived {bar} with latency {latency.microseconds / 1000} ms")
        LOG.info(f"Computing some fancy signal ...")

        

if __name__ == "__main__":
    
    LOG.debug("Tesing EventBus")
    bus = EventBus(sample_freq=0.05)
    strat = Strategy()
    feed = DummyBarFeed(bus)
    engine = Engine(bus, strategy=strat, feed=feed)

    engine.run()
