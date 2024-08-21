import 'package:flutter/material.dart';
import 'package:investor_pro/providers/stock_page_provider.dart';
import 'package:investor_pro/theme.dart';
import 'package:provider/provider.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:investor_pro/models/stock_model.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';

// class StockPage extends StatelessWidget {
//   final StockModel stock;
//
//   const StockPage({Key? key, required this.stock}) : super(key: key);
//
//   @override
//   Widget build(BuildContext context) {
//     return ChangeNotifierProvider<StockProvider>(
//       create: (_) => StockProvider(stock),
//       child: Consumer<StockProvider>(
//         builder: (context, viewModel, child) {
//           return Scaffold(
//             appBar: CustomAppBar(
//               title: 'Stock Details',
//               showBackButton: true,
//               actions: [
//                 IconButton(
//                   icon: Icon(Icons.add),
//                   onPressed: () {
//                     // Handle add to portfolio action
//                     _showAddToPortfolioDialog(context, viewModel);
//                   },
//                 ),
//               ],
//             ),
//             body: viewModel.isLoading
//                 ? Center(child: CircularProgressIndicator())
//                 : SingleChildScrollView(
//                     padding: const EdgeInsets.all(16.0),
//                     child: Column(
//                       crossAxisAlignment: CrossAxisAlignment.start,
//                       children: [
//                         Text(
//                           stock.ticker,
//                           style: Theme.of(context).textTheme.headline4,
//                         ),
//                         SizedBox(height: 8),
//                         Text(
//                           stock.name,
//                           style: Theme.of(context).textTheme.subtitle1,
//                         ),
//                         SizedBox(height: 8),
//                         Divider(),
//                         SizedBox(height: 8),
//                         Text(
//                           'Company Details',
//                           style: Theme.of(context).textTheme.headline6,
//                         ),
//                         SizedBox(height: 8),
//                         Text(stock.info),
//                         SizedBox(height: 8),
//                         Divider(),
//                         SizedBox(height: 8),
//                         Text(
//                           'Price Chart',
//                           style: Theme.of(context).textTheme.headline6,
//                         ),
//                         SizedBox(height: 8),
//                         _buildPriceChart(viewModel.priceData),
//                         SizedBox(height: 8),
//                         Divider(),
//                         SizedBox(height: 8),
//                         Text(
//                           'Predictions',
//                           style: Theme.of(context).textTheme.headline6,
//                         ),
//                         SizedBox(height: 8),
//                       ],
//                     ),
//                   ),
//           );
//         },
//       ),
//     );
//   }
//
//   Widget _buildPriceChart(List<ChartData> data) {
//     List<ChartData> mockData = [
//       ChartData(date: 'Jan', price: 100),
//       ChartData(date: 'Feb', price: 120),
//       ChartData(date: 'Mar', price: 110),
//       ChartData(date: 'Apr', price: 150),
//       ChartData(date: 'May', price: 130),
//       ChartData(date: 'Jun', price: 160),
//     ];
//
//     return SizedBox(
//       height: 300,
//       child: LineChart(
//         LineChartData(
//           gridData: FlGridData(show: true),
//           titlesData: FlTitlesData(
//             bottomTitles: AxisTitles(
//               sideTitles: SideTitles(
//                 showTitles: true,
//                 getTitlesWidget: (value, meta) {
//                   const style = TextStyle(
//                     color: Color(0xff68737d),
//                     fontWeight: FontWeight.bold,
//                     fontSize: 16,
//                   );
//                   Widget text;
//                   switch (value.toInt()) {
//                     case 0:
//                       text = const Text('Jan', style: style);
//                       break;
//                     case 1:
//                       text = const Text('Feb', style: style);
//                       break;
//                     case 2:
//                       text = const Text('Mar', style: style);
//                       break;
//                     case 3:
//                       text = const Text('Apr', style: style);
//                       break;
//                     case 4:
//                       text = const Text('May', style: style);
//                       break;
//                     case 5:
//                       text = const Text('Jun', style: style);
//                       break;
//                     default:
//                       text = const Text('', style: style);
//                       break;
//                   }
//                   return SideTitleWidget(
//                     axisSide: meta.axisSide,
//                     space: 8.0,
//                     child: text,
//                   );
//                 },
//               ),
//             ),
//             leftTitles: AxisTitles(
//               sideTitles: SideTitles(
//                 showTitles: true,
//                 getTitlesWidget: (value, meta) {
//                   const style = TextStyle(
//                     color: Color(0xff67727d),
//                     fontWeight: FontWeight.bold,
//                     fontSize: 15,
//                   );
//                   String text;
//                   switch (value.toInt()) {
//                     case 100:
//                       text = '100';
//                       break;
//                     case 120:
//                       text = '120';
//                       break;
//                     case 140:
//                       text = '140';
//                       break;
//                     case 160:
//                       text = '160';
//                       break;
//                     default:
//                       return Container();
//                   }
//                   return Text(text, style: style, textAlign: TextAlign.left);
//                 },
//                 reservedSize: 28,
//               ),
//             ),
//           ),
//           borderData: FlBorderData(
//             show: true,
//             border: Border.all(
//               color: const Color(0xff37434d),
//             ),
//           ),
//           minX: 0,
//           maxX: 5,
//           minY: 90,
//           maxY: 170,
//           lineBarsData: [
//             LineChartBarData(
//               spots: mockData
//                   .asMap()
//                   .entries
//                   .map(
//                       (e) => FlSpot(e.key.toDouble(), e.value.price.toDouble()))
//                   .toList(),
//               isCurved: true,
//               color: Colors.blue,
//               barWidth: 4,
//               isStrokeCapRound: true,
//               belowBarData: BarAreaData(show: false),
//               dotData: FlDotData(show: false),
//             ),
//           ],
//         ),
//       ),
//     );
//   }
//
//   void _showAddToPortfolioDialog(
//       BuildContext context, StockProvider viewModel) {
//     showDialog(
//       context: context,
//       builder: (context) {
//         return AlertDialog(
//           title: Text('Add to Portfolio'),
//           content: Text('Select a portfolio to add this stock to.'),
//           actions: [
//             TextButton(
//               onPressed: () {
//                 Navigator.of(context).pop();
//               },
//               child: Text('Cancel'),
//             ),
//             TextButton(
//               onPressed: () {
//                 // Handle adding to portfolio
//                 Navigator.of(context).pop();
//               },
//               child: Text('Add'),
//             ),
//           ],
//         );
//       },
//     );
//   }
// }

import 'package:flutter/material.dart';
import 'package:investor_pro/providers/stock_page_provider.dart';
import 'package:provider/provider.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:investor_pro/models/stock_model.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';

class StockPage extends StatelessWidget {
  final String stockId;

  const StockPage({Key? key, required this.stockId}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<StockProvider>(
      create: (_) => StockProvider(stockId),
      child: Consumer<StockProvider>(
        builder: (context, viewModel, child) {
          final stock = viewModel.stock;
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
                        // Ticker and Name Section
                        Text(
                          stock.ticker,
                          style:
                              Theme.of(context).textTheme.headline3?.copyWith(
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.secondary,
                                  ),
                        ),
                        SizedBox(height: 4),
                        Text(
                          stock.name,
                          style:
                              Theme.of(context).textTheme.subtitle1?.copyWith(
                                    color: Colors.grey[600],
                                  ),
                        ),
                        SizedBox(height: 16),
                        Divider(color: Colors.grey[400]),
                        SizedBox(height: 16),

                        // Company Details Section
                        Text(
                          'Company Details',
                          style:
                              Theme.of(context).textTheme.headline6?.copyWith(
                                    fontWeight: FontWeight.bold,
                                  ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          stock.info,
                          style: TextStyle(
                              fontSize: 16, color: AppColors.onBackground),
                        ),
                        SizedBox(height: 16),
                        Divider(color: Colors.grey[400]),
                        SizedBox(height: 16),

                        // Price Chart Section
                        Text(
                          'Price Chart',
                          style:
                              Theme.of(context).textTheme.headline6?.copyWith(
                                    fontWeight: FontWeight.bold,
                                  ),
                        ),
                        SizedBox(height: 16),
                        _buildPriceChart(viewModel.priceData),
                        SizedBox(
                            height: 32), // Added extra spacing below the chart
                        Divider(color: Colors.grey[400]),
                        SizedBox(height: 16),

                        // Predictions Section
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
                              TextSpan(
                                text: 'Outlook: ',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.blueAccent,
                                  fontSize: 16,
                                ),
                              ),
                              TextSpan(
                                text: 'Positive with Cautious Optimism\n\n',
                                style: TextStyle(
                                  fontSize: 16,
                                  color: Colors.black,
                                ),
                              ),
                              TextSpan(
                                text:
                                    'TEVA Pharmaceutical Industries has shown a steady recovery in recent months, buoyed by strong financial performance and strategic initiatives aimed at streamlining operations and expanding its global footprint. Analysts predict a continued upward trend, with potential short-term volatility due to market conditions and regulatory factors.\n\n',
                                style: TextStyle(
                                  fontSize: 16,
                                  color: Colors.black,
                                ),
                              ),
                              TextSpan(
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

  Widget _buildPriceChart(List<ChartData> data) {
    List<ChartData> mockData = [
      ChartData(date: 'Jan', price: 100),
      ChartData(date: 'Feb', price: 120),
      ChartData(date: 'Mar', price: 110),
      ChartData(date: 'Apr', price: 150),
      ChartData(date: 'May', price: 130),
      ChartData(date: 'Jun', price: 160),
    ];

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.2),
            spreadRadius: 5,
            blurRadius: 7,
            offset: Offset(0, 3), // changes position of shadow
          ),
        ],
      ),
      padding: const EdgeInsets.all(12),
      child: SizedBox(
        height: 320,
        // Increased the height to allow more space for the X-axis labels
        child: LineChart(
          LineChartData(
            gridData: FlGridData(
              show: true,
              drawVerticalLine: true,
              horizontalInterval: 20,
              verticalInterval: 10,
              // Adjusted for more data points on the Y-axis
              getDrawingHorizontalLine: (value) {
                return FlLine(
                  color: const Color(0xffe7e8ec),
                  strokeWidth: 1,
                );
              },
              getDrawingVerticalLine: (value) {
                return FlLine(
                  color: const Color(0xffe7e8ec),
                  strokeWidth: 1,
                );
              },
            ),
            titlesData: FlTitlesData(
              bottomTitles: AxisTitles(
                sideTitles: SideTitles(
                  showTitles: true,
                  reservedSize: 22, // Increased reserved size to avoid cutoff
                  getTitlesWidget: (value, meta) {
                    const style = TextStyle(
                      color: Color(0xff68737d),
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                    );
                    Widget text;
                    switch (value.toInt()) {
                      case 0:
                        text = const Text('Jan', style: style);
                        break;
                      case 1:
                        text = const Text('Feb', style: style);
                        break;
                      case 2:
                        text = const Text('Mar', style: style);
                        break;
                      case 3:
                        text = const Text('Apr', style: style);
                        break;
                      case 4:
                        text = const Text('May', style: style);
                        break;
                      case 5:
                        text = const Text('Jun', style: style);
                        break;
                      default:
                        text = const Text('', style: style);
                        break;
                    }
                    return SideTitleWidget(
                      axisSide: meta.axisSide,
                      space: 8.0,
                      child: text,
                    );
                  },
                ),
              ),
              leftTitles: AxisTitles(
                sideTitles: SideTitles(
                  showTitles: true,
                  interval: 10,
                  // Adjusted interval for more data points on the Y-axis
                  getTitlesWidget: (value, meta) {
                    const style = TextStyle(
                      color: Color(0xff67727d),
                      fontWeight: FontWeight.bold,
                      fontSize: 15,
                    );
                    return Text(value.toInt().toString(),
                        style: style, textAlign: TextAlign.left);
                  },
                  reservedSize: 40,
                ),
              ),
            ),
            borderData: FlBorderData(
              show: true,
              border: Border.all(
                color: const Color(0xff37434d),
                width: 1,
              ),
            ),
            minX: 0,
            maxX: 5,
            minY: 90,
            maxY: 170,
            lineBarsData: [
              LineChartBarData(
                spots: mockData
                    .asMap()
                    .entries
                    .map((e) =>
                        FlSpot(e.key.toDouble(), e.value.price.toDouble()))
                    .toList(),
                isCurved: true,
                color: AppColors.secondaryVariant,
                barWidth: 2,
                isStrokeCapRound: true,
                belowBarData: BarAreaData(
                  show: true,
                  gradient: LinearGradient(
                    colors: [
                      Colors.blueAccent.withOpacity(0.3),
                      Colors.blueAccent.withOpacity(0.0)
                    ],
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                  ),
                ),
                dotData: FlDotData(show: false),
              ),
            ],
          ),
        ),
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
          title: Text('Add to Portfolio'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Select a portfolio to add this stock to.'),
              SizedBox(height: 16),
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
              child: Text(
                'Cancel',
                style: TextStyle(color: Colors.white),
              ),
            ),
            ElevatedButton(
              onPressed: () {
                // Handle adding to portfolio using selectedPortfolio
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
