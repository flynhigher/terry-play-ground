/*
using System;
using System.IO;
using System.Threading;
using WatiN.Core;
using WatiN.Core.DialogHandlers;
using WatiN.Core.Exceptions;
using WatiN.Core.Interfaces;
using WatiN.Core.Logging;

namespace TestSpace
{
	public class TestClass
	{
		[STAThread]
		static void Main()
		{
			SDYD250();

			System.Environment.Exit(0);
		}
	
		
public static void SDYD250 ()
{
			IE ie = new IE("about:blank");
            ie.ShowWindow(NativeMethods.WindowShowStyle.Hide);
		ie.GoTo("http://www.amazon.com/exec/obidos/tg/detail/-/B00005QFL0/");
        Table t = ie.Table(Find.By("classname", "product"));
        TableRow r = t.TableRows[1];
        TableCell c1 = r.TableCells[0];
        if (c1.Text == "Price:")
        {
            string s = r.TableCells[1].Text;
            Console.WriteLine(s.Substring(1, s.IndexOf(' ')));
        }
        else
            Console.WriteLine("Error: document changed!");
        Console.Read();
}


	}
}

*/