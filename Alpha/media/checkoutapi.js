var secureHostName = "secure.ultracart.com";
var merchantId = "";
var version = "1.0";
var callbackUrl = "https://" + secureHostName + "/cgi-bin/UCCheckoutAPIJSON";

// Global cart variable
var cart = null;

// Background timer
var backgroundUpdateTimer;

// Variables used to make shipping calculation more robust
var ucInternalLastShippingEstimates = null;
var ucInternalLastShipToAddress1 = null;
var ucInternalLastShipToAddress2 = null;
var ucInternalLastShipToCity = null;
var ucInternalLastShipToState = null;
var ucInternalLastShipToPostalCode = null;
var ucInternalLastShipToCountry = null;

// Static data used by the getStateProvinces() and getStateProvinceCodes()
var ucStateProvinces = [
  {
    'country': 'United States',
    'stateProvinces' : ["Alabama","Alaska","American Samoa","Arizona","Arkansas","Armed Forces Africa","Armed Forces Americas","Armed Forces Canada","Armed Forces Europe","Armed Forces Middle East","Armed Forces Pacific","California","Colorado","Connecticut","Delaware","District of Columbia","Federated States of Micronesia","Florida","Georgia","Guam","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Marshall Islands","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Northern Mariana Islands","Ohio","Oklahoma","Oregon","Palau","Pennsylvania","Puerto Rico","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virgin Islands","Virginia","Washington","West Virginia","Wisconsin","Wyoming"],
    'codes': ["AL","AK","AS","AZ","AR","AE","AA","AE","AE","AE","AP","CA","CO","CT","DE","DC","FM","FL","GA","GU","HI","ID","IL","IN","IA","KS","KY","LA","ME","MH","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","MP","OH","OK","OR","PW","PA","PR","RI","SC","SD","TN","TX","UT","VT","VI","VA","WA","WV","WI","WY"]
  },
  {
    'country': 'Canada',
    'stateProvinces' : ["Alberta","British Columbia","Manitoba","New Brunswick","Newfoundland","Northwest Territories","Nova Scotia","Nunavut","Ontario","Prince Edward Island","Quebec","Saskatchewan","Yukon Territory"],
    'codes' : ["AB","BC","MB","NB","NF","NT","NS","NU","ON","PE","QC","SK","YT"]
  }
];

function genericCall(functionParameters, args) {
  var result = null;

  // Do we want async?
  var async = false;
  var onComplete;

  if (args != undefined && args.async != undefined) {
    async = args.async;
  }
  if (args != undefined && args.onComplete != undefined) {
    onComplete = args.onComplete;
  }

  // Send the request
  new Request.JSON({url: callbackUrl, async: async, onComplete: function(jsonResult) {
    // Store the result into our variable.
    result = jsonResult;

    // If this was a call to estimateShipping then we need to store the results
    try {
      if ("estimateShipping" == functionParameters.functionName) {
        ucInternalLastShippingEstimates = result;
      }
    } catch(e) {
    }

    // Call their function
    if (async && onComplete != undefined) {
      onComplete(result);
    }

  }}).post(functionParameters);

  return result;
}

function createCart(args) {
  return genericCall({'functionName': 'createCart', 'merchantId': merchantId, 'version': version}, args);
}

function getCart(cartId, args) {
  return genericCall({'functionName': 'getCart', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cartId)}, args);
}

function setCart(c) {
  // Let's make sure we have a valid cart object.
  if (c == null || c.cartId == null) return;
  cart = c;
}

function sanitizeDataTypes() {
  try {
    // Make sure the integer fields are actually set as a number of serialization purposes
    if (cart != null) {
      cart.creditCardExpirationMonth = (cart.creditCardExpirationMonth).toInt();
      cart.creditCardExpirationYear = (cart.creditCardExpirationYear).toInt();
    }
  } catch (e) {
  }
}

function updateCart(args) {
  clearBackgroundUpdateTimer();

  sanitizeDataTypes();
  var result = genericCall({'functionName': 'updateCart', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
  if (result != null) setCart(result);
  return cart;
}

function backgroundUpdateCart(args) {
  sanitizeDataTypes();
  genericCall({'functionName': 'backgroundUpdateCart', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
}


function clearBackgroundUpdateTimer() {
  try {
    window.clearTimeout(backgroundUpdateTimer);
  } catch (e) {
  }
}

function triggerBackgroundUpdateCart() {
  clearBackgroundUpdateTimer();

  try {
    backgroundUpdateTimer = window.setTimeout("backgroundUpdateCart({'async': true})", 2500);
  } catch (e) {
  }
}

function search(catalogHost, search, itemsPerPage, currentPage, args) {
  return genericCall({'functionName': 'search', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(catalogHost), 'parameter2': JSON.encode(search), 'parameter3': JSON.encode(itemsPerPage), 'parameter4': JSON.encode(currentPage)}, args);
}

function addItems(items, args) {
  ucInternalLastShippingEstimates = null;
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'addItems', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(items)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["addItems result was null"];
  return result.errors;
}

function removeItems(itemIds, args) {
  ucInternalLastShippingEstimates = null;
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'removeItems', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(itemIds)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["removeItems result was null"];
  return result.errors;
}

function removeItem(itemId, args) {
  ucInternalLastShippingEstimates = null;
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'removeItem', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(itemId)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["removeItem result was null"];
  return result.errors;
}

function clearItems(args) {
  ucInternalLastShippingEstimates = null;
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'clearItems', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["clearItems result was null"];
  return result.errors;
}

function updateItems(items, args) {
  ucInternalLastShippingEstimates = null;
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'updateItems', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(items)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["updateItems result was null"];
  return result.errors;
}

function establishCustomerProfile(email, password, args) {
  ucInternalLastShippingEstimates = null;
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'establishCustomerProfile', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(email), 'parameter3': JSON.encode(password)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["establishCustomerProfile result was null"];
  return result.errors;
}

function getAdvertisingSources(args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'getAdvertisingSources', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
}

function logError(error, args) {
  // Automatically include browser information when the error is logged
  error = "Browser Engine Name: " + Browser.Engine.name + "\nBrowser Engine Version: " + Browser.Engine.version + "\nBrowser Platform Name: " + Browser.Platform.name + "\n" + error;
  return genericCall({'functionName': 'logError', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(error)}, args);
}

function getReturnPolicy(args) {
  return genericCall({'functionName': 'getReturnPolicy', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
}

function getAllowedCountries(args) {
  return genericCall({'functionName': 'getAllowedCountries', 'merchantId': merchantId, 'version': version}, args);
}

function isDiff(o1, o2) {
  if (o1 == null && o2 == null) return false;
  if (o1 == null && o2 != null) return true;
  if (o1 != null && o2 == null) return true;
  return o1 == o2;
}

function estimateShipping(args) {

  // We need to know if they're calling this async
  var async = false;
  var onComplete = null;

  // This code is contained in a try/catch to make sure it never jeopardizes anything from running.
  try {
    if (args != undefined && args.async != undefined) {
      async = args.async;
    }
    if (args != undefined && args.onComplete != undefined) {
      onComplete = args.onComplete;
    }

    // Do we need to call the server again?
    if (
        cart != null &&
        ucInternalLastShippingEstimates != null &&
        !isDiff(ucInternalLastShipToAddress1, cart.shipToAddress1) &&
        !isDiff(ucInternalLastShipToAddress2, cart.shipToAddress2) &&
        !isDiff(ucInternalLastShipToCity, cart.shipToCity) &&
        !isDiff(ucInternalLastShipToState, cart.shipToState) &&
        !isDiff(ucInternalLastShipToPostalCode, cart.shipToPostalCode) &&
        !isDiff(ucInternalLastShipToCountry, cart.shipToCountry)
        ) {

      // If they specified an async method then we need to feed the result back to that function handler
      if (async && onComplete != null) onComplete(ucInternalLastShippingEstimates);

      // Return the last shipping estimates
      return ucInternalLastShippingEstimates;
    }

    // Store the values we're using to ask for the shipping methods
    ucInternalLastShipToAddress1 = cart.shipToAddress1;
    ucInternalLastShipToAddress2 = cart.shipToAddress2;
    ucInternalLastShipToCity = cart.shipToCity;
    ucInternalLastShipToState = cart.shipToState;
    ucInternalLastShipToPostalCode = cart.shipToPostalCode;
    ucInternalLastShipToCountry = cart.shipToCountry;
  } catch (e) {
  }

  sanitizeDataTypes();
  var result = genericCall({'functionName': 'estimateShipping', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);

  // If the call wasn't async then we'll store away the results
  try {
    if (!async || onComplete == null) {
      ucInternalLastShippingEstimates = result;
    }
  } catch (e) {
  }

  return result;
}

function getRelatedItems(args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'getRelatedItems', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
}

function getGiftSettings(args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'getGiftSettings', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
}

function getItems(itemIds, args) {
  return genericCall({'functionName': 'getItems', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(itemIds), 'parameter2': JSON.encode(cart)}, args);
}

function getItem(itemId, args) {
  return genericCall({'functionName': 'getItem', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(itemId), 'parameter2': JSON.encode(cart)}, args);
}

function validate(checks, args) {
  clearBackgroundUpdateTimer();

  sanitizeDataTypes();
  return genericCall({'functionName': 'validate', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(checks)}, args);
}

function validateAll(args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'validate', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
}

function getTaxCounties(args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'getTaxCounties', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
}

function loginCustomerProfile(email, password, args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'loginCustomerProfile', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(email), 'parameter3': JSON.encode(password)}, args);
}

function getCustomerProfile(args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'getCustomerProfile', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
}

function updateCustomerProfile(customerProfile, args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'updateCustomerProfile', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(customerProfile)}, args);
}

function logoutCustomerProfile(args) {
  ucInternalLastShippingEstimates = null;
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'logoutCustomerProfile', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["logoutCustomerProfile result was null"];
  return result.errors;
}

function setFinalizeAfter(minutes, args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'setFinalizeAfter', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(minutes)}, args);
}

function clearFinalizeAfter(args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'clearFinalizeAfter', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
}

function checkoutHandoff(returnOnErrorUrl, errorMessageParameterName, args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'checkoutHandoff', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(returnOnErrorUrl), 'parameter3': JSON.encode(errorMessageParameterName)}, args);
}

function checkoutHandoffOnCustomSSL(secureHostName, returnOnErrorUrl, errorMessageParameterName, args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'checkoutHandoff', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(secureHostName), 'parameter3': JSON.encode(returnOnErrorUrl), 'parameter4': JSON.encode(errorMessageParameterName)}, args);
}

function googleCheckoutHandoff(returnOnErrorUrl, errorMessageParameterName, args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'googleCheckoutHandoff', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(returnOnErrorUrl), 'parameter3': JSON.encode(errorMessageParameterName)}, args);
}

function googleCheckoutHandoffOnCustomSSL(secureHostName, returnOnErrorUrl, errorMessageParameterName, args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'googleCheckoutHandoff', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(secureHostName), 'parameter3': JSON.encode(returnOnErrorUrl), 'parameter4': JSON.encode(errorMessageParameterName)}, args);
}

function paypalHandoff(returnOnErrorUrl, errorMessageParameterName, args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'paypalHandoff', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(returnOnErrorUrl), 'parameter3': JSON.encode(errorMessageParameterName)}, args);
}

function paypalHandoffOnCustomSSL(secureHostName, returnOnErrorUrl, errorMessageParameterName, args) {
  sanitizeDataTypes();
  return genericCall({'functionName': 'paypalHandoff', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(secureHostName), 'parameter3': JSON.encode(returnOnErrorUrl), 'parameter4': JSON.encode(errorMessageParameterName)}, args);
}

function validateGiftCertificate(giftCertificateCode, args) {
  return genericCall({'functionName': 'validateGiftCertificate', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(giftCertificateCode)}, args);
}

function applyGiftCertificate(giftCertificateCode, args) {
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'applyGiftCertificate', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(giftCertificateCode)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["applyGiftCertificate result was null"];
  return result.errors;
}

function removeGiftCertificate(args) {
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'removeGiftCertificate', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["removeGiftCertificate result was null"];
  return result.errors;
}

function applyCoupon(couponCode, args) {
  ucInternalLastShippingEstimates = null;
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'applyCoupon', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(couponCode)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["applyCoupon result was null"];
  return result.errors;
}

function removeCoupon(couponCode, args) {
  ucInternalLastShippingEstimates = null;
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'removeCoupon', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(couponCode)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["removeCoupon result was null"];
  return result.errors;
}

function getStateProvinces(country, args) {
  // They really shouldn't use the async call since the local call is instanteous, but for constantly sake we'll support it
  if (args != null) {
    return genericCall({'functionName': 'getStateProvinces', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(country)}, args);
  }

  var i;
  for (i = 0; i < ucStateProvinces.length; i++) {
    if (ucStateProvinces[i].country == country) {
      return ucStateProvinces[i].stateProvinces;
    }
  }

  return new Array();
}

function unabbreviateStateProvinceCode(country, code) {
  var i;
  var j;

  for (i = 0; i < ucStateProvinces.length; i++) {
    if (ucStateProvinces[i].country == country) {
      for (j = 0; j < ucStateProvinces[i].codes.length; j++) {
        if (ucStateProvinces[i].codes[j] == code) {
          return ucStateProvinces[i].stateProvinces[j];
        }
      }
    }
  }

  return code;
}

function getStateProvinceCodes(country, args) {
  // They really shouldn't use the async call since the local call is instanteous, but for constantly sake we'll support it
  if (args != null) {
    return genericCall({'functionName': 'getStateProvinceCodes', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(country)}, args);
  }

  var i;
  for (i = 0; i < ucStateProvinces.length; i++) {
    if (ucStateProvinces[i].country == country) {
      return ucStateProvinces[i].codes;
    }
  }

  return new Array();
}

function getIpAddress(args) {
  var result = null;

  // Do we want async?
  var async = false;
  var onComplete;

  if (args != undefined && args.async != undefined) {
    async = args.async;
  }
  if (args != undefined && args.onComplete != undefined) {
    onComplete = args.onComplete;
  }

  // Send the request
  new Request({url: callbackUrl, async: async, onSuccess: function(responseText) {
    // Store the result into our variable.
    result = responseText;

    // Call their function
    if (async && onComplete != undefined) {
      onComplete(responseText);
    }
    
  }}).post({'functionName': 'getIpAddress', 'merchantId': merchantId, 'version': version});

  return result;
}

// Create, or get cart instance
function getCartInstance()
{
  // Return the cart we already have
  if (cart != null) return cart;

  if (Cookie.read('UltraCartShoppingCartID'))
  {
    cart = getCart(Cookie.read('UltraCartShoppingCartID'));
    if (cart == null)
    {
      Cookie.dispose('UltraCartShoppingCartID');
      cart = createCart();
      Cookie.write('UltraCartShoppingCartID', cart.cartId, {path: '/'});
    }
  }
  else
  {
    cart = createCart();
    Cookie.write('UltraCartShoppingCartID', cart.cartId, {path: '/'});
  }
  return cart;
}

function initializeCheckoutAPI(mid, shn, cbu) {
  merchantId = mid;
  if (shn != null) secureHostName = shn;
  if (cbu != null) {
    callbackUrl = cbu;
  } else {
    callbackUrl = "https://" + secureHostName + "/cgi-bin/UCCheckoutAPIJSON";
  }
}

function subscribeToAutoResponder(autoResponderName, listIds, args) {
  sanitizeDataTypes();
  var result = genericCall({'functionName': 'subscribeToAutoResponder', 'merchantId': merchantId, 'version': version, 'parameter1': JSON.encode(cart), 'parameter2': JSON.encode(autoResponderName), 'parameter3': JSON.encode(listIds)}, args);
  if (result != null && result.cart != null) setCart(result.cart);
  if (result == null) return ["subscribeToAutoResponder result was null"];
  return result.errors;
}

function getParameterValues(parameterName) {
  var result = new Array();

  // Make sure there is a query parameter
  if (window.location.search == null) return result;

  // Get everything after the ?
  var query = window.location.search.substring(1);

  // Split into name/value pairs
  var vars = query.split("&");
  for (var i = 0; i < vars.length; i++) {

    // Split into name and value array
    var pair = vars[i].split("=");

    // Does the name match our errorParameterName?
    if (pair[0] == parameterName) {

      // Add it to the result, but properly decode it.
      result[result.length] = javaUrlDecode(pair[1]);
    }
  }

  return result;
}

function getParameterValue(parameterName) {

  // Make sure there is a query parameter
  if (window.location.search == null) return result;

  // Get everything after the ?
  var query = window.location.search.substring(1);

  // Split into name/value pairs
  var vars = query.split("&");
  for (var i = 0; i < vars.length; i++) {

    // Split into name and value array
    var pair = vars[i].split("=");

    // Does the name match our errorParameterName?
    if (pair[0] == parameterName) {

      return javaUrlDecode(pair[1]);
    }
  }

  return null;
}

// Helper method for getErrorsFromQueryString
function javaUrlDecode(s) {
  return _utf8_decode(unescape(s)).replace(/\+/g, ' ');
}

// Private helper method for javaUrlDecode
function _utf8_decode(utftext) {
  var s = "";
  var i = 0;
  var c = c1 = c2 = 0;

  while (i < utftext.length) {
    c = utftext.charCodeAt(i);

    if (c < 128) {
      s += String.fromCharCode(c);
      i++;
    }
    else if ((c > 191) && (c < 224)) {
      c2 = utftext.charCodeAt(i + 1);
      s += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
      i += 2;
    }
    else {
      c2 = utftext.charCodeAt(i + 1);
      c3 = utftext.charCodeAt(i + 2);
      s += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
      i += 3;
    }
  }

  return s;
}

// Methods to help work with JSON seralized dates like shipOnDate and deliveryDate

function ucMonthNumberToAbbrev(m) {
  if (m == 0) return "Jan";
  if (m == 1) return "Feb";
  if (m == 2) return "Mar";
  if (m == 3) return "Apr";
  if (m == 4) return "May";
  if (m == 5) return "Jun";
  if (m == 6) return "Jul";
  if (m == 7) return "Aug";
  if (m == 8) return "Sep";
  if (m == 9) return "Oct";
  if (m == 10) return "Nov";
  if (m == 11) return "Dec";
  return "Dec";
}

function ucGetHoursAMPM(h) {
  if (h >= 12) h = h - 12;
  if (h == 0) return 12;
  return h;
}

function ucGetAMPM(h) {
  if (h < 12) return "AM";
  return "PM";
}

function ucPadTwo(v) {
  var s = "" + v;
  if (s.length == 1) s = "0" + s;
  return s;
}

function ucJsonStringToDate(s) {
  if (s == null) return null;
  return new Date(s);
}

function ucDateToJsonString(d) {
  if (d == null) return null;
  return ucMonthNumberToAbbrev(d.getMonth()) + " " + d.getDate() +", " + d.getFullYear() + " " + ucGetHoursAMPM(d.getHours()) + ":" + ucPadTwo(d.getMinutes()) + ":" + ucPadTwo(d.getSeconds()) + " " + ucGetAMPM(d.getHours());
}

// Validation Options
var OPTION_ITEM_QUANTITY_VALID = "Item Quantity Valid";
var OPTION_BILLING_ADDRESS_PROVIDED = "Billing Address Provided";
var OPTION_BILLING_STATE_ABBREVIATION_VALID = "Billing State Abbreviation Valid";
var OPTION_BILLING_BILLING_PHONE_NUMBERS_PROVIDED = "Billing Phone Numbers Provided";
var OPTION_EMAIL_PROVIDED_IF_REQUIRED = "Email provided if required";
var OPTION_BILLING_VALIDATE_CITY_STATE_ZIP = "Billing Validate City State Zip";
var OPTION_TAX_COUNTY_SPECIFIED = "Tax County Specified";
var OPTION_SHIPPING_METHOD_PROVIDED = "Shipping Method Provided";
var OPTION_ADVERTISING_SOURCE_PROVIDED = "Advertising Source Provided";
var OPTION_REFERRAL_CODE_PROVIDED = "Referral Code Provided";
var OPTION_SHIPPING_ADDRESS_PROVIDED = "Shipping Addres Provided";
var OPTION_SHIPPING_STATE_ABBREVIATION_VALID = "Shipping State Abbreviation Valid";
var OPTION_GIFT_MESSAGE_LENGTH = "Gift Message Length";
var OPTION_SHIPPING_VALIDATE_CITY_STATE_ZIP = "Shipping Validate City State Zip";
var OPTION_SHIPPING_DESTINATION_RESTRICTION = "Shipping Destination Restriction";
var OPTION_ONE_PER_CUSTOMER_VIOLATIONS = "One per customer violations";
var OPTION_PAYMENT_METHOD_SHIPPING_METHOD_CONFLICT = "Credit Card Shipping Method Conflict";
var OPTION_PAYMENT_INFORMATION_VALIDATE = "Payment Information Validate";
var OPTION_PAYMENT_METHOD_PROVIDED = "Payment Method Provided";
var OPTION_QUANTITY_REQUIREMENTS_MET = "Quantity requirements met";
var OPTION_ITEMS_PRESENT = "Items Present";
var OPTION_OPTIONS_PROVIDED = "Options Provided";
var OPTION_CVV2_NOT_REQUIRED = "CVV2 Not Required";
var OPTION_ELECTRONIC_CHECK_CONFIRM_ACCOUNT_NUMBER = "Electronic Check Confirm Account Number";
var OPTION_CUSTOMER_PROFILE_DOES_NOT_EXIST = "Customer Profile Does Not Exist.";
var OPTION_VALID_SHIP_ON_DATE = "Valid Ship On Date";
var OPTION_PRICING_TIER_LIMITS = "Pricing Tier Limits";
var OPTION_SHIPPING_NEEDS_RECALCULATION = "Shipping Needs Recalculation";
var OPTION_MERCHANT_SPECIFIC_ITEM_RELATIONSHIPS = "Merchant Specific Item Relationships";
var OPTION_ALL = "All";

// Types of payment method
var PAYMENT_METHOD_CREDIT_CARD = "Credit Card";
var PAYMENT_METHOD_PURCHASE_ORDER = "Purchase Order";
var PAYMENT_METHOD_PAYPAL = "PayPal";

// Types of credit cards
var CREDIT_CARD_TYPE_AMEX = "AMEX";
var CREDIT_CARD_TYPE_DISCOVER = "Discover";
var CREDIT_CARD_TYPE_MASTERCARD = "MasterCard";
var CREDIT_CARD_TYPE_JCB = "JCB";
var CREDIT_CARD_TYPE_DINERS_CLUB = "Diners Club";
var CREDIT_CARD_TYPE_VISA = "Visa";

// Types of options
var OPTION_TYPE_SINGLE = "single";
var OPTION_TYPE_MULTILINE = "multiline";
var OPTION_TYPE_DROPDOWN = "dropdown";
var OPTION_TYPE_HIDDEN = "hidden";
var OPTION_TYPE_RADIO = "radio";
var OPTION_TYPE_FIXED = "fixed";

// Distance units of measure
var DISTANCE_UOM_IN = "IN";
var DISTANCE_UOM_CM = "CM";

// Item multimedia types
var ITEM_MULTIMEDIA_TYPE_IMAGE = "Image";
var ITEM_MULTIMEDIA_TYPE_VIDEO = "Video";
var ITEM_MULTIMEDIA_TYPE_UNKNOWN = "Unknown";
var ITEM_MULTIMEDIA_TYPE_PDF = "PDF";
var ITEM_MULTIMEDIA_TYPE_TEXT = "Text";

// Weight units of measure
var WEIGHT_UOM_LB = "LB";
var WEIGHT_UOM_KG = "KG";

// Auto response names
var AUTO_RESPONDER_NAME_ICONTACT = "icontact";
var AUTO_RESPONDER_NAME_SILVERPOP = "silverpop";
var AUTO_RESPONDER_NAME_MAILCHIMP = "mailchimp";
var AUTO_RESPONDER_NAME_LYRIS = "lyris";
var AUTO_RESPONDER_NAME_CAMPAIGNMONITOR = "campaignMonitor";
var AUTO_RESPONDER_NAME_GETRESPONSE = "getResponse";

var AUTO_RESPONDER_NAMES = [
  AUTO_RESPONDER_NAME_ICONTACT,
  AUTO_RESPONDER_NAME_SILVERPOP,
  AUTO_RESPONDER_NAME_MAILCHIMP,
  AUTO_RESPONDER_NAME_LYRIS,
  AUTO_RESPONDER_NAME_CAMPAIGNMONITOR,
  AUTO_RESPONDER_NAME_GETRESPONSE
];