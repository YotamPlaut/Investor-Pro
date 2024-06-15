

import 'package:flutter/material.dart';
import 'package:investor_pro/theme.dart';

class SearchSection extends StatelessWidget {
  const SearchSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Search Assets',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: AppColors.onPrimary,
          ),
        ),
        const SizedBox(height: 10),
        TextField(
          decoration: InputDecoration(
            hintText: 'search assets',
            hintStyle: TextStyle(color: AppColors.onPrimary),
            prefixIcon: Icon(Icons.search, color: AppColors.secondary),
            enabledBorder: OutlineInputBorder(
              borderSide: BorderSide(color: AppColors.secondary),
              borderRadius: BorderRadius.circular(10),
            ),
            focusedBorder: OutlineInputBorder(
              borderSide: BorderSide(color: AppColors.secondaryVariant),
              borderRadius: BorderRadius.circular(10),
            ),
          ),
          cursorColor: AppColors.secondary,
          onChanged: (value) {
            // TODO: Implement search logic
          },
        ),
      ],
    );
  }
}