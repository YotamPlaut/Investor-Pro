import 'package:flutter/material.dart';
import 'package:investor_pro/models/user_model.dart';

// import 'package:investor_pro/models/portfolio_model.dart';
// import 'package:investor_pro/services/api_service.dart';

class MainPageProvider with ChangeNotifier {
  UserModel? user;

  //List<PortfolioModel> portfolios = [];
  bool isLoading = false;

  MainPageProvider() {
    _init();
  }

  Future<void> _init() async {
    await _getUser();
    await _getPortfolios();
  }

  Future<void> _getUser() async {
    try {
      isLoading = true;
      notifyListeners();
      // Fetch user data from API
      // user = await ApiService.fetchUser();
    } catch (e) {
      // Handle error
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> _getPortfolios() async {
    try {
      isLoading = true;
      notifyListeners();
      // Fetch user's portfolios from API
      // portfolios = await ApiService.fetchPortfolios(user!.id);
    } catch (e) {
      // Handle error
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> addPortfolio(String portfolioName) async {
    try {
      isLoading = true;
      notifyListeners();
      // Fetch user's portfolios from API
      // portfolios = await ApiService.fetchPortfolios(user!.id);
    } catch (e) {
      // Handle error
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }
}
