using System;
using System.Data;
using System.Configuration;
using System.Collections;
using System.Web;
using System.Web.Security;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.WebControls.WebParts;
using System.Web.UI.HtmlControls;
using Microsoft.Practices.EnterpriseLibrary.Data;

namespace REMap {
	public partial class List : System.Web.UI.Page {
		protected void Page_Load(object sender, EventArgs e) {
			Database db = DatabaseFactory.CreateDatabase("REMap");
			using (IDataReader reader = db.ExecuteReader(CommandType.Text, "SELECT * FROM REProperty ORDER BY Price DESC")) {
				while (reader.Read()) {
					for (int i=0;i<reader.FieldCount;i++) {
						if(i==0 || i==1) continue;
						if (i == 2) data.Text += "$";
						if(i==6)
							data.Text += "<a href=\"http://maps.google.com/maps?q=";
						if (i == 10)
							data.Text += "<a href=\"" + reader[i].ToString() + "\">listing</a>|";
						else if(i == 11)
							data.Text += "<img src=\"" + reader[i].ToString() + "\">|";
						else
							data.Text += reader[i].ToString() + "|";
						if(i==9)
							data.Text += "\">" + reader[6].ToString() + " " + reader[7].ToString() + " " + reader[8].ToString() + " " + reader[9].ToString() + "</a>|";
					}
					data.Text += "<br><br>";
				}
			}
		}
	}
}
