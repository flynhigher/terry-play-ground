using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Common;
using System.Text;
using Microsoft.Practices.EnterpriseLibrary.Data;

namespace REScraper {
	public class REPropertyDataAccessor {
		public void Insert(List<REPropertyInfo> propList) {
			foreach (REPropertyInfo propertyInfo in propList) {
				Insert(propertyInfo);
			}
		}
		
		public void Insert(REPropertyInfo propInfo) {
			Database db = DatabaseFactory.CreateDatabase("REMap");
			db.ExecuteNonQuery("usp_insert_property", propInfo.Source, propInfo.Id, propInfo.Price, propInfo.Style, propInfo.Bedrooms, propInfo.Bathrooms, propInfo.StreetAddress, propInfo.Town, propInfo.State, propInfo.Zipcode, propInfo.Url, propInfo.PhotoUrl, propInfo.Status, propInfo.Longitude, propInfo.Latitude, propInfo.Description);
		}
		
		public REPropertyInfo Get(string source, string id) {
			Database db = DatabaseFactory.CreateDatabase("REMap");
			using (IDataReader reader = db.ExecuteReader(CommandType.Text, String.Format("SELECT * FROM REProperty WHERE Source = {0} AND Id = {1}", source, id))) {
				while (reader.Read()) {
					return REPropertyInfo.LoadFromReader(reader);
				}
			}
			return null;
		}
		
		public List<REPropertyInfo> GetAllList() {
			List<REPropertyInfo> list = new List<REPropertyInfo>();
			Database db = DatabaseFactory.CreateDatabase("REMap");
			using (IDataReader reader = db.ExecuteReader(CommandType.Text, "SELECT * FROM REProperty")) {
				while (reader.Read()) {
					list.Add(REPropertyInfo.LoadFromReader(reader));
				}
			}
			return list;
		}
	}
}
