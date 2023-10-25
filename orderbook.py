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
        if order.order_id in self.order_map:
            self.order_map[order.order_id].quantity = 0
            if order.side == 'buy':
                self.bids.discard(order)
            else:
                self.asks.discard(order)
        else:
            raise ValueError(f"Invalid order ID {order.order_id}.")

    def create_df(self):
        data = {
            "Ask_id": [],
            "Ask_p": [],
            "Ask_q": [],
            "Bid_id": [],
            "Bid_p": [],
            "Bid_q": [],
        }

        for ask in self.asks[self.depth::-1]:
            data["Ask_id"].append(ask.order_id)
            data["Ask_p"].append(ask.price)
            data["Ask_q"].append(ask.quantity)

        for bid in self.bids[self.depth::-1]:
            data["Bid_id"].append(bid.order_id)
            data["Bid_p"].append(bid.price)
            data["Bid_q"].append(bid.quantity)

        df = pd.DataFrame(data)
        return df

    def get_instrument(self):
        return self.instrument
      
    def get_bids(self):
        return self.bids

    def get_asks(self):
        return self.asks
    
    def get_matching_asks(self, price):
        return [ask for ask in self.asks if ask.price <= price]

    def get_matching_bids(self, price):
        return [bid for bid in self.bids if bid.price >= price]

    def __repr__(self):
        lines = []
        lines.append("-"*10 + f" OrderBook ({self.instrument}) " + "-"*10)
        lines.append("\nAsks:")
        lines.append("Order ID\tPrice\tQuantity")
        
        for ask in self.asks[self.depth::-1]:
            lines.append(str(ask.order_id) + "\t\t" + str(ask))
        
        lines.append("\nBids:")
        lines.append("Order ID\tPrice\tQuantity")
        
        for bid in self.bids[self.depth::-1]:
            lines.append(str(bid.order_id) + "\t\t" + str(bid))
            
        lines.append("-"*34 + "-" * len(self.instrument))
        return "\n".join(lines)

