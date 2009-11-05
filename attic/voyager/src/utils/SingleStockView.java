package utils;

import detailed.DetailedData;
import detailed.DetailedItem;
import android.app.Activity;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;

/**
 * 
 * @author dryganets
 * 
 */
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

//	@Override
//	public void onConfigurationChanged(Configuration newConfig) {
//		super.onConfigurationChanged(newConfig);
//	}

//	@Override
//	protected void onDestroy() {
//		super.onDestroy();
//	}

	private void initActivity() {
		 setContentView(getChartView().getView());
	}

	private DetailedItem getChartView() {
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