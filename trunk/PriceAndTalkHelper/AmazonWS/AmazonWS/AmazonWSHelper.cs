using System;
using System.IO;
using AmazonWS.com.amazonaws.ecs;

namespace AmazonWS {
	public class AmazonWSHelper {
		private const string AssociateTag = "priandtal-20";
		private const string AWSAccessKeyId = "0V7P7P46HB9BK7YDBE82";
		private const string CartInfoPath = "cartId.txt";

		public ItemLookupResponse GetItemLookupResponse(AWSECommerceService ecs, string[] itemASINs) {
			ItemLookup lookup = new ItemLookup();
			lookup.AssociateTag = AssociateTag;
			lookup.AWSAccessKeyId = AWSAccessKeyId;
			//lookup.Version = "2008-08-19";
			ItemLookupRequest request = new ItemLookupRequest();
			request.ItemId = itemASINs;
			request.MerchantId = "Featured";
			request.ResponseGroup = new string[] {"Medium", "OfferFull", "ShippingCharges"};
			lookup.Request = new ItemLookupRequest[] {request};
			ItemLookupResponse response = ecs.ItemLookup(lookup);
			CheckRequestError(response.OperationRequest);
			return response;
		}

		public string[] GetPriceTupleFromCart(AWSECommerceService ecs, Item item, OfferListing offerListing) {
			Cart cart = null;
			string cartInfo = ReadCartInfo();
			if (string.IsNullOrEmpty(cartInfo)) {
				CartCreateResponse response = ecs.CartCreate(GetCartCreate(item, offerListing));
				CheckRequestError(response.OperationRequest);
				cart = response.Cart[0];
				WriteCartInfo(cart);
			} else {
				CartAddResponse response = ecs.CartAdd(GetCartAdd(cartInfo, item, offerListing));
				CheckRequestError(response.OperationRequest);
				cart = response.Cart[0];
			}
			string[] prices = new string[2];
			prices[0] = cart.SubTotal.Amount;
			prices[1] = cart.SubTotal.FormattedPrice;
			CartClearResponse clearResponse = ecs.CartClear(GetCartClear(cart));
			CheckRequestError(clearResponse.OperationRequest);
			return prices;
		}

		public string GetPriceFromCart(AWSECommerceService ecs, Item item, OfferListing offerListing) {
			string[] prices = GetPriceTupleFromCart(ecs, item, offerListing);
			return prices[0];
		}

		public string GetFormattedPriceFromCart(AWSECommerceService ecs, Item item, OfferListing offerListing) {
			string[] prices = GetPriceTupleFromCart(ecs, item, offerListing);
			return prices[1];
		}

		private void CheckRequestError(OperationRequest operationRequest) {
			if (operationRequest.Errors != null && operationRequest.Errors.Length > 0)
				throw new ApplicationException(operationRequest.Errors[0].Message);
		}

		private CartAdd GetCartAdd(string cartInfo, Item item, OfferListing offerListing) {
			CartAdd cartAdd = new CartAdd();
			cartAdd.AssociateTag = AssociateTag;
			cartAdd.AWSAccessKeyId = AWSAccessKeyId;
			CartAddRequestItem cartItem = new CartAddRequestItem();
			//cartItem.ASIN = item.ASIN;
			cartItem.AssociateTag = AssociateTag;
			cartItem.OfferListingId = offerListing.OfferListingId;
			cartItem.Quantity = "1";
			CartAddRequest request = new CartAddRequest();
			string[] split = cartInfo.Split(',');
			request.CartId = split[0];
			request.HMAC = split[1];
			request.Items = new CartAddRequestItem[] {cartItem};
			cartAdd.Request = new CartAddRequest[] {request};
			return cartAdd;
		}

		private string ReadCartInfo() {
			if (File.Exists(CartInfoPath)) {
				using (StreamReader reader = new StreamReader(CartInfoPath)) {
					return reader.ReadLine();
				}
			} else
				return "";
		}

		private void WriteCartInfo(Cart cart) {
			using (StreamWriter writer = new StreamWriter(CartInfoPath)) {
				writer.WriteLine(cart.CartId + "," + cart.HMAC);
			}
		}

		private CartCreate GetCartCreate(Item item, OfferListing offerListing) {
			CartCreate cartCreate = new CartCreate();
			cartCreate.AssociateTag = AssociateTag;
			cartCreate.AWSAccessKeyId = AWSAccessKeyId;
			CartCreateRequestItem cartItem = new CartCreateRequestItem();
			//cartItem.ASIN = item.ASIN;
			cartItem.AssociateTag = AssociateTag;
			cartItem.OfferListingId = offerListing.OfferListingId;
			cartItem.Quantity = "1";
			CartCreateRequest request = new CartCreateRequest();
			request.Items = new CartCreateRequestItem[] {cartItem};
			cartCreate.Request = new CartCreateRequest[] {request};
			return cartCreate;
		}

		private CartClear GetCartClear(Cart cart) {
			CartClear cartClear = new CartClear();
			cartClear.AssociateTag = AssociateTag;
			cartClear.AWSAccessKeyId = AWSAccessKeyId;
			CartClearRequest clearReq = new CartClearRequest();
			clearReq.CartId = cart.CartId;
			clearReq.HMAC = cart.HMAC;
			cartClear.Request = new CartClearRequest[] {clearReq};
			return cartClear;
		}
	}
}