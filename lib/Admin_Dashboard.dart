import 'package:chatjust/LoginPage.dart';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'AppColors.dart';

class AdminDashboard extends StatefulWidget {
  const AdminDashboard({super.key});

  @override
  State<AdminDashboard> createState() => _AdminDashboardState();
}

class _AdminDashboardState extends State<AdminDashboard> {
   final List<String> _databaseFiles = [
      'Just_Student_Handbook.pdf',
      'CIS_Graduation_Requirements.pdf'
    ];
    bool _isUploading=false;
    Future <void> _pickAndUploadFiles() async{
      FilePickerResult? result=await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['pdf'],
        allowMultiple: true
      );
      if(result !=null){
        List<String> validFiles= [];
        List<String> duplicateFiles=[];

        for(var file in result.files){
          if(_databaseFiles.contains(file.name)){
            duplicateFiles.add(file.name);
          }
          else{
            validFiles.add(file.name);
          }
        }

        if(duplicateFiles.isNotEmpty && mounted ){
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content:Text('Skipped ${duplicateFiles.length} duplicate file(s).'), 
          backgroundColor: Colors.orangeAccent,
          duration: const Duration(seconds: 4),
          ),
          );
        }
        if (validFiles.isEmpty){
          return;
        }

        setState(() {
          _isUploading=true;
        });

        await Future.delayed(const Duration(seconds: 3));

        if(mounted){
          setState(() {
            _databaseFiles.addAll(validFiles);
            _isUploading=false;

          });

          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Success: ${validFiles.length} files added to the Knowledge Base.'),
            backgroundColor: AppColors.justBlue,));
        }
      }
    }
  @override
  Widget build(BuildContext context) {
   
    return Scaffold(
      backgroundColor: AppColors.ghostWhite,
      appBar: AppBar(
        backgroundColor:AppColors.justBlue,
        title:const Text( 'Admin Portal',
        style: TextStyle(color: Colors.white,
        fontWeight: FontWeight.bold),
        ),
        iconTheme: const IconThemeData(color: Colors.white),
        
      ),
      drawer: Drawer(
        child: Column(
          children: [
            DrawerHeader(decoration: BoxDecoration(color: AppColors.justBlue),
            child: Center(
              child: Text('Active Database Files',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.white,

              ),
              ),
            ),
            ),
            Expanded(child: ListView.builder(
              itemCount: _databaseFiles.length,
              itemBuilder: (context, index) {
                return ListTile(
                  leading: const Icon(Icons.picture_as_pdf,
                  color: AppColors.errorRed,),
                  title: Text(_databaseFiles[index]),
                );

              },
            ),
            ),
            ElevatedButton(onPressed:()=>Navigator.pushReplacement(context, MaterialPageRoute(builder: (context)=>LoginPage())),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.errorRed,
                foregroundColor: Colors.white,
                padding: EdgeInsets.all(8),
                elevation: 2,

              ),
              child: Text('LOG OUT',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                letterSpacing: 1.1,

              ),
              ),
              
)
          ],
          
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.cloud_upload_outlined, size: 100, color: AppColors.electricViolet,),
            const SizedBox(height: 20,),
            const Text(
              'Upload University Documentation',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: AppColors.slateCharcoal,
                ),
            ),
            const SizedBox(height: 24,),
            const Text('Files must be in PDF form. Duplicates will be rejected',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey
            ),
            ),
            const SizedBox(height: 32,),
            ElevatedButton.icon(onPressed: _isUploading? null: _pickAndUploadFiles, 
            icon: _isUploading
            ? const SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2,)
              )
              :const Icon(Icons.add_circle_outline, color: Colors.white,),
            label: Text(_isUploading?
            'Processing':
            'Select PDF',
            style: TextStyle(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.bold
            ),
            ),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.electricViolet,
              padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 20),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8))
            ),
            ),

          ],
        ),
      ),
    );
  }
}