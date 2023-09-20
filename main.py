from orderbook import OrderBook
from matching_engine import MatchingEngine
from input_queue import InputQueue
from output_queue import OutputQueue
from order import Order
from time import perf_counter

def main():
    orderbooks = {} 
    input_queue = InputQueue()
    output_queue = OutputQueue()
    matching_engine = MatchingEngine(orderbooks, output_queue)

    modes = ["command_line", "file"]
    
    while True:
        print("Enter a number to select the input method:\n\tCommand Line [0]\n\tFile [1]")
        num = input(">> ")
        while num not in ["0", "1"]:
            print("Invalid input. Try again")
            num = input(">> ")
        num = int(num)
        mode = modes[num]
        
        if mode == "command_line":
            commands = ["buy", "sell", "cancel", "orderbook", "trades", "help", "exit"]
            print("Commands: buy, sell, cancel, orderbook, trades, help, exit")
            while True:
                line = input(">> ").split(" ")
                cmd = line[0].lower()
                while cmd not in commands:
                    print("Command not found")
                    line = input(">> ").split(" ")
                    cmd = line[0]
                
                match cmd:
                    case "buy":
                        if len(line) != 4:
                            print("Invalid usage of 'buy' command")
                            continue
                        instrument = line[1]
                        price = float(line[2])
                        qty = int(line[3])
                        
                        if instrument not in matching_engine.orderbooks:
                            matching_engine.orderbooks[instrument] = OrderBook(instrument)
                            
                        orderbook = matching_engine.orderbooks[instrument]
                        order = Order(orderbook.order_id, instrument, 'buy', price, qty)
                        input_queue.send_order(order)
                        incoming_order = input_queue.receive_order()
                        
                        if incoming_order:
                            matching_engine.process_order(incoming_order)
                        
                    case "sell":
                        if len(line) != 4:
                            print("Invalid usage of 'sell' command")
                            continue
                        instrument = line[1]
                        price = float(line[2])
                        qty = int(line[3])
                        
                        if instrument not in matching_engine.orderbooks:
                            matching_engine.orderbooks[instrument] = OrderBook(instrument)
                            
                        orderbook = matching_engine.orderbooks[instrument]
                        order = Order(orderbook.order_id, instrument, 'sell', price, qty)
                        input_queue.send_order(order)
                        incoming_order = input_queue.receive_order()
                        
                        if incoming_order:
                            matching_engine.process_order(incoming_order)
                        
                    case "cancel":
                        if len(line) != 3:
                            print("Invalid usage of 'cancel' command")
                            continue
                        
                        instrument = line[1]
                        order_id = int(line[2])
                        matching_engine.cancel_order(instrument, order_id)
                        
                    case "orderbook":
                        if len(line) != 2:
                            print("Invalid usage of 'orderbook' command")
                            continue
                        
                        instrument = line[1]
                        if instrument in orderbooks:
                            print(orderbooks[instrument])
                        else:
                            print(f"Orderbook for {instrument} does not exist")
                        
                    case "trades":
                        if len(line) != 2:
                            print("Invalid usage of 'trades' command")
                            continue
                        
                        if instrument not in matching_engine.trades:
                            matching_engine.trades[instrument] = []
            
                        print(f"Trades: {matching_engine.trades[instrument]}")
                        
                    case "help":
                        if len(line) != 1:
                            print("Invalid usage of 'help' command")
                            continue
                        
                        print("Commands Usage: \n\tbuy INSTRUMENT PRICE QUANTITY\n\tsell INSTRUMENT PRICE QUANTITY\n\tcancel INSTRUMENT ORDER_ID\n\torderbook INSTRUMENT\n\ttrades INSTRUMENT\n\thelp\n\texit")
                    
                    case "exit":
                        if len(line) != 1:
                            print("Invalid usage of 'exit' command")
                            continue
                        
                        return
        else:
            input_file = input("Input file name (.txt):\n>> ").split(".")[0]

            with open(f"file_input/{input_file}.txt", "r") as f:
                lines = f.read().splitlines()
            
            start_time = perf_counter()
            
            for line in lines:
                line = line.split(" ")
                commands = ["buy", "sell", "cancel"]
                print(line)
                cmd = line[0].lower()
                
                if cmd not in commands:
                    print(f"Command {cmd} not found")
                    continue
                
                match cmd:
                    case "buy":
                        if len(line) != 4:
                            print("Invalid usage of 'buy' command")
                            continue
                        instrument = line[1]
                        price = float(line[2])
                        qty = int(line[3])
                        if instrument not in matching_engine.orderbooks:
                            matching_engine.orderbooks[instrument] = OrderBook(instrument)
                            
                        orderbook = matching_engine.orderbooks[instrument]
                        order = Order(orderbook.order_id, instrument, 'buy', price, qty)
                        input_queue.send_order(order)
                        incoming_order = input_queue.receive_order()
                        
                        if incoming_order:
                            matching_engine.process_order(incoming_order)
                            
                        print(matching_engine.orderbooks[instrument])
                        
                    case "sell":
                        if len(line) != 4:
                            print("Invalid usage of 'sell' command")
                            continue
                        instrument = line[1]
                        price = float(line[2])
                        qty = int(line[3])
                        if instrument not in matching_engine.orderbooks:
                            matching_engine.orderbooks[instrument] = OrderBook(instrument)
                            
                        orderbook = matching_engine.orderbooks[instrument]
                        order = Order(orderbook.order_id, instrument, 'sell', price, qty)
                        input_queue.send_order(order)
                        incoming_order = input_queue.receive_order()
                        
                        if incoming_order:
                            matching_engine.process_order(incoming_order)
                            
                        print(matching_engine.orderbooks[instrument])
                        
                    case "cancel":
                        if len(line) != 3:
                            print("Invalid usage of 'cancel' command")
                            continue
                        
                        instrument = line[1]
                        order_id = int(line[2])
                        matching_engine.cancel_order(instrument, order_id)
                        print(matching_engine.orderbooks[instrument])
            
            end_time = perf_counter()
            
            for instrument, orderbook in matching_engine.orderbooks.items():
                updated_instrument = "_".join(instrument.split("/")) # eg. BTC/USDT to BTC_USDT
                output_file = f"file_output/{input_file}_{updated_instrument}_orderbook.csv"
                
                df = orderbook.create_df()
                
                if instrument not in matching_engine.trades:
                    matching_engine.trades[instrument] = []
                
                print()
                print(instrument)
                print(df.head())
                print()
                print(f"Trades: {matching_engine.trades[instrument]}")
                print()
                    
                with open(output_file, "w+") as f:
                    df.to_csv(f)
                    
            print()
            print(f"Time taken: {end_time - start_time}s")
            print(f"Number of orders executed = {len(lines)}")
            
            print(f"Time taken per order = {(end_time - start_time) / len(lines)}s")
            print()
                    

if __name__ == "__main__":
    main()