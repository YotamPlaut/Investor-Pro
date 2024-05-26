import 'package:flutter/material.dart';
import 'package:awesome_snackbar_content/awesome_snackbar_content.dart';

class SnackBarHelper {
  // Private constructor
  SnackBarHelper._();

  // Public method to show snackbar
  static void showSnackBar({
    required BuildContext context,
    required String title,
    required String message,
    required ContentType
        contentType, // Use ContentType from awesome_snackbar_content
  }) {
    final snackBar = SnackBar(
      content: AwesomeSnackbarContent(
        title: title,
        message: message,
        contentType: contentType,
      ),
      backgroundColor: Colors.transparent,
      behavior: SnackBarBehavior.floating,

      elevation: 0,
    );

    ScaffoldMessenger.of(context).showSnackBar(snackBar);
  }
}
