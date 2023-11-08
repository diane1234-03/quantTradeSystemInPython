# 事件总线类
from typing import Any, Dict, List, Callable
from collections import defaultdict
from time import sleep
import logging
from threading import Thread
from model import Event, EventType
LOG = logging.getLogger(__name__)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logging.getLogger().addHandler(consoleHandler)
LOG.setLevel(logging.DEBUG)
class EventBus:
    def __init__(self, sample_freq: float=0.2):
        # 事件类型和对应的回调函数
        self.topics: Dict[EventType, List[Callable]] = defaultdict(list)  
        # 用于缓存推到总线的事件。
        # TODO:可以是一个消息队列
        self.events: List[Event] = list()
        # 隔多久发送一次数据
        self.sample_freq = sample_freq
        # 多线程：内部有自己的线程。线程内运行的函数为blocking_run方法。
        self.thread = Thread(target=self.blocking_run)
    
    # 订阅,将一个回调函数订阅一个事件类型。
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


