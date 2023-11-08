from __future__ import annotations


# 事件驱动的量化框架

from collections import defaultdict
from typing import Any, Dict, List, Callable

from time import sleep
import logging
from threading import Thread


from model import Event, EventType, Bar, Order, OrderType, Asset, AssetType

from bus_and_engine import EventBus
from strategy import Strategy
from data_feed import DataFeed,DummyBarFeed
from execution import Execution,DummyExecution

# 2. I write down strategy class
class Strategy:
    def __init__(self, bus: EventBus):
        self.bus = bus

    def on_bar(self, bar: Bar):
        latency = datetime.now() - bar.timestamp
        LOG.info(
            f"Strategy reveived {bar} with latency {latency.microseconds / 1000} ms"
        )
        LOG.info(f"Computing some fancy signal ...")
        LOG.info(f"submiting order...")
        
        self.submit_order()

    def submit_order(self):
        order = Order(
            asset=Asset(AssetType.CASH, name="Bitcoin"),
            type=OrderType.MARKET,
            price=-1,
            amount=1.0,
        )
        event = Event(EventType.ORDER_CREATE, payload=order)
        self.bus.push(event)
