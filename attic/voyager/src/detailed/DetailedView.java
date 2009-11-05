package detailed;

import com.axhive.R;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.ListView;

public class DetailedView {
	private Activity context;
	private DetailedAdapter adapter;
	private ListView list;

	public DetailedView(Activity context, DetailedAdapter adapter) {
		this.context = context;
		this.adapter = adapter;
		init();
	}

	private View init() {
		LayoutInflater inflator = (LayoutInflater) context
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		LinearLayout rootLayout = (LinearLayout) inflator.inflate(
				R.layout.detailed, null);
		list = new ListView(context);
		//list.setAdapter(adapter);
		rootLayout.addView(list);
		return rootLayout;
	}

	public ListView getList() {
		return list;
	}
}
