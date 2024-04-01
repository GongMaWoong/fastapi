from pybitget import Client
import websocket
import json

api_key = "bg_fa752778970fc73a4b9f1cfa2f1b5538"
api_secret = "d5c3575453ffb8bb482fbdabe03e9a4bec8737161c5f87ab8b957ca8299da8cd"
api_passphrase = "WXDdugod"

# Initialize the Bitget client
client = Client(api_key, api_secret, passphrase=api_passphrase)

def place_plan_order(symbol, margin_coin, size, side, order_type, trigger_price, trigger_type, preset_take_profit_price, preset_stop_loss_price):
    plan_order_data = client.mix_place_plan_order(symbol, margin_coin, size, side, order_type, trigger_price, trigger_type, clientOid=None, presetTakeProfitPrice=preset_take_profit_price, presetStopLossPrice=preset_stop_loss_price)
    return plan_order_data

def handle_message(message):
    data = json.loads(message)
    symbol = data['symbol']
    mark_price = data['markPrice']

    # Check if mark price triggers stop loss for any order
    for order_id, order_data in order_info.items():
        if symbol == order_data['symbol'] and mark_price <= order_data['preset_stop_loss']:
            print(f"Stop loss triggered for order {order_id}. Re-entering order.")
            re_enter_order(order_data)

def re_enter_order(order_data):
    symbol = order_data['symbol']
    margin_coin = order_data['margin_coin']
    size = order_data['size']
    side = order_data['side']
    order_type = order_data['order_type']
    trigger_price = order_data['trigger_price']
    trigger_type = order_data['trigger_type']
    preset_take_profit_price = order_data['preset_take_profit_price']
    preset_stop_loss_price = order_data['preset_stop_loss_price']

    new_order_data = place_plan_order(symbol, margin_coin, size, side, order_type, trigger_price, trigger_type, preset_take_profit_price, preset_stop_loss_price)
    if isinstance(new_order_data, dict) and new_order_data.get('code') == '00000':
        print("Re-entry order successful!")
        order_info[new_order_data['data']['orderId']] = order_data
    else:
        print("Re-entry order failed. Please check the response for more details.")

# Store order information in a dictionary
order_info = {}

# Subscribe to the Bitget WebSocket for mark price updates
websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://api.bitget.com/market/v1/ws",
                            on_message=handle_message)
ws.run_forever()
