package com.example.helloandroid;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

/**
 * MainActivity - First Assignment Solution
 * 
 * This is the solution for the first Android assignment.
 * This activity displays a welcome message "Hi Android" in the center of the screen.
 * 
 * @author Solution
 * @version 1.0
 */
public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
