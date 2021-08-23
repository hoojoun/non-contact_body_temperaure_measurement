package com.ondocha.ondochaApp.Activity

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import kotlinx.android.synthetic.main.activity_record.*
import com.ondocha.ondochaApp.R

class RecordActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_record)


        /** 뒤로가기 버튼 **/
        back_record.setOnClickListener {
            finish()
        }


    }
}