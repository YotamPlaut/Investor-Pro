from datetime import datetime, timedelta
from backend.functions.stock_db_manager import StockManager
from flask import jsonify, request

stock_list = [
    {'index_id': 137, 'name': 'TA_125', 'IsIndex': True},
    {'index_id': 147, 'name': 'TA_SME_60', 'IsIndex': True},
    {'index_id': 709, 'name': 'TA_Bond_60', 'IsIndex': True},
    {'index_id': 662577, 'name': 'Bank_Hapoalim', 'IsIndex': False},
    {'index_id': 691212, 'name': 'Bank_Discont', 'IsIndex': False},
]


def get_stock_info():
    curr_datetime = datetime.now()
    http_data = request.json
    date = datetime.now() - timedelta(days=365)
    if 'username' not in http_data or 'stock_name' not in http_data:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        stock_manager = StockManager()
        stock_info = stock_manager.get_stock_data_by_date(http_data['stock_name'], date)
        for key in stock_info['info'].keys():
            print(key)
            print(stock_info['info'][key])
        return jsonify({'message': 'test'}), 200
