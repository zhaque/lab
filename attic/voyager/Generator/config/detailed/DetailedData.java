package ${packageDetailName};

import android.os.Parcel;
import android.os.Parcelable;

public class DetailedData {
	
	<#list widgets as widget>
	private String ${widget.name} = "";
	</#list>
	
	protected DetailedData(Parcel in) {
		<#list widgets as widget>
		${widget.name} = in.readString();
		</#list>
	}
	<#list widgets as widget>
	public String get${widget.name}Text(){
		return ${widget.name};
	}
	public void set${widget.name}Text(String text){
		this.${widget.name} = text;
	}
	</#list>

	@Override
	public int describeContents() {
		return 0;
	}

	@Override
	public void writeToParcel(Parcel parc, int arg1) {
		<#list widgets as widget>
		parc.writeString(${widget.name});
		</#list>
	}
	public static final Parcelable.Creator<DetailedData> CREATOR = new Parcelable.Creator<DetailedData>() {
		public DetailedData createFromParcel(Parcel in) {
			return new DetailedData(in);
		}

		@Override
		public DetailedData[] newArray(int size) {
			return new DetailedData[size];
		}
	};
}
