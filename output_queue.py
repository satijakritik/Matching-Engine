from collections import deque
from order import Order
from trade import Trade

class OutputQueue:
    def __init__(self):
        self.queue = deque()

    def send_acknowledgment(self, order: Order):
        acknowledgment_message = f"Acknowledgment: Order {order.order_id} received and stored."
        self.queue.append(acknowledgment_message)

    def send_trade_message(self, trade: Trade):
        self.queue.append(trade) 

    def get_message(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return None

    def __len__(self):
        return len(self.queue)

    def __repr__(self):
        return f"Output Queue: {self.queue}"