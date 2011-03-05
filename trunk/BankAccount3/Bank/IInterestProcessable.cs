using System;

namespace Bank {
	public interface IInterestProcessable {
		DateTime CreatedDate { get; }
		double GetAverageDailyBalance();
		void ProcessMonthlyInterest(double interestRate);
	}
}