from orderbook import OrderBook
from order import Order
from output_queue import OutputQueue
from trade import Trade
from collections import defaultdict

class MatchingEngine:
    def __init__(self, orderbooks: OrderBook, output_queue: OutputQueue):
        self.orderbooks = orderbooks
        self.trade_history = defaultdict(list)
        self.output_queue = output_queue

    def find_matching_orders(self, incoming_order: Order):
        instrument = incoming_order.instrument
        matching_orders = []

        if instrument in self.orderbooks:
            order_book = self.orderbooks[instrument]

            if incoming_order.side == 'buy':
                matching_orders = order_book.get_matching_asks(incoming_order.price)
            elif incoming_order.side == 'sell':
                matching_orders = order_book.get_matching_bids(incoming_order.price)

        return matching_orders

    def execute_trade(self, incoming_order: Order, matching_order: Order):
        order_book = self.orderbooks[incoming_order.instrument]
        trade_quantity = min(incoming_order.quantity, matching_order.quantity)

        trade = Trade(incoming_order.side, matching_order.price, trade_quantity, incoming_order.order_id, matching_order.order_id)
        self.output_queue.send_trade_message(trade)
        self.trade_history[incoming_order.instrument].append(trade)

        incoming_order.quantity -= trade_quantity
        matching_order.quantity -= trade_quantity

        if incoming_order.quantity == 0:
            order_book.remove_order(incoming_order)
        if matching_order.quantity == 0:
            order_book.remove_order(matching_order)

    def process_order(self, incoming_order: Order):
        instrument = incoming_order.instrument

        matching_orders = self.find_matching_orders(incoming_order)
        
        if incoming_order.quantity > 0:
            order_book = self.orderbooks[instrument]
            order_book.add_order(incoming_order)

        for matching_order in matching_orders:
            if incoming_order.quantity == 0:
                break
            if matching_order.quantity == 0:
                continue
            self.execute_trade(incoming_order, matching_order)

        self.output_queue.send_acknowledgment(incoming_order)

    def cancel_order(self, instrument: str, order_id: int):
        order_book = self.orderbooks[instrument]
        order = order_book.order_map.get(order_id)

        if order and order.quantity > 0:
            order_book.remove_order(order)

    def retrieve_trades(self, instrument: str):
        return self.trade_history[instrument]
