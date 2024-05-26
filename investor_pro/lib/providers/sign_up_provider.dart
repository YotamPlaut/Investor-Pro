import 'package:flutter/cupertino.dart';
import 'package:investor_pro/models/user_model.dart';

class SignUpProvider with ChangeNotifier {
  late final UserModel? user;

  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController confirmPasswordController =
      TextEditingController();

  bool isLoading = false;

  Future? registerUser(
      String username, String password, String emailAddress) async {
    isLoading = true;
    notifyListeners();

    UserModel user =
        UserModel(username: username, email: emailAddress, password: password);

    debugPrint('stop');
    try {
      await UserModel.registerUser(user);
    } catch (err) {
      isLoading = false;
      notifyListeners();
      rethrow;
    }

    isLoading = false;
    notifyListeners();
  }
}
