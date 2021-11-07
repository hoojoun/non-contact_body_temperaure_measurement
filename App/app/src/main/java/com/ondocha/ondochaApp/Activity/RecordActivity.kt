package com.ondocha.ondochaApp.Activity

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import com.google.firebase.firestore.FirebaseFirestore
import com.ondocha.ondochaApp.MainVisitorListItem
import kotlinx.android.synthetic.main.activity_record.*
import com.ondocha.ondochaApp.R
import com.ondocha.ondochaApp.RecordInfoListItem
import kotlinx.android.synthetic.main.activity_main.*

class RecordActivity : AppCompatActivity() {

    val db = FirebaseFirestore.getInstance().collection("Root")

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_record)


        /** 뒤로가기 버튼 **/
        back_record.setOnClickListener {
            finish()
        }

        /** 메모 버튼 **/


        val items = mutableListOf<RecordInfoListItem>()
        val adapter = com.ondocha.ondochaApp.RecordInfoAdapter(items)
        record_list.adapter = adapter

        db.document("Suspected").collection("Info").get()
            .addOnSuccessListener { result ->
                items.clear()
                for (document in result){
                    var Wtem = document["Atem"].toString()
                    var Ftem = document["Ftem"].toString()
                    var tem : String
                    if(Wtem.toDouble() >= 37.5)   {tem = Ftem}
                    else    {tem = Wtem}
                    val item = RecordInfoListItem(
                        document["Date"] as String?, document["Time"].toString(),
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