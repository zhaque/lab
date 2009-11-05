package ${packageListName};

import utils.SingleStockView;

import ${packageDetailName}.DetailedAdapter;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.AdapterView.OnItemClickListener;




public class JSONListView {
	private Activity context;
	private JSONAdapter adapter;
	private ListView list;
	private EditText text;
	private LinearLayout rootLayout;
	private static final String TAG = "JSONListView";
	
	public JSONListView(Activity context) {
		this.context = context;
	}
	private View init(){
		LayoutInflater inflator = (LayoutInflater) context
		.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		LinearLayout rootLayout = (LinearLayout) inflator.inflate(
		R.layout.${layoutName}, null);
		adapter = new JSONAdapter(context);
		list = (ListView) rootLayout.findViewById(R.id.search_result);//TODO:change to list name
		list.setOnItemClickListener(new OnItemClickListener() {

			@Override
			public void onItemClick(AdapterView<?> adapterview, View view,
					int i, long l) {
				JSONItem item = (JSONItem) adapter.getItem(i);
				JSONData data = item.getData();
				Intent intent = new Intent();
				intent.setClass(context, SingleStockView.class);
				intent.putExtra(SingleStockView.UIN, new DetailedAdapter(data).fillData());
				context.startActivity(intent);
			}

		});
		list.setAdapter(adapter);
		text = (EditText) rootLayout.findViewById(R.id.url_editor);//TODO:change to text field name

		Button button = (Button) rootLayout.findViewById(R.id.search);//TODO:change to button name
		button.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View arg0) {
				String query = text.getText().toString();
				adapter.createList(query);
			}
		});
		return rootLayout;
	}
	public View getView() {
		if (rootLayout == null) {
			return init();
		} else {
			return rootLayout;
		}
	}
}
