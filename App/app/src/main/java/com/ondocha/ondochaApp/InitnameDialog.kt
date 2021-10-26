package com.ondocha.ondochaApp

import android.app.Dialog
import android.content.Context
import android.view.WindowManager
import android.widget.EditText
import kotlinx.android.synthetic.main.activity_initialsetname_dialog.*

class InitnameDialog(context: Context) {
    private val dialog = Dialog(context)
    private lateinit var onClickListener: OnDialogClickListener

    fun setOnClickListener(listener: OnDialogClickListener)
    {
        onClickListener = listener
    }

    fun showDialog()
    {
        dialog.setContentView(R.layout.activity_initialsetname_dialog)
        dialog.window!!.setLayout(WindowManager.LayoutParams.WRAP_CONTENT, WindowManager.LayoutParams.WRAP_CONTENT)
        dialog.setCancelable(false)
        dialog.show()

        val setinitname = dialog.findViewById<EditText>(R.id.initName)

        dialog.set_initName.setOnClickListener {
            onClickListener.onClicked(setinitname.text.toString())
            dialog.dismiss()
        }

    }

    interface OnDialogClickListener
    {
        fun onClicked(name: String)
    }
}