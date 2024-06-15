import 'package:flutter/material.dart';
import 'package:investor_pro/theme.dart';

class HorizontalAssetsList extends StatelessWidget {
  final String title;

  const HorizontalAssetsList({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: AppColors.onPrimary,
          ),
        ),
        const SizedBox(height: 10),
        Container(
          height: 150, // Adjust height as needed
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: 10, // Number of items in the section
            itemBuilder: (context, index) {
              return Card(
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                child: Container(
                  width: 150, // Adjust width as needed
                  padding: const EdgeInsets.all(10),
                  child: Center(
                    child: Text(
                      'Item $index',
                      style: TextStyle(color: AppColors.onPrimary),
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}