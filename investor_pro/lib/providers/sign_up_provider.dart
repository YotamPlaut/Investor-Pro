import 'package:flutter/cupertino.dart';
import 'package:investor_pro/models/user_model.dart';

class SignUpProvider with ChangeNotifier {
  late final UserModel? user;

  Future<UserModel?>? registerUser(
      String username, String password, String emailAddress) async {
    UserModel user =
        UserModel(username: username, email: emailAddress, password: password);

    final result = await UserModel.registerUser(user).catchError((error) {
      debugPrint(error.toString());
    });
    debugPrint('stop');
    //return user;
  }
}
