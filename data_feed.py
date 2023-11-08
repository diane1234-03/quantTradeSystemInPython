# import tushare as ts
import pandas as pd 
from abc import ABC, abstractmethod
from time import sleep
from threading import Thread
from datetime import datetime
import logging


from bus import EventBus
from model import Bar,EventType,Event

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
# 获取行情数据，并推送给事件总线

# 创建一个日志记录器实例
LOG = logging.getLogger(__name__)

# abc:定义自己的基类（抽象类接口），可以强制要求子类实现接口。
class DataFeed(ABC):
    # a interface
    @abstractmethod
    def start(self):
        ...

# push a bar to the event bus every 2 seconds
class DummyBarFeed(DataFeed):
    # Does Bar feed needs to know EventBus?

    def __init__(self,bus:EventBus) -> None:
        self.bus = bus
        self.file_path = "C:\cslearning\quant code\system\data\sh600001.csv"
        # 线程内运行的即为run函数。一个类有一个线程，该线程直接运行该类的功能
        self.thread = Thread(target=self._run)

    def get_price(self):
        # 读取数据
        file = pd.read_csv(self.file_path,encoding='gbk')
        df1 = pd.DataFrame(file, columns=['交易日期', '开盘价', '最高价', '最低价', '收盘价', '成交量'])
        for index,row in df1.iterrows():
            # 遍历每一行，其中，row是一个series对象。可以使用字典索引的形式获取对应列的值。 
            yield row

    def start(self):
        # 添加日志
        LOG.info(f"{self} thread starting...")
        # 开始运行该线程
        self.thread.start()

    # 运行逻辑：每隔两秒钟生成一个bar数据，并作为载荷生成一个事件实例。
    # 最后将实例推送给事件总线。
    def _run(self):
        bar_data = self.get_price()
        i = 1 
        while i<5:
            sleep(2)
            t = next(bar_data)
            print(t["交易日期"],":",t["开盘价"])
            i+=1
            bar = Bar(
                open=t['开盘价'],
                high=t['最高价'],
                low=t['最低价'],
                close=t['收盘价'],
                volume=t['成交量'],
                timestamp=datetime.now(),
            )
            event = Event(type=EventType.BAR, payload=bar)
            LOG.debug(f"DummyBarFeed pushed {event}")
            self.bus.push(event)

if __name__ == '__main__':
    bus = EventBus()
    df = DummyBarFeed(bus)
    df._run()
