using System;
using System.Data;
using System.Data.Common;

namespace REScraper {
	public enum REStatus {
		Active = 0,
		OutOfTheMarket = 1,
		UnderContract = 2,
		Closed = 3
	}

	public enum REStyle {
		Unknown = 0,
		Condo = 1,
		SingleFamily = 2,
		MultiFamily = 3
	}

	public class REPropertyInfo {
		string _source;
		string _id;
		uint _price;
		string _style;
		int _bedrooms;
		int _bathrooms;
		string _streetAddress;
		string _town;
		string _state;
		string _zipcode;
		string _description;
		string _url;
		string _photoUrl;
		REStatus _status;
		DateTime _listedDate;
		DateTime _revisedDate;
		DateTime _closedDate;
		uint _originalPrice;
		uint _closedPrice;
		string _longitude;
		string _latitude;

		public string Source {
			get { return _source; }
			set { _source = value; }
		}

		public string Id {
			get { return _id; }
			set { _id = value; }
		}

		public uint Price {
			get { return _price; }
			set { _price = value; }
		}

		public string Style {
			get { return _style; }
			set { _style = value; }
		}

		public int Bedrooms {
			get { return _bedrooms; }
			set { _bedrooms = value; }
		}

		public int Bathrooms {
			get { return _bathrooms; }
			set { _bathrooms = value; }
		}

		public string Address {
			get { return _streetAddress + ", " + _town + ", " + _state + " " + _zipcode;
; }
		}

		public string StreetAddress {
			get { return _streetAddress; }
			set { _streetAddress = value; }
		}

		public string Town {
			get { return _town; }
			set { _town = value; }
		}

		public string State {
			get { return _state; }
			set { _state = value; }
		}

		public string Zipcode {
			get { return _zipcode; }
			set { _zipcode = value; }
		}

		public string Description {
			get { return _description; }
			set { _description = value; }
		}

		public string Url {
			get { return _url; }
			set { _url = value; }
		}

		public string PhotoUrl {
			get { return _photoUrl; }
			set { _photoUrl = value; }
		}

		public REStatus Status {
			get { return _status; }
			set { _status = value; }
		}

		public DateTime ListedDate {
			get { return _listedDate; }
			set { _listedDate = value; }
		}

		public DateTime RevisedDate {
			get { return _revisedDate; }
			set { _revisedDate = value; }
		}

		public DateTime ClosedDate {
			get { return _closedDate; }
			set { _closedDate = value; }
		}

		public uint OriginalPrice {
			get { return _originalPrice; }
			set { _originalPrice = value; }
		}

		public uint ClosedPrice {
			get { return _closedPrice; }
			set { _closedPrice = value; }
		}

		public string Longitude {
			get { return _longitude; }
			set { _longitude = value; }
		}

		public string Latitude {
			get { return _latitude; }
			set { _latitude = value; }
		}

		public REPropertyInfo(string source, string id, uint price, string style, int bedrooms, int bathrooms, string streetAddress, string town, string state, string zipcode, string url, string photoUrl, string longitude, string latitude) {
			_source = source;
			_id = id;
			_price = price;
			_style = style;
			_bedrooms = bedrooms;
			_bathrooms = bathrooms;
			_streetAddress = streetAddress;
			_town = town;
			_state = state;
			_zipcode = zipcode;
			_url = url;
			_photoUrl = photoUrl;
			_longitude = longitude;
			_latitude = latitude;
		}

		public string ToHtmlString() {
			return string.Format("#{1}{0}{2}{0}${3}{0}{4}br {5}ba{0}{6}{0}", "<br>", _id, _price, _style, _bedrooms, _bathrooms, Address);
		}

		public static REPropertyInfo LoadFromReader(IDataReader reader) {
			throw new NotImplementedException();
		}
	}
}