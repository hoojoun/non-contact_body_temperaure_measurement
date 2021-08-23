package com.ondocha.ondochaApp.Activity

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.ondocha.ondochaApp.R
import kotlinx.android.synthetic.main.activity_setname.*

class SetNameActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_setname)

        current_name.setText("Name")    /** 파베에서 가져오기    **/
        /** 뒤로가기 버튼 **/
        back_settingname.setOnClickListener {
            finish()
        }
        save_name.setOnClickListener{
            // '파베 지점명' = change_name.text.toString()
        }

    }
}