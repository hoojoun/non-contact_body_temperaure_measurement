package com.ondocha.ondochaApp.Activity

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.content.Intent
import com.ondocha.ondochaApp.R
import kotlinx.android.synthetic.main.activity_setting.*

class SettingActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_setting)


        set_name_button.setOnClickListener {
            val set_nameIntent = Intent(this, SetNameActivity::class.java)
            startActivity(set_nameIntent)
        }

        /** 뒤로가기 버튼 **/
        back_setting.setOnClickListener {
            finish()
        }

    }
}