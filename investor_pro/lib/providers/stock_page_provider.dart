import 'package:flutter/material.dart';
import 'package:investor_pro/models/price_data_model.dart';
import 'package:investor_pro/models/stock_model.dart';

class ChartData {
  final String date;
  final double price;

  ChartData({required this.date, required this.price});
}

class StockProvider with ChangeNotifier {
  StockModel? stock;
  List<ChartData> priceData = [];
  bool isLoading = false;

  StockProvider(String stockId) {
    initData(stockId);
  }

  void initData(String stockId) async {
    await _fetchStock(stockId);
  }

  Future<StockModel?> _fetchStock(String stockId) async {
    try {
      isLoading = true;
      notifyListeners();
      stock = await StockModel.fetchStockDetails(stockId);
      notifyListeners();
      return stock;
    } catch (e) {
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

// Future<void> _fetchPriceData() async {
//   try {
//     isLoading = true;
//     notifyListeners();
//     // priceData = await StockModel.fetchPriceData(stock.id);
//   } catch (e) {
//     print(e);
//   } finally {
//     isLoading = false;
//     notifyListeners();
//   }
// }
}
