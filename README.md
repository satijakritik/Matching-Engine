# Matching-Engine

An order matching engine implementation that can process buy and sell orders for different instruments (BTC/ETH/USDT). 
The matching engine receives all incoming orders through an input queue and stores them in an order book based on their instrument and price. 
After an order is successfully stored in the order book, an acknowledgment message is sent to an output queue.

When a new order arrives, the matching engine checks if it can be matched with any existing orders in the order book based on their price and instrument. 
If a match is found, the orders are executed, and trade messages are be sent to the output queue. The residual quantities of the orders are updated in the order book.
The program supports the following operations:
1. Place a new buy or sell order with a specified instrument and quantity at a given price.
2. Retrieve the current order book for a specific instrument.
3. Retrieve the executed trades for a specific instrument.
4. Cancel an existing order.

## Setup

1. Unzip the Matching-Engine folder
2. Open a terminal window and create a virtual environment using `conda create -n <env-name>`
3. Activate the environment using `conda activate <env-name>`, and install pip with `conda install pip`
4. Install the required packages using `pip install -r requirements.txt`
5. Run the program using `python main.py`

## While running the program

The matching-engine has 2 input modes that the user can run, i.e. `Command Line` and `File`. Input 0 for Command Line, or 1 for File input. For the file input, 
place the input file inside `file_input` directory. Three example input files have been placed there already. 

Commands for Command Line mode:
```
buy INSTRUMENT PRICE QUANTITY (Places a limit BUY order for INSTRUMENT QUANTITY at PRICE)
sell INSTRUMENT PRICE QUANTITY (Places a limit SELL order for INSTRUMENT QUANTITY at PRICE)
cancel INSTRUMENT ORDER_ID (CANCELS INSTRUMENT order with ORDER_ID)
orderbook INSTRUMENT (Retrieves the ORDERBOOK for INSTRUMENT)
trades INSTRUMENT (Retrieves the TRADES for INSTRUMENT)
help (Displays all the commands and their usage)
exit (EXITS the program)
```

For using File input, enter `<input_file_name>`; the orderbook output will get stored in `file_output` directory in the .csv file 
named `<input_file_name>_<instrument>_orderbook.csv`

## Assumptions

1. The orderID is unique for the orderbook of every instrument (and not unique for all instruments). This means that a BTC/USDT orderbook and ETH/USDT orderbook can have an order with the same orderID
2. The orderbook displays the top 5 bids and top 5 asks. To change this, update the value of the `depth` field in the Orderbook class
3. The program has not been dockerized, and may not work on all systems. It has been tested on the 2.4 GHz Quad-Core Intel Core i5 2019 MacBook Pro.
4. Large volume of orders has been assumed to be ~20,000 orders. The file `input_test_3.txt` has ~20,000 orders and runs in ~1.8s. Thus, it takes ~90μs for processing an order.
