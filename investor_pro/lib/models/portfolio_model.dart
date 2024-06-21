import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:investor_pro/models/stock_model.dart';

class PortfolioModel {
  String name;
  List<StockModel> stocks;

  PortfolioModel({required this.name, required this.stocks});

  factory PortfolioModel.fromJson(Map<String, dynamic> json) {
    return PortfolioModel(
      name: json['name'],
      stocks:
          (json['stocks'] as List).map((i) => StockModel.fromJson(i)).toList(),
    );
  }

  static Future<List<PortfolioModel>> fetchPortfolios(String userId) async {
    final response = await http
        .get(Uri.parse('http://your-api-url.com/user/$userId/portfolios'));
    if (response.statusCode == 200) {
      Iterable list = jsonDecode(response.body);
      return list.map((model) => PortfolioModel.fromJson(model)).toList();
    } else {
      throw Exception('Failed to load portfolios');
    }
  }

  static Future<void> addPortfolio(String userId, String portfolioName) async {
    final response = await http.post(
      Uri.parse('http://your-api-url.com/user/$userId/portfolios'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'name': portfolioName}),
    );
    if (response.statusCode != 201) {
      throw Exception('Failed to add portfolio');
    }
  }

  static Future<void> deletePortfolio(String userId, String portfolioId) async {
    final response = await http.delete(
      Uri.parse('http://your-api-url.com/user/$userId/portfolios/$portfolioId'),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to delete portfolio');
    }
  }
}
