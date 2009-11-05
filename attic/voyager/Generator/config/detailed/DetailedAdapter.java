package ${packageDetailName};

import org.json.JSONException;
import org.json.JSONObject;

import ${packageListName}.JSONData;

public class DetailedAdapter {
	private JSONData externalData;

	public DetailedAdapter(JSONData data) {
		this.externalData = data;
	}

	public DetailedData prepareData() {
		DetailedData data = new DetailedData();
		JSONObject itemData = externalData.getJSONObject();
		try {
		<#list widgets as widget>
			<#if (widget.reqname)??>
			data.set${widget.name}Text(itemData.getString("${widget.reqname}"));
			</#if>
		</#list>
		} catch (JSONException e) {
			e.printStackTrace();
		}
		return data;
	}
}
