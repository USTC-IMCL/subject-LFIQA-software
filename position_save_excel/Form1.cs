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
//using MySql.Data.MySqlClient;




namespace position_save_excel
{
    public partial class Form1 : Form
    {
       
        ListViewItem lv;
        public static int pictrue_num = 1 ;
        public static string current_image;
        string mom_path = ".\\Picture\\";   // 当前目录下存储光场图像
        string son_path;
        string img_fn;
        string fold_path;
        string depth_path;
        // 2017-08-31新修改处
        string org_fold_path;
        string org_depth_path;
        string view_fold_path;
        string org_view_fold_path;

 //       public double lambda;
        string imagepath;
        public static int num = 0;
        public int[] randnum;
        //  public static int i = 0;
        public static int i = 1;
        public static string[] result_QP;
        public static string[] result_noQP;
        //USE MOUSE TO CHANGE VIEWS
        bool MoveFlag;
        bool ButtonFlag = true;
        int xPos, yPos;
        int CurrentY = 7;
        int CurrentX = 7;
        int StepX, StepY;
        int MouseRateDivder = 30;
        int max_num_horizontal_images   = 1;
        int max_num_vertical_images     = 1;
        int default_horizontal = 1;
        int default_vertical   = 1;
            

        public Form1()
        {
            FormBorderStyle = FormBorderStyle.None;
            InitializeComponent();
            this.WindowState = FormWindowState.Maximized;
            button2.Visible = false;
            //button1.Visible = false;
            this.KeyPreview = true;
            //设置图片框等控件位置
            int SH = Screen.PrimaryScreen.Bounds.Height;
            int SW = Screen.PrimaryScreen.Bounds.Width;


            int x = Convert.ToInt32(SW / 4 - 625 / 2);
            int y = Convert.ToInt32(SH / 2 - 434 / 2);
            pictureBox1.Location = new Point(x, y);

            max_num_horizontal_images   = login.num_horizontal_images;
            max_num_vertical_images     = login.num_vertical_images;
            default_horizontal          = (max_num_horizontal_images + 1) / 2;
            default_vertical            = (max_num_vertical_images + 1) / 2;


            x = Convert.ToInt32(SW / 4*3 - 625 / 2);
            y = Convert.ToInt32(SH / 2 - 434 / 2);
            //pictureBox2.Location = new Point(x, y);

            x = Convert.ToInt32(SW / 6);
            y = Convert.ToInt32(SH / 5 * 4);
            //button1.Location = new Point(x, y);
            listView1.Visible = false;
            x = Convert.ToInt32(SW / 11 * 5);
            y = Convert.ToInt32(SH / 5 * 4);
            To_assess.Location = new Point(x, y);

            //设置播放时间 此功能关闭
            timer1.Interval = 5000;//设置时间为15秒
            timer1.Tick += new EventHandler(timer1_Tick);
            timer1.Start();//窗体加载时这个计时器自动启动


            //  read all images
            List<string> list = new List<string>();
            using (TextReader reader = File.OpenText(".\\Picture\\data.txt"))   // write images to data.txt
            {
                string s = reader.ReadLine();
                while (s.Length != 0)
                {
                    list.Add(s);
                    s = reader.ReadLine();
                    num++;
                    if (s == null)
                    {
                        break;
                    }
                }
            }

            //转换成数组
            result_QP = (string[])list.ToArray();

            randnum = getRandomNum(num);                //生成随机的序列
            pictrue_num = randnum[0];                   //取第一个随机数
            
            img_fn = result_QP[pictrue_num - 1];            // HEVC_Bikes_39    distorted fold
            current_image = img_fn;

            org_view_fold_path = img_fn + "_views";

            imagepath = mom_path + org_view_fold_path + "\\"+ org_view_fold_path + "_" + default_vertical.ToString() + "_" + default_horizontal.ToString() + ".bmp";               // 
            pictureBox1.ImageLocation = imagepath;                                     //在Box1处显示distortion图像
            
            //对view图像显示
            //int len1 = son_path.Length;
            view_fold_path = org_view_fold_path;    //distortion image 视角变换路径

        }

       
        //计时器计时事件
        void timer1_Tick(object sender, EventArgs e)
        {
            if (pictrue_num == 13) { }
     //      else To_assess_Click(null,null);
        }

        
        private void Form1_MouseClick(object sender, MouseEventArgs e)
        {
           // Record_position();
            
            int i, j, gray_value;
            if (ButtonFlag == true)
            {//2017-10-27 kun
                //trackBar1.Value = 7;
                //trackBar2.Value = 7;
                CurrentY = 7;
                CurrentX = 7;
                //textBox3.Text = CurrentX.ToString();
                //textBox4.Text = CurrentY.ToString();
                Record_position();
                Point formPoint = this.pictureBox1.PointToClient(Control.MousePosition);
                i = formPoint.X;
                j = formPoint.Y;
                //  depth_path = mom_path + fold_path + "\\" + fold_path + "_depth.png";
                depth_path = ".\\Depth\\" + img_fn + ".png";             //读取失真图像的深度图

                Color[][] colorMatrix = GetBitMapColorMatrix(depth_path);
                gray_value = colorMatrix[i - 1][j - 1].G;

                imagepath = mom_path + img_fn + "\\" + img_fn + '_' + gray_value.ToString() + ".bmp";
                pictureBox1.ImageLocation = imagepath;

            }
                        
        }

        //读取txt文件中的图片名


            static char[] ToCharArray(string s)
            {
            //  string[] sdata = s.Split(',');
 
                char[] data = new char[s.Length];
                for (int i = 0; i < s.Length; i++)
                {
                
                data[i] = s[i];
                }
                return data;
            } 
      

    void Record_position()
        {
            Point formPoint = this.pictureBox1.PointToClient(Control.MousePosition);
            //     lv = new ListViewItem((((Cursor.Position.X))).ToString());
            //     lv.SubItems.Add( (((Cursor.Position.Y))).ToString());
            lv = new ListViewItem(formPoint.X.ToString());
            lv.SubItems.Add(formPoint.Y.ToString());
            listView1.Items.Add(lv);
            //给textbox一个值
            

        }
      

        private void button1_Click(object sender, EventArgs e)
        {
            ExportToExecl();
        }

        /// <summary>
        /// 执行导出数据
        /// </summary>
        public void ExportToExecl()
        {
            System.Windows.Forms.SaveFileDialog sfd = new SaveFileDialog();
            sfd.DefaultExt = "xls";
            sfd.Filter = "Excel文件(*.xls)|*.xls";
            if (sfd.ShowDialog() == DialogResult.OK)
            {
                DoExport(this.listView1, sfd.FileName);
            }
        }
        [DllImport("user32.dll")]
        static extern IntPtr SetParent(IntPtr hwc, IntPtr hwp);

              private void button2_Click(object sender, EventArgs e)
        {       }

        /// <summary>
        /// 具体导出的方法
        /// </summary>
        /// <param name="listView">ListView</param>
        /// <param name="strFileName">导出到的文件名</param>
        private void DoExport(ListView listView, string strFileName)
        {
            int rowNum = listView.Items.Count;
            int columnNum = listView.Items[0].SubItems.Count;
            int rowIndex = 1;
            int columnIndex = 0;
            if (rowNum == 0 || string.IsNullOrEmpty(strFileName))
            {
                return;
            }
            if (rowNum > 0)
            {

                Microsoft.Office.Interop.Excel.Application xlApp = new Microsoft.Office.Interop.Excel.ApplicationClass();
                if (xlApp == null)
                {
                    MessageBox.Show("无法创建excel对象，可能您的系统没有安装excel");
                    return;
                }
                xlApp.DefaultFilePath = "";
                xlApp.DisplayAlerts = true;
                xlApp.SheetsInNewWorkbook = 1;
                Microsoft.Office.Interop.Excel.Workbook xlBook = xlApp.Workbooks.Add(true);
                //将ListView的列名导入Excel表第一行
                foreach (ColumnHeader dc in listView.Columns)
                {
                    columnIndex++;
                    xlApp.Cells[rowIndex, columnIndex] = dc.Text;
                }
                //将ListView中的数据导入Excel中
                for (int i = 0; i < rowNum; i++)
                {
                    rowIndex++;
                    columnIndex = 0;
                    for (int j = 0; j < columnNum; j++)
                    {
                        columnIndex++;
                        //注意这个在导出的时候加了“\t” 的目的就是避免导出的数据显示为科学计数法。可以放在每行的首尾。
                        xlApp.Cells[rowIndex, columnIndex] = Convert.ToString(listView.Items[i].SubItems[j].Text) + "\t";
                    }
                }
                //例外需要说明的是用strFileName,Excel.XlFileFormat.xlExcel9795保存方式时 当你的Excel版本不是95、97 而是2003、2007 时导出的时候会报一个错误：异常来自 HRESULT:0x800A03EC。 解决办法就是换成strFileName, Microsoft.Office.Interop.Excel.XlFileFormat.xlWorkbookNormal。
                xlBook.SaveAs(strFileName, Microsoft.Office.Interop.Excel.XlFileFormat.xlWorkbookNormal, Type.Missing, Type.Missing, Type.Missing, Type.Missing, Microsoft.Office.Interop.Excel.XlSaveAsAccessMode.xlExclusive, Type.Missing, Type.Missing, Type.Missing, Type.Missing, Type.Missing);
                xlApp = null;
                xlBook = null;
                MessageBox.Show("OK");
            }
        }



        public Color[][] GetBitMapColorMatrix(string bitmapFilePath)
        {
            Bitmap b1 = new Bitmap(bitmapFilePath);

            int hight = b1.Height;
            int width = b1.Width;

            Color[][] colorMatrix = new Color[width][];
            for (int i = 0; i < width; i++)
            {
                colorMatrix[i] = new Color[hight];
                for (int j = 0; j < hight; j++)
                {
                    colorMatrix[i][j] = b1.GetPixel(i, j);
                }

            }

            return colorMatrix;

        }
        //随机生成不重复的数 
        public int[] getRandomNum(int num)
        {
            int[] index = new int[num];
            for (int i = 0; i < num; i++)
                index[i] = i+1;
            Random r = new Random();
          
            int[] result = new int[num];
            int site = num;
            int id;
            for (int j = 0; j < num; j++)
            {
                id = r.Next(0, site - 1);
                
                result[j] = index[id];
               
                index[id] = index[site - 1];
                
                site--;
            }
            return result;
        }


        private void To_assess_Click(object sender, EventArgs e)
        {
          
            if (i <= num) {
                Form2 f2 = new Form2();
                f2.ShowDialog();
                if (i < num)
                {
                    pictrue_num = randnum[i];
                    i++;
                }
                else { i++;

                    button2.Visible = true;
                    //button1.Visible = true;   
                }

                img_fn = result_QP[pictrue_num - 1];            // HEVC_Bikes_39    distorted fold
                current_image = img_fn;

                org_view_fold_path = img_fn + "_views";

                //imagepath = mom_path + org_view_fold_path + "\\" + org_view_fold_path + "_center.bmp";               // 
                imagepath = mom_path + org_view_fold_path + "\\" + org_view_fold_path + "_" + default_vertical.ToString() + "_" + default_horizontal.ToString() + ".bmp";

                pictureBox1.ImageLocation = imagepath;                                     //在Box1处显示distortion图像

                //对view图像显示
                //int len1 = son_path.Length;
                view_fold_path = org_view_fold_path;    //distortion image 视角变换路径

                lv = new ListViewItem("#");
                lv.SubItems.Add("#");
                listView1.Items.Add(lv);
            }
            
        }
        

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            System.Environment.Exit(0);
            Application.Exit();
        }

        private void button2_Click_1(object sender, EventArgs e)
        {
            
            Application.Exit();
        }

        private void Form1_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == (char)27)
            {
                Formexit f3 = new Formexit();
                f3.ShowDialog();
            }
        }



        private void pictureBox1_MouseDown(object sender, MouseEventArgs e)
        {
            MoveFlag = true;//已经按下.
            xPos = e.X;//当前x坐标.
            yPos = e.Y;//当前y坐标.
            //textBox1.Text = xPos.ToString();//设置x坐标.
            //textBox2.Text = yPos.ToString(); //设置y坐标.
            //textBox3.Text = CurrentX.ToString();
            //textBox4.Text = CurrentY.ToString();
        }

        //在picturebox的鼠标按下事件里.
        private void pictureBox1_MouseUp(object sender, MouseEventArgs e)
        {
            MoveFlag = false;
            ButtonFlag = true; 
        }

        //在picturebox鼠标移动
        private void pictureBox1_MouseMove(object sender, MouseEventArgs e)
        {
            if (MoveFlag)
            {
                ButtonFlag = false; //如果移动则不需要

                //textBox1.Text = (e.X - xPos).ToString();//设置x坐标.
                //textBox2.Text = (e.Y - yPos).ToString(); //设置y坐标.
                StepX = (e.X - xPos) / MouseRateDivder;
                StepY = (e.Y - yPos) / (MouseRateDivder - 10);
                if (System.Math.Abs(StepX) >= 1 || System.Math.Abs(StepY) >= 1)
                {
                    CurrentX -= StepX;
                    if (CurrentX < 1) CurrentX = 1;
                    if (CurrentX > 8) CurrentX = 8;

                    CurrentY -= StepY;
                    if (CurrentY < 1) CurrentY = 1;
                    if (CurrentY > 9) CurrentY = 9;
                    pictureBox1.ImageLocation = mom_path + org_view_fold_path + "\\" + org_view_fold_path + "_" + CurrentY.ToString() + "_" + CurrentX.ToString() + ".bmp";
                    //pictureBox2.ImageLocation = mom_path + org_view_fold_path + "\\" + org_view_fold_path + "_" + CurrentY.ToString() + "_" + CurrentX.ToString() + ".bmp";
                    xPos = e.X; yPos = e.Y;
                }
                //textBox3.Text = CurrentX.ToString();
                //textBox4.Text = CurrentY.ToString();


            }
   
        }


        //private void trackBar1_Scroll(object sender, EventArgs e)
        //{
        //   // textBox1.Text = trackBar1.Value.ToString();
        //    pictureBox1.ImageLocation = mom_path + view_fold_path + "\\" + view_fold_path + "_" + trackBar1.Value.ToString() + "_" + trackBar2.Value.ToString() + ".bmp";
        //    pictureBox2.ImageLocation = mom_path + org_view_fold_path + "\\" + org_view_fold_path + "_" + trackBar1.Value.ToString() + "_" + trackBar2.Value.ToString() + ".bmp";
            
        //}

        //private void trackBar2_Scroll(object sender, EventArgs e)
        //{
        //    pictureBox1.ImageLocation = mom_path + view_fold_path + "\\" + view_fold_path + "_" + trackBar1.Value.ToString() + "_" + trackBar2.Value.ToString() + ".bmp";
        //    pictureBox2.ImageLocation = mom_path + org_view_fold_path + "\\" + org_view_fold_path + "_" + trackBar1.Value.ToString() + "_" + trackBar2.Value.ToString() + ".bmp";

        //}

       

        

       

        
    }
}
