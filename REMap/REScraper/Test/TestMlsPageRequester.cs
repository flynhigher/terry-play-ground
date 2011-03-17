using System;
using System.Collections.Generic;
using System.Text;
using NUnit.Framework;

namespace REScraper.Test {
	[TestFixture]
	public class TestMlsPageRequester {
		IMlsPageRequester _unitUnderTest;
		
		[SetUp]
		public void SetUp() {
			_unitUnderTest = new MlsPageRequester("http://njmls.com/cf/search.cfm?LineNbr=1&StartRow=1&thrshld=true&Cat=2&Town=0903%2C0906%2C0908%2C0911%2C0912&MinPrice=400000&MaxPrice=850000&bdrms=0&baths=0&HTMLPage=select.cfm?County=Hudson&sortmethod=area&display=20&id=999999&searchtype=1");
		}
		[TearDown]
		public void TearDown() {
			_unitUnderTest = null;
		}
		
		[Test]
		public void TestParseWebPageAndGetPropertyList() {
			List<REPropertyInfo> propertyList = _unitUnderTest.ParseWebPageAndGetPropertyList();
			Assert.AreEqual(20, propertyList.Count);
			Assert.AreNotEqual(propertyList[0].Address, propertyList[1].Address);
		}
	}
}
