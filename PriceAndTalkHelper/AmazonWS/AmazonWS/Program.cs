using System;
using System.Collections.Generic;
using System.IO;
using AmazonWS.com.amazonaws.ecs;

namespace AmazonWS {
	internal class Program {
		private const string AmazonComMerchantId = "ATVPDKIKX0DER";

		private static void Main(string[] args) {
			List<AlertTarget> alertList = new List<AlertTarget>();
			using (StreamReader reader = new StreamReader("tracking.txt")) {
				while (!reader.EndOfStream) {
					alertList.Add(new AlertTarget(reader.ReadLine()));
				}
			}
			foreach (AlertTarget target in alertList) {
				ProcessAlert(target);
			}
			Console.Read();
		}

		private static void ProcessAlert(AlertTarget target) {
			Console.WriteLine(target.Email);
			Console.WriteLine("");
			AWSECommerceService ecs = new AWSECommerceService();

			AmazonWSHelper helper = new AmazonWSHelper();
			try {
				ItemLookupResponse response = helper.GetItemLookupResponse(ecs, target.GetProductASINs());
				using (StringWriter writer = new StringWriter()) {
					foreach (Items i in response.Items) {
						foreach (Item item in i.Item) {
							writer.WriteLine("Product: " + item.ItemAttributes.Title);
							writer.WriteLine("Product Url: " + item.DetailPageURL);
							writer.WriteLine("");
							Product targetProduct = target.ProductList[item.ASIN];
							if (!string.IsNullOrEmpty(targetProduct.MerchantId) && !string.IsNullOrEmpty(targetProduct.Price)) {
								//List offer that's below specific price for a specific merchant
								writer.WriteLine(GetMerchantAndPriceSpecificOutputString(targetProduct, helper, ecs, item));
							} else if (!string.IsNullOrEmpty(targetProduct.MerchantId)) {
								//List all the offers for a specific merchant
								writer.WriteLine(GetMerchantSpecificOutputString(targetProduct, helper, ecs, item));
							} else if (!string.IsNullOrEmpty(targetProduct.Price)) {
								//List all the offers below a specific price
								writer.WriteLine(GetPriceSpecificOutputString(targetProduct, helper, ecs, item));
							} else {
								//List all the available prices
								writer.WriteLine(GetOutputString(targetProduct, helper, ecs, item));
							}
						}
					}
					Console.WriteLine(writer.ToString());
				}
			} catch (Exception ex) {
				Console.WriteLine(ex.ToString());
			}
		}

		private static string GetMerchantAndPriceSpecificOutputString(Product targetProduct, AmazonWSHelper helper, AWSECommerceService ecs, Item item) {
			using (StringWriter writer = new StringWriter()) {
				foreach (Offer o in item.Offers.Offer) {
					if (targetProduct.MerchantId == o.Merchant.MerchantId) {
						string[] listPrices, salePrices;
						string[] prices = GetPrices(item, o, helper, ecs, out listPrices, out salePrices);
						if (Int64.Parse(targetProduct.Price) > Int64.Parse(prices[0])) {
							writer.WriteLine(GetOfferString(item, o, listPrices, salePrices));
						}
						writer.WriteLine("");
					}
				}
				return writer.ToString();
			}
		}

		private static string GetMerchantSpecificOutputString(Product targetProduct, AmazonWSHelper helper, AWSECommerceService ecs, Item item) {
			using (StringWriter writer = new StringWriter()) {
				foreach (Offer o in item.Offers.Offer) {
					if (targetProduct.MerchantId == o.Merchant.MerchantId) {
						string[] listPrices, salePrices;
						string[] prices = GetPrices(item, o, helper, ecs, out listPrices, out salePrices);
						writer.WriteLine(GetOfferString(item, o, listPrices, salePrices));
						writer.WriteLine("");
					}
				}
				return writer.ToString();
			}
		}

		private static string GetPriceSpecificOutputString(Product targetProduct, AmazonWSHelper helper, AWSECommerceService ecs, Item item) {
			using (StringWriter writer = new StringWriter()) {
				foreach (Offer o in item.Offers.Offer) {
						string[] listPrices, salePrices;
						string[] prices = GetPrices(item, o, helper, ecs, out listPrices, out salePrices);
						if (Int64.Parse(targetProduct.Price) > Int64.Parse(prices[0])) {
							writer.WriteLine(GetOfferString(item, o, listPrices, salePrices));
						}
						writer.WriteLine("");
				}
				return writer.ToString();
			}
		}

		private static string GetOutputString(Product targetProduct, AmazonWSHelper helper, AWSECommerceService ecs, Item item) {
			using (StringWriter writer = new StringWriter()) {
				foreach (Offer o in item.Offers.Offer) {
					string[] listPrices, salePrices;
					string[] prices = GetPrices(item, o, helper, ecs, out listPrices, out salePrices);
					writer.WriteLine(GetOfferString(item, o, listPrices, salePrices));
					writer.WriteLine("");
				}
				return writer.ToString();
			}
		}

		private static string[] GetPrices(Item item, Offer o, AmazonWSHelper helper, AWSECommerceService ecs, out string[] listPrices, out string[] salePrices) {
			string[] prices = o.OfferListing[0].Price.FormattedPrice == "Too low to display"
			                  	?
			                  		helper.GetPriceTupleFromCart(ecs, item, o.OfferListing[0])
			                  	:
			                  		new string[] {o.OfferListing[0].Price.Amount, o.OfferListing[0].Price.FormattedPrice};
			listPrices = new string[2];
			salePrices = null;
			prices.CopyTo(listPrices, 0);
			if (o.OfferListing[0].SalePrice != null) {
				salePrices = new string[2];
				prices = o.OfferListing[0].SalePrice.FormattedPrice == "Too low to display"
				         	?
				         		helper.GetPriceTupleFromCart(ecs, item, o.OfferListing[0])
				         	:
				         		new string[] {o.OfferListing[0].SalePrice.Amount, o.OfferListing[0].SalePrice.FormattedPrice};
				prices.CopyTo(salePrices, 0);
			}
			return prices;
		}

		private static string GetOfferString(Item item, Offer o, string[] listPrices, string[] salePrices) {
			using (StringWriter writer = new StringWriter()) {
				writer.WriteLine("Merchant: " + o.Merchant.Name);
				if (o.Merchant.MerchantId != AmazonComMerchantId)
					writer.WriteLine(
						"Shipping information by Merchant: http://www.amazon.com/gp/help/seller/shipping.html?seller=" +
						o.Merchant.MerchantId + "&asin=" + item.ASIN);
				if (o.Merchant.MerchantId == AmazonComMerchantId) {
					if (!o.OfferListing[0].IsEligibleForSuperSaverShipping)
						writer.Write("Not ");
					writer.WriteLine("Eligible for Super Saver Shipping");
				}
				writer.WriteLine("List Price: " + listPrices[1]);
				if(salePrices != null)
					writer.WriteLine("Sale Price: " + salePrices[1]);
				if (o.OfferListing[0].ShippingCharge != null) {
					writer.Write("Shipping Charge: ");
					foreach (OfferListingShippingCharge charge in o.OfferListing[0].ShippingCharge) {
						writer.Write("  ");
						writer.WriteLine(charge.ShippingType + " - " + charge.ShippingPrice.FormattedPrice);
					}
				}
				return writer.ToString();
			}
		}
	}
}