import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:investor_pro/providers/stock_page_provider.dart';

class StockModel {
  final String ticker;
  final String name;
  final String details;
  final String predictions;

  StockModel({
    required this.ticker,
    required this.name,
    required this.details,
    required this.predictions,
  });

  factory StockModel.fromJson(Map<String, dynamic> json) {
    return StockModel(
      ticker: json['ticker'],
      name: json['name'],
      details: json['details'],
      predictions: json['predictions'],
    );
  }

  static Future<List<StockModel>> searchAssets(String query) async {
    final response = await http.get(Uri.parse('http://your-api-url.com/search?query=$query'));
    if (response.statusCode == 200) {
      Iterable list = jsonDecode(response.body);
      return list.map((model) => StockModel.fromJson(model)).toList();
    } else {
      throw Exception('Failed to search assets');
    }
  }

  static Future<StockModel> fetchStockDetails(String stockId) async {
    final response = await http.get(Uri.parse('http://your-api-url.com/stocks/$stockId'));
    if (response.statusCode == 200) {
      return StockModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load stock details');
    }
  }

  static Future<void> addStockToPortfolio(String portfolioId, String stockId) async {
    final response = await http.post(
      Uri.parse('http://your-api-url.com/portfolios/$portfolioId/stocks'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'stockId': stockId}),
    );
    if (response.statusCode != 201) {
      throw Exception('Failed to add stock to portfolio');
    }
  }

  static Future<List<ChartData>> fetchPriceData(String stockId) async {
    final response = await http.get(Uri.parse('http://your-api-url.com/stocks/$stockId/price-data'));
    if (response.statusCode == 200) {
      Iterable list = jsonDecode(response.body);
      return list.map((model) => ChartData(model['date'], model['price'])).toList();
    } else {
      throw Exception('Failed to load price data');
    }
  }
}
