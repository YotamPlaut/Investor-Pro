import 'dart:convert';
import 'package:http/http.dart' as http;

class StockModel {
  final String name;
  final String ticker;
  final int index;
  final String info;
  final int numDays;
  final DateTime beginDate;
  final DateTime endDate;

  StockModel(
      {required this.name,
      required this.ticker,
      required this.index,
      required this.info,
      required this.numDays,
      required this.beginDate,
      required this.endDate});

  factory StockModel.fromJson(Map<String, dynamic> json) {
    return StockModel(
      name: json['name'] as String,
      ticker: json['ticker'] as String,
      index: json['index'] as int,
      info: json['info'] as String,
      numDays: json['numDays'] as int,
      beginDate: DateTime.parse(json['beginDate'] as String),
      endDate: DateTime.parse(json['endDate'] as String),
    );
  }

  static Future<List<StockModel>> searchAssets(String query) async {
    final response = await http
        .get(Uri.parse('http://your-api-url.com/search?query=$query'));
    if (response.statusCode == 200) {
      Iterable list = jsonDecode(response.body);
      return list.map((model) => StockModel.fromJson(model)).toList();
    } else {
      throw Exception('Failed to search assets');
    }
  }

  static Future<StockModel> fetchStockDetails(String stockId) async {
    final response =
        await http.get(Uri.parse('http://your-api-url.com/stocks/$stockId'));
    if (response.statusCode == 200) {
      return StockModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load stock details');
    }
  }

  static Future<void> addStockToPortfolio(
      String portfolioId, String stockId) async {
    final response = await http.post(
      Uri.parse('http://your-api-url.com/portfolios/$portfolioId/stocks'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'stockId': stockId}),
    );
    if (response.statusCode != 201) {
      throw Exception('Failed to add stock to portfolio');
    }
  }

// static Future<List<ChartData>> fetchPriceData(String stockId) async {
//   final response = await http.get(Uri.parse('http://your-api-url.com/stocks/$stockId/price-data'));
//   if (response.statusCode == 200) {
//     Iterable list = jsonDecode(response.body);
//    // return list.map((model) => ChartData(model['date'], model['price'])).toList();
//   } else {
//     throw Exception('Failed to load price data');
//   }
// }
}
