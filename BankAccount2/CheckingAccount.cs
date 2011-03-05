using System;

namespace Bank {
	public class CheckingAccount : Account {
		public CheckingAccount(double initialAmount) : base(initialAmount) {}
		public CheckingAccount(double initialAmount, DateTime createdDate) : base(initialAmount, createdDate) {}
	}
}