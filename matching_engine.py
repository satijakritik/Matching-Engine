from orderbook import OrderBook
from order import Order
from output_queue import OutputQueue
from trade import Trade

class MatchingEngine:
    def __init__(self, orderbooks: OrderBook, output_queue: OutputQueue):
        self.orderbooks = orderbooks
        self.trades = {}
        self.output_queue = output_queue
        
    def find_matching_orders(self, incoming_order: Order):
        instrument = incoming_order.instrument

        matching_orders = []

        if instrument in self.orderbooks:
            order_book = self.orderbooks[instrument]

            # Find matching orders in order book
            if incoming_order.side == 'buy':
                matching_orders = order_book.get_asks()
                matching_orders = [
                order for order in reversed(matching_orders) if order.price <= incoming_order.price
            ]
                
            elif incoming_order.side == 'sell':
                matching_orders = order_book.get_bids()
                matching_orders = [
                order for order in reversed(matching_orders) if order.price >= incoming_order.price
            ]
                
            else:
                raise ValueError("Order side should be 'buy' or 'sell")

        return matching_orders

    def execute_trade(self, incoming_order: Order, matching_order: Order):
        orderbook = self.orderbooks[incoming_order.instrument]
        
        if incoming_order.instrument not in self.trades:
            self.trades[incoming_order.instrument] = []
            
        trade_quantity = min(incoming_order.quantity, matching_order.quantity)
        
        trade = Trade(incoming_order.side, matching_order.price, trade_quantity, incoming_order.order_id, matching_order.order_id)
        self.output_queue.send_trade_message(trade)
        self.trades[incoming_order.instrument].append(trade)
        
        if incoming_order.quantity == matching_order.quantity:
            # Both orders completely match.
            orderbook.remove_order(incoming_order)
            orderbook.remove_order(matching_order)
            
        elif incoming_order.quantity < matching_order.quantity:
            # incoming_order partially filled by matching_order.
            matching_order.quantity -= incoming_order.quantity
            orderbook.remove_order(incoming_order)
            
        else:
            # matching_order partially filled by incoming_order.
            incoming_order.quantity -= matching_order.quantity
            orderbook.remove_order(matching_order)
            
    def process_order(self, incoming_order: Order):
        instrument = incoming_order.instrument

        matching_orders = self.find_matching_orders(incoming_order)
        
        if incoming_order.quantity > 0:
            order_book = self.orderbooks[instrument]
            order_book.add_order(incoming_order)

        self.output_queue.send_acknowledgment(incoming_order)

        for matching_order in matching_orders:
            if incoming_order.quantity == 0:
                break

            if matching_order.quantity == 0:
                continue
            
            self.execute_trade(incoming_order, matching_order)
        
    def cancel_order(self, instrument: str, order_id: int):
        orderbook = self.orderbooks[instrument]
        
        if orderbook.order_map[order_id].quantity == 0:
            return
        
        order = orderbook.order_map[order_id]
        orderbook.remove_order(order)
        
    def retrieve_trades(self, instrument: str):
        return self.trades[instrument]