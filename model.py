
from __future__ import annotations 

#此文件为数据类型

# 事件驱动的量化框架
# the FUTURE of annotation...hah 
from collections import defaultdict
from typing import Any, Dict, List, Callable
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from time import sleep
import logging
from threading import Thread

# 事件类型
# Basic Data Types
class EventType(Enum):
    # 事件类型，可以是bar数据，可以是停缴订单，可以的订单执行后的确认事件
    BAR = "BAR"
    ORDER_CREATE = "ORDER_CREATE"
    TRADE = "TRADE"

@dataclass(frozen=True)
class Event:
    # 一个事件由事件类型和事件载荷组成
    type: EventType
    payload: Any  # this could be a enum as well

class AssetType(Enum):
    CASH = "cash"


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


# 继承enum类
class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "MARKET"
    STOP = "STOP"
    




@dataclass
class Asset:
    type:AssetType 
    name:str

@dataclass(frozen = True, slots = True)
class Order: 
    asset: Asset 
    type:OrderType 
    price:float 
    amount:float 
    

# 一个订单可能对应多次交易
@dataclass(frozen=True, slots= True)
class Trade:
    order_id:int 
    amount:float
    price:float 
    








