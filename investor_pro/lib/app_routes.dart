import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:investor_pro/pages/explore/explore_page.dart';
import 'package:investor_pro/pages/login_page.dart';
import 'package:investor_pro/pages/main_page/main_page.dart';
import 'package:investor_pro/pages/sign_up_page.dart';

enum AppRoutes {
  login,
  signUp,
  main,
  explore;

  String get path {
    switch (this) {
      case AppRoutes.login:
        return '/';
      case AppRoutes.signUp:
        return '/signup';
      case AppRoutes.main:
        return '/main';
      case AppRoutes.explore:
        return '/explore';
    }
  }
}

class AppRouter {
  static GoRouter router = GoRouter(
    initialLocation: AppRoutes.login.path,
    routes: [
      GoRoute(
        path: AppRoutes.login.path,
        builder: (context, state) => const LoginPage(),
      ),
      GoRoute(
        path: AppRoutes.signUp.path,
        builder: (context, state) => SignUpPage(),
      ),
      GoRoute(
        path: AppRoutes.main.path,
        builder: (context, state) => MainPage(),
      ),GoRoute(
        path: AppRoutes.explore.path,
        builder: (context, state) => ExplorePage(),
      ),
    ],
  );
}

class NavigationHelper {
  static void navigateTo(BuildContext context, AppRoutes route) {
    context.push(route.path);
  }
}
