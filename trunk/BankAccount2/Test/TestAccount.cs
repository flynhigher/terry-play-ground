using System;
using NUnit.Framework;

namespace Bank {
	[TestFixture]
	public class TestAccount {
		private SavingsAccount _unitUnderTest;

		[SetUp]
		public void SetUp() {
			_unitUnderTest = new SavingsAccount(100);
		}

		[TearDown]
		public void TearDown() {
			_unitUnderTest = null;
		}

		[Test]
		public void TestConstructorAccount() {
			Account testAccount = new SavingsAccount(100);
			Assert.IsNotNull(testAccount, "Constructor of type, SavingsAccount failed to create instance.");
			Assert.AreEqual(100, testAccount.GetBalance(), "Initial amount is not recorded correctly.");
		}

		[Test]
		public void TestWithdraw() {
			Assert.AreEqual(60, _unitUnderTest.Withdraw(60), "Withdraw method returned unexpected amount.");
		}

		[Test]
		[ExpectedException(typeof (ArgumentException))]
		public void TestWithdrawWithException() {
			_unitUnderTest.Withdraw(150);
		}

		[Test]
		public void TestDeposit() {
			_unitUnderTest.Deposit(50);
			Assert.AreEqual(150, _unitUnderTest.GetBalance(), "Deposit method generated unexpected state.");
		}

		[Test]
		public void TestGetBalance() {
			_unitUnderTest.Withdraw(55);
			Assert.AreEqual(45, _unitUnderTest.GetBalance(), "Withdraw method changed SavingsAccount state unexpectedly.");
			_unitUnderTest.Deposit(50);
			Assert.AreEqual(95, _unitUnderTest.GetBalance(), "Deposit method changed SavingsAccount state unexpectedly.");
			_unitUnderTest.Withdraw(15);
			Assert.AreEqual(80, _unitUnderTest.GetBalance(), "Withdraw method changed SavingsAccount state unexpectedly.");
		}

		[Test()]
		public void TestSnapShotDailyBalance() {
			_unitUnderTest.Deposit(50);
			_unitUnderTest.SnapShotDailyBalance();
			Assert.AreEqual(150, _unitUnderTest.DailyBalanceHistory[0]);
			_unitUnderTest.Withdraw(45);
			_unitUnderTest.SnapShotDailyBalance();
			Assert.AreEqual(105, _unitUnderTest.DailyBalanceHistory[1]);
		}

		//Initial version of TestProcessMonthlyInterest()
		//[Test()]
		//public void TestProcessMonthlyInterest()
		//{
		//  double interestRate = 0.025;
		//  TestSnapShotDailyBalance();
		//  _unitUnderTest.ProcessMonthlyInterest(interestRate);
		//  Assert.AreEqual(105 + ((150.0 + 105.0) / 2 * interestRate)/*108.1875*/, _unitUnderTest.GetBalance());

		//  Account oldAccount = new Account(150, new DateTime(DateTime.Now.AddYears(-7).Ticks));
		//  oldAccount.SnapShotDailyBalance();
		//  oldAccount.Withdraw(45); oldAccount.SnapShotDailyBalance();
		//  oldAccount.ProcessMonthlyInterest(interestRate);
		//  Assert.AreEqual(105 + ((150.0 + 105.0) / 2 * interestRate), oldAccount.GetBalance());

		//  Account newAccountWHighBalance = new Account(70000);
		//  newAccountWHighBalance.SnapShotDailyBalance();
		//  newAccountWHighBalance.Deposit(60000); newAccountWHighBalance.SnapShotDailyBalance();
		//  newAccountWHighBalance.ProcessMonthlyInterest(interestRate);
		//  Assert.AreEqual(130000 + ((70000.0 + 130000.0) / 2 * interestRate)/*132500*/, newAccountWHighBalance.GetBalance());

		//  Account oldAccountWHighBalance = new Account(70000, new DateTime(DateTime.Now.AddYears(-7).Ticks));
		//  oldAccountWHighBalance.SnapShotDailyBalance();
		//  oldAccountWHighBalance.Deposit(60000); oldAccountWHighBalance.SnapShotDailyBalance();
		//  oldAccountWHighBalance.ProcessMonthlyInterest(interestRate);
		//  Assert.AreEqual(130000 + ((70000.0 + 130000.0) / 2 * (interestRate + 0.005)), oldAccountWHighBalance.GetBalance());
		//}

		//Revised version of TestProcessMonthlyInterest()
		//[Test()]
		//public void TestProcessMonthlyInterest() {
		//  TestSnapShotDailyBalance();
		//  InterestController interestController = new InterestController();
		//  double interestRate = interestController.GetInterestRate(_unitUnderTest);
		//  _unitUnderTest.ProcessMonthlyInterest(interestRate);
		//  Assert.AreEqual(105 + ((150.0 + 105.0)/2*interestRate) /*108.1875*/, _unitUnderTest.GetBalance());

		//  Account oldAccount = new Account(150, new DateTime(DateTime.Now.AddYears(-7).Ticks));
		//  oldAccount.SnapShotDailyBalance();
		//  oldAccount.Withdraw(45);
		//  oldAccount.SnapShotDailyBalance();
		//  interestRate = interestController.GetInterestRate(oldAccount);
		//  oldAccount.ProcessMonthlyInterest(interestRate);
		//  Assert.AreEqual(105 + ((150.0 + 105.0)/2*interestRate), oldAccount.GetBalance());

		//  Account newAccountWHighBalance = new Account(70000);
		//  newAccountWHighBalance.SnapShotDailyBalance();
		//  newAccountWHighBalance.Deposit(60000);
		//  newAccountWHighBalance.SnapShotDailyBalance();
		//  interestRate = interestController.GetInterestRate(newAccountWHighBalance);
		//  newAccountWHighBalance.ProcessMonthlyInterest(interestRate);
		//  Assert.AreEqual(130000 + ((70000.0 + 130000.0)/2*interestRate) /*132500*/, newAccountWHighBalance.GetBalance());

		//  Account oldAccountWHighBalance =
		//    new Account(70000, new DateTime(DateTime.Now.AddYears(-7).Ticks));
		//  oldAccountWHighBalance.SnapShotDailyBalance();
		//  oldAccountWHighBalance.Deposit(60000);
		//  oldAccountWHighBalance.SnapShotDailyBalance();
		//  interestRate = interestController.GetInterestRate(oldAccountWHighBalance);
		//  oldAccountWHighBalance.ProcessMonthlyInterest(interestRate);
		//  Assert.AreEqual(130000 + ((70000.0 + 130000.0)/2*interestRate), oldAccountWHighBalance.GetBalance());
		//}
	}
}