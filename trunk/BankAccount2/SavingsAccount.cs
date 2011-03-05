using System;

namespace Bank {
	public class SavingsAccount : Account, IInterestProcessable {
		public SavingsAccount(double initialAmount) : base(initialAmount) {}
		public SavingsAccount(double initialAmount, DateTime createdDate) : base(initialAmount, createdDate) {}

		public void ProcessMonthlyInterest(double interestRate) {
			Deposit(GetAverageDailyBalance()*interestRate);
			_dailyBalanceHistory.Clear();
		}
	}
}