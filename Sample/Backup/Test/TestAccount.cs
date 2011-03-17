using System;
using NUnit.Framework;

namespace Bank {
	[TestFixture()]
	public class TestAccount {
		private Account _unitUnderTest;

		[SetUp()]
		public void SetUp() {
			_unitUnderTest = new Account(100);
		}

		[TearDown()]
		public void TearDown() {
			_unitUnderTest = null;
		}

		[Test()]
		public void TestSnapShotDailyBalance() {
			_unitUnderTest.Deposit(50); _unitUnderTest.SnapShotDailyBalance();
			Assert.AreEqual(150, _unitUnderTest.DailyBalanceHistory[0]);
			_unitUnderTest.Withdraw(45); _unitUnderTest.SnapShotDailyBalance();
			Assert.AreEqual(105, _unitUnderTest.DailyBalanceHistory[1]);
		}

		[Test()]
		public void TestProcessMonthlyInterest() {
			TestSnapShotDailyBalance();
			InterestController interestController = new InterestController();
			double interestRate = interestController.GetInterestRate(_unitUnderTest);
			_unitUnderTest.ProcessMonthlyInterest(interestRate);
			Assert.AreEqual(105 + ((150.0 + 105.0) / 2 * interestRate) /*108.1875*/, _unitUnderTest.GetBalance());

			Account oldAccount = new Account(150, new DateTime(DateTime.Now.AddYears(-7).Ticks));
			oldAccount.SnapShotDailyBalance();
			oldAccount.Withdraw(45);
			oldAccount.SnapShotDailyBalance();
			interestRate = interestController.GetInterestRate(oldAccount);
			oldAccount.ProcessMonthlyInterest(interestRate);
			Assert.AreEqual(105 + ((150.0 + 105.0) / 2 * interestRate), oldAccount.GetBalance());

			Account newAccountWHighBalance = new Account(70000);
			newAccountWHighBalance.SnapShotDailyBalance();
			newAccountWHighBalance.Deposit(60000);
			newAccountWHighBalance.SnapShotDailyBalance();
			interestRate = interestController.GetInterestRate(newAccountWHighBalance);
			newAccountWHighBalance.ProcessMonthlyInterest(interestRate);
			Assert.AreEqual(130000 + ((70000.0 + 130000.0) / 2 * interestRate) /*132500*/, newAccountWHighBalance.GetBalance());

			Account oldAccountWHighBalance =
				new Account(70000, new DateTime(DateTime.Now.AddYears(-7).Ticks));
			oldAccountWHighBalance.SnapShotDailyBalance();
			oldAccountWHighBalance.Deposit(60000);
			oldAccountWHighBalance.SnapShotDailyBalance();
			interestRate = interestController.GetInterestRate(oldAccountWHighBalance);
			oldAccountWHighBalance.ProcessMonthlyInterest(interestRate);
			Assert.AreEqual(130000 + ((70000.0 + 130000.0) / 2 * interestRate), oldAccountWHighBalance.GetBalance());
		}
	}
}