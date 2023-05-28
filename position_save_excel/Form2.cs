using System;
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
using System.Data.Common;
//using MySql.Data.MySqlClient;

namespace position_save_excel
{
    public partial class Form2 : Form
    {
        int grade_defi;
        int grade_depth;
        int grade_overall;
        public static int row = 2;
        public static int column = 1;
        

        public Form2()
        {
            
            FormBorderStyle = FormBorderStyle.None;
            InitializeComponent();
            this.WindowState = FormWindowState.Maximized;
            this.AcceptButton = Save_result;   //默认回车键
            this.KeyPreview = true;

            label2.Text = Form1.i.ToString()+"/"+Form1.num.ToString();

            //2017-09-19改  修改打分界面适应屏幕尺寸

            int SH = Screen.PrimaryScreen.Bounds.Height;
            int SW = Screen.PrimaryScreen.Bounds.Width;
            int w = Convert.ToInt32(SW / 12 * 2);
            int h = Convert.ToInt32(SH / 2);

            this.question_name.Size = new Size(w, h);
            //      if (this.Save_result!= null)
            //      Save_result.Size = new Size(10, 20);
            //groupBox1.Size = new Size(w, h);

            //2017-09-19改
            overallBox.Size = new Size(w, h);



            int x = Convert.ToInt32(SW / 24 * 6 - this.question_name.Size.Width / 2);
            int y = Convert.ToInt32(SH / 2 - this.question_name.Size.Height / 2);
            question_name.Location = new Point(x, y);

            x = Convert.ToInt32(SW / 24 * 12 - this.question_name.Width / 2);
//            y = Convert.ToInt32(SH / 2 - this.question_name.Height / 2);
            //groupBox1.Location = new Point(x, y);

            //2017-09-19改
            x = Convert.ToInt32(SW / 24 * 18 - this.question_name.Width / 2);
            overallBox.Location = new Point(x, y);

            x = Convert.ToInt32(SW / 7 * 3);
            y = Convert.ToInt32(SH / 7 * 6);
            Save_result.Location = new Point(x, y);

            x = Convert.ToInt32(SW / 7 * 3);
            y = Convert.ToInt32(SH / 14 * 11);
            groupBox2.Location = new Point(x, y);


        }
        public class KillExcel
        {
            [DllImport("User32.dll", CharSet = CharSet.Auto)]
            public static extern int GetWindowThreadProcessId(IntPtr hwnd, out int ID);


            /// <summary>  
            /// 强制关闭当前Excel进程  
            /// </summary>  
            public static void Kill(IntPtr intPtr)
            {
                try
                {
                    Process[] ps = Process.GetProcesses();
                    int ExcelID = 0;
                    GetWindowThreadProcessId(intPtr, out ExcelID); //得到本进程唯一标志k     
                    foreach (Process p in ps)
                    {
                        if (p.ProcessName.ToLower().Equals("excel"))
                        {
                            if (p.Id == ExcelID)
                            {
                                p.Kill();
                            }
                        }
                    }
                }
                catch
                {
                    //不做任何处理     
                }
            }
        }
        private bool WriteGrade(string filename,int picno, int g1,int g2,int g3,int i)
        {
            //启动Excel应用程序
            Excel.Application xls = new Excel.Application();
            Excel.Workbook book = xls.Workbooks.Open(filename);

            xls.Visible = false;//设置Excel后台运行
            xls.DisplayAlerts = false;//设置不显示确认修改提示

            xls.Cells[row, column] = Form1.current_image;
            column++;
            xls.Cells[row, column] = picno;
            column++;
            xls.Cells[row, column] = g1;
            column++;
            //xls.Cells[row, column] = g2;
            //column++;
            xls.Cells[row, column] = g3;
            row++;
            column = 1;
            book.Save();
            book.Close(false, Missing.Value, Missing.Value);


            xls.Quit();
            
            xls = null;
            book = null;
            GC.Collect();

            return true;
        }


        private void Save_result_Click(object sender, EventArgs e)
        {
            
            if (overallButton5.Checked || overallButton4.Checked || overallButton3.Checked
                        || overallButton2.Checked || overallButton1.Checked)
            {
                
                StreamWriter ss = File.AppendText(".\\light_filed_image_subjective_exp\\user_defi_" + login.s + ".txt");
                string picnum = Form1.pictrue_num.ToString();
                ss.Write("imagenum：" + picnum + "\r\n");
                ss.Close();
           
                StreamWriter sw = File.AppendText(".\\light_filed_image_subjective_exp\\user_defi_" + login.s + ".txt");

                if (Button1.Checked)
                {
                    string w = "5\r\n";
                    sw.Write(w);
                    sw.Close();
                    grade_defi = 5;
                }
                else if (Button2.Checked)
                {
                    string w = "4\r\n";
                    sw.Write(w);
                    sw.Close();
                    grade_defi = 4;
                }
                else if (Button3.Checked)
                {
                    string w = "3\r\n";
                    sw.Write(w);
                    sw.Close();
                    grade_defi = 3;

                }
                else if (Button4.Checked)
                {
                    string w = "2\r\n";
                    sw.Write(w);
                    sw.Close();
                    grade_defi = 2;
                }
                else if (Button5.Checked)
                {
                    string w = "1\r\n";
                    sw.Write(w);
                    sw.Close();
                    grade_defi = 1;
                }

                StreamWriter sd = File.AppendText(".\\light_filed_image_subjective_exp\\user_depth_" + login.s + ".txt");

                sd.Write("imagenum：" + picnum + "\r\n");
                sd.Close();
                //  StreamWriter sw = File.AppendText(".\\light_filed_image_subjective_exp\\light_filed_image_subjective_exp.txt");
                
               
                //2017-09-19改
                StreamWriter overallTxt = File.AppendText(".\\light_filed_image_subjective_exp\\user_overall_" + login.s + ".txt");

                overallTxt.Write("imagenum：" + picnum + "\r\n");
                overallTxt.Close();
                StreamWriter overallTxt2 = File.AppendText(".\\light_filed_image_subjective_exp\\user_overall_" + login.s + ".txt");

                if (overallButton5.Checked)
                {
                    string w = "5\r\n";
                    overallTxt2.Write(w);
                    overallTxt2.Close();
                    grade_overall = 5;
                }
                else if (overallButton4.Checked)
                {
                    string w = "4\r\n";
                    overallTxt2.Write(w);
                    overallTxt2.Close();
                    grade_overall = 4;
                }
                else if (overallButton3.Checked)
                {
                    string w = "3\r\n";
                    overallTxt2.Write(w);
                    overallTxt2.Close();
                    grade_overall = 3;
                }
                else if (overallButton2.Checked)
                {
                    string w = "2\r\n";
                    overallTxt2.Write(w);
                    overallTxt2.Close();
                    grade_overall = 2;
                }
                else if (overallButton1.Checked)
                {
                    string w = "1\r\n";
                    overallTxt2.Write(w);
                    overallTxt2.Close();
                    grade_overall = 1;
                }


                this.Close();
                //this.Hide();

                if (Form1.i != Form1.num + 1)
                {
                    WriteGrade(login.file_excel, Form1.pictrue_num, grade_defi, grade_depth,grade_overall,Form1.i);
                }

                if (Form1.i == Form1.num)
                {
                    MessageBox.Show("Thank you for cooperation. That's all.");
                    //     Close();
                    //  StreamWriter st = File.AppendText(".\\light_filed_image_subjective_exp\\light_filed_image_subjective_exp.txt");
                    StreamWriter st = File.AppendText(".\\light_filed_image_subjective_exp\\user_defi_" + login.s + ".txt");

                    string dt = DateTime.Now.ToString();
                    st.Write(dt + "\r\n");
                    st.Close();
                   

                }

            }
                else
                {
                    MessageBox.Show("Please check your grades.");

                }
                // imagepath = @"D:\Pictures\9.jpg";
                //  Form1.pictureBox1.ImageLocation = imagepath;
                //  this.Visible = false;
               
            }

        private void Form2_FormClosing(object sender, FormClosingEventArgs e)
        {
          //  System.Environment.Exit(0);
        }

        private void Form2_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == (char)27)
            {
                Formexit f3 = new Formexit();
                f3.ShowDialog();
            }
        }

        private void Form2_Load(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }
    }
}
