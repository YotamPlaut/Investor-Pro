// PortfolioCard Widget
import 'package:flutter/material.dart';
import 'package:investor_pro/theme.dart';

import '../../models/portfolio_model.dart';

class PortfolioCard extends StatefulWidget {
  final PortfolioModel portfolio;

  const PortfolioCard({super.key, required this.portfolio});

  @override
  _PortfolioCardState createState() => _PortfolioCardState();
}

class _PortfolioCardState extends State<PortfolioCard> {
  bool _isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: Column(
        children: [
          ListTile(
            title: Text(widget.portfolio.name, style: TextStyle(color: AppColors.onPrimary)),
            trailing: IconButton(
              icon: Icon(
                _isExpanded ? Icons.expand_less : Icons.expand_more,
                color: AppColors.secondary,
              ),
              onPressed: () {
                setState(() {
                  _isExpanded = !_isExpanded;
                });
              },
            ),
          ),
          if (_isExpanded)
            Column(
              children: widget.portfolio.stocks.map((stock) {
                return ListTile(
                  title: Text(stock.name, style: TextStyle(color: AppColors.onPrimary)),
                );
              }).toList(),
            ),
        ],
      ),
    );
  }
}