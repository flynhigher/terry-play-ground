using System;
using System.Collections.Generic;

namespace Bank {
	public class SavingsAccount : BankAccount {
		List<double> _dailyBalanceHistory = new List<double>();

		public SavingsAccount(double initialAmount) : base(initialAmount) {
			_dailyBalanceHistory.Add(GetBalance());
		}
		public void ProcessMonthlyInterest(double interestRate, double higherInterestRate) {
			double averageDailyBalance = GetAverageDailyBalance();
			if(IsEligibleForHigherRate(averageDailyBalance))
				Deposit(averageDailyBalance * higherInterestRate);
			else
				Deposit(averageDailyBalance * interestRate);
			_dailyBalanceHistory.Clear();
		}

		private bool IsEligibleForHigherRate(double averageDailyBalance) {
			return averageDailyBalance > 50000
			       && (DateTime.Now - CreatedDate).Days > 365 * 5;
		}

		private double GetAverageDailyBalance() {
			double balanceSum = 0;
			_dailyBalanceHistory.ForEach(delegate(double dailyBalance) { balanceSum += dailyBalance; });
			return _dailyBalanceHistory.Count > 0 ? balanceSum / _dailyBalanceHistory.Count : 0;
		}
	}
}