package com.ondocha.ondochaApp.Activity

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.content.Intent
import android.os.Build
import android.util.Log
import android.widget.Toast
import androidx.annotation.RequiresApi
import kotlinx.android.synthetic.main.activity_main.*
import com.google.firebase.firestore.FirebaseFirestore
import com.ondocha.ondochaApp.InitnameDialog
import com.ondocha.ondochaApp.MainVisitorListItem
import com.ondocha.ondochaApp.R
import kotlinx.android.synthetic.main.activity_initialsetname_dialog.*
import kotlinx.android.synthetic.main.activity_setting.*
import java.time.format.DateTimeFormatter
import java.time.LocalDateTime
import java.util.*


class MainActivity : AppCompatActivity() {
    /** 만약 ID를 쓴다면 Root를 ID로 변경 **/
    val db = FirebaseFirestore.getInstance().collection("Root")

    /** 현재 날짜   **/
    val cal = Calendar.getInstance()
    val year = cal.get(Calendar.YEAR).toString()
    var month = (cal.get(Calendar.MONTH)+1).toString()
    var day = cal.get(Calendar.DATE).toString()


    /** 임시 문서 명    year + month + day  **/
    var todaydoc : String = "2020814"


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if(month.toInt() < 10)  { month = "0$month" }
        if(day.toInt() < 10)    { month = "0$day"   }
        //todaydoc = year+month+day


        /**  초기 지점명 설정   **/
        db.document("Name").get().addOnSuccessListener{ document ->
            main_name.text = document["name"].toString()
        }

        if(main_name.getText().toString() == "NAME"){
            val dialog = InitnameDialog(this)

            dialog.showDialog()
            dialog.setOnClickListener(object : InitnameDialog.OnDialogClickListener {
                override fun onClicked(name: String) {
                    main_name.text = name
                    var map = mutableMapOf<String,Any>()
                    map["name"] = name
                    db.document("Name").update(map).addOnSuccessListener { Toast.makeText(this@MainActivity,"지점명이 설정되었습니다.",Toast.LENGTH_SHORT).show() }
                }
            })
        }




        date.setText(year + "년 " + month + "월 " + day + "일")


        get_data()

        /** RecordActivity로 이동 **/
        recordbutton.setOnClickListener {
            val chartIntent = Intent(this, RecordActivity::class.java)
            startActivity(chartIntent)
        }

        /** SettingActivity로 이동 **/
        setting.setOnClickListener {
            val settingIntent = Intent(this, SettingActivity::class.java)
            startActivity(settingIntent)
        }

        /** 새로고침 버튼 **/
        reload.setOnClickListener {

            get_data()
        }

    }



    private fun get_data() {

        val items = mutableListOf<MainVisitorListItem>()
        val adapter = com.ondocha.ondochaApp.MainVisitorAdaptor(items)
        visitor_list.adapter = adapter
        var MainVisitorCount : Int = 0

        db.document("Visitor_Info")   /** 문서명 **/
            .collection(todaydoc)    /** 당일 날짜 **/
            .get()
            .addOnSuccessListener{ result ->
                items.clear()
                for (document in result){
                    var Wtem = document["Atem"].toString()
                    var Ftem = document["Ftem"].toString()
                    var tem : String
                    if(Wtem.toDouble() >= 37.5)   {tem = Ftem}
                    else    {tem = Wtem}
                   val item = MainVisitorListItem( document["Time"].toString(),
                        tem)

                        items.add(0,item)
                    Log.d("AWER", "data : ${document.data}")

                }
                adapter.notifyDataSetChanged()
            }
            .addOnFailureListener { exception ->
                Log.e("MainActivity", "Error getting documents: $exception")
            }




    }

}

