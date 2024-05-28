import 'package:flutter/material.dart';
import 'package:investor_pro/models/utils/portfolio_model.dart';
import 'package:investor_pro/pages/main_page/widgets/portfolio_card.dart';
import 'package:investor_pro/pages/main_page/widgets/portfolio_list.dart';
import 'package:investor_pro/theme.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';
import 'package:provider/provider.dart';

// MainPage Widget
class MainPage extends StatelessWidget {
  const MainPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(
        title: 'Investor Pro',
        showBackButton: false,
      ),
      body: Padding(
        padding: EdgeInsets.all(8.0),
        child: Column(
          children: [
            // Search Section
            SearchSection(),
            SizedBox(
              height: 20,
            ),
            Divider(
              color: AppColors.onPrimary,
            ),
            SizedBox(height: 20),
            CustomAppBar(
              title: 'My Portfolios',
              showBackButton: false,
              transparentBackGround: true,
              actions: [
                IconButton(
                  icon: Icon(Icons.add),
                  onPressed: () {
                    // TODO: Implement portfolio addition logic
                  },
                ),
              ],
            ),
            SizedBox(height: 15),
            Expanded(child: PortfolioList()),
          ],
        ),
      ),
    );
  }
}

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
