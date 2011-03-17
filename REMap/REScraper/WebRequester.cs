using System;
using System.IO;
using System.Net;
using System.Text;
using System.Web;

namespace REScraper {
	public class WebRequester {

		public static string GetWebPage(string url) {
			HttpWebRequest request = WebRequest.Create(url) as HttpWebRequest;
			request.Proxy = WebRequest.GetSystemWebProxy();
			request.Method = "GET";
			request.UserAgent = "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+.NET+CLR+1.1.4322)";
			request.Timeout = -1;
			WebResponse response = request.GetResponse();
			Stream responseStream = response.GetResponseStream();
			responseStream.ReadTimeout = 10000;
			StringBuilder sb = new StringBuilder();
			StreamReader reader = new StreamReader(responseStream);
			try {
				int counter = 0;
				while (!reader.EndOfStream) {// && counter < 180 && sb.Length < 16765) {
					++counter;
					string line = reader.ReadLine();
					sb.Append(line);
				}
				return sb.ToString();
			}
			finally {
				response.Close();
				reader.Close();
			}
		}

		public static string PostAndGetResponse(string url, string postData) {
			HttpWebRequest webRequest = WebRequest.Create(url) as HttpWebRequest;
			webRequest.Method = "POST";
			webRequest.ContentType = "application/x-www-form-urlencoded";

			// write the form values into the request message
			StreamWriter requestWriter = new StreamWriter(webRequest.GetRequestStream());
			requestWriter.Write(HttpUtility.HtmlEncode(postData));
			requestWriter.Close();

			webRequest.UserAgent = "Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+.NET+CLR+1.1.4322)";
			webRequest.Timeout = 10000;
			WebResponse response = webRequest.GetResponse();
			Stream responseStream = response.GetResponseStream();
			responseStream.ReadTimeout = 10000;
			StringBuilder sb = new StringBuilder();
			using (StreamReader reader = new StreamReader(responseStream)) {
				int counter = 0;
				while (counter < 154 && sb.Length < 15373 && !reader.EndOfStream) {
					++counter;
					string line = reader.ReadLine();
					sb.Append(line);
				}
				return sb.ToString();
				return reader.ReadToEnd();
			}
		}

		public static string ExtractViewState(string pageContent) {
			string viewStateNameDelimiter = "__VIEWSTATE";
			string valueDelimiter = "value=\"";

			int viewStateNamePosition = pageContent.IndexOf(viewStateNameDelimiter);
			int viewStateValuePosition = pageContent.IndexOf(valueDelimiter, viewStateNamePosition);
			int viewStateStartPosition = viewStateValuePosition + valueDelimiter.Length;
			int viewStateEndPosition = pageContent.IndexOf("\"", viewStateStartPosition);

			return HttpUtility.UrlEncodeUnicode(pageContent.Substring(viewStateStartPosition, viewStateEndPosition - viewStateStartPosition));
		}

		public static string GetWebPageFromFile(string url) {
			using(StreamReader reader = new StreamReader(url)) {
				return reader.ReadToEnd();
			}
		}
	}
}