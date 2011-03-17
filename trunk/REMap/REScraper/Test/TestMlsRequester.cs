using System;
using System.Collections.Generic;
using System.Text;
using NUnit.Framework;

namespace REScraper.Test {
	[TestFixture]
	public class TestMlsRequester {
		IMlsRequester _unitUnderTest;
		
		[SetUp]
		public void SetUp() {
			_unitUnderTest = new MlsRequester("http://njmls.com/cf/search.cfm?LineNbr=1&StartRow=1&thrshld=true&Cat=2&Town=0903%2C0906%2C0908%2C0911%2C0912&MinPrice=400000&MaxPrice=850000&bdrms=0&baths=0&HTMLPage=select.cfm?County=Hudson&sortmethod=area&display=20&id=999999&searchtype=1");
		}
		[TearDown]
		public void TearDown() {
			_unitUnderTest = null;
		}
		
		[Test]
		public void TestGetNextPageUrl() {
			int count = 1;
			foreach (string url in _unitUnderTest.GetNextPageUrl()) {
				++count;
				if(count == 2)
					Assert.AreEqual("http://njmls.com/cf/search.cfm?LineNbr=2&StartRow=21&thrshld=true&Cat=2&Town=0903%2C0906%2C0908%2C0911%2C0912&MinPrice=400000&MaxPrice=850000&bdrms=0&baths=0&HTMLPage=select.cfm?County=Hudson&sortmethod=area&display=20&id=999999&searchtype=1", url);
				else if (count == 3)
					Assert.AreEqual("http://njmls.com/cf/search.cfm?LineNbr=3&StartRow=41&thrshld=true&Cat=2&Town=0903%2C0906%2C0908%2C0911%2C0912&MinPrice=400000&MaxPrice=850000&bdrms=0&baths=0&HTMLPage=select.cfm?County=Hudson&sortmethod=area&display=20&id=999999&searchtype=1", url);
				else if (count == 4)
					Assert.AreEqual("http://njmls.com/cf/search.cfm?LineNbr=4&StartRow=61&thrshld=true&Cat=2&Town=0903%2C0906%2C0908%2C0911%2C0912&MinPrice=400000&MaxPrice=850000&bdrms=0&baths=0&HTMLPage=select.cfm?County=Hudson&sortmethod=area&display=20&id=999999&searchtype=1", url);
				else
					Assert.AreEqual("http://njmls.com/cf/search.cfm?LineNbr=5&StartRow=81&thrshld=true&Cat=2&Town=0903%2C0906%2C0908%2C0911%2C0912&MinPrice=400000&MaxPrice=850000&bdrms=0&baths=0&HTMLPage=select.cfm?County=Hudson&sortmethod=area&display=20&id=999999&searchtype=1", url);
			}
		}
	}
}
