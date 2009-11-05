package ${packageListName};

import org.json.JSONObject;

public class JSONData {
	
	<#list widgets as widget>
	 <#if widget.reqname??>
	private String ${widget.name} = "";
	 </#if>
	</#list>
	private JSONObject jsonObject;
	<#list widgets as widget>
	<#if widget.reqname??>
	public String get${widget.name}Text(){
		return ${widget.name};
	}
	public void set${widget.name}Text(String text){
		this.${widget.name} = text;
	}
	 </#if>
	</#list>

	public JSONObject getJSONObject(){
		return jsonObject  ;
	}
	public void setJSONObject(JSONObject object){
		this.jsonObject = object;
	}
}
