package ${packageListName};

import java.util.ArrayList;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import utils.HttpUtils;
import android.content.Context;
import android.os.Handler;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;

public class JSONAdapter extends BaseAdapter {
	private ArrayList<JSONItem> items = new ArrayList<JSONItem>();
	private static final Object lock = new Object();
	private static final String REQUEST = "http://ec2-67-202-7-247.compute-1.amazonaws.com:8983/solr/select/";
	private Context context;
	private Handler handler;
	private static final String TAG = "JSONAdapter";
	public JSONAdapter(Context context) {
		this.context = context;
		handler = new Handler();
	}

	@Override
	public int getCount() {
		return items.size();
	}

	@Override
	public Object getItem(int idx) {
		return items.get(idx);
	}

	@Override
	public long getItemId(int idx) {
		return idx;
	}

	@Override
	public View getView(int idx, View arg1, ViewGroup arg2) {
		return items.get(idx).getView();
	}

	public static JSONObject search(String query) {
		return HttpUtils.executeJSONRequest(HttpUtils.formatUrl(REQUEST,
				new String[] { "wt", "q" }, new String[] { "json", query }));
	}

	public void createList(String searchString) {
		JSONObject json = search(searchString);
		try {
			JSONObject resp = json.getJSONObject("response");
			JSONArray docs = resp.getJSONArray("docs");
			synchronized (lock) {
				items.clear();
			
			for (int i = 0, length = docs.length(); i < length; i++) {
				JSONObject doc = docs.getJSONObject(i);
				JSONData data = new JSONData();
				<#list widgets as widget>
					<#if (widget.reqname)??>
					data.set${widget.name}Text(doc.getString("${widget.reqname}"));
					</#if>
				</#list>
				items.add(new JSONItem(context,data));
			}
			notifyChanges();
			}
		} catch (JSONException e) {
			e.printStackTrace();
		}
	}
	private synchronized void notifyChanges() {
		handler.post(new Runnable() {

			@Override
			public void run() {
				notifyDataSetChanged();
			}

		});
	}
}
