import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        // On aligne le fond de l'application sur ton noir premium #09090B
        scaffoldBackgroundColor: const Color(0xFF09090B),
      ),
      home: const StreamlitWrapperScreen(),
    );
  }
}

class StreamlitWrapperScreen extends StatefulWidget {
  const StreamlitWrapperScreen({super.key});

  @override
  State<StreamlitWrapperScreen> createState() => _StreamlitWrapperScreenState();
}

class _StreamlitWrapperScreenState extends State<StreamlitWrapperScreen> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();
    // Initialisation et configuration du moteur web
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted) // INDISPENSABLE pour Streamlit
      ..setBackgroundColor(const Color(0xFF09090B))
      ..loadRequest(Uri.parse('https://nbabet-uefv9n5suppdeum9icjsnj.streamlit.app/')); // 👈 TA PAGE ICI
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: WebViewWidget(controller: _controller),
      ),
    );
  }
}