package com.example.appcmup.ui.main;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.example.appcmup.MainActivity;
import com.example.appcmup.R;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthEmailException;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.HashMap;
import java.util.Map;


public class Register_screen extends AppCompatActivity {

    private Button mBack2, mRegister;
    private EditText mEmail, mPassword, mName;
    private FirebaseAuth firebaseAuth;
    private FirebaseAuth.AuthStateListener firebaseAuthStateListener;
    private String emailPattern = "[a-zA-Z0-0._-]+@[a-z]+\\.+[a-z]+";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.register_menu);

        mBack2 = (Button) findViewById(R.id.login_screen2);
        mRegister = (Button) findViewById(R.id.register_screen);
        mEmail = (EditText) findViewById(R.id.mEmail);
        mPassword = (EditText) findViewById(R.id.mPassword);
        mName = (EditText) findViewById(R.id.mName);

        // Initialize Firebase Auth
        firebaseAuth = FirebaseAuth.getInstance();

        firebaseAuthStateListener = new FirebaseAuth.AuthStateListener() {
            @Override
            public void onAuthStateChanged(@NonNull FirebaseAuth firebaseAuth) {

                final FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
                if (user != null && user.isEmailVerified()) {
                    Intent i = new Intent(Register_screen.this, User_screen.class);
                    startActivity(i);
                    finish();
                    return;
                }
            }
        };

        mRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final String email = mEmail.getText().toString();
                final String name = mName.getText().toString();
                final String password = mPassword.getText().toString();

                if (checkInputs(email, name, password)) {
                    firebaseAuth.createUserWithEmailAndPassword(email, password).addOnCompleteListener(Register_screen.this, new OnCompleteListener<AuthResult>() {
                        @Override
                        public void onComplete(@NonNull Task<AuthResult> task) {
                            if (!task.isSuccessful()) {
                                Toast.makeText(Register_screen.this, task.getException().getMessage(), Toast.LENGTH_SHORT).show();
                            } else {
                                firebaseAuth.getCurrentUser().sendEmailVerification().addOnCompleteListener(new OnCompleteListener<Void>() {
                                    @Override
                                    public void onComplete(@NonNull Task<Void> task) {
                                        if (!task.isSuccessful()) {
                                            Toast.makeText(Register_screen.this, "Registration sucessfully. " + "Please check your email for verification. ", Toast.LENGTH_SHORT).show();
                                            String userId = firebaseAuth.getCurrentUser().getUid();
                                            DatabaseReference currentUserDb = FirebaseDatabase.getInstance().getReference().child("Users").child(userId);

                                            Map userInfo = new HashMap<>();
                                            userInfo.put("name", name);
                                            userInfo.put("profileImageUrl", "default");
                                            currentUserDb.updateChildren(userInfo);

                                            mEmail.setText("");
                                            mName.setText("");
                                            mPassword.setText("");

                                            Intent i = new Intent(Register_screen.this, User_screen.class);
                                            startActivity(i);
                                            Toast.makeText(Register_screen.this, "Registration sucessfully. " + "Please check your email for verification. ", Toast.LENGTH_SHORT).show();
                                            finish();
                                            return;
                                        } else {
                                            Toast.makeText(Register_screen.this, task.getException().getMessage(), Toast.LENGTH_SHORT).show();
                                        }
                                    }
                                });
                            }
                        }
                    });
                }

            }

        });


        mBack2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent i = new Intent(Register_screen.this, User_screen.class);
                startActivity(i);
            }
        });

    }

    private boolean checkInputs(String email, String name, String password) {
        if (email.equals("") || name.equals("") || password.equals("")) {
            Toast.makeText(this, "Fill this", Toast.LENGTH_SHORT).show();
            return false;
        }
        if (!email.matches(emailPattern)) {
            Toast.makeText(this, "Invaild email address, enter valid email", Toast.LENGTH_SHORT).show();
            return false;
        }
        return true;
    }


}