import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:go_router/go_router.dart';
import 'package:investor_pro/app_routes.dart';
import 'package:investor_pro/providers/login_page_provider.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';
import 'package:investor_pro/theme.dart';
import 'package:investor_pro/widgets/custom_button.dart';
import 'package:provider/provider.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<LoginProvider>(
      create: (_) => LoginProvider(),
      child: Consumer<LoginProvider>(
        builder: (context, viewModel, child) {
          return Scaffold(
            backgroundColor: AppColors.background,
            body: SingleChildScrollView(
              child: Center(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 50),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const SizedBox(
                        height: 20,
                      ),
                      Image.asset(
                        height: 400,
                        width: 400,
                        'assets/images/investor_pro_huge.png',
                        fit: BoxFit.cover,
                      ),
                      TextField(
                        controller: viewModel.usernameController,
                        decoration: const InputDecoration(
                          hintText: 'username',
                          hintStyle: TextStyle(color: AppColors.onPrimary),
                        ),
                        cursorColor: AppColors.secondary,
                      ),
                      const SizedBox(
                        height: 15,
                      ),
                      TextField(
                        controller: viewModel.passwordController,
                        decoration: const InputDecoration(
                          hintText: 'password',
                          hintStyle: TextStyle(color: AppColors.onPrimary),
                        ),
                        cursorColor: AppColors.secondary,
                      ),
                      const SizedBox(
                        height: 70,
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Expanded(
                              child: CustomButton(
                                  title: 'Login', onPressed: () => {})),
                        ],
                      ),
                      const SizedBox(
                        height: 10,
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Expanded(
                              child: CustomButton(
                                  title: 'Sign-up',
                                  onPressed: () => NavigationHelper.navigateTo(
                                      context, AppRoutes.signUp))),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
