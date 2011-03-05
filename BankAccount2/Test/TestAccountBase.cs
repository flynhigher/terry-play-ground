using System;

namespace Bank {
	public class TestAccountBase {
		protected SavingsAccount GetOldSavingsAccountWHighBalance() {
			SavingsAccount oldSavingsAccountWHighBalance =
				new SavingsAccount(70000, new DateTime(DateTime.Now.AddYears(-7).Ticks));
			oldSavingsAccountWHighBalance.SnapShotDailyBalance();
			oldSavingsAccountWHighBalance.Deposit(60000);
			oldSavingsAccountWHighBalance.SnapShotDailyBalance();
			return oldSavingsAccountWHighBalance;
		}

		protected SavingsAccount GetOldSavingsAccountLowBalance() {
			SavingsAccount oldSavingsAccountLowBalance = new SavingsAccount(150, new DateTime(DateTime.Now.AddYears(-7).Ticks));
			oldSavingsAccountLowBalance.SnapShotDailyBalance();
			oldSavingsAccountLowBalance.Withdraw(45);
			oldSavingsAccountLowBalance.SnapShotDailyBalance();
			return oldSavingsAccountLowBalance;
		}

		protected SavingsAccount GetNewSavingsAccountWHighBalance() {
			SavingsAccount newSavingsAccountWHighBalance = new SavingsAccount(70000);
			newSavingsAccountWHighBalance.SnapShotDailyBalance();
			newSavingsAccountWHighBalance.Deposit(60000);
			newSavingsAccountWHighBalance.SnapShotDailyBalance();
			return newSavingsAccountWHighBalance;
		}

		protected SavingsAccount GetNewSavingsAccountWLowBalance() {
			SavingsAccount newSavingsAccountWLowBalance = new SavingsAccount(100);
			newSavingsAccountWLowBalance.Deposit(50);
			newSavingsAccountWLowBalance.SnapShotDailyBalance();
			newSavingsAccountWLowBalance.Withdraw(45);
			newSavingsAccountWLowBalance.SnapShotDailyBalance();
			return newSavingsAccountWLowBalance;
		}

		protected InterestCheckingAccount GetOldInterestCheckingAccountWHighBalance() {
			InterestCheckingAccount oldInterestCheckingAccountWHighBalance =
				new InterestCheckingAccount(70000, new DateTime(DateTime.Now.AddYears(-7).Ticks));
			oldInterestCheckingAccountWHighBalance.SnapShotDailyBalance();
			oldInterestCheckingAccountWHighBalance.Deposit(60000);
			oldInterestCheckingAccountWHighBalance.SnapShotDailyBalance();
			return oldInterestCheckingAccountWHighBalance;
		}

		protected InterestCheckingAccount GetOldInterestCheckingAccountLowBalance() {
			InterestCheckingAccount oldInterestCheckingAccountLowBalance =
				new InterestCheckingAccount(150, new DateTime(DateTime.Now.AddYears(-7).Ticks));
			oldInterestCheckingAccountLowBalance.SnapShotDailyBalance();
			oldInterestCheckingAccountLowBalance.Withdraw(45);
			oldInterestCheckingAccountLowBalance.SnapShotDailyBalance();
			return oldInterestCheckingAccountLowBalance;
		}

		protected InterestCheckingAccount GetNewInterestCheckingAccountWHighBalance() {
			InterestCheckingAccount newInterestCheckingAccountWHighBalance = new InterestCheckingAccount(70000);
			newInterestCheckingAccountWHighBalance.SnapShotDailyBalance();
			newInterestCheckingAccountWHighBalance.Deposit(60000);
			newInterestCheckingAccountWHighBalance.SnapShotDailyBalance();
			return newInterestCheckingAccountWHighBalance;
		}

		protected InterestCheckingAccount GetNewInterestCheckingAccountWLowBalance() {
			InterestCheckingAccount newInterestCheckingAccountWLowBalance = new InterestCheckingAccount(100);
			newInterestCheckingAccountWLowBalance.Deposit(50);
			newInterestCheckingAccountWLowBalance.SnapShotDailyBalance();
			newInterestCheckingAccountWLowBalance.Withdraw(45);
			newInterestCheckingAccountWLowBalance.SnapShotDailyBalance();
			return newInterestCheckingAccountWLowBalance;
		}

		protected CheckingAccount GetNewCheckingAccountWHighBalance() {
			CheckingAccount newCheckingAccountWHighBalance = new CheckingAccount(70000);
			newCheckingAccountWHighBalance.SnapShotDailyBalance();
			newCheckingAccountWHighBalance.Deposit(60000);
			newCheckingAccountWHighBalance.SnapShotDailyBalance();
			return newCheckingAccountWHighBalance;
		}

		protected CheckingAccount GetOldCheckingAccountWHighBalance() {
			CheckingAccount oldCheckingAccountWHighBalance =
				new CheckingAccount(70000, new DateTime(DateTime.Now.AddYears(-7).Ticks));
			oldCheckingAccountWHighBalance.SnapShotDailyBalance();
			oldCheckingAccountWHighBalance.Deposit(60000);
			oldCheckingAccountWHighBalance.SnapShotDailyBalance();
			return oldCheckingAccountWHighBalance;
		}
	}
}