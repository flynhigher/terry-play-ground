using System;

namespace Bank {
	public class BankAccount {
		private int _id = 0;
		protected double _balance = 0;
		private DateTime _createdDate = DateTime.MinValue;

		public BankAccount(double initialAmount) {
			_balance = initialAmount;
		}

		public int Id {
			get { return _id; }
		}

		public DateTime CreatedDate {
			get { return _createdDate; }
		}

		public double Withdraw(double amount) {
			if (_balance < amount)
				throw new ArgumentException("Invalid whthdraw amount", "amount");
			_balance -= amount;
			return amount;
		}

		public void Deposit(double amount) {
			if (amount <= 0)
				throw new ArgumentException("Invalid deposit amount", "amount");
			_balance += amount;
		}

		public double GetBalance() {
			return _balance;
		}
	}
}