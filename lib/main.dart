import 'package:flutter/material.dart';
import 'LoginPage.dart';
import 'AppColors.dart';


void main (){
  
  runApp( const ChatJust());
  
}

class ChatJust extends StatelessWidget {
  const ChatJust({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      
      title: 'ChatJust',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: AppColors.justBlue,
        scaffoldBackgroundColor: AppColors.ghostWhite,
        colorScheme: ColorScheme.fromSeed(
          seedColor: AppColors.justBlue,
          primary: AppColors.justBlue,
          secondary: AppColors.electricViolet),
          appBarTheme: const AppBarTheme(backgroundColor: AppColors.justBlue,
          foregroundColor: Colors.white,),
        useMaterial3: true,
      ),
      home: const LoginPage(),
    );
  }
}
