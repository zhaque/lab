package detailed;

import generated.JSONData;

import org.json.JSONException;
import org.json.JSONObject;

public class DetailedAdapter {
	private JSONData externalData;

	public DetailedAdapter(JSONData data) {
		this.externalData = data;
	}

	public DetailedData fillData() {
		DetailedData data = new DetailedData();
		JSONObject itemData = externalData.getJSONObject();
		try {
			data.setTdetails_idText(itemData.getString("id"));
			data.setTdetails_titleText(itemData.getString("title"));
		} catch (JSONException e) {
			e.printStackTrace();
		}
		return data;
	}

}
