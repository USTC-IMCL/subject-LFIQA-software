﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using Excel = Microsoft.Office.Interop.Excel;
using System.Reflection;
using System.Data.OleDb;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading;
//using MySql.Data.MySqlClient;

/*
 * username: []
 * image hrizontal number
 * image vertical number
 * display mode: 2D or 3D
 *
 * 
*/

namespace position_save_excel
{
    public partial class login : Form
    {
        public static string Current = Directory.GetCurrentDirectory();//获取当前根目录,
        public static string file_excel;
        public static int num_horizontal_images;
        public static int num_vertical_images;
        public static string s;
        public login()
        {
            InitializeComponent();
            this.WindowState = FormWindowState.Maximized;
            this.AcceptButton = NEXT;   //默认回车键
            this.Visible = true;
            int SH = Screen.PrimaryScreen.Bounds.Height;
            int SW = Screen.PrimaryScreen.Bounds.Width;
           
            groupBox1.Size = new Size(Convert.ToInt32(SW / 3), Convert.ToInt32(SH / 3));        //  1920 / 3 = 640; 1080 / 3 = 360;
            int x = Convert.ToInt32(SW / 2 - groupBox1.Width/ 2);                               //  1920 / 2 - 640 / 2 = 960 - 320 = 640
            int y = Convert.ToInt32(SH / 3 - groupBox1.Height/ 2);
            groupBox1.Location = new Point(x, y);               //  box location

            NEXT.Size = new Size(Convert.ToInt32(SW / 18), Convert.ToInt32( SH / 30));          // 
            x = Convert.ToInt32(groupBox1.Size.Width / 2 - NEXT.Size.Width / 2);                //  640 / 2 - 100 / 2 = 270
            y = Convert.ToInt32(groupBox1.Size.Height / 6*5 - NEXT.Size.Height / 2);            //  360 / 6 * 5 - 36 / 2 = 282
            NEXT.Location = new Point(x, y);                    


            textBox1.Size = new Size(Convert.ToInt32(SW / 10), Convert.ToInt32(SH / 30));       //  
            x = Convert.ToInt32(groupBox1.Size.Width / 2 - textBox1.Size.Width );               //  640 / 2 - SW / 10 = 320 - 190 = 130
            y = Convert.ToInt32(groupBox1.Size.Height / 6 * 2 - textBox1.Size.Height);          //  360 / 6 * 2 - SH / 30 = 120 - 1080 / 30 = 84
            label1.Location = new Point(x, y);
            x = Convert.ToInt32(groupBox1.Size.Width / 2 - textBox1.Size.Width + label1.Size.Width * 1.2);
            textBox1.Location = new Point(x, y);

            x = Convert.ToInt32(groupBox1.Size.Width / 2 - textBox1.Size.Width);               //  640 / 2 - SW / 10 = 320 - 190 = 130
            y = Convert.ToInt32(groupBox1.Size.Height / 6 * 2 + textBox1.Size.Height * 1.5);          //  360 / 6 * 2 - SH / 30 = 120 - 1080 / 30 = 84
            label2.Location = new Point(x, y);
            x = Convert.ToInt32(groupBox1.Size.Width / 2 - textBox1.Size.Width + label2.Size.Width + 10);
            numHorizontalImages.Location = new Point(x, y);

            x = Convert.ToInt32(groupBox1.Size.Width / 2 - textBox1.Size.Width);
            y = Convert.ToInt32(groupBox1.Size.Height / 6 * 2 + textBox1.Size.Height * 1.5 + label2.Size.Height * 1.5);
            label3.Location = new Point(x, y);
            x = Convert.ToInt32(groupBox1.Size.Width / 2 - textBox1.Size.Width + label2.Size.Width + 10);
            numVerticalImages.Location = new Point(x, y);
        }

        void starttime(string s)
        {
            
        }
       
       private bool WriteXls(string filename)
        {
            //启动Excel应用程序
            Excel.Application xls = new Excel.Application();
            Excel.Workbook book =   xls.Workbooks.Add(true);

            //如果表已经存在，可以用下面的命令打开
            //Excel.Workbook book = xls.Workbooks.Open(filename);

            xls.Visible = false;//设置Excel后台运行
            xls.DisplayAlerts = false;//设置不显示确认修改提示

            xls.Cells[1,1] = "fileName" ;
            xls.Cells[1,2] = "displayOrder";
            xls.Cells[1,3] = "pictureQuality";
            //xls.Cells[1,4] = "Refocus";
            xls.Cells[1,4] = "overallQuality";
           //2017-09-19改
 //         xls.Cells[2,1] = s;

            book.SaveAs(filename, Type.Missing, "", "", false, Type.Missing, Excel.XlSaveAsAccessMode.xlNoChange, 1, false, Type.Missing, Type.Missing, Type.Missing);
            //xbook.Save();
            book.Close(false, Missing.Value, Missing.Value);
            
            //GC.Collect(System.GC.GetGeneration(worksheet));
            //GC.Collect(System.GC.GetGeneration(workbook));
            GC.Collect(System.GC.GetGeneration(xls));

            xls.Quit();
            System.Runtime.InteropServices.Marshal.ReleaseComObject(xls);
            book = null;
            xls = null;
          //   System.Runtime.InteropServices.Marshal.ReleaseComObject(xls);
            GC.Collect();//系统回收资源*/
            return true;
        }



    

        private void NEXT_Click(object sender, EventArgs e)
        {
            s = textBox1.Text;
            num_horizontal_images = (int)numHorizontalImages.Value;
            num_vertical_images = (int)numVerticalImages.Value;

            MessageBox.Show("OK");

            if (!Directory.Exists(@".\light_filed_image_subjective_exp"))
            {
                Directory.CreateDirectory(@".\light_filed_image_subjective_exp");
            }

            if (!File.Exists(".\\light_filed_image_subjective_exp\\user_defi_"+s+".txt:\\TestTxt.txt"))
            {
                FileStream fs = new FileStream(".\\light_filed_image_subjective_exp\\user_defi_" + s + ".txt", FileMode.OpenOrCreate);
                StreamWriter ms = new StreamWriter(fs);

                ms.WriteLine(" result:\n");
                ms.Close();
            }
            
            StreamWriter ss = File.AppendText(".\\light_filed_image_subjective_exp\\user_defi_" + s + ".txt");
           
            string dt = DateTime.Now.ToString();
            ss.Write("\r\n user： "+s + "\r\n" + dt + "\r\n");
            ss.Close();

            //create a new txt
            if (!File.Exists(".\\light_filed_image_subjective_exp\\user_depth_" + s + ".txt:\\TestTxt.txt"))
            {
                FileStream fs = new FileStream(".\\light_filed_image_subjective_exp\\user_depth_" + s + ".txt", FileMode.OpenOrCreate);
                StreamWriter ms = new StreamWriter(fs);

                ms.WriteLine(" light_filed_image_subjective_exp:\n");
                ms.Close();
            }
            

            StreamWriter ss1 = File.AppendText(".\\light_filed_image_subjective_exp\\user_depth_" + s + ".txt");
            
           
            ss1.Write("\r\n user： " + s + "\r\n" + dt + "\r\n");
            ss1.Close();

            file_excel = Current + "\\light_filed_image_subjective_exp\\light_filed_image_subjective_exp_" + s + ".xlsx";
            WriteXls(file_excel);

            this.Hide();  //跳出新的窗体form2 
            Form1 f2 = new Form1();
            f2.ShowDialog();
        }
    }
}
