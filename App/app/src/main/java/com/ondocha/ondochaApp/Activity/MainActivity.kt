package com.ondocha.ondochaApp.Activity

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.content.Intent
import android.util.Log
import androidx.appcompat.app.AlertDialog
import java.util.Calendar
import kotlinx.android.synthetic.main.activity_main.*
import com.google.firebase.firestore.FirebaseFirestore
import com.ondocha.ondochaApp.MainVisitorListItem
import com.ondocha.ondochaApp.R
import java.lang.Exception


class MainActivity : AppCompatActivity() {
    val db = FirebaseFirestore.getInstance()

    /** 현재 날짜   **/
    val cal = Calendar.getInstance()
    val year = cal.get(Calendar.YEAR).toString()
    val month = (cal.get(Calendar.MONTH)+1).toString()
    val day = cal.get(Calendar.DATE).toString()
    val todaycollection = year + month + day


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        db.collection("Name").document("name").get().addOnSuccessListener { document ->
            if(document["name"].toString() == "NAME"){
                AlertDialog.Builder(this)
                    .setTitle("지점명을 입력하세요.")
                    .setView
            }
        }

        main_name.setText("name")
        /** 파베에서 가져오기    **/


        date.setText(year + "년 " + month + "월 " + day + "일")


        get_data()

        /** ChartActivity로 이동 **/
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
    //데이터 가져오는 함수
    private fun get_data() {
        val cusinfo = db.collection(todaycollection)

        val items = mutableListOf<MainVisitorListItem>()
        val adapter = com.ondocha.ondochaApp.MainVisitorAdaptor(items)
        visitor_list.adapter = adapter


        db.collection(todaycollection)
            .get()
            .addOnSuccessListener { result ->
                items.clear()
                for (document in result){
                    val item = MainVisitorListItem(0, document["time"].toString(),
                        document["Ftem"].toString())
                    if(document["Ftem"].toString() >= "37.5"){
                        //visitor_list_item.setBackgroundResource(R.color.warning)
                    }
                    items.add(item)
                }
                adapter.notifyDataSetChanged()
            }
            .addOnFailureListener { exception ->
                Log.e("MainActivity","Error getting documents: $exception")
            }





    }

}

