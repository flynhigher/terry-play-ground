using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Common;
using System.Text;
using Microsoft.Practices.EnterpriseLibrary.Data;

namespace REScraper {
	class Program {
		static void Main(string[] args) {
			string startUrl = args.Length > 0 ? args[0] :
				//"http://hudson.fnismls.com/publink/Report.aspx?outputtype=HTML&GUID=e1c08c8d-5d71-47d8-9185-9c147a94d2dc&ListingID=60015393&Report=Yes&view=30&layout_id=41";
			"http://njmls.com/cf/search.cfm?LineNbr=1&StartRow=1&thrshld=true&Cat=2&Town=0903%2C0906%2C0908%2C0911%2C0912&MinPrice=400000&MaxPrice=1000000&bdrms=0&baths=0&HTMLPage=select.cfm?County=Hudson&sortmethod=area&display=20&id=999999&searchtype=1";
			Factory factory = new Factory(startUrl);
			IMlsRequester njmlsRequester = factory.CreateMlsRequester();
			List<REPropertyInfo> propertyList = factory.CreateMlsPageRequester().ParseWebPageAndGetPropertyList(njmlsRequester.Webpage);
			REPropertyDataAccessor dataAccessor = new REPropertyDataAccessor();
			dataAccessor.Insert(propertyList);
			foreach (string url in njmlsRequester.GetNextPageUrl()) {
				List<REPropertyInfo> propList = factory.CreateMlsPageRequester(url).ParseWebPageAndGetPropertyList();
				dataAccessor.Insert(propList);
			}
		}
	}
	
	class Factory {
		private string _url;

		public Factory(string url) {
			_url = url;
		}

		public IMlsRequester CreateMlsRequester() {
			if (_url.Contains("njmls"))
				return new MlsRequester(_url);
			else
				return new HudsonMlsRequester(_url);
		}
		
		public IMlsPageRequester CreateMlsPageRequester() {
			if (_url.Contains("njmls"))
				return new MlsPageRequester(_url);
			else
				return new HudsonMlsPageRequester(_url);
		}

		public IMlsPageRequester CreateMlsPageRequester(string url) {
			if (url.Contains("njmls"))
				return new MlsPageRequester(url);
			else
				return new HudsonMlsPageRequester(url);
		}
	}
}
