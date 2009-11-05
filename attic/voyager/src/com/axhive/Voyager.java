package com.axhive;

import generated.JSONListView;
import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.ViewGroup;

public class Voyager extends Activity {
	/** Called when the activity is first created. */
	ViewGroup rootLayout = null;
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		createView();
	}

	private void createView() {
		LayoutInflater inflator = (LayoutInflater) this
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		rootLayout = (ViewGroup) inflator
				.inflate(R.layout.main, null);
		JSONListView jlistView = new JSONListView(this);
		rootLayout.addView(jlistView.getView());
		setContentView(rootLayout);
	}
}