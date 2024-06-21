import 'package:flutter/material.dart';
import 'package:investor_pro/models/stock_model.dart';

class ChartData {
  final String date;
  final double price;

  ChartData({required this.date, required this.price});
}

class StockProvider with ChangeNotifier {
  final StockModel stock;
  List<ChartData> priceData = [];
  bool isLoading = false;

  StockProvider(this.stock) {
    _fetchPriceData();
  }

  Future<void> _fetchPriceData() async {
    try {
      isLoading = true;
      notifyListeners();
     // priceData = await StockModel.fetchPriceData(stock.id);
    } catch (e) {
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }
}
