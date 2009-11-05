package ${packageListName};

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.*;



public class JSONItem {
	private Context context;
	private JSONData data;

	private LinearLayout layout;
	<#list widgets as widget>
	 <#if widget.reqname??>
	private ${widget.type} ${widget.name};
	 </#if>
	</#list>
	public JSONItem(Context context, JSONData data) {
		this.context = context;
		this.data = data;
		init();
	}

	private void init() {
		LayoutInflater inflater = (LayoutInflater) context
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		layout = (LinearLayout)inflater.inflate(R.layout.${layoutName}, null);
		<#list widgets as widget>
		    <#if widget.reqname??>
		    ${widget.name} = (${widget.type})layout.findViewById(R.id.${widget.id});
		    ${widget.name}.setText(data.get${widget.name}Text());
		    </#if>
		</#list>
	}

	public View getView() {
		return layout;
	}

	public JSONData getData() {
		return data;
	}
}
