using System.Collections;

namespace REScraper {
	public interface IMlsRequester {
		string Webpage { get; }

		IEnumerable GetNextPageUrl();
	}
}