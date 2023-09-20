from sortedcontainers import SortedList
from order import Order
import pandas as pd


class OrderBook:
    def __init__(self, instrument: str):
        self.instrument = instrument
        self.order_map = {}
        self.bids = SortedList()
        self.asks = SortedList()
        self.depth = 5
        self.order_id = 1

    def add_order(self, order: Order):
        if order.side == 'buy':
            self.bids.add(order)
            self.order_map[order.order_id] = order
            self.order_id += 1
        elif order.side == 'sell':
            self.asks.add(order)
            self.order_map[order.order_id] = order
            self.order_id += 1
        else:
            raise ValueError("Invalid order side. Must be 'buy' or 'sell'.")

    def remove_order(self, order: Order):
        if order.side == 'buy' and order.order_id in [bid.order_id for bid in self.bids]:
            self.bids.discard(order)
            self.order_map[order.order_id].quantity = 0
        elif order.side == 'sell' and order.order_id in [ask.order_id for ask in self.asks]:
            self.asks.discard(order)
            self.order_map[order.order_id].quantity = 0
        else:
            raise ValueError(f"Invalid order side {order.side}. Must be 'buy' or 'sell'.")
    
    def create_df(self):
        asks = list(self.asks.copy()) if len(self.asks) < self.depth else list(self.asks.copy())[:self.depth]
        bids = list(reversed(self.bids.copy())) if len(self.bids) < self.depth else list(reversed(self.bids.copy()))[:self.depth]
        
        data = {
                "Ask_id": [ask.order_id for ask in asks],
                "Ask_p": [ask.price for ask in asks],
                "Ask_q": [ask.quantity for ask in asks],
                "Bid_id": [bid.order_id for bid in bids],
                "Bid_p": [bid.price for bid in bids],
                "Bid_q": [bid.quantity for bid in bids],
                }
        
        df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in data.items() ]))
        
        return df
        
    def get_instrument(self):
        return self.instrument
      
    def get_bids(self):
        return self.bids

    def get_asks(self):
        return self.asks

    def __repr__(self):
        lines = []
        lines.append("-"*10 + f" OrderBook ({self.instrument}) " + "-"*10)
        lines.append("\nAsks:")
        lines.append("Order ID\tPrice\tQuantity")
        asks = self.asks.copy()
        
        i = 0
        
        while len(asks) > 0 and i < self.depth:
            ask = asks.pop()
            lines.append(str(ask.order_id) + "\t\t" + str(ask))
            i += 1
        
        lines.append("\nBids:")
        lines.append("Order ID\tPrice\tQuantity")
        
        bids = list(self.bids.copy())
        
        j = 0
        
        while len(bids) > 0 and j < self.depth:
            bid = bids.pop()
            lines.append(str(bid.order_id) + "\t\t" + str(bid))
            j += 1
            
        lines.append("-"*34 + "-" * len(self.instrument))
        return "\n".join(lines)