using System;
using System.Collections;
using System.Collections.Generic;
using System.Data;
using System.Configuration;
using System.IO;
using System.Net;
using System.Text.RegularExpressions;

namespace REScraper {
	public class MlsRequester : IMlsRequester {
		private string _url;
		private string _webpage;
		private int _pgCnt;
		private int _currentPg = 1;

		public string Webpage {
			get { return _webpage; }
		}

		public MlsRequester(string url) {
			_url = url;
			_webpage = WebRequester.GetWebPage(_url);
			MatchCollection matches = Regex.Matches(_webpage, "<A\\sHREF=\"search.cfm.*?\">(?<pgcount>\\d)</A>", RegexOptions.Compiled);
			_pgCnt = Convert.ToInt32(matches[matches.Count-1].Groups["pgcount"].Value.Trim());
		}
		
		public IEnumerable GetNextPageUrl() {
			while (++_currentPg <= _pgCnt)
				yield return Regex.Replace(_url, "LineNbr=\\d+?&StartRow=\\d+?&", String.Format("LineNbr={0}&StartRow={1}&", _currentPg, (_currentPg - 1) * 20 + 1));
		}
	}

	public class HudsonMlsRequester : IMlsRequester {
		private string _url;
		private string _webpage;
		private int _pgCnt;
		private int _currentPg = 1;
		private List<string> _urlList = new List<string>();
		private int _currentUrlIndex;

		public string Webpage {
			get { return _webpage; }
		}

		public HudsonMlsRequester(string url) {
			//_url = url;
			//_webpage = WebRequester.GetWebPage(_url);
			//string viewState = WebRequester.ExtractViewState(_webpage);
			//string postData =
			//      String.Format("__VIEWSTATE={0}&gTownZip={1}&lbTown={2}&lbTown={3}&lbTown={4}&lbTown={5}&lbTown={6}&ddlminPrice={7}&ddlMaxPrice={8}&chkBPropTypesRes:1={9}&chkBPropTypesRes:2={10}&ddlbItemsPerPage={11}&ddlbSortBy={12}&txtOHFrom={13}&Imagebutton2.x={14}&Imagebutton2.y={15}", viewState, "rbCity", "0903", "0906", "0908", "0911", "0912", "400000", "800000", "on", "on", "25", "Price Ascending", "2/9/2007", "67", "12");
			//_webpage = WebRequester.PostAndGetResponse(_url, postData);
			foreach (string filename in Directory.GetFiles("data", "*.htm")) {
				string webpage = WebRequester.GetWebPageFromFile(filename);
				foreach (Match match in Regex.Matches(webpage, "_listnum\">(?<id>\\d+)</span>", RegexOptions.Compiled)) {
					_urlList.Add("http://hudson.fnismls.com/publink/Report.aspx?outputtype=HTML&GUID=e1c08c8d-5d71-47d8-9185-9c147a94d2dc&Report=Yes&view=30&layout_id=41&ListingID=" + match.Groups["id"].Value);
				}
			}
			_webpage = WebRequester.GetWebPage(_urlList[_currentUrlIndex]);
		}

		public IEnumerable GetNextPageUrl() {
			while (++_currentUrlIndex < _urlList.Count)
				yield return _urlList[_currentUrlIndex];
			//while (++_currentPg <= _pgCnt)
			//  yield return Regex.Replace(_url, "LineNbr=\\d+?&StartRow=\\d+?&", String.Format("LineNbr={0}&StartRow={1}&", _currentPg, (_currentPg - 1) * 20 + 1));
		}
	}
}
