import 'package:flutter/cupertino.dart';
import 'package:investor_pro/models/user_model.dart';

class MainPageProvider with ChangeNotifier {
  late final UserModel? user;

  MainPageProvider() {
    _getUser();
  }

  _getUser() async {
    /// add fetch user function
    // user = await getUser().fromJson();
    //notifyListeners();
  }
}
