import 'package:investor_pro/models/stock_model.dart';

class MockStockData {
  static List<StockModel> portfolio1 = [
    StockModel(
      ticker: 'AAPL',
      name: 'Apple Inc.',
      details:
          'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.',
      predictions: 'The stock is predicted to rise by 5% in the next quarter.',
    ),
    StockModel(
      ticker: 'GOOGL',
      name: 'Alphabet Inc.',
      details:
          'Alphabet Inc. provides online advertising services in the United States, Europe, the Middle East, Africa, the Asia-Pacific, Canada, and Latin America.',
      predictions: 'The stock is predicted to rise by 8% in the next quarter.',
    ),
    StockModel(
      ticker: 'MSFT',
      name: 'Microsoft Corporation',
      details:
          'Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide.',
      predictions: 'The stock is predicted to rise by 7% in the next quarter.',
    ),
    StockModel(
      ticker: 'AMZN',
      name: 'Amazon.com, Inc.',
      details:
          'Amazon.com, Inc. engages in the retail sale of consumer products and subscriptions in North America and internationally.',
      predictions: 'The stock is predicted to rise by 6% in the next quarter.',
    ),
    StockModel(
      ticker: 'TSLA',
      name: 'Tesla, Inc.',
      details:
          'Tesla, Inc. designs, develops, manufactures, and sells electric vehicles and energy generation and storage systems.',
      predictions: 'The stock is predicted to rise by 10% in the next quarter.',
    ),
  ];

  static List<StockModel> portfolio2 = [
    StockModel(
      ticker: 'NFLX',
      name: 'Netflix, Inc.',
      details:
          'Netflix, Inc. provides subscription streaming entertainment services.',
      predictions: 'The stock is predicted to rise by 4% in the next quarter.',
    ),
    StockModel(
      ticker: 'FB',
      name: 'Meta Platforms, Inc.',
      details:
          'Meta Platforms, Inc. develops products that enable people to connect and share with friends and family through mobile devices, personal computers, and other surfaces worldwide.',
      predictions: 'The stock is predicted to rise by 3% in the next quarter.',
    ),
    StockModel(
      ticker: 'NVDA',
      name: 'NVIDIA Corporation',
      details:
          'NVIDIA Corporation operates as a visual computing company worldwide.',
      predictions: 'The stock is predicted to rise by 9% in the next quarter.',
    ),
    StockModel(
      ticker: 'ADBE',
      name: 'Adobe Inc.',
      details:
          'Adobe Inc. operates as a diversified software company worldwide.',
      predictions: 'The stock is predicted to rise by 5% in the next quarter.',
    ),
    StockModel(
      ticker: 'PYPL',
      name: 'PayPal Holdings, Inc.',
      details:
          'PayPal Holdings, Inc. operates as a technology platform and digital payments company that enables digital and mobile payments on behalf of consumers and merchants worldwide.',
      predictions: 'The stock is predicted to rise by 6% in the next quarter.',
    ),
  ];

  static List<StockModel> portfolio3 = [
    StockModel(
      ticker: 'DIS',
      name: 'The Walt Disney Company',
      details:
          'The Walt Disney Company, together with its subsidiaries, operates as an entertainment company worldwide.',
      predictions: 'The stock is predicted to rise by 5% in the next quarter.',
    ),
    StockModel(
      ticker: 'BABA',
      name: 'Alibaba Group Holding Limited',
      details:
          'Alibaba Group Holding Limited, through its subsidiaries, provides online and mobile commerce businesses in the People\'s Republic of China and internationally.',
      predictions: 'The stock is predicted to rise by 7% in the next quarter.',
    ),
    StockModel(
      ticker: 'V',
      name: 'Visa Inc.',
      details: 'Visa Inc. operates as a payments technology company worldwide.',
      predictions: 'The stock is predicted to rise by 4% in the next quarter.',
    ),
    StockModel(
      ticker: 'MA',
      name: 'Mastercard Incorporated',
      details:
          'Mastercard Incorporated, a technology company, provides transaction processing and other payment-related products and services in the United States and internationally.',
      predictions: 'The stock is predicted to rise by 5% in the next quarter.',
    ),
    StockModel(
      ticker: 'INTC',
      name: 'Intel Corporation',
      details:
          'Intel Corporation designs, manufactures, and sells essential technologies for the cloud, smart, and connected devices for retail, industrial, and consumer uses worldwide.',
      predictions: 'The stock is predicted to rise by 3% in the next quarter.',
    ),
  ];
}
