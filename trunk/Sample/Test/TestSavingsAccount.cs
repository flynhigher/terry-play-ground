using NUnit.Framework;

namespace Bank {
	[TestFixture()]
	public class TestSavingsAccount {
		private SavingsAccount _unitUnderTest;

		[SetUp()]
		public void SetUp() {
			double initialAmount = 100;
			_unitUnderTest = new SavingsAccount(initialAmount);
		}

		[TearDown()]
		public void TearDown() {
			_unitUnderTest = null;
		}

		[Test()]
		public void TestCalculateInterest() {
			double interestRate = 1;
			_unitUnderTest.ProcessMonthlyInterest(interestRate, interestRate + 0.5);
			Assert.AreEqual(200, _unitUnderTest.GetBalance(), "ProcessMonthlyInterest method returned unexpected result.");
		}
	}
}
