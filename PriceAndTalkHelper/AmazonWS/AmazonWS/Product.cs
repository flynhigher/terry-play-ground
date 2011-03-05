namespace AmazonWS {
	public class Product {
		private string _asin;
		private string _price;
		private string _MerchantId;

		public Product(string[] productInfo) {
			_asin = productInfo[0];
			if (productInfo.Length > 1)
				_price = productInfo[1];
			if (productInfo.Length > 2)
				_MerchantId = productInfo[2];
		}

		public Product(string asin) {
			_asin = asin;
		}

		public Product(string asin, string price) {
			_asin = asin;
			_price = price;
		}

		public Product(string asin, string price, string merchant) {
			_asin = asin;
			_price = price;
			_MerchantId = merchant;
		}

		public string Asin {
			get { return _asin; }
			set { _asin = value; }
		}

		public string Price {
			get { return _price; }
			set { _price = value; }
		}

		public string MerchantId {
			get { return _MerchantId; }
			set { _MerchantId = value; }
		}
	}
}