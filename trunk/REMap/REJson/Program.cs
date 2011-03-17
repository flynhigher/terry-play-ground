using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Security.Policy;
using System.Text;
using Microsoft.Practices.EnterpriseLibrary.Data;

namespace REJson {
	class Program {
		static void Main(string[] args) {
			string filename = args.Length > 0 ? args[0] : "properties.txt";
			using (StreamWriter writer = new StreamWriter(filename)) {
				writer.WriteLine("{\"items\":[");
				Database db = DatabaseFactory.CreateDatabase("REMap");
				using (IDataReader reader = db.ExecuteReader(CommandType.Text, "SELECT * FROM REProperty ORDER BY Price DESC")) {
					while (reader.Read()) {
						writer.WriteLine("{" + String.Format("\"i\":\"{0}\",\"p\":\"{1}\",\"s\":\"{2}\",\"a1\":\"{3}\",\"a2\":\"{4}\",\"u\":\"{5}\",\"ph\":\"{6}\",\"lo\":\"{7}\",\"la\":\"{8}\",\"d\":\"{9}\"", reader["Id"].ToString().Trim(), reader["Price"].ToString().Trim(), reader["Style"].ToString().Trim(), reader["StreetAddress"].ToString().Trim(), reader["Town"].ToString().Trim() + ", " + reader["State"].ToString().Trim(), reader["Url"].ToString().Trim(), reader["PhotoUrl"].ToString().Trim(), reader["Longitude"].ToString().Trim(), reader["Latitude"].ToString().Trim(), reader["CreatedDate"].ToString().Trim()) + "},");
					}
				}
				writer.WriteLine("]}");
			}
		}
	}
}