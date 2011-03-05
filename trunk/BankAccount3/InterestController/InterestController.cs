using System;

namespace Bank {
	public class InterestController {
		public double GetInterestRate(Account account) {
			double interestRate = 0.025;
			double highInterestRate = interestRate + 0.005;
			int thresholdBalance = 50000;
			int thresholdDays = 365*5;
			bool isEligibleForHigherRate = account.GetAverageDailyBalance() > thresholdBalance
			                               && (DateTime.Now - account.CreatedDate).Days > thresholdDays;
			return isEligibleForHigherRate ? highInterestRate : interestRate;
		}
	}
}