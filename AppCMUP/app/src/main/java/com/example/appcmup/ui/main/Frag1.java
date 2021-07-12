package com.example.appcmup.ui.main;


import android.Manifest;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.example.appcmup.R;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

import de.hdodenhof.circleimageview.CircleImageView;

public class Frag1 extends Fragment {

    private FirebaseAuth.AuthStateListener mAuthStateListener;
    private Button mSignOut;
   /* private CircleImageView ProfileImage;
    String[] permissions = {Manifest.permission.READ_EXTERNAL_STORAGE};
    int REQUEST_CODE = 1123;
    boolean isPermissionGranted = false;*/

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.frag1_layout, container, false);

        /*ProfileImage = (CircleImageView) view.findViewById(R.id.image_galery);

        ProfileImage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent gallery = new Intent();
                gallery.setType("image/*");
                gallery.setType(Intent.ACTION_GET_CONTENT);

                startActivityForResult(Intent.createChooser(gallery, "Select Picture"), PICK_IMAGE);
            }
        });*/

        mSignOut = (Button) view.findViewById(R.id.btnlogout);

        setupFirebaseListener();

        mSignOut.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                FirebaseAuth.getInstance().signOut();
            }
        });

        return view;
    }

    private void setupFirebaseListener() {
        mAuthStateListener = new FirebaseAuth.AuthStateListener() {
            @Override
            public void onAuthStateChanged(@NonNull FirebaseAuth firebaseAuth) {
                FirebaseUser user = firebaseAuth.getCurrentUser();
                if (user != null) {
                } else {
                    Toast.makeText(getActivity(), "Signed out", Toast.LENGTH_SHORT).show();
                    Intent intent = new Intent(getActivity(), User_screen.class);
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                    startActivity(intent);
                }
            }
        };
    }


    @Override
    public void onStart() {
        super.onStart();
        FirebaseAuth.getInstance().addAuthStateListener(mAuthStateListener);
    }

    @Override
    public void onStop() {
        super.onStop();
        if (mAuthStateListener != null) {
            FirebaseAuth.getInstance().removeAuthStateListener(mAuthStateListener);
        }
    }

 /*   @Override
    public void onActivityResult(int requestCode, int resulCode, Intent data) {
        super.onActivityResult(requestCode, resulCode, data);

        if (requestCode == 1) {
            Uri uri = data.getData();
            ProfileImage.setImageURI(uri);
            Toast.makeText(getActivity(), "Login efetuado com sucesso", Toast.LENGTH_SHORT).show();
        }

    }*/

}
