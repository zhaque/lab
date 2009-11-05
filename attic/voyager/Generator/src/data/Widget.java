package data;

public class Widget {
	String id;
	String type;
	String name;
	String reqname;

	public Widget(String id, String type, String name, String reqname) {
		super();
		this.id = id;
		this.type = type;
		this.name = name;
		this.reqname = reqname;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getReqname() {
		return reqname;
	}

	public void setReqname(String reqname) {
		this.reqname = reqname;
	}
}
