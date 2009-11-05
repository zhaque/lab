package data;

import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringWriter;
import java.io.Writer;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;
import org.xmlpull.v1.XmlPullParserFactory;

import freemarker.template.Configuration;
import freemarker.template.SimpleHash;
import freemarker.template.Template;
import freemarker.template.TemplateException;

public class Generator {

	private static final String packageDetailName = "detailed";
	private static final String packageListName = "listview";

	/**
	 * app <source dir> <output dir> <main xml> <detail xml>
	 * 
	 * @param args
	 */

	public static void main(String[] args) {
		if (args.length < 4) {
			System.out.println("too few args");
			return;
		}
		String templatePath = args[0];
		String outputPath = args[1];
		String listPath = args[2];// main view
		String detailedPath = args[3];// detailed view
		if (!listPath.endsWith("xml") || !detailedPath.endsWith("xml")) {
			return;
		}
		System.out.println("processing " + listPath);
		String layoutName = listPath.substring(0, listPath.lastIndexOf("."));
		String detailedName = detailedPath.substring(0, detailedPath
				.lastIndexOf("."));

		Configuration config = new Configuration();
		try {
			config.setDirectoryForTemplateLoading(new File("."));
			config.setTemplateUpdateDelay(2);
			// --------------listview----------------
			String inputLV = templatePath + File.separator + packageListName;
			String outputLV = outputPath + File.separator + "src"
					+ File.separator + packageListName;
			generateDir(config, inputLV, outputLV, listPath, layoutName);
			inputLV = templatePath + File.separator + packageDetailName;
			outputLV = outputPath + File.separator + "src"
					+ File.separator + packageDetailName;
			generateDir(config, inputLV, outputLV, listPath, detailedName);
			// --------------detailview----------------

		} catch (IOException e) {
			e.printStackTrace();
		} catch (TemplateException e) {
			e.printStackTrace();
		}

	}
	private void copyfile(String from, String to){
		
	}
	
	private static void generateDir(Configuration config,String inputDir, String outputDir, String xmlPath,String layoutName) throws IOException, TemplateException {
		File f = new File(outputDir);
		if (!f.exists()) {
			f.mkdirs();
		}
		File input = new File(inputDir);
		if (!input.exists()) {
			throw new IllegalArgumentException("");
		}
		List<Widget> widgets = parseXML(xmlPath);
		String[] files = input.list();
		for (int i = 0; i < files.length; i++) {
			Template t = config.getTemplate(inputDir + File.separator
					+ files[i]);
			generate(t, new FileWriter(new File(outputDir + File.separator
					+ files[i])), widgets, layoutName);
		}
	}

	private static List<Widget> parseXML(String filePath) {
		List<Widget> widgets = null;
		try {
			XmlPullParserFactory factory = XmlPullParserFactory.newInstance(
					System.getProperty(XmlPullParserFactory.PROPERTY_NAME),
					null);
			factory.setNamespaceAware(true);
			XmlPullParser xpp = factory.newPullParser();
			xpp.setInput(new FileReader(filePath));
			widgets = processDocument(xpp);
		} catch (XmlPullParserException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return widgets;
	}

	public static List<Widget> processDocument(XmlPullParser xpp)
			throws XmlPullParserException, IOException {
		List<Widget> widgets = new ArrayList<Widget>();
		int eventType = xpp.getEventType();
		while (eventType != XmlPullParser.END_DOCUMENT) {
			if (eventType == XmlPullParser.START_DOCUMENT) {
				// System.out.println("Start document");
			} else if (eventType == XmlPullParser.END_DOCUMENT) {
				// System.out.println("End document");
			} else if (eventType == XmlPullParser.START_TAG) {
				// System.out.println("Start tag " + xpp.getName());
				// System.out.println(xpp.getName() + " attributes: ");
				// for (int i = 0, length = xpp.getAttributeCount(); i < length;
				// i++) {
				// System.out.println(xpp.getAttributeName(i) + " = "
				// + xpp.getAttributeValue(i));
				// }
				String tagName = xpp.getName();
				if (tagName.toLowerCase().contains("layout")) {// layout def
					// skip now, TODO: add collection support
				} else {
					HashMap<String, String> attributes = new HashMap<String, String>();
					for (int i = 0, length = xpp.getAttributeCount(); i < length; i++) {
						attributes.put(xpp.getAttributeName(i), xpp
								.getAttributeValue(i));
					}
					if (attributes.containsKey("id")) {
						String id = attributes.get("id");// @+id/widgetname
						// id = id.substring(id.indexOf("/") + 1);// widgetname
						String type = tagName;
						// String name = tagName.substring(0, 1) + id;
						String name = getPreparedName(id);
						String text = attributes.get("text");
						String reqName = attributes.get("reqname");
						widgets.add(new Widget(id, type, name, reqName));
					}
				}
			} else if (eventType == XmlPullParser.END_TAG) {
				// System.out.println("End tag " + xpp.getName());
			} else if (eventType == XmlPullParser.TEXT) {
				// System.out.println("Text " + xpp.getText());
			}
			eventType = xpp.next();
		}
		return widgets;
	}

	private static String getPreparedName(String name) {
		if (name == null) {
			return "null";// or ""
		}
		int slash = name.indexOf("/");
		if (slash == -1) {
			return name;
		}
		String id = name.substring(slash + 1);
		return id;
	}

	private static void generate(Template t, Writer w, List<Widget> widgets,
			String layoutName) throws TemplateException, IOException {
		SimpleHash context = new SimpleHash();
		context.put("widgets", widgets);
		context.put("packageDetailName", packageDetailName);
		context.put("packageListName", packageListName);
		context.put("layoutName", layoutName);
		t.process(context, w);
	}
}
