// PortfolioList Widget
import 'package:flutter/material.dart';
import 'package:investor_pro/models/utils/portfolio_model.dart';
import 'package:investor_pro/pages/main_page/widgets/portfolio_card.dart';

class PortfolioList extends StatefulWidget {
  const PortfolioList({super.key});

  @override
  _PortfolioListState createState() => _PortfolioListState();
}

class _PortfolioListState extends State<PortfolioList> {
  final List<Portfolio> portfolios = [
    Portfolio(name: 'Tech Stocks', stocks: ['AAPL', 'GOOGL', 'MSFT']),
    Portfolio(name: 'Energy Funds', stocks: ['XOM', 'CVX', 'BP']),
    // Add more portfolios here
  ];

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: portfolios.length,
      itemBuilder: (context, index) {
        final portfolio = portfolios[index];
        return PortfolioCard(portfolio: portfolio);
      },
    );
  }
}
