package ${packageDetailName};

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.*;

public class DetailedItem {
	private Context context;
	private DetailedData data;

	private LinearLayout layout;
	<#list widgets as widget>
	private ${widget.type} ${widget.name};
	</#list>

	public DetailedItem(Context context, DetailedData data) {
		this.context = context;
		this.data = data;
		init();
	}

	private void init() {
		LayoutInflater inflater = (LayoutInflater) context
				.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		layout = (LinearLayout) inflater.inflate(R.layout.detailed, null);
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

	public DetailedData getData() {
		return data;
	}
}
