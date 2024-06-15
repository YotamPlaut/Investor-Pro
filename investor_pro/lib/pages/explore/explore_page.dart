import 'package:flutter/material.dart';
import 'package:investor_pro/pages/explore/horizonal_asstes_list.dart';
import 'package:investor_pro/providers/explore_page_provider.dart';
import 'package:investor_pro/widgets/custom_search_bar.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';
import 'package:provider/provider.dart';

class ExplorePage extends StatelessWidget {
  const ExplorePage({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<ExplorePageProvider>(
      create: (_) => ExplorePageProvider(),
      child: Consumer<ExplorePageProvider>(
        builder: (context, viewModel, child) {
          return Scaffold(
            appBar: CustomAppBar(
              title: 'Explore',
              showBackButton: true,
            ),
            body: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  // Search Bar
                  const SearchSection(),
                  const SizedBox(height: 20),
                  // Sections
                  Expanded(
                    child: ListView(
                      children: const [
                        HorizontalAssetsList(title: 'Trending Stocks'),
                        SizedBox(height: 20),
                        HorizontalAssetsList(title: 'Popular Funds'),
                        SizedBox(height: 20),
                        HorizontalAssetsList(title: 'Recently Added'),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
