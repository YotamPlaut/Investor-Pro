import 'package:flutter/material.dart';
import 'package:investor_pro/providers/stock_page_provider.dart';
import 'package:provider/provider.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:investor_pro/models/stock_model.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';

class StockPage extends StatelessWidget {
  final StockModel stock;

  const StockPage({Key? key, required this.stock}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<StockProvider>(
      create: (_) => StockProvider(stock),
      child: Consumer<StockProvider>(
        builder: (context, viewModel, child) {
          return Scaffold(
            appBar: CustomAppBar(
              title: 'Stock Details',
              showBackButton: true,
              actions: [
                IconButton(
                  icon: Icon(Icons.add),
                  onPressed: () {
                    // Handle add to portfolio action
                    _showAddToPortfolioDialog(context, viewModel);
                  },
                ),
              ],
            ),
            body: viewModel.isLoading
                ? Center(child: CircularProgressIndicator())
                : SingleChildScrollView(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          stock.ticker,
                          style: Theme.of(context).textTheme.headline4,
                        ),
                        SizedBox(height: 8),
                        Text(
                          stock.name,
                          style: Theme.of(context).textTheme.subtitle1,
                        ),
                        SizedBox(height: 16),
                        Text(
                          'Company Details',
                          style: Theme.of(context).textTheme.headline6,
                        ),
                        SizedBox(height: 8),
                        Text(stock.details),
                        SizedBox(height: 16),
                        Text(
                          'Price Chart',
                          style: Theme.of(context).textTheme.headline6,
                        ),
                        SizedBox(height: 8),
                        _buildPriceChart(viewModel.priceData),
                        SizedBox(height: 16),
                        Text(
                          'Predictions',
                          style: Theme.of(context).textTheme.headline6,
                        ),
                        SizedBox(height: 8),
                        Text(stock.predictions),
                      ],
                    ),
                  ),
          );
        },
      ),
    );
  }

  Widget _buildPriceChart(List<ChartData> data) {
    return SfCartesianChart(
      primaryXAxis: CategoryAxis(),
      series: <ChartSeries>[
        LineSeries<ChartData, String>(
          dataSource: data,
          xValueMapper: (ChartData data, _) => data.date,
          yValueMapper: (ChartData data, _) => data.price,
        ),
      ],
    );
  }

  void _showAddToPortfolioDialog(
      BuildContext context, StockProvider viewModel) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Add to Portfolio'),
          content: Text('Select a portfolio to add this stock to.'),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                // Handle adding to portfolio
                Navigator.of(context).pop();
              },
              child: Text('Add'),
            ),
          ],
        );
      },
    );
  }
}
