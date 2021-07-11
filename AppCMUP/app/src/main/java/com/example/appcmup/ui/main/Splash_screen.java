package com.example.appcmup.ui.main;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;
import androidx.viewpager.widget.ViewPager;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

import com.example.appcmup.MainActivity;
import com.example.appcmup.R;
import com.google.android.material.tabs.TabLayout;


public class Splash_screen extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.splash_screen_fragment);

        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent i = new Intent(Splash_screen.this, User_screen.class);
                startActivity(i);
                finish();
            }
        }, 2000);

    }


}