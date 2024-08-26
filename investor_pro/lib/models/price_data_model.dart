// To parse this JSON data, do
//
//     final priceDataModel = priceDataModelFromJson(jsonString);

import 'dart:convert';

PriceDataModel priceDataModelFromJson(String str) =>
    PriceDataModel.fromJson(json.decode(str));

String priceDataModelToJson(PriceDataModel data) => json.encode(data.toJson());

class PriceDataModel {
  final DateTime date;
  final double closePrice;

  PriceDataModel({
    required this.date,
    required this.closePrice,
  });

  factory PriceDataModel.fromJson(Map<String, dynamic> json) => PriceDataModel(
        date: json["date"] as DateTime,
        closePrice: json["close_price"] as double,
      );

  Map<String, dynamic> toJson() => {
        "date": date,
        "close_price": closePrice,
      };
}
