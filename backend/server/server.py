from flask import Flask, jsonify
from backend.functions.event_db_manager import EventDatabaseManager
from backend.functions.portfolio_db_manager import PortfolioDatabaseManager
from user_endpoints import create_new_account, login, get_all_users_info, change_password
from portfolio_endpoints import create_new_portfolio, delete_portfolio, add_stock_to_portfolio,\
    remove_stock_from_portfolio, get_all_user_portfolios
from stats_endpoints import get_single_stat, get_all_stats
from stock_endpoints import get_stock_info, get_all_stocks

app = Flask(__name__)


@app.route('/alive', methods=['GET'])
def alive():
    return jsonify({'message': 'alive'}), 200


# ------ user endpoints ------
app.route('/create-new-account', methods=['POST'])(create_new_account)


app.route('/login', methods=['POST'])(login)


app.route('/get-all-users-info', methods=['GET'])(get_all_users_info)


app.route('/change-password', methods=['POST'])(change_password)


# ------- stocks endpoints -------
app.route('/get-all-stocks', methods=['GET'])(get_all_stocks)


app.route('/get-stock-info', methods=['GET'])(get_stock_info)
# def get_stock_info():
#     curr_datetime = datetime.now()
#     data = request.json
#     date = datetime(2024, 5, 20)
#     if 'username' not in data or 'stock_name' not in data:
#         return jsonify({'error': 'Missing required fields'}), 400
#     else:
#         stock_manager = StockManager()
#         df, shape = stock_manager.get_stock_data_by_date(data['stock_name'], date.time())
#         print(df)


# ------- event test -----
@app.route('/get-all-events', methods=['GET'])
def get_all_events():
    events_db_manager = EventDatabaseManager()
    data = events_db_manager.get_all_events()
    print(data)
    print(type(data))
    return jsonify({'message': 'test'}), 200


# ------- portfolio endpoints -------
@app.route('/get-all-portfolios', methods=['GET'])
def get_all_portfolios():
    port_manager = PortfolioDatabaseManager()
    data = port_manager.get_all_portfolios()
    print(data)
    return jsonify({'message': 'test'}), 200


app.route('/create-new-portfolio', methods=['POST'])(create_new_portfolio)

app.route('/delete-portfolio', methods=['DELETE'])(delete_portfolio)

app.route('/add-stock-to-portfolio', methods=['POST'])(add_stock_to_portfolio)
# def add_stock_to_portfolio():
#     curr_datetime = datetime.now()
#     data = request.json
#     if 'username' not in data or 'portfolio_id' not in data or 'stock_id' not in data:
#         return jsonify({'error': 'Missing required fields'}), 400
#     else:
#         portfolio_manager = PortfolioDatabaseManager()
#         if not portfolio_manager.is_username_and_portfolio_name_exists(data['username'], data['portfolio_id']):
#             return jsonify({'error': 'portfolio id not found for this user'}), 404
#
#         portfolio_manager.add_new_stock_to_portfolio(data['username'], data['portfolio_id'], data['stock_id'])
#         event_db_manager = EventDatabaseManager()
#         event_db_manager.insert_raw_action('add stock to portfolio', curr_datetime,
#                                            data['username'], {'port_id': data['portfolio_id'],
#                                                               'stock_id': data['stock_id']})
#         return jsonify({'message': 'successfully added stock to portfolio'}), 200


app.route('/remove-stock-from-portfolio', methods=['POST'])(remove_stock_from_portfolio)
# def remove_stock_from_portfolio():
#     curr_datetime = datetime.now()
#     data = request.json
#     if 'username' not in data or 'portfolio_id' not in data or 'stock_id' not in data:
#         return jsonify({'error': 'Missing required fields'}), 400
#     else:
#         portfolio_manager = PortfolioDatabaseManager()
#         if not portfolio_manager.is_username_and_portfolio_name_exists(data['username'], data['portfolio_id']):
#             return jsonify({'error': 'portfolio id not found for this user'}), 404
#
#         portfolio_manager.remove_stock_from_portfolio(data['username'], data['portfolio_id'], data['stock_id'])
#         event_db_manager = EventDatabaseManager()
#         event_db_manager.insert_raw_action('removed stock from portfolio', curr_datetime,
#                                            data['username'], {'port_id': data['portfolio_id'],
#                                                               'stock_id': data['stock_id']})
#         return jsonify({'message': 'successfully removed stock from portfolio'}), 200
app.route('/get-all-user-portfolios', methods=['GET'])(get_all_user_portfolios)

# ------ statistics endpoints ------
# #untested#
app.route('/get-single-stats', methods=['GET'])(get_single_stat)

app.route('/get-all-stats', methods=['GET'])(get_all_stats)

if __name__ == '__main__':
    # app.run(debug=True)
    # to allow machines in my network access the server
    # run the following function with the none local host ip it prints on the screen
    app.run(host='0.0.0.0', port=5000, debug=True)
