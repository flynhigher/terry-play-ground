using System;

namespace Bank {
	public class InterestCheckingAccount : CheckingAccount, IInterestProcessable {
		public InterestCheckingAccount(double initialAmount) : base(initialAmount) {}
		public InterestCheckingAccount(double initialAmount, DateTime createdDate) : base(initialAmount, createdDate) {}

		public void ProcessMonthlyInterest(double interestRate) {
			Deposit(GetAverageDailyBalance()*interestRate);
			_dailyBalanceHistory.Clear();
		}
	}
}