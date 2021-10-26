package com.ondocha.ondochaApp.Activity

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Toast
import com.google.firebase.firestore.FirebaseFirestore
import com.ondocha.ondochaApp.R
import kotlinx.android.synthetic.main.activity_setname.*

class SetNameActivity : AppCompatActivity() {
    val db = FirebaseFirestore.getInstance().collection("Root")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_setname)

        db.document("Name").get().addOnSuccessListener { document ->
            current_name.setText(document["name"].toString())
        }

        /** 뒤로가기 버튼 **/
        back_settingname.setOnClickListener {
            finish()
        }
        save_name.setOnClickListener {
            // '파베 지점명' = change_name.text.toString()
            var map = mutableMapOf<String, Any>()
            map["name"] = change_name.getText().toString()
            db.document("Name").update(map).addOnSuccessListener {
                val intent = Intent(this, SettingActivity::class.java)
                startActivity(intent)
                Toast.makeText(this, "지점명이 변경되었습니다.", Toast.LENGTH_SHORT).show()
            }

        }
    }
}