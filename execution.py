from abc import ABC,abstractmethod


class Execution(ABC):
    @abstractmethod
    def submit_order(self, order: Order) -> int:
        ...

    @abstractmethod
    def cancle_order(self, order_id: int):
        ...

    @abstractmethod
    def modify_order(self, order_id: int, order: Order):
        ...

    @abstractmethod
    def on_order_create(self, order: Order):
        ...

    @abstractmethod
    def start(self) -> int:
        ...


class DummyExecution(Execution):
    def __init__(self, bus: EventBus):
        self.bus = EventBus

    def submit_order(self, order: Order) -> int:
        return super().submit_order(order)

    def cancle_order(self, order_id: int):
        return super().cancle_order(order_id)

    def modify_order(self, order_id: int, order: Order):
        return super().modify_order(order_id, order)

    def on_order_create(self, order: Order):
        LOG.info(f"Execution received {order = }")

    def start(self) -> int:
        super().start()