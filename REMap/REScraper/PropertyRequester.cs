using System;
using System.Text.RegularExpressions;

namespace REScraper {
	public class PropertyRequester {
		private string _url;
		private string _addressPage;

		public PropertyRequester(string url) {
			_url = url;
		}

		public REPropertyInfo GetREPropertyInfo() {
			string webpage = WebRequester.GetWebPage(_url);
			Match match = Regex.Match(webpage, "Number:<.*?>\\s*?<.*?>(?<id>.*?)<", RegexOptions.Compiled);
			string id = match.Groups["id"].Value.Trim();
			match = Regex.Match(webpage, "Town:<.*?>\\s*?<.*?>(?<town>.*?)<", RegexOptions.Compiled);
			string town = match.Groups["town"].Value.Trim();
			match = Regex.Match(webpage, "Price:<.*?>\\s*?<.*?>\\s*?\\$(?<price>.*?)<", RegexOptions.Compiled);
			string price = Regex.Replace(match.Groups["price"].Value.Trim(), "[$,]", "");
			match = Regex.Match(webpage, "Style:<.*?>\\s*?<.*?>(?<style>.*?)<", RegexOptions.Compiled);
			string style = match.Groups["style"].Value.Trim();
			match = Regex.Match(webpage, "Bedrooms:<.*?>\\s*?<.*?>(?<bed>.*?)<", RegexOptions.Compiled);
			string bedrooms = match.Groups["bed"].Value.Trim();
			match = Regex.Match(webpage, "Full\\s*?Baths:<.*?>\\s*?<.*?>(?<bath>.*?)<", RegexOptions.Compiled);
			string bathrooms = match.Groups["bath"].Value.Trim();
			string[] geoCode = GetGeoCodeFromId(id);
			return new REPropertyInfo("njmls", id, Convert.ToUInt32(price), style, Convert.ToInt32(bedrooms), Convert.ToInt32(bathrooms), GetAddressFromId(id), town, "NJ", "", "http://njmls.com/cf/details.cfm?id=999999&mls_number=" + id, "http://photos.njmls.com/thumbnails/" + id + ".1.jpg", geoCode[0], geoCode[1]);
		}

		private string[] GetGeoCodeFromId(string id) {
			if (String.IsNullOrEmpty(_addressPage))
				_addressPage = WebRequester.GetWebPage("http://www.priv.njmls.xmlsweb.com/VIRTUALEARTH/MAPDISPLAY.ASP?LISTING_ID=" + id);
			Match match = Regex.Match(_addressPage, "LoadMap\\(new\\sVELatLong\\((?<lng>.*?)\\,\\s(?<lat>.*?)\\)", RegexOptions.Compiled);
			string[] latLng = new string[2];
			latLng[0] = match.Groups["lat"].Value.Trim();
			latLng[1] = match.Groups["lng"].Value.Trim();
			return latLng;
		}

		private string GetAddressFromId(string id) {
			if (String.IsNullOrEmpty(_addressPage))
				_addressPage = WebRequester.GetWebPage("http://www.priv.njmls.xmlsweb.com/VIRTUALEARTH/MAPDISPLAY.ASP?LISTING_ID=" + id);
			Match match = Regex.Match(_addressPage, "driving\\sdirections\\sto\\s(?<address>.*?)\\.", RegexOptions.Compiled);
			return match.Groups["address"].Value.Trim();
		}

		private REStyle GetStyleFromString(string style) {
			switch (style) {
				case "2FAM":
					return REStyle.MultiFamily;
				default:
					return REStyle.Unknown;
			}
		}
	}
}