import 'package:flutter/material.dart';
import 'package:investor_pro/app_routes.dart';
import 'package:investor_pro/theme.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: AppRouter.router,
      title: 'Flutter Demo',
      theme: appTheme, // Apply the theme
    );
  }
}
