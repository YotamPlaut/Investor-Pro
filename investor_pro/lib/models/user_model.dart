import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

UserModel userModelFromJson(String str) => UserModel.fromJson(json.decode(str));

String welcomeToJson(UserModel data) => json.encode(data.toJson());

class UserModel {
  String username;
  String email;
  String password;

  UserModel({
    required this.username,
    required this.email,
    required this.password,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) => UserModel(
        username: json["username"],
        email: json["email"],
        password: json["password"],
      );

  Map<String, dynamic> toJson() => {
        "username": username,
        "email": email,
        "password": password,
      };

  static const String baseUrl = 'http://10.100.102.13:5000';

  static Future<String> registerUser(UserModel user) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/create-new-account'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(user.toJson()),
          )
          .timeout(const Duration(seconds: 5));

      if (response.statusCode == 201) {
        return response.body;
      } else {
        throw http.ClientException(
            'Failed to register user: ${response.reasonPhrase}');
      }
    } on http.ClientException catch (e) {
      throw http.ClientException('Network error: ${e.message}');
    } on TimeoutException {
      throw http.ClientException('Request timed out');
    } catch (e) {
      throw http.ClientException('Unexpected error: $e');
    }
  }
}
