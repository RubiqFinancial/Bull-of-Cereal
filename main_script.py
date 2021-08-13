import pandas as pd
import numpy as np
import bybit_fn
import binance_fn
from binance.client import Client
import bybit
import os
import config_file
import time

while True:
    try:
        # load orders
        if os.path.exists("order_details.csv"):
            try:
                orders = pd.read_csv("order_details.csv")
            except:
                time.sleep(1)
                orders = pd.read_csv("order_details.csv")
            for i in range(orders.shape[0]):
                exchange = orders['Exchange'].iloc[i]
                cancel_all = orders["CancelAllOpenOrders"].iloc[i]
                account = orders['Account'].iloc[i]
                symbol = orders['Symbol'].iloc[i]
                ordertype = orders['OrderType'].iloc[i]
                oco_order = orders['Oco'].iloc[i]
                side = orders['Side'].iloc[i]
                price = orders['Price'].iloc[i]
                quantity = orders['Quantity'].iloc[i]
                trigger_price = orders['TriggerPrice'].iloc[i]
                base_price = orders['BasePrice'].iloc[i]
                trigger_by = orders['Trigger_by'].iloc[i]
                take_profit_price = orders['TakeProfitPrice'].iloc[i]
                stop_loss_price = orders['StopLossPrice'].iloc[i]
                reduce_only = orders['ReduceOnly'].iloc[i]
                tif_binance = {"GoodTillCancel": "GTC", "ImmediateOrCancel": "IOC", "FillOrKill": "FOK",
                               "PostOnly": "GTX"}
                tif = tif_binance[orders['TimeInForce'].iloc[i]]
                close_on_trigger = orders['CloseOnTrigger'].iloc[i]
                close_position = orders['ClosePosition'].iloc[i]
                working_type = orders['WorkingType'].iloc[i]
                price_protect = orders['PriceProtect'].iloc[i]


                if exchange == 'binance':
                    client = Client(api_key=config_file.accounts['binance'][account]['api_key'],
                                    api_secret=config_file.accounts['binance'][account]['api_secret'])
                    if orders['ModifyLeverageType'].iloc[i] == True:
                        binance_fn.change_margin(client, symbol, orders['LeverageType'])
                    if orders['ModifyLeverage'].iloc[i]:
                        binance_fn.change_leverage(client, symbol, orders['Leverage'])
                    if cancel_all:
                        binance_fn.cancel_all_orders(client, symbol)
                    resp = {}
                    if orders['status'].iloc[i] == 'unplaced':
                        if ordertype == 'LIMIT':
                            if side == "Buy":
                                resp = binance_fn.place_limit_buy_order(client=client, symbol=symbol, price=price,
                                                                        qty=quantity, reduceOnly=reduce_only, tif=tif)
                            if side == "Sell":
                                resp = binance_fn.place_limit_sell_order(client=client, symbol=symbol, price=price,
                                                                 qty=quantity, reduceOnly=reduce_only, tif=tif)
                        elif ordertype == 'STOP_LIMIT':
                            if side == "Buy":
                                resp = binance_fn.place_stop_limit_buy_order(client=client, symbol=symbol, price=price, qty=quantity, trigger=stop_loss_price,
                                        reduceOnly=reduce_only, workingType=working_type, priceProtect=price_protect)
                            if side == "Sell":
                                resp = binance_fn.place_stop_limit_sell_order(client=client, symbol=symbol, price=price, qty=quantity, trigger=stop_loss_price,
                                        reduceOnly=reduce_only, workingType=working_type, priceProtect=price_protect)
                        elif ordertype == 'TAKE_PROFIT_LIMIT':
                            if side == "Buy":
                                resp = binance_fn.place_take_profit_limit_buy_order(client=client, symbol=symbol, price=price, qty=quantity, trigger=take_profit_price,
                                        reduceOnly=reduce_only, workingType=working_type, priceProtect=price_protect)
                            if side == "Sell":
                                resp = binance_fn.place_take_profit_limit_sell_order(client=client, symbol=symbol, price=price, qty=quantity, trigger=take_profit_price,
                                        reduceOnly=reduce_only, workingType=working_type, priceProtect=price_protect)
                        elif ordertype == 'MARKET':
                            if side == "Buy":
                                resp = binance_fn.place_market_buy_order(client=client, symbol=symbol, qty=quantity, reduceOnly=reduce_only)
                            if side == "Sell":
                                resp = binance_fn.place_market_sell_order(client=client, symbol=symbol, qty=quantity, reduceOnly=reduce_only)
                        elif ordertype == 'STOP_MARKET':
                            if side == "Buy":
                                resp = binance_fn.place_stop_buy_order(client=client, symbol=symbol, price=stop_loss_price, qty=quantity,
                                        reduceOnly=reduce_only, workingType=working_type, priceProtect=price_protect, closePosition=close_position)
                            if side == "Sell":
                                resp = binance_fn.place_stop_sell_order(client=client, symbol=symbol, price=stop_loss_price, qty=quantity,
                                        reduceOnly=reduce_only, workingType=working_type, priceProtect=price_protect, closePosition=close_position)
                        elif ordertype == 'TAKE_PROFIT_MARKET':
                            if side == "Buy":
                                resp = binance_fn.place_take_profit_buy_order(client=client, symbol=symbol, price=take_profit_price, qty=quantity,
                                        reduceOnly=reduce_only, workingType=working_type, priceProtect=price_protect, closePosition=close_position)
                            if side == "Sell":
                                resp = binance_fn.place_take_profit_sell_order(client=client, symbol=symbol, price=take_profit_price, qty=quantity,
                                        reduceOnly=reduce_only, workingType=working_type, priceProtect=price_protect, closePosition=close_position)
                        time.sleep(0.1)
                        # new order is a market order
                        if len(resp) > 0:
                            order_details = binance_fn.get_order_status(client, symbol, resp["orderId"])
                            if oco_order == False:
                                orders['orderid'].iloc[i] = order_details["orderId"]
                                orders['status'].iloc[i] = order_details["status"]
                            else:
                                orders['orderid'].iloc[i] = order_details["orderId"]
                                orders['status'].iloc[i] = "active"
                    if orders['status'].iloc[i] == 'active':
                        order_details = binance_fn.get_order_status(client, symbol, resp["orderId"])
                        if order_details['status'] == "FILLED":
                            orders['status'].iloc[i] = 'brackets_active'
                            if side == "Buy":
                                resp = binance_fn.place_take_profit_sell_order(client=client, symbol=symbol,
                                price=take_profit_price, qty=quantity, reduceOnly=reduce_only, workingType=working_type,
                                priceProtect=price_protect, closePosition=close_position)
                                orders['take_profit_orderid'].iloc[i] = resp["orderId"]
                                resp = binance_fn.place_stop_sell_order(client=client, symbol=symbol,
                                price=stop_loss_price, qty=quantity, reduceOnly=reduce_only, workingType=working_type,
                                priceProtect=price_protect, closePosition=close_position)
                                orders['stop_orderid'].iloc[i] = resp["orderId"]
                            if side == "Sell":
                                resp = binance_fn.place_take_profit_buy_order(client=client, symbol=symbol,
                                price=take_profit_price, qty=quantity, reduceOnly=reduce_only, workingType=working_type,
                                priceProtect=price_protect, closePosition=close_position)
                                orders['take_profit_orderid'].iloc[i] = resp["orderId"]
                                resp = binance_fn.place_stop_buy_order(client=client, symbol=symbol,
                                price=stop_loss_price, qty=quantity, reduceOnly=reduce_only, workingType=working_type,
                                priceProtect=price_protect, closePosition=close_position)
                                orders['stop_orderid'].iloc[i] = resp["orderId"]
                    if orders['status'].iloc[i] == 'brackets_active':
                        stop_order_details = binance_fn.get_order_status(client, symbol,orders['take_profit_orderid'].iloc[i])
                        take_profit_order_details = binance_fn.get_order_status(client, symbol, orders['stop_orderid'].iloc[i])
                        if stop_order_details['status'].iloc[i] == "FILLED":
                            binance_fn.cancel_order(client, symbol,orders['take_profit_orderid'].iloc[i])
                            orders['status'].iloc[i] = "Inactive"
                        elif take_profit_order_details['status'].iloc[i] == "FILLED":
                            binance_fn.cancel_order(client, symbol, orders['stop_orderid'].iloc[i])
                            orders['status'].iloc[i] = "Inactive"
                elif exchange == 'bybit':
                    client = bybit.bybit(test=True, api_key=config_file.accounts['bybit'][account]['api_key'],
                                         api_secret=config_file.accounts['bybit'][account]['api_secret'])

                    if cancel_all:
                        bybit_fn.cancel_ip_all_orders(client, symbol)
                        bybit_fn.cancel_ip_all_conditional_orders(client, symbol)
                    resp = {}
                    if orders['status'].iloc[i] == 'unplaced' and oco_order is False:
                        if ordertype == 'LIMIT':
                            if side == "Buy":
                                resp = bybit_fn.place_ip_limit_buy(client=client, symbol=symbol, price=price,
                                        qty=quantity, reduce_only=reduce_only, tif=tif, close_on_trigger=close_on_trigger)
                            if side == "Sell":
                                resp = bybit_fn.place_ip_limit_sell(client=client, symbol=symbol, price=price,
                                        qty=quantity, reduce_only=reduce_only, tif=tif, close_on_trigger=close_on_trigger)
                        elif ordertype == 'STOP_LIMIT':
                            if side == "Buy":
                                resp = bybit_fn.place_ip_limit_buy_conditional_order(client=client, symbol=symbol, price=price,
                                    qty=quantity, base_price=base_price, stop_price=stop_loss_price, tif = "GoodTillCancel", close_on_trigger = False)
                            if side == "Sell":
                                resp = bybit_fn.place_ip_limit_sell_conditional_order(client=client, symbol=symbol, price=price,
                                    qty=quantity, base_price=base_price, stop_price=stop_loss_price, tif = "GoodTillCancel", close_on_trigger = False)
                        elif ordertype == 'TAKE_PROFIT_LIMIT':
                            if side == "Buy":
                                resp = bybit_fn.place_ip_limit_buy_conditional_order(client=client, symbol=symbol, price=price,
                                    qty=quantity, base_price=base_price, stop_price=take_profit_price, tif = "GoodTillCancel", close_on_trigger = False)
                            if side == "Sell":
                                resp = bybit_fn.place_ip_limit_sell_conditional_order(client=client, symbol=symbol, price=price,
                                    qty=quantity, base_price=base_price, stop_price=take_profit_price, tif = "GoodTillCancel", close_on_trigger = False)
                        elif ordertype == 'MARKET':
                            if side == "Buy":
                                resp = bybit_fn.place_ip_market_buy(client=client, symbol=symbol, qty=quantity, reduce_only=reduce_only, close_on_trigger=close_on_trigger)
                            if side == "Sell":
                                resp = bybit_fn.place_ip_market_sell(client=client, symbol=symbol, qty=quantity, reduce_only=reduce_only, close_on_trigger=close_on_trigger)
                        elif ordertype == 'STOP_MARKET':
                            if side == "Buy":
                                resp = bybit_fn.place_ip_market_buy_conditional_order(client=client, symbol=symbol,
                                    qty=quantity, base_price=base_price, stop_price=stop_loss_price, tif = "GoodTillCancel", close_on_trigger = False)
                            if side == "Sell":
                                resp = bybit_fn.place_ip_market_sell_conditional_order(client=client, symbol=symbol,
                                    qty=quantity, base_price=base_price, stop_price=stop_loss_price, tif = "GoodTillCancel", close_on_trigger = False)
                        elif ordertype == 'TAKE_PROFIT_MARKET':
                            if side == "Buy":
                                resp = bybit_fn.place_ip_market_buy_conditional_order(client=client, symbol=symbol,
                                    qty=quantity, base_price=base_price, stop_price=take_profit_price, tif = "GoodTillCancel", close_on_trigger = False)
                            if side == "Sell":
                                resp = bybit_fn.place_ip_market_sell_conditional_order(client=client, symbol=symbol,
                                    qty=quantity, base_price=base_price, stop_price=take_profit_price, tif = "GoodTillCancel", close_on_trigger = False)
                        time.sleep(0.1)
                        if len(resp) > 0:
                            orders['status'].iloc[i] = "placed"
                    if orders['status'].iloc[i] == 'unplaced' and oco_order is True:
                        if ordertype == 'LIMIT':
                            if side == "Buy":
                                resp = bybit_fn.place_ip_limit_buy_oco(client=client, symbol=symbol, price=price,
                                        qty=quantity, reduce_only=reduce_only, tif=tif, close_on_trigger=close_on_trigger,
                                        tp_price=take_profit_price, sl_price=stop_loss_price)
                            if side == "Sell":
                                resp = bybit_fn.place_ip_limit_sell_oco(client=client, symbol=symbol, price=price,
                                        qty=quantity, reduce_only=reduce_only, tif=tif, close_on_trigger=close_on_trigger,
                                        tp_price=take_profit_price, sl_price=stop_loss_price)
                        elif ordertype == 'MARKET':
                            if side == "Buy":
                                resp = bybit_fn.place_ip_market_buy_oco(client=client, symbol=symbol, qty=quantity,
                                                        reduce_only=reduce_only, close_on_trigger=close_on_trigger,
                                                        tp_price=take_profit_price, sl_price=stop_loss_price)
                            if side == "Sell":
                                resp = bybit_fn.place_ip_market_sell_oco(client=client, symbol=symbol, qty=quantity,
                                                reduce_only=reduce_only, close_on_trigger=close_on_trigger,
                                                tp_price=take_profit_price, sl_price=stop_loss_price)
                        time.sleep(0.1)
                        if len(resp) > 0:
                            orders['status'].iloc[i] = "placed"

                orders.to_csv("order_details.csv", index=False)

        time.sleep(5)
    except Exception as ex:
        print(ex)
        time.sleep(10)
        continue
