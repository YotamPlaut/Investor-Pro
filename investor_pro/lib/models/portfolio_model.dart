import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:investor_pro/models/stock_model.dart';

class PortfolioModel {
  final String id;
  final String name;
  final List<StockModel> stocks;

  PortfolioModel({required this.name, required this.id, required this.stocks});

  static const String baseUrl = 'http://192.168.1.194:5000';

  factory PortfolioModel.fromJson(Map<String, dynamic> json) {
    return PortfolioModel(
      name: json['name'],
      stocks:
          (json['stocks'] as List).map((i) => StockModel.fromJson(i)).toList(),
      id: json['id'],
    );
  }

  static Future<List<PortfolioModel>> fetchPortfolios(String userId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/get-all-user-portfolios')
          .replace(queryParameters: {'username': 'shachar'}),
    );
    if (response.statusCode == 200) {
      Iterable list = jsonDecode(response.body);
      return list.map((model) => PortfolioModel.fromJson(model)).toList();
    } else {
      throw Exception('Failed to load portfolios');
    }
  }

  static Future<void> addPortfolio(String userId, String portfolioName) async {
    final response = await http.post(
      Uri.parse('$baseUrl/create-new-portfolio'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(
          {'username': userId, 'portfolio_id': portfolioName, 'stocks_id': []}),
    );
    if (response.statusCode != 200) {
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
