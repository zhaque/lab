package generated;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.axhive.R;



public class JSONItem {
	private Context context;
	private JSONData data;

	private LinearLayout layout;
	private TextView Twatch_item_code;
	public JSONItem(Context context, JSONData data) {
		this.context = context;
		this.data = data;
		init();
	}

	private void init() {
		LayoutInflater inflater = (LayoutInflater) context
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		layout = (LinearLayout)inflater.inflate(R.layout.list_item, null);
		Twatch_item_code = (TextView)layout.findViewById(R.id.watch_item_code);
	    Twatch_item_code.setText(data.getTwatch_item_codeText());
	}

	public View getView() {
		return layout;
	}

	public JSONData getData() {
		return data;
	}
}
