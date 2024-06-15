import 'package:flutter/material.dart';
import 'package:investor_pro/models/stock_model.dart';

class ExplorePageProvider with ChangeNotifier {
  List<StockModel> searchResults = [];
  bool isLoading = false;

  Future<void> searchAssets(String query) async {
    try {
      isLoading = true;
      notifyListeners();
      searchResults = await StockModel.searchAssets(query);
    } catch (e) {
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> fetchStockDetails(String stockId) async {
    try {
      isLoading = true;
      notifyListeners();
      StockModel stock = await StockModel.fetchStockDetails(stockId);
    } catch (e) {
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> addStockToPortfolio(String portfolioId, String stockId) async {
    try {
      isLoading = true;
      notifyListeners();
      await StockModel.addStockToPortfolio(portfolioId, stockId);
    } catch (e) {
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }
}
