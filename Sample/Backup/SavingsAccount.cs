using System;
using System.Collections.Generic;

namespace Bank {
	public class SavingsAccount {
		private double _balance = 0;
		private List<double> _dailyBalanceHistory = new List<double>();

		private DateTime _createdDate;

		public DateTime CreatedDate {
			get { return _createdDate; }
		}
		public SavingsAccount(double initialAmount) {
			_balance = initialAmount;
			_createdDate = DateTime.Now;
		}
		public SavingsAccount(double initialAmount, DateTime createdDate)
			: this(initialAmount) {
			_createdDate = createdDate;
		}
		internal List<double> DailyBalanceHistory {
			get { return _dailyBalanceHistory; }
		}
		public double Withdraw(double amount) {
			if(_balance < amount)
				throw new ArgumentException("Invalid whthdraw amount", "amount");
			_balance -= amount;
			return amount;
		}
		public void Deposit(double amount) {
			if(amount <= 0)
				throw new ArgumentException("Invalid deposit amount", "amount");
			_balance += amount;
		}
		public double GetBalance() {
			return _balance;
		}
		public void SnapShotDailyBalance() {
			_dailyBalanceHistory.Add(_balance);
		}
		public void ProcessMonthlyInterest(double interestRate) {
			//interestRate = new InterestController().GetInterestRate(this);
			Deposit(GetAverageDailyBalance() * interestRate);
			_dailyBalanceHistory.Clear();
		}
		public double GetAverageDailyBalance() {
			double balanceSum = 0;
			_dailyBalanceHistory.ForEach(delegate(double dailyBalance) { balanceSum += dailyBalance; });
			double averageDailyBalance = _dailyBalanceHistory.Count > 0 ? balanceSum / _dailyBalanceHistory.Count : 0;
			return averageDailyBalance;
		}
	}
}
