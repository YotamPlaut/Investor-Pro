import 'package:flutter/cupertino.dart';
import 'package:investor_pro/models/user_model.dart';

class LoginProvider with ChangeNotifier {

  late final TextEditingController usernameController = TextEditingController();
  late final TextEditingController passwordController = TextEditingController();

  final bool isLoading = false;


  Future? performLogin(
      String username, String password) async {



    // final result = await UserModel.registerUser(user).catchError((error) {
    //   debugPrint(error.toString());
    // });
    // debugPrint('stop');
    // //return user;
    return null;

  }
}
