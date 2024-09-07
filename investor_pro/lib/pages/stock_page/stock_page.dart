import 'package:flutter/material.dart';
import 'package:investor_pro/models/price_data_model.dart';
import 'package:investor_pro/pages/stock_page/date_range_selector.dart';
import 'package:provider/provider.dart';
import 'package:investor_pro/pages/stock_page/price_chart.dart';
import 'package:investor_pro/providers/stock_page_provider.dart';
import 'package:investor_pro/theme.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';

class StockPage extends StatefulWidget {
  final String stockId;

  const StockPage({Key? key, required this.stockId}) : super(key: key);

  @override
  _StockPageState createState() => _StockPageState();
}

class _StockPageState extends State<StockPage> {
  String currentRange = '1M'; // Default range

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<StockProvider>(
      create: (_) => StockProvider(widget.stockId),
      child: Consumer<StockProvider>(
        builder: (context, viewModel, child) {
          final stock = viewModel.stock;
          final filteredData =
              filterDataByRange(viewModel.priceData, currentRange);


          return Scaffold(
            appBar: CustomAppBar(
              title: 'Stock Details',
              showBackButton: true,
              actions: [
                IconButton(
                  icon: const Icon(Icons.add),
                  onPressed: () {
                    _showAddToPortfolioDialog(context, viewModel);
                  },
                ),
              ],
            ),
            body: viewModel.isLoading
                ? const Center(child: CircularProgressIndicator())
                : SingleChildScrollView(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          stock?.symbol.toString() ?? '',
                          style:
                              Theme.of(context).textTheme.headline3?.copyWith(
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.secondary,
                                  ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          stock?.name ?? '',
                          style:
                              Theme.of(context).textTheme.subtitle1?.copyWith(
                                    color: Colors.grey[600],
                                  ),
                        ),
                        const SizedBox(height: 16),
                        Divider(color: Colors.grey[400]),
                        const SizedBox(height: 16),
                        Text(
                          'Company Details',
                          style:
                              Theme.of(context).textTheme.headline6?.copyWith(
                                    fontWeight: FontWeight.bold,
                                  ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          stock?.description ?? '',
                          style: const TextStyle(
                              fontSize: 16, color: AppColors.onBackground),
                        ),
                        const SizedBox(height: 16),
                        Divider(color: Colors.grey[400]),
                        const SizedBox(height: 16),
                        Text(
                          'Price Chart',
                          style:
                              Theme.of(context).textTheme.headline6?.copyWith(
                                    fontWeight: FontWeight.bold,
                                  ),
                        ),
                        const SizedBox(height: 8),
                        DateRangeSelector(
                          onRangeSelected: (range) {
                            setState(() {
                              currentRange = range;
                            });
                          },
                        ),
                        const SizedBox(height: 16),
                        StockPriceChart(
                          data: filteredData,
                          dateRange: currentRange,
                        ),
                        const SizedBox(height: 32),
                        Divider(color: Colors.grey[400]),
                        const SizedBox(height: 16),
                        Text.rich(
                          TextSpan(
                            children: [
                              TextSpan(
                                text: 'TEVA Stock Prediction:\n\n',
                                style: Theme.of(context)
                                    .textTheme
                                    .headline6
                                    ?.copyWith(
                                      fontWeight: FontWeight.bold,
                                    ),
                              ),
                              const TextSpan(
                                text: 'Outlook: ',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.blueAccent,
                                  fontSize: 16,
                                ),
                              ),
                              const TextSpan(
                                text: 'Positive with Cautious Optimism\n\n',
                                style: TextStyle(
                                  fontSize: 16,
                                  color: Colors.black,
                                ),
                              ),
                              const TextSpan(
                                text:
                                    'TEVA Pharmaceutical Industries has shown a steady recovery in recent months, buoyed by strong financial performance and strategic initiatives aimed at streamlining operations and expanding its global footprint. Analysts predict a continued upward trend, with potential short-term volatility due to market conditions and regulatory factors.\n\n',
                                style: TextStyle(
                                  fontSize: 16,
                                  color: Colors.black,
                                ),
                              ),
                              const TextSpan(
                                text:
                                    'Investors are advised to monitor key developments, including upcoming earnings reports and regulatory approvals, which could significantly impact the stock\'s trajectory. The consensus among analysts suggests a target price increase of 5-10% over the next quarter, making TEVA a potentially lucrative, albeit cautious, buy for those looking to capitalize on the pharmaceutical sector\'s growth.',
                                style: TextStyle(
                                  fontSize: 16,
                                  color: Colors.black,
                                ),
                              ),
                            ],
                          ),
                        )
                      ],
                    ),
                  ),
          );
        },
      ),
    );
  }

  void _showAddToPortfolioDialog(
      BuildContext context, StockProvider viewModel) {
    showDialog(
      context: context,
      builder: (context) {
        String selectedPortfolio = 'Tech Portfolio'; // Default selection

        return AlertDialog(
          title: const Text('Add to Portfolio'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text('Select a portfolio to add this stock to.'),
              const SizedBox(height: 16),
              DropdownButton<String>(
                value: selectedPortfolio,
                items: <String>[
                  'Tech Portfolio',
                  'Banking Portfolio',
                  'Chemical Portfolio',
                  'Real Estate Portfolio'
                ].map((String value) {
                  return DropdownMenuItem<String>(
                    value: value,
                    child: Text(value),
                  );
                }).toList(),
                onChanged: (String? newValue) {
                  selectedPortfolio = newValue!;
                },
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text(
                'Cancel',
                style: TextStyle(color: Colors.white),
              ),
            ),
            ElevatedButton(
              onPressed: () {
                // Handle adding to portfolio using selectedPortfolio
                Navigator.of(context).pop();
              },
              child: const Text('Add'),
            ),
          ],
        );
      },
    );
  }

  List<PriceDataModel> filterDataByRange(
      List<PriceDataModel> data, String range) {
    DateTime now = DateTime.now();
    DateTime startDate;

    switch (range) {
      case '1M':
        startDate = DateTime(now.year, now.month - 1, now.day);
        break;
      case '3M':
        startDate = DateTime(now.year, now.month - 3, now.day);
        break;
      case '6M':
        startDate = DateTime(now.year, now.month - 6, now.day);
        break;
      case '1Y':
        startDate = DateTime(now.year - 1, now.month, now.day);
        break;
      default:
        startDate =
            DateTime(now.year, now.month - 1, now.day); // Default to 1 year
        break;
    }

    return data.where((item) {
      DateTime itemDate = DateTime.parse(item.date);
      return itemDate.isAfter(startDate) &&
          itemDate.isBefore(DateTime(now.year, now.month, now.day + 7));
    }).toList();
  }
}
