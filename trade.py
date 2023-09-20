from time import time

from datetime import datetime

class Trade(object):
	def __init__(self, incoming_side: str, price: float, trade_quantity: int, incoming_order_id: int, book_order_id: int):
		self.timestamp = time()
		self.side = incoming_side
		self.price = price
		self.quantity = trade_quantity
		self.incoming_order_id = incoming_order_id
		self.book_order_id = book_order_id

	def __repr__(self):
		return f'({datetime.fromtimestamp(self.timestamp)}) Executed: {"BUY" if self.side == "B" else "SELL"} {self.quantity} units at {self.price}'