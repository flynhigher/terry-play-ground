<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="REMap._Default" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" >
<head runat="server">
    <title>Real Estate Map</title>
    <script src="script/XHConn.js" type="text/javascript"></script>
    <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAWODszYhDtC7_xwLICoryGBR_6XnM6K3P7KD04N15PQBX6Gwb9hTyOTRZVGi-pHTzDD8k-re8XhAbkg"
      type="text/javascript"></script>
    <script type="text/javascript">
    //<![CDATA[
        function load() {
            if (GBrowserIsCompatible()) {
                var map = new GMap2(document.getElementById("map"));
				map.addControl(new GSmallMapControl());
				map.addControl(new GMapTypeControl());
                var geocoder = new GClientGeocoder();
				geocoder.getLatLng("280 marin blvd jersey city nj", function(point) {
					if (!point) {
						alert(address + " not found");
					} else {
						map.setCenter(point, 13);
					}
				});

                // Create our "tiny" marker icon
                var icon = new GIcon();
                icon.image = "http://labs.google.com/ridefinder/images/mm_20_red.png";
                icon.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png";
                icon.iconSize = new GSize(12, 20);
                icon.shadowSize = new GSize(22, 20);
                icon.iconAnchor = new GPoint(6, 20);
                icon.infoWindowAnchor = new GPoint(5, 1);

	            // XMLHttpRequest completion function
                var myConn = new XHConn();
                if (!myConn) alert("XMLHTTP not available. Try a newer/better browser.");
	            var OnComplete = function(resXml){
		            var o = eval('(' + resXml.responseText + ')');
		            for (var i=0; i < o.items.length; i++){
			            AddPropertyOverlay(o.items[i]);
		            }
	            }
                myConn.connect("properties.txt", "GET", "", OnComplete);

                function AddPropertyOverlay(p) {
                        var marker = new GMarker(new GLatLng(p.la, p.lo), icon);
                        GEvent.addListener(marker, "click", function() {
                          marker.openInfoWindowHtml("#" + p.i + "<br>Price: $" + p.p + "<br>Style: " + p.s + "<br>Address: " + p.a1 + "<br>" + p.a2 + "<br><a href=\"" + p.u + "\">Orig. Listing</a>");
                        });
                        map.addOverlay(marker);
                }
			}
		}

		function getPointFromGeoResponse(response) {
			if (!response || response.Status.code != 200) {
				alert("\"" + address + "\" not found");
			} else {
				place = response.Placemark[0];
				return new GLatLng(place.Point.coordinates[1],
														place.Point.coordinates[0]);
			}
		}

		// Creates a marker at the given point with the given number label
		function createMarker(point, number) {
			var marker = new GMarker(point);
			GEvent.addListener(marker, "click", function() {
				marker.openInfoWindowHtml("Marker #<b>" + number + "</b><br>Point: " + point);
			});
			return marker;
		}
    //]]>
    </script>
</head>
 <body onload="load()" onunload="GUnload()">
    <form id="form1" runat="server">
    <div id="map" style="width: 1000px; height: 800px"></div>
    </form>
</body>
</html>
