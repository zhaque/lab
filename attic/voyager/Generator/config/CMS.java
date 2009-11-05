package com.axhive;

import detailed.DetailedData;
import detailed.DetailedItem;
import generated.JSONAdapter;
import generated.JSONListView;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TableLayout;
import android.widget.TextView;

public class CMS extends Activity {
	private JSONAdapter adapter;
	ViewGroup rootLayout = null;
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		adapter = new JSONAdapter(this);
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