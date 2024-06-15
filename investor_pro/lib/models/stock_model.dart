import 'dart:convert';
import 'package:http/http.dart' as http;

class StockModel {
  String id;
  String name;
  String ticker;

  StockModel({required this.id, required this.name, required this.ticker});

  factory StockModel.fromJson(Map<String, dynamic> json) {
    return StockModel(
      id: json['id'],
      name: json['name'],
      ticker: json['ticker'],
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
}
