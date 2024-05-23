import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';

class SignUpPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: 'Sign Up',
        showBackButton: true,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Sign Up Page'),
            ElevatedButton(
              onPressed: () {
                // Navigate to the main page after sign up
                context.go('/main');
              },
              child: Text('Sign Up'),
            ),
          ],
        ),
      ),
    );
  }
}
