from collections import deque

class InputQueue:
    def __init__(self):
        self.queue = deque()

    def send_order(self, order):
        self.queue.append(order)

    def receive_order(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return None
        
    def __len__(self):
        return len(self.queue)

    def __repr__(self):
        return f"Input Queue: {self.queue}"