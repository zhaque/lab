package utils;

import ${packageDetailName}.DetailedData;
import ${packageDetailName}.DetailedItem;
import android.app.Activity;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;


public class SingleStockView extends Activity {

	public static final String UIN = "uin";

	private DetailedItem item;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		initActivity();
	}

	@Override
	protected void onResume() {
		super.onResume();
		initActivity();
	}

	private void initActivity() {
		 setContentView(getDetailView().getView());
	}

	private DetailedItem getDetailView() {
		if (item == null) {
			item = new DetailedItem(this, getData());
		}
		return item;
	}

	private DetailedData getData(){
		final Intent intent = getIntent();
		DetailedData data = intent.getParcelableExtra(UIN);
		return data;
	}

}