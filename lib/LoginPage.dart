import 'package:chatjust/Admin_Dashboard.dart';
import 'package:chatjust/Student_Dashboard.dart';
import 'package:flutter/material.dart';
import 'AppColors.dart';


class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState()=> _LoginPageState();
}

class _LoginPageState extends State<LoginPage>{
final _formKey= GlobalKey<FormState>();

final TextEditingController _idController =TextEditingController();
final TextEditingController _passwordController =TextEditingController();


bool _isPasswordVisible =false;
bool _isLoading= false;



void _handleMockLogin(){
  if(_formKey.currentState!.validate()){
    setState(() {
      _isLoading=true;
    });
    Future.delayed(const Duration(seconds: 2),// should be removed when the backend is connected 
    (){
      setState(() {
        _isLoading=false;
      });
    });

    final String username=_idController.text.trim();

    if(username.toLowerCase()=="admin"){
    
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (context)=> const AdminDashboard()));


    }
    else{
      
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (context)=> const StudentDashboard()));
    }
    }
    
  }
    @override
    void dispose(){
      _idController.dispose();
      _passwordController.dispose();
      super.dispose();
    }
  @override
Widget build(BuildContext context) {
  return Scaffold(
    backgroundColor: AppColors.ghostWhite,
    body: SafeArea(child: Center(
      child: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: 24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,          
          children: [
            const Icon(Icons.auto_stories_rounded, size: 80, color: AppColors.justBlue,),
            const SizedBox(height: 12,),
            const Text("ChatJust",
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.black45,
            fontSize: 20,
            fontWeight: FontWeight.w400
            ),
            ),
            const SizedBox(
              height: 48,
            ),
            TextFormField(controller: _idController,
            keyboardType: TextInputType.numberWithOptions(),
            decoration: InputDecoration(
              prefixIcon: const Icon(Icons.person_outlined, color: AppColors.justBlue,),
              labelText: 'Student ID',
              labelStyle: const TextStyle(color: Colors.black54),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
              focusedBorder:OutlineInputBorder(borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: AppColors.justBlue,width: 2)),
               ),
               validator: (value){
                if (value == null || value.trim().isEmpty){
                  return 'Please enter your username';
                }
                if(value.length<6){
                  return'Please enter a valid Student ID';
                }
                return null;
               },

            ),

            const SizedBox(height: 20,),
            Form(
              key: _formKey,
              child: Column(
                children: [

            TextFormField(
              controller: _passwordController,
            keyboardType: TextInputType.numberWithOptions(),
            obscureText: !_isPasswordVisible,
            decoration: InputDecoration(
              prefixIcon: const Icon(Icons.lock_outlined, color: AppColors.justBlue,),
              suffixIcon:IconButton(
                 icon: Icon(_isPasswordVisible?Icons.visibility_outlined:Icons.visibility_off_outlined),
                onPressed: (){
                  setState(() {
                    _isPasswordVisible=!_isPasswordVisible;
                  });
                },
              ),
              labelText: 'Password',
              labelStyle: const TextStyle(color: Colors.black54),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
              focusedBorder:OutlineInputBorder(borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: AppColors.justBlue,width: 2)),
               ),
               validator: (value){
                if (value == null || value.isEmpty){
                  return 'Please enter your password';
                }
                if (value.length < 6){
                  return'Password too short';
                }
                return null;
               },


            ),


            const SizedBox(height: 20,),
            ElevatedButton(onPressed: _isLoading?null:_handleMockLogin,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.justBlue,
              foregroundColor: Colors.white,
              padding: EdgeInsets.symmetric(vertical: 16, horizontal: 32),
              disabledBackgroundColor: AppColors.justBlue.withValues(alpha: 0.6),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              elevation: 2
            )
          
            , child: _isLoading? SizedBox(height: 20,
            width: 20,
            child: CircularProgressIndicator(color: Colors.white,
            strokeWidth: 2,),
            ):const Text("LOG IN",
           style: TextStyle(
            fontSize: 16,
            letterSpacing: 1.1,
            fontWeight: FontWeight.bold,
           ),
            ),
            ),
            
                ],
              ),
            )
          ],
        ),
      ),

    )),

  );
}
}