package detailed;


import android.os.Parcel;
import android.os.Parcelable;

public class DetailedData implements Parcelable {

	private String Tdetails_id = "";
	private String Tdetails_title = "";

	public DetailedData(){
		
	}
	protected DetailedData(Parcel in) {
		Tdetails_id = in.readString();
		Tdetails_title= in.readString();
	}
	public String getTdetails_idText() {
		return Tdetails_id;
	}

	public void setTdetails_idText(String text) {
		this.Tdetails_id = text;
	}

	public String getTdetails_titleText() {
		return Tdetails_title;
	}

	public void setTdetails_titleText(String text) {
		this.Tdetails_title = text;
	}

	@Override
	public int describeContents() {
		return 0;
	}

	@Override
	public void writeToParcel(Parcel arg0, int arg1) {
		arg0.writeString(Tdetails_id);
		arg0.writeString(Tdetails_title);

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
