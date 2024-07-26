import 'package:flutter/material.dart';
import 'package:investor_pro/navigation/app_routes.dart';
import 'package:investor_pro/session_manager.dart';
import 'package:investor_pro/theme.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<SessionMgr>(
      create: (context) => SessionMgr(),
      child: MaterialApp.router(
        routerConfig: AppRouter.router,
        title: 'Flutter Demo',
        theme: appTheme, // Apply the theme
      ),
    );
  }
}
