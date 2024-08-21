from datetime import datetime
from flask import jsonify, request
from backend.functions.event_db_manager import EventDatabaseManager
from backend.functions.portfolio_db_manager import PortfolioDatabaseManager
from backend.classes_backend.portfolio import Portfolio


def create_new_portfolio():
    curr_datetime = datetime.now()
    data = request.json
    if 'username' not in data or 'portfolio_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        portfolio_manager = PortfolioDatabaseManager()
        if portfolio_manager.is_username_and_portfolio_name_exists(data['username'], data['portfolio_id']):
            return jsonify({'error': 'portfolio already exist for user'}), 400

        portfolio_manager.insert_new_portfolio(data['username'], data['portfolio_id'])

        event_db_manager = EventDatabaseManager()
        event_db_manager.insert_raw_action('created new portfolio', curr_datetime,
                                           data['username'], {'port_id': data['portfolio_id']})
        return jsonify({'message': 'successfully created new portfolio'}), 200


def delete_portfolio():
    curr_datetime = datetime.now()
    data = request.json
    if 'username' not in data or 'portfolio_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        portfolio_manager = PortfolioDatabaseManager()
        if not portfolio_manager.is_username_and_portfolio_name_exists(data['username'], data['portfolio_id']):
            return jsonify({'error': 'portfolio id not found for this user'}), 404

        portfolio_manager.remove_portfolio(data['username'], data['portfolio_id'])
        event_db_manager = EventDatabaseManager()
        event_db_manager.insert_raw_action('deleted portfolio', curr_datetime,
                                           data['username'], {'port_id': data['portfolio_id']})
        return jsonify({'message': 'successfully removed portfolio'}), 200


def add_stock_to_portfolio():
    curr_datetime = datetime.now()
    data = request.json
    if 'username' not in data or 'portfolio_id' not in data or 'stock_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        portfolio_manager = PortfolioDatabaseManager()
        if not portfolio_manager.is_username_and_portfolio_name_exists(data['username'], data['portfolio_id']):
            return jsonify({'error': 'portfolio id not found for this user'}), 404

        portfolio_manager.add_new_stock_to_portfolio(data['username'], data['portfolio_id'], data['stock_id'])
        event_db_manager = EventDatabaseManager()
        event_db_manager.insert_raw_action('add stock to portfolio', curr_datetime,
                                           data['username'], {'port_id': data['portfolio_id'],
                                                              'stock_id': data['stock_id']})
        return jsonify({'message': 'successfully added stock to portfolio'}), 200


def remove_stock_from_portfolio():
    curr_datetime = datetime.now()
    data = request.json
    if 'username' not in data or 'portfolio_id' not in data or 'stock_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        portfolio_manager = PortfolioDatabaseManager()
        if not portfolio_manager.is_username_and_portfolio_name_exists(data['username'], data['portfolio_id']):
            return jsonify({'error': 'portfolio id not found for this user'}), 404

        portfolio_manager.remove_stock_from_portfolio(data['username'], data['portfolio_id'], data['stock_id'])
        event_db_manager = EventDatabaseManager()
        event_db_manager.insert_raw_action('removed stock from portfolio', curr_datetime,
                                           data['username'], {'port_id': data['portfolio_id'],
                                                              'stock_id': data['stock_id']})
        return jsonify({'message': 'successfully removed stock from portfolio'}), 200


def get_all_user_portfolios():
    data = request.args.get('username')
    if data is None:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        pm = PortfolioDatabaseManager()
        portfolios_temp = pm.get_all_user_portfolios(data)
        portfolios = []
        for port_id in portfolios_temp.keys():
            port = Portfolio(port_id, portfolios_temp[port_id])
            portfolios.append(port.to_dict())

        return jsonify(portfolios), 200
