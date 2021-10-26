package com.ondocha.ondochaApp

import android.view.View
import android.view.ViewGroup
import android.view.LayoutInflater
import android.widget.BaseAdapter
import android.widget.TextView

class RecordInfoAdapter (val items: MutableList<RecordInfoListItem>): BaseAdapter() {
    override fun getCount(): Int = items.size

    override fun getItem(position: Int): Any = items[position]

    override fun getItemId(position: Int): Long = position.toLong()

    override fun getView(position: Int, view: View?, parent: ViewGroup?): View {

        val visitorview: View = LayoutInflater.from(parent?.context).inflate(R.layout.record_list_item, null)

        val Recordlist : RecordInfoListItem = items[position]
        val date = visitorview.findViewById<TextView>(R.id.text_date)
        val time = visitorview.findViewById<TextView>(R.id.text_time)
        val temperature = visitorview.findViewById<TextView>(R.id.text_temperature)

        var hour = Integer.parseInt(Recordlist.time) / 100
        var min = Integer.parseInt(Recordlist.time) % 100

        date.text = Recordlist.date.toString()
        time.text = (hour.toString() + " : " + min.toString())
        temperature.text = Recordlist.Ftem.toString()

        return visitorview
    }
}