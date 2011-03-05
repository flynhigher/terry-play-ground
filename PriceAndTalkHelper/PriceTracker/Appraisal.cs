using System;
using System.Collections.Generic;
using System.IO;
using WatiN.Core;
using WatiN.Core.Exceptions;

namespace TestSpace {
	public class TestClass {
		[STAThread]
		private static void Main() {
			SDYD250();

			Environment.Exit(0);
		}


		public static void SDYD250() {
			IE ie = new IE("about:blank");
			ie.ShowWindow(NativeMethods.WindowShowStyle.Hide);
			using(StreamWriter writer = new StreamWriter("data.txt")) {
				writer.Write("Block:");
				writer.Write(",");
				writer.Write("Lot:");
				writer.Write(",");
				writer.Write("Prop Loc:");
				writer.Write(",");
				writer.Write("Land Desc:");
				writer.Write(",");
				writer.Write("Bldg Desc:");
				writer.Write(",");
				writer.Write("Taxes:");
				writer.Write(",");
				writer.Write("Sale Date:");
				writer.Write(",");
				writer.Write("Price:");
				writer.Write(",");
				writer.WriteLine("NU#:");
				for(int blockNum = 1; blockNum <= 106; blockNum++) {
					ie.GoTo("http://tax1.co.monmouth.nj.us/cgi-bin/prc6.cgi?&ms_user=glou&passwd=data&district=0912");
					SelectList listSize = ie.SelectList(Find.By("name", "ms_ln"));
					listSize.Select("1000");
					TextField block = ie.TextField(Find.By("name", "block"));
					block.TypeText(blockNum.ToString());
					ie.Forms[0].Submit();
					List<string> links = new List<string>();
					Button submit = null;
					bool goNextPage = false;
					do {
						foreach(Link l in ie.Links) {
							links.Add(l.Url);
						}
						try {
							submit = ie.Button(Find.By("value", "Next"));
							if(submit != null && submit.Text.ToLower() == "next") {
								ie.Forms[0].Submit();
								goNextPage = true;
							}
						} catch(ElementNotFoundException e) {}
					} while(goNextPage);

					foreach(string url in links) {
						ie.GoTo(url);
						writer.Write(GetData("Block:", ie.Tables));
						writer.Write(",");
						writer.Write(GetData("Lot:", ie.Tables));
						writer.Write(",");
						writer.Write(GetData("Prop Loc:", ie.Tables));
						writer.Write(",");
						writer.Write(GetData("Land Desc:", ie.Tables));
						writer.Write(",");
						writer.Write(GetData("Bldg Desc:", ie.Tables));
						writer.Write(",");
						writer.Write(GetData("Taxes:", ie.Tables));
						writer.Write(",");
						writer.Write(GetData("Sale Date:", ie.Tables));
						writer.Write(",");
						string priceData = GetData("Price:", ie.Tables);
						string[] split = priceData.Split(new string[] {"NU#:"}, StringSplitOptions.RemoveEmptyEntries);
						writer.Write(split[0]);
						if(split.Length > 1) {
							writer.Write(",");
							writer.WriteLine(split[1]);
						}
						writer.WriteLine("");
					}
				}

			}
			//ie.ShowWindow(NativeMethods.WindowShowStyle.Show);
			//ie.CaptureWebPageToFile("searchresult.htm");
			Console.WriteLine("Done!");
			Console.Read();
		}

		private static string GetData(string header, TableCollection tables) {
			int tableIndex = 0, rowIndex = 0, headerCellIndex = 0;
			switch(header) {
				case "Block:":
					tableIndex = rowIndex = 0;
					break;
				case "Lot:":
					tableIndex = 0;
					rowIndex = 1;
					break;
				case "Prop Loc:":
					tableIndex = 0;
					rowIndex = 0;
					headerCellIndex = 2;
					break;
				case "Land Desc:":
					tableIndex = 0;
					rowIndex = 5;
					headerCellIndex = 4;
					break;
				case "Bldg Desc:":
					tableIndex = 0;
					rowIndex = 6;
					headerCellIndex = 4;
					break;
				case "Taxes:":
					tableIndex = 0;
					rowIndex = 8;
					headerCellIndex = 6;
					break;
				case "Sale Date:":
					tableIndex = 0;
					rowIndex = 10;
					headerCellIndex = 0;
					break;
				case "Price:":
					tableIndex = 0;
					rowIndex = 10;
					headerCellIndex = 4;
					break;
					
			}
			Table table = tables[tableIndex];
			TableRow row = table.TableRows[rowIndex];
			TableCell[] ret = null;
			if(row.TableCells[headerCellIndex].Text.Trim() == header) {
				return row.TableCells[headerCellIndex + 1].Text;
			} else {
				throw new Exception("Error: document changed! I can't find the " + header);
			}
		}
	}
}