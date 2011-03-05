using System.Collections.Generic;

namespace AmazonWS {
	public class AlertTarget {
		private string _email;
		private Dictionary<string, Product> _productList = new Dictionary<string, Product>();

		public AlertTarget() {}

		public AlertTarget(string line) {
			Parse(line);
		}

		public string Email {
			get { return _email; }
			set { _email = value; }
		}

		public Dictionary<string, Product> ProductList {
			get { return _productList; }
		}

		public string[] GetProductASINs() {
			string[] productASINs = new string[_productList.Keys.Count]; //new string[] { "B000YMNZ7E", "B0010YWPZ8", "B001413D94" };
			_productList.Keys.CopyTo(productASINs, 0);
			return productASINs;
		}

		public void Parse(string line)
		{
			string[] units = line.Split(',');
			_email = units[0];
			for (int i = 1; i < units.Length; i++)
			{
				string[] info = units[i].Split(':');
				_productList.Add(info[0], new Product(info));
			}
		}
	}
}