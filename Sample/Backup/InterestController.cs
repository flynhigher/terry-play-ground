using System;
using System.Collections.Generic;
using System.Text;

namespace Bank {
	public class InterestController {
		public double GetInterestRate(SavingsAccount savingsAccount) {
			double interestRate = 0.025;
			double highInterestRate = interestRate + 0.005;
			int thresholdBalance = 50000;
			int thresholdDays = 365 * 5;
			bool isEligibleForHigherRate = savingsAccount.GetAverageDailyBalance() > thresholdBalance
				&& (DateTime.Now - savingsAccount.CreatedDate).Days > thresholdDays;
			return isEligibleForHigherRate ? highInterestRate : interestRate;
		}
	}
}
