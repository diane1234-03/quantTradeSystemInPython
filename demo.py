# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 16:20:46 2023

@author: 11347
"""

from model import EventBus,Strategy,DummyBarFeed,DummyExecution,Engine
from model import Event,EventType,Bar,Order,OrderType,Asset,AssetType


if __name__ == "__main__":
    
    
    bus = EventBus(sample_freq=0.05)
    strat = Strategy(bus)
    execution = DummyExecution(bus)
    feed = DummyBarFeed(bus)
    engine = Engine(bus, strategy=strat, feed=feed,execution=execution)
    

    engine.run()
