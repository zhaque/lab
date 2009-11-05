package detailed;

import com.axhive.R;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.*;

public class DetailedItem {
	private Context context;
	private DetailedData data;

	private LinearLayout layout;
	private TextView Tdetails_id;
	private TextView Tdetails_title;

	public DetailedItem(Context context, DetailedData data) {
		this.context = context;
		this.data = data;
		init();
	}

	private void init() {
		LayoutInflater inflater = (LayoutInflater) context
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		layout = (LinearLayout) inflater.inflate(R.layout.detailed, null);

		Tdetails_id = (TextView) layout.findViewById(R.id.details_id);
		Tdetails_id.setText(data.getTdetails_idText());
		Tdetails_title = (TextView) layout.findViewById(R.id.details_title);
		Tdetails_title.setText(data.getTdetails_titleText());
	}

	public View getView() {
		return layout;
	}

	public DetailedData getData() {
		return data;
	}
}
