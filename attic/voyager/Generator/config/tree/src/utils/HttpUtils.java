package utils;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URLEncoder;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONObject;

import android.util.Log;

/**
 * 
 * @author dryganets
 * 
 */
public class HttpUtils {

	private static final String TAG = "HttpUtils";

	public static JSONObject executeJSONRequest(final String url,
			String[] names, String[] values) {
		return executeJSONRequest(formatUrl(url, names, values));
	}

	public static String executeRequest(final String url) {
		String result = null;
		HttpClient client = new DefaultHttpClient();
		HttpUriRequest request = new HttpGet(url);
		try {
			HttpResponse response = client.execute(request);
			HttpEntity entity = response.getEntity();
			InputStream input = entity.getContent();
			DataInputStream data = new DataInputStream(input);
			result = readAll(data);
		} catch (Exception e) {
			Log.e("HttpUtils", Log.getStackTraceString(e));
		}
		return result;
	}

	public static HttpResponse executeHttpRequest(HttpClient client,
			final String url) {
		if (client == null) {
			client = new DefaultHttpClient();
		}

		HttpUriRequest request = new HttpGet(url);
		HttpResponse response = null;
		try {
			response = client.execute(request);
		} catch (Exception e) {
			Log.e(TAG, Log.getStackTraceString(e));
		}
		return response;
	}

	public static HttpResponse executeHttpRequest(final String url) {
		return executeHttpRequest(null, url);
	}

	public static JSONObject executeJSONRequest(HttpClient client,
			final String url) {
		JSONObject result = null;
		HttpResponse response = executeHttpRequest(client, url);
		if (response != null) {
			try {
				HttpEntity entity = response.getEntity();
				InputStream input = entity.getContent();
				DataInputStream data = new DataInputStream(input);
				String line = readAll(data);
				result = new JSONObject(line);
			} catch (Exception e) {
				Log.e(TAG, Log.getStackTraceString(e));
			}
		}
		return result;
	}

	public static JSONObject executeJSONRequest(final String url) {
		return executeJSONRequest(null, url);
	}

	/**
	 * Create url from string
	 * 
	 * @param urlBase
	 * @param names
	 * @param values
	 * @return
	 */
	public static String formatUrl(final String urlBase, String[] names,
			String[] values) {
		if ((names != null && values != null) && names.length != values.length) {
			throw new IllegalArgumentException("Illegal names/values length");
		}
		StringBuilder result = new StringBuilder(urlBase);
		int length = 0;

		if (names != null) {
			length = names.length;
		}

		for (int i = 0; i < length; i++) {
			if (i == 0) {
				result.append("?");
			}
			result.append(URLEncoder.encode(names[i])).append("=").append(
					URLEncoder.encode(values[i]));

			if (i != length - 1) {
				result.append("&");
			}
		}
		return result.toString();
	}

	private static final String readAll(InputStream in) throws IOException {
		StringBuffer line = new StringBuffer(300);
		do {
			int nextByte = in.read();
			switch (nextByte) {
			case -1:
				if (line.length() == 0)
					return null;
				else
					return line.toString();
			default:
				line.append((char) nextByte);
				break;
			}
		} while (true);
	}
}
