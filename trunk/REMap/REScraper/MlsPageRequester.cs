using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace REScraper {
	public class MlsPageRequester : IMlsPageRequester {
		private string _url;
		private string _currentFolder;
		private string _webpage;

		public MlsPageRequester(string url) {
			_url = url;
			_currentFolder = _url.Substring(0, _url.LastIndexOf("/") + 1); ;
		}

		public List<REPropertyInfo> ParseWebPageAndGetPropertyList() {
			if(String.IsNullOrEmpty(_webpage))
				_webpage = WebRequester.GetWebPage(_url);
			return ParseWebPageAndGetPropertyList(_webpage);
		}

		public List<REPropertyInfo> ParseWebPageAndGetPropertyList(string webpage) {
			List<REPropertyInfo> properties = new List<REPropertyInfo>();
			MatchCollection matches = Regex.Matches(webpage, "MLS\\sReference\\snumber\\:\\s</b><A\\sHREF=\"(?<url>.+?)\"", RegexOptions.IgnoreCase|RegexOptions.Compiled);
			foreach (Match match in matches) {
				string url = match.Groups["url"].Value;
				properties.Add(new PropertyRequester(url.StartsWith("http") ? url : _currentFolder + url).GetREPropertyInfo()); 
			}
			return properties;
		}
	}

	public class HudsonMlsPageRequester : IMlsPageRequester {
		private string _url;
		private string _webpage;

		public HudsonMlsPageRequester(string url) {
			_url = url;
		}

		public List<REPropertyInfo> ParseWebPageAndGetPropertyList() {
			if (String.IsNullOrEmpty(_webpage))
				_webpage = WebRequester.GetWebPage(_url);
			return ParseWebPageAndGetPropertyList(_webpage);
		}

		public List<REPropertyInfo> ParseWebPageAndGetPropertyList(string webpage) {
			List<REPropertyInfo> properties = new List<REPropertyInfo>();
			properties.Add(ParseREPropertyInfo(webpage));
			return properties;
		}

		private REPropertyInfo ParseREPropertyInfo(string webpage) {
			Match match = Regex.Match(webpage, "<div\\sstyle=\"font-weight:bold;white-space:nowrap;left:363px;overflow:hidden;background-color:transparent;position:absolute;padding-left:0;width:67px;vertical-align:Top;font-family:tahoma;top:32px;color:\\#000000;z-index:2;text-align:Left;font-size:11px;height:16px;text-overflow:ellipsis;\">(?<id>.*?)</div>", RegexOptions.Compiled);
			string id = match.Groups["id"].Value.Trim();
			match = Regex.Match(webpage, "<div\\sstyle=\"font-weight:bold;white-space:nowrap;left:390px;overflow:hidden;background-color:transparent;position:absolute;padding-left:0;width:150px;vertical-align:Top;font-family:tahoma;top:64px;color:\\#000000;z-index:2;text-align:Left;font-size:11px;height:16px;text-overflow:ellipsis;\">(?<town>.*?)</div>", RegexOptions.Compiled);
			string value = match.Groups["town"].Value;
			int indexOf = value.IndexOf(",");
			string town = (indexOf > 0 ? value.Substring(0, indexOf) : value).Trim();
			town = GetCorrectTownName(town);
			match = Regex.Match(webpage, "<div\\sstyle=\"font-weight:bold;white-space:nowrap;left:634px;overflow:hidden;background-color:transparent;position:absolute;padding-left:0;width:90px;vertical-align:Top;font-family:tahoma;top:32px;color:\\#000000;z-index:2;text-align:Left;font-size:11px;height:16px;text-overflow:ellipsis;\">(?<price>.*?)</div>", RegexOptions.Compiled);
			string price = Regex.Replace(match.Groups["price"].Value.Trim(), "[$,]", "");
			match = Regex.Match(webpage, "<div\\sstyle=\"font-weight:bold;white-space:nowrap;left:390px;overflow:hidden;background-color:transparent;position:absolute;padding-left:0;width:150px;vertical-align:Top;font-family:tahoma;top:80px;color:\\#000000;z-index:2;text-align:Left;font-size:11px;height:16px;text-overflow:ellipsis;\">(?<style>.*?)</div>", RegexOptions.Compiled);
			string style = match.Groups["style"].Value.Trim();
			string bedrooms = "";
			string bathrooms = "";
			match = Regex.Match(webpage, "<div\\sstyle=\"font-weight:bold;white-space:nowrap;left:446px;overflow:hidden;background-color:transparent;position:absolute;padding-left:0;width:59px;vertical-align:Top;font-family:tahoma;top:32px;color:\\#000000;z-index:2;text-align:Left;font-size:11px;height:16px;text-overflow:ellipsis;\">(?<status>.*?)</div>", RegexOptions.Compiled);
			string status = match.Groups["status"].Value.Trim();
			match = Regex.Match(webpage, "<div\\sstyle=\"font-weight:bold;white-space:nowrap;left:390px;overflow:hidden;background-color:transparent;position:absolute;padding-left:0;width:150px;vertical-align:Top;font-family:tahoma;top:48px;color:\\#000000;z-index:2;text-align:Left;font-size:11px;height:16px;text-overflow:ellipsis;\">(?<address>.*?)</div>", RegexOptions.Compiled);
			string address = match.Groups["address"].Value.Trim();
			string[] geoCode = GetGeoCodeFromAddress(address + " " + town + " NJ");
			return new REPropertyInfo("hudsonmls", id, Convert.ToUInt32(price), style, 0, 0, address, town, "NJ", "", "http://hudson.fnismls.com/publink/Report.aspx?outputtype=HTML&GUID=e1c08c8d-5d71-47d8-9185-9c147a94d2dc&Report=Yes&view=30&layout_id=41&ListingID=" + id, "http://photos.mlsguide.com/F06/" + id + ".jpg", geoCode[0], geoCode.Length >= 2 ? geoCode[1] : "");
		}

		private string GetCorrectTownName(string town) {
			switch(town) {
				case "JC":
					return "Jersey City";
				default:
					return town;
			}
		}

		private string[] GetGeoCodeFromAddress(string address) {
			string page = WebRequester.GetWebPage("http://maps.google.com/maps/geo?output=xml&key=ABQIAAAAWODszYhDtC7_xwLICoryGBR_6XnM6K3P7KD04N15PQBX6Gwb9hTyOTRZVGi-pHTzDD8k-re8XhAbkg&q=" + address);

			Match match = Regex.Match(page, "<coordinates>(?<geocode>.*?)</coordinates>", RegexOptions.Compiled);
			return match.Groups["geocode"].Value.Trim().Split(',');
		}
	}
}