using NUnit.Framework;

namespace Bank {
	[TestFixture()]
	public class TestInterestController : TestAccountBase {
		private InterestController _unitUnderTest;

		[SetUp()]
		public void SetUp() {
			_unitUnderTest = new InterestController();
		}

		[TearDown()]
		public void TearDown() {
			_unitUnderTest = null;
		}

		[Test()]
		public void TestGetInterestRate() {
			Assert.AreEqual(0.025, _unitUnderTest.GetInterestRate(GetNewSavingsAccountWLowBalance()));
			Assert.AreEqual(0.025, _unitUnderTest.GetInterestRate(GetNewSavingsAccountWHighBalance()));
			Assert.AreEqual(0.025, _unitUnderTest.GetInterestRate(GetOldSavingsAccountLowBalance()));
			Assert.AreEqual(0.025 + 0.005, _unitUnderTest.GetInterestRate(GetOldSavingsAccountWHighBalance()));
			Assert.AreEqual(0.025, _unitUnderTest.GetInterestRate(GetNewInterestCheckingAccountWLowBalance()));
			Assert.AreEqual(0.025, _unitUnderTest.GetInterestRate(GetNewInterestCheckingAccountWHighBalance()));
			Assert.AreEqual(0.025, _unitUnderTest.GetInterestRate(GetOldInterestCheckingAccountLowBalance()));
			Assert.AreEqual(0.025 + 0.005, _unitUnderTest.GetInterestRate(GetOldInterestCheckingAccountWHighBalance()));
		}
	}
}