import 'package:flutter/material.dart';
import 'package:investor_pro/theme.dart';
import 'package:investor_pro/models/portfolio_model.dart';
import 'package:investor_pro/app_routes.dart';

class PortfolioCard extends StatefulWidget {
  final PortfolioModel portfolio;

  const PortfolioCard({super.key, required this.portfolio});

  @override
  _PortfolioCardState createState() => _PortfolioCardState();
}

class _PortfolioCardState extends State<PortfolioCard>
    with SingleTickerProviderStateMixin {
  bool _isExpanded = false;
  late AnimationController _controller;
  late Animation<double> _expandAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    _expandAnimation = CurvedAnimation(
      parent: _controller,
      curve: Curves.fastOutSlowIn,
    );
  }

  void _toggleExpansion() {
    setState(() {
      _isExpanded = !_isExpanded;
      if (_isExpanded) {
        _controller.forward();
      } else {
        _controller.reverse();
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _toggleExpansion,
      child: Card(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        child: Column(
          children: [
            ListTile(
              title: Text(
                widget.portfolio.name,
                style: TextStyle(color: AppColors.onPrimary),
              ),
              trailing: Icon(
                _isExpanded ? Icons.expand_less : Icons.expand_more,
                color: AppColors.secondary,
              ),
            ),
            SizeTransition(
              sizeFactor: _expandAnimation,
              child: Column(
                children: List.generate(
                  widget.portfolio.stocks.length,
                  (index) {
                    final stock = widget.portfolio.stocks[index];
                    return Column(
                      children: [
                        if (index == 0) const Divider(thickness: 0.3,),
                        ListTile(
                          title: Text(
                            stock.name,
                            style: TextStyle(color: AppColors.onPrimary),
                          ),
                          onTap: () => NavigationHelper.navigateTo(
                            context,
                            AppRoutes.stock,
                            data: stock,
                          ),
                        ),
                        if (index != widget.portfolio.stocks.length - 1)
                          const Divider(thickness: 0.3,),
                      ],
                    );
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
