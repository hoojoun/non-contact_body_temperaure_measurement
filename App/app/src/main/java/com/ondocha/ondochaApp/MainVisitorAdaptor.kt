package com.ondocha.ondochaApp

import android.view.View
import android.view.ViewGroup
import android.view.LayoutInflater
import android.widget.BaseAdapter
import android.widget.TextView


class MainVisitorAdaptor(val items: MutableList<MainVisitorListItem>): BaseAdapter() {


    override fun getCount(): Int = items.size

    override fun getItem(position: Int): Any = items[position]

    override fun getItemId(position: Int): Long = position.toLong()

    override fun getView(position: Int, view: View?, parent: ViewGroup?): View {

        val visitorview: View = LayoutInflater.from(parent?.context).inflate(R.layout.visitor_list_item, null)
        //var convertView = view
        //if (convertView == null) convertView = LayoutInflater.from(parent?.context).inflate(R.layout.visitor_list_item, parent, false)

        val visitorlist : MainVisitorListItem = items[position]
        val count = visitorview.findViewById<TextView>(R.id.text_count)
        val time = visitorview.findViewById<TextView>(R.id.text_time)
        val temperature = visitorview.findViewById<TextView>(R.id.text_temperature)
        var size = items.size
        count.text = size.toString()
        time.text = visitorlist.time
        temperature.text = visitorlist.Ftem.toString()
        if(visitorlist.Ftem.toString().toDouble() >= 37.5){
            visitorview.setBackgroundResource(R.color.warning)
        }
        return visitorview
    }


}