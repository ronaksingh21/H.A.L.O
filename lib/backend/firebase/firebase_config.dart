import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

Future initFirebase() async {
  if (kIsWeb) {
    await Firebase.initializeApp(
        options: const FirebaseOptions(
            apiKey: "AIzaSyDNkZXP35VFn9WwVvRupaxFInSHyZSSHsM",
            authDomain: "caca-c9b2tk.firebaseapp.com",
            projectId: "caca-c9b2tk",
            storageBucket: "caca-c9b2tk.appspot.com",
            messagingSenderId: "522675091669",
            appId: "1:522675091669:web:4bed8edf044db3e9508a5c"));
  } else {
    await Firebase.initializeApp();
  }
}
