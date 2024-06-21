import 'package:flutter/material.dart';
import 'package:investor_pro/mock_data.dart';
import 'package:investor_pro/models/portfolio_model.dart';
import 'package:investor_pro/pages/main_page/portfolio_card.dart';
import 'package:investor_pro/providers/main_page_provider.dart';
import 'package:provider/provider.dart';

class PortfolioList extends StatelessWidget {
  final List<PortfolioModel> portfolios = [
    PortfolioModel(name: 'Tech Stocks', stocks: MockStockData.portfolio1),
    PortfolioModel(name: 'Energy Funds', stocks: MockStockData.portfolio2),
    PortfolioModel(name: 'Energy Funds', stocks: MockStockData.portfolio3),
  ];

  PortfolioList({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<MainPageProvider>(
      builder: (context, viewModel, child) {
        return ListView.builder(
          itemCount: portfolios.length, //viewModel.portfolios.length,
          itemBuilder: (context, index) {
            final portfolio = portfolios[index]; //viewModel.portfolios[index];
            return PortfolioCard(portfolio: portfolio);
          },
        );
      },
    );
  }
}
