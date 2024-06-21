import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:investor_pro/app_routes.dart';
import 'package:investor_pro/pages/main_page/add_portfolio_dialog.dart';
import 'package:investor_pro/pages/main_page/portfolio_list.dart';
import 'package:investor_pro/providers/main_page_provider.dart';
import 'package:investor_pro/theme.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';
import 'package:investor_pro/widgets/custom_button.dart';
import 'package:provider/provider.dart';

class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<MainPageProvider>(
      create: (_) => MainPageProvider(),
      child: Consumer<MainPageProvider>(
        builder: (context, viewModel, child) {
          return Scaffold(
            appBar: const CustomAppBar(
              title: 'Investor Pro',
              showBackButton: false,
            ),
            body: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  SizedBox(
                    height: 8,
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Expanded(
                        child: CustomButton(
                          onPressed: () => NavigationHelper.navigateTo(
                              context, AppRoutes.explore),
                          title: 'Explore',
                        ),
                      ),
                    ],
                  ),
                  SizedBox(
                    height: 8,
                  ),
                  Divider(
                    color: AppColors.onPrimary,
                  ),
                  //SearchSection(),
                  SizedBox(height: 10),
                  CustomAppBar(
                    title: 'My Portfolios',
                    showBackButton: false,
                    transparentBackGround: true,
                    actions: [
                      IconButton(
                        icon: Icon(Icons.add),
                        onPressed: () {
                          showDialog(
                            context: context,
                            builder: (context) => AddPortfolioDialog(
                              onPortfolioCreated: (portfolioName) {
                                // Call a function in your provider to handle the portfolio creation
                                viewModel.addPortfolio(portfolioName);
                              },
                            ),
                          );
                        },
                      ),
                    ],
                  ),
                  const SizedBox(height: 15),
                  Expanded(child: PortfolioList()),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
