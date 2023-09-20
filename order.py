class Order:
    def __init__(self, order_id: str, instrument: str, side: str, price: float, quantity: int):
        self.order_id = order_id
        self.instrument = instrument
        self.side = side
        self.quantity = quantity
        self.price = price
        
    def __lt__(self, other):
        if self.price != other.price:
            if self.side == "buy":
                return self.price < other.price
            else:
                return self.price > other.price
            
        elif self.order_id != other.order_id:
            return self.order_id < other.order_id
            
        elif self.quantity != other.quantity:
            return self.quantity < other.quantity

    def __repr__(self):
        return f"{self.price}\t{self.quantity}"
