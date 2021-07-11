package com.example.appcmup.ui.main;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.example.appcmup.MainActivity;
import com.example.appcmup.R;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;


public class Login_screen extends AppCompatActivity {

    private static final String TAG = "LoginActivity";
    private Button mLogin2, mBack2;
    private boolean loginBtnClicked;
    private EditText mEmail, mPassword;
    private FirebaseAuth firebaseAuth;
    private ProgressBar mProgressBar;
    private FirebaseAuth.AuthStateListener firebaseAuthStateListener2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login_menu);

        loginBtnClicked = false;
        mBack2 = (Button) findViewById(R.id.back_login);
        mProgressBar = findViewById(R.id.progressBar);
        mProgressBar.setVisibility(View.GONE);

        // Initialize Firebase Auth
        firebaseAuth = FirebaseAuth.getInstance();

        //Firebase
        mEmail = findViewById(R.id.email2);
        mPassword = findViewById(R.id.password2);
        mLogin2 = findViewById(R.id.login);

        mLogin2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                loginBtnClicked = true;
                mProgressBar.setVisibility(View.VISIBLE);
                if (mEmail.getText().toString().isEmpty()) {
                    mEmail.setError("Introduza o e-mail");
                    return;
                } else {
                    mEmail.setError(null);
                }
                if (mPassword.getText().toString().isEmpty()) {
                    mPassword.setError("Introduza a password");
                    return;
                } else {
                    mPassword.setError(null);
                }
                firebaseAuth.signInWithEmailAndPassword(mEmail.getText().toString(), mPassword.getText().toString()).addOnCompleteListener(new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            Intent i = new Intent(Login_screen.this, MainActivity.class);
                            Toast.makeText(Login_screen.this, "Login efetuado com sucesso", Toast.LENGTH_SHORT).show();
                            startActivity(i);
                            finish();
                        } else {
                            Toast.makeText(Login_screen.this, "As credencias estão incorretas", Toast.LENGTH_SHORT).show();
                        }
                        mProgressBar.setVisibility(View.INVISIBLE);
                    }
                });
            }
        });

        mBack2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent i = new Intent(Login_screen.this, User_screen.class);
                startActivity(i);
            }
        });

    }

    /*protected void onStart() {
        super.onStart();
        firebaseAuth.addAuthStateListener(firebaseAuthStateListener2);
    }

    protected void onStop() {
        super.onStop();
        firebaseAuth.removeAuthStateListener(firebaseAuthStateListener2);
    }

    public void onBackPressed() {
        Intent i = new Intent(Login_screen.this, User_screen.class);
        startActivity(i);
        finish();
    }*/


}