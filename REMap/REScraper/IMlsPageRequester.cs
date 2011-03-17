using System.Collections.Generic;

namespace REScraper {
	public interface IMlsPageRequester {
		List<REPropertyInfo> ParseWebPageAndGetPropertyList();
		List<REPropertyInfo> ParseWebPageAndGetPropertyList(string webpage);
	}
}