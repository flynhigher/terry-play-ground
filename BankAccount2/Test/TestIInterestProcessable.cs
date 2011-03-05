using System.Collections.Generic;
using NUnit.Framework;

namespace Bank.Test {
	[TestFixture]
	public class TestIInterestProcessable : TestAccountBase {
		[Test()]
		public void TestProcessMonthlyInterest() {
			double normalInterestRate = 0.025;
			double highInterestRate = 0.03;

			List<Account> accounts = new List<Account>();
			List<double> interestRates = new List<double>();
			List<double> previousBalances = new List<double>();
			List<double> averageDailyBalances = new List<double>();
			accounts.Add(GetNewSavingsAccountWLowBalance()); interestRates.Add(normalInterestRate);
			accounts.Add(GetNewSavingsAccountWHighBalance()); interestRates.Add(normalInterestRate);
			accounts.Add(GetOldSavingsAccountLowBalance()); interestRates.Add(normalInterestRate);
			accounts.Add(GetOldSavingsAccountWHighBalance()); interestRates.Add(highInterestRate);
			accounts.Add(GetNewInterestCheckingAccountWHighBalance()); interestRates.Add(normalInterestRate);
			accounts.Add(GetNewInterestCheckingAccountWLowBalance()); interestRates.Add(normalInterestRate);
			accounts.Add(GetOldInterestCheckingAccountLowBalance()); interestRates.Add(normalInterestRate);
			accounts.Add(GetOldInterestCheckingAccountWHighBalance()); interestRates.Add(highInterestRate);
			accounts.Add(GetNewCheckingAccountWHighBalance());
			accounts.Add(GetOldCheckingAccountWHighBalance());

			for (int i = 0; i < accounts.Count; i++) {
				//Prepare
				previousBalances.Add(accounts[i].GetBalance());
				averageDailyBalances.Add(accounts[i].GetAverageDailyBalance());

				//Interest processing start
				if (accounts[i] is IInterestProcessable) {
					IInterestProcessable interestAccount = accounts[i] as IInterestProcessable;
					interestAccount.ProcessMonthlyInterest(interestRates[i]);
				}
			}

			//Test
			for (int i = 0; i < accounts.Count; i++) {
				if (accounts[i] is IInterestProcessable)
					Assert.AreEqual(previousBalances[i] + (averageDailyBalances[i] * interestRates[i]), accounts[i].GetBalance());
				else
					Assert.AreEqual(previousBalances[i], accounts[i].GetBalance());
			}
		}
	}
}