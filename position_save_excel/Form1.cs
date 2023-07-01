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
//using Microsoft.Office.Interop.Excel;
//using MySql.Data.MySqlClient;




namespace position_save_excel
{
    public partial class Form1 : Form
    {
       
        ListViewItem lv;
        public static int pictrue_num = 1 ;
        public static string current_image;
        string pair_filenames;
        string src_view_path;
        string dis_view_path;
        string src_depth_path;
        string dis_depth_path;
        string src_refous_path;
        string dis_refous_path;

        string pic1_image;
        string pic2_image;
        string pic3_image;
        string pic4_image;
        public static int num = 0;
        public int[] randnum;
        public static int i = 1;
        public static string[] result_QP;
        public static string[] result_noQP;
        public static string[] image_pair_list;
        public static Image[] source_views;
        public static Image[] distortion_images;
        private static Color[][] srcColorMatrix;
        private static Color[][] disColorMatrix;

        int picture_box_height = login.num_image_height;
        int picture_box_width  = login.num_image_width;
   
        //USE MOUSE TO CHANGE VIEWS
        bool MoveFlag;
        bool ButtonFlag = true;
        int xPos, yPos;
        int CurrentY;
        int CurrentX;
        int StepX, StepY;
        int MouseRateDivder             = login.num_view_change_distance;
        int max_num_horizontal_images   = login.num_horizontal_images;
        int max_num_vertical_images     = login.num_vertical_images;
        int default_horizontal;
        int default_vertical;
        int depth_map_width;
        int depth_map_height;
            

        public Form1()
        {
            FormBorderStyle = FormBorderStyle.None;
            InitializeComponent();
            this.WindowState = FormWindowState.Maximized;
            button2.Visible = false;

            this.KeyPreview = true;
            //  screen size
            int SH = Screen.PrimaryScreen.Bounds.Height;
            int SW = Screen.PrimaryScreen.Bounds.Width;

            //  set picture box size
            pictureBox1.Size = new Size(picture_box_width, picture_box_height);
            pictureBox2.Size = new Size(picture_box_width, picture_box_height);
            pictureBox3.Size = new Size(picture_box_width, picture_box_height);
            pictureBox4.Size = new Size(picture_box_width, picture_box_height);

            //  set picture box location
            int y = Convert.ToInt32(SH / 2 - picture_box_height / 2);
            int x = 0;
            pictureBox1.Location = new Point(x, y);

            x = Convert.ToInt32(SW / 2 - picture_box_width);
            pictureBox2.Location = new Point(x, y);

            x = Convert.ToInt32(SW / 2);
            pictureBox3.Location = new Point(x, y);

            x = Convert.ToInt32(SW - picture_box_width);
            pictureBox4.Location = new Point(x, y);

            //  set default view id
            default_horizontal          = (max_num_horizontal_images + 1) / 2;
            default_vertical            = (max_num_vertical_images + 1) / 2;


            listView1.Visible = true;
            x = Convert.ToInt32(SW / 11 * 5);
            y = Convert.ToInt32(SH / 5 * 4);
            To_assess.Location = new Point(x, y);

            //设置播放时间 此功能关闭
            //timer1.Interval = 5000;//设置时间为15秒
            //timer1.Tick += new EventHandler(timer1_Tick);
            //timer1.Start();//窗体加载时这个计时器自动启动

            //  read all images
            List<string> list = new List<string>();
            using (TextReader reader = File.OpenText(login.dataset_config_path))   // write images to data.txt
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

            randnum = getRandomNum(num);                //生成随机的序列
            pictrue_num = randnum[0];                   //取第一个随机数

            image_pair_list = (string[])list.ToArray();
            pair_filenames = image_pair_list[pictrue_num - 1];

            string[] splittedStrings = pair_filenames.Split(' ');

            if (splittedStrings.Length != 2)
            {
                throw new Exception($"input data shoule be paired, but get {pair_filenames}");
            }
            src_refous_path = splittedStrings[1];
            dis_refous_path = splittedStrings[0];

            current_image = src_refous_path;
            src_view_path = src_refous_path + "_views";
            dis_view_path = dis_refous_path + "_views";

            if (login.is_cache_images)     //  read view data to array
            {
                string[] src_fns = GenerateSubViewsFnPaths(login.view_config_path, src_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);
                string[] dst_fns = GenerateSubViewsFnPaths(login.view_config_path, dis_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);

                source_views        = LoadLightFieldViewImages(src_fns);
                distortion_images   = LoadLightFieldViewImages(dst_fns);

                int left_view_index  = mapping_hori_veri_to_array_index(default_horizontal, default_vertical, max_num_horizontal_images, max_num_vertical_images);
                int right_view_index = mapping_hori_veri_to_array_index(default_horizontal + login.num_disparity_distance, default_vertical, max_num_horizontal_images, max_num_vertical_images);
                pictureBox1.Image    = source_views[left_view_index];
                pictureBox2.Image    = distortion_images[left_view_index];
                pictureBox3.Image    = source_views[right_view_index];
                pictureBox4.Image    = distortion_images[right_view_index];

            }
            else
            {
                pic1_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + default_vertical.ToString() + "_" + default_horizontal.ToString() + "." + login.picture_format;
                pic2_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + default_vertical.ToString() + "_" + default_horizontal.ToString() + "." + login.picture_format;
                pic3_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + default_vertical.ToString() + "_" + (default_horizontal + login.num_disparity_distance).ToString() + "." + login.picture_format;
                pic4_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + default_vertical.ToString() + "_" + (default_horizontal + login.num_disparity_distance).ToString() + "." + login.picture_format;

                pictureBox1.ImageLocation = pic1_image;
                pictureBox2.ImageLocation = pic2_image;
                pictureBox3.ImageLocation = pic3_image;
                pictureBox4.ImageLocation = pic4_image;
            }

            src_depth_path = login.depth_config_path + "\\" + src_refous_path + "." + login.picture_format;
            dis_depth_path = login.depth_config_path + "\\" + dis_refous_path + "." + login.picture_format;
            srcColorMatrix = GetBitMapColorMatrix(src_depth_path);
            disColorMatrix = GetBitMapColorMatrix(dis_depth_path);

            CurrentX = default_horizontal;
            CurrentY = default_vertical;
        }

       
        //计时器计时事件
        void timer1_Tick(object sender, EventArgs e)
        {
            if (pictrue_num == 13) { }
     //      else To_assess_Click(null,null);
        }

        //  mouse click event
        private void Form1_MouseClick(object sender, MouseEventArgs e)
        {
            int i, j, src_gray_value, dis_gray_value;
            if (ButtonFlag == true)
            {
                j = e.Y;
                i = e.X;

                if (i < depth_map_width && i > 0 && j < depth_map_height && j > 0)
                {
                    src_gray_value = srcColorMatrix[i - 1][j - 1].G;
                    dis_gray_value = disColorMatrix[i - 1][j - 1].G;

                    pic1_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + src_gray_value.ToString() + "." + login.picture_format;
                    pic3_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + src_gray_value.ToString() + "." + login.picture_format;
                    pic2_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + dis_gray_value.ToString() + "." + login.picture_format;
                    pic4_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + dis_gray_value.ToString() + "." + login.picture_format;

                    pictureBox1.ImageLocation = pic1_image;
                    pictureBox2.ImageLocation = pic2_image;
                    pictureBox3.ImageLocation = pic3_image;
                    pictureBox4.ImageLocation = pic4_image;
                }   
            }         
        }

        private void Form1_MouseClick_box2(object sender, MouseEventArgs e)
        {
            int i, j, src_gray_value, dis_gray_value;
            if (ButtonFlag == true)
            {
                j = e.Y;
                i = e.X;

                if (i < depth_map_width && i > 0 && j < depth_map_height && j > 0)
                {
                    src_gray_value = srcColorMatrix[i - 1][j - 1].G;
                    dis_gray_value = disColorMatrix[i - 1][j - 1].G;

                    pic1_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + src_gray_value.ToString() + "." + login.picture_format;
                    pic3_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + src_gray_value.ToString() + "." + login.picture_format;
                    pic2_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + dis_gray_value.ToString() + "." + login.picture_format;
                    pic4_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + dis_gray_value.ToString() + "." + login.picture_format;

                    pictureBox1.ImageLocation = pic1_image;
                    pictureBox2.ImageLocation = pic2_image;
                    pictureBox3.ImageLocation = pic3_image;
                    pictureBox4.ImageLocation = pic4_image;
                }
            }
        }

        private void Form1_MouseClick_box3(object sender, MouseEventArgs e)
        {
            int i, j, src_gray_value, dis_gray_value;
            if (ButtonFlag == true)
            {
                j = e.Y;
                i = e.X;

                if (i < depth_map_width && i > 0 && j < depth_map_height && j > 0)
                {
                    src_gray_value = srcColorMatrix[i - 1][j - 1].G;
                    dis_gray_value = disColorMatrix[i - 1][j - 1].G;

                    pic1_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + src_gray_value.ToString() + "." + login.picture_format;
                    pic3_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + src_gray_value.ToString() + "." + login.picture_format;
                    pic2_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + dis_gray_value.ToString() + "." + login.picture_format;
                    pic4_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + dis_gray_value.ToString() + "." + login.picture_format;

                    pictureBox1.ImageLocation = pic1_image;
                    pictureBox2.ImageLocation = pic2_image;
                    pictureBox3.ImageLocation = pic3_image;
                    pictureBox4.ImageLocation = pic4_image;
                }
            }
        }

        private void Form1_MouseClick_box4(object sender, MouseEventArgs e)
        {
            int i, j, src_gray_value, dis_gray_value;
            if (ButtonFlag == true)
            {
                j = e.Y;
                i = e.X;

                if (i < depth_map_width && i > 0 && j < depth_map_height && j > 0)
                {
                    src_gray_value = srcColorMatrix[i - 1][j - 1].G;
                    dis_gray_value = disColorMatrix[i - 1][j - 1].G;

                    pic1_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + src_gray_value.ToString() + "." + login.picture_format;
                    pic3_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + src_gray_value.ToString() + "." + login.picture_format;
                    pic2_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + dis_gray_value.ToString() + "." + login.picture_format;
                    pic4_image = login.view_config_path + "\\" + src_refous_path + "\\" + src_refous_path + "_" + dis_gray_value.ToString() + "." + login.picture_format;

                    pictureBox1.ImageLocation = pic1_image;
                    pictureBox2.ImageLocation = pic2_image;
                    pictureBox3.ImageLocation = pic3_image;
                    pictureBox4.ImageLocation = pic4_image;
                }
            }
        }



        //  generate light field sub-view filename list
        static string[] GenerateSubViewsFnPaths(string fold_path, string image_fn, int vertical_num, int horizontal_num, string picture_format)
        {
            int total_num = vertical_num * horizontal_num;
            string[] imagePaths = new string[total_num]; // 创建图像文件路径数组

            for (int v = 1; v <= vertical_num; ++v)
            {
                for (int h = 1; h <= horizontal_num; ++h)
                {
                    string tmpImagePath = fold_path + "\\" + image_fn + "\\" + image_fn + "_" + v.ToString() + "_" +  h.ToString() + "." + picture_format;
                    int index = (v - 1) * horizontal_num + (h - 1);
                    imagePaths[index] = tmpImagePath;
                }
            }

            return imagePaths; // 返回生成的图像文件路径数组
        }

        //  read light filed sub-view to array
        static Image[] LoadLightFieldViewImages(string[] imagePaths)
        {
            Image[] images = new Image[imagePaths.Length]; // 创建一个图像数组

            for (int i = 0; i < imagePaths.Length; i++)
            {
                // 读取图像文件并将其存储在数组中
                images[i] = Image.FromFile(imagePaths[i]);
            }
            return images; // 返回加载的图像数组
        }


        static int mapping_hori_veri_to_array_index(int hori_idx, int ver_idx, int horizontal_num, int vertical_num)
        {
            return (ver_idx - 1) * horizontal_num + (hori_idx - 1);
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
      



        public Color[][] GetBitMapColorMatrix(string bitmapFilePath)
        {
            Bitmap b1 = new Bitmap(bitmapFilePath);

            int hight = b1.Height;
            int width = b1.Width;

            depth_map_height = hight;
            depth_map_width = width;

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

                pair_filenames = image_pair_list[pictrue_num - 1];

                string[] splittedStrings = pair_filenames.Split(' ');

                if (splittedStrings.Length != 2)
                {
                    throw new Exception($"input data shoule be paired, but get {pair_filenames}");
                }
                src_refous_path = splittedStrings[1];
                dis_refous_path = splittedStrings[0];

                current_image = src_refous_path;
                src_view_path = src_refous_path + "_views";
                dis_view_path = dis_refous_path + "_views";

                if (login.is_cache_images)     //  read view data to array
                {
                    string[] src_fns = GenerateSubViewsFnPaths(login.view_config_path, src_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);
                    string[] dst_fns = GenerateSubViewsFnPaths(login.view_config_path, dis_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);

                    source_views = LoadLightFieldViewImages(src_fns);
                    distortion_images = LoadLightFieldViewImages(dst_fns);

                    int left_view_index = mapping_hori_veri_to_array_index(default_horizontal, default_vertical, max_num_horizontal_images, max_num_vertical_images);
                    int right_view_index = mapping_hori_veri_to_array_index(default_horizontal + login.num_disparity_distance, default_vertical, max_num_horizontal_images, max_num_vertical_images);
                    pictureBox1.Image = source_views[left_view_index];
                    pictureBox2.Image = distortion_images[left_view_index];
                    pictureBox3.Image = source_views[right_view_index];
                    pictureBox4.Image = distortion_images[right_view_index];

                }
                else
                {
                    pic1_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + default_vertical.ToString() + "_" + default_horizontal.ToString() + "." + login.picture_format;
                    pic2_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + default_vertical.ToString() + "_" + default_horizontal.ToString() + "." + login.picture_format;
                    pic3_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + default_vertical.ToString() + "_" + (default_horizontal + login.num_disparity_distance).ToString() + "." + login.picture_format;
                    pic4_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + default_vertical.ToString() + "_" + (default_horizontal + login.num_disparity_distance).ToString() + "." + login.picture_format;

                    pictureBox1.ImageLocation = pic1_image;
                    pictureBox2.ImageLocation = pic2_image;
                    pictureBox3.ImageLocation = pic3_image;
                    pictureBox4.ImageLocation = pic4_image;
                }

                src_depth_path = login.depth_config_path + "\\" + src_refous_path + "." + login.picture_format;
                dis_depth_path = login.depth_config_path + "\\" + dis_refous_path + "." + login.picture_format;

                CurrentX = default_horizontal;
                CurrentY = default_vertical;

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
        }
        private void pictureBox2_MouseDown(object sender, MouseEventArgs e)
        {
            MoveFlag = true;//已经按下.
            xPos = e.X;//当前x坐标.
            yPos = e.Y;//当前y坐标.
        }
        private void pictureBox3_MouseDown(object sender, MouseEventArgs e)
        {
            MoveFlag = true;//已经按下.
            xPos = e.X;//当前x坐标.
            yPos = e.Y;//当前y坐标.
        }
        private void pictureBox4_MouseDown(object sender, MouseEventArgs e)
        {
            MoveFlag = true;//已经按下.
            xPos = e.X;//当前x坐标.
            yPos = e.Y;//当前y坐标.
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
            int left_image_id, right_image_id;
            if (MoveFlag)
            {
                ButtonFlag = false; //如果移动则不需要

                StepX = (e.X - xPos) / MouseRateDivder;
                StepY = (e.Y - yPos) / MouseRateDivder;
                if (System.Math.Abs(StepX) >= 1 || System.Math.Abs(StepY) >= 1)
                {

                    CurrentX -= StepX;
                    if (CurrentX < 1)
                    {
                        CurrentX = 1;
                        left_image_id = 1;
                        right_image_id = login.num_disparity_distance + 1;
                    }
                    else if ((CurrentX + login.num_disparity_distance) > max_num_horizontal_images)
                    {
                        CurrentX = max_num_horizontal_images - login.num_disparity_distance;
                        left_image_id = CurrentX;
                        right_image_id = max_num_horizontal_images;
                    }
                    else
                    {
                        left_image_id = CurrentX ;
                        right_image_id = CurrentX + login.num_disparity_distance;
                    }

                    CurrentY -= StepY;
                    if (CurrentY < 1) CurrentY = 1;
                    if (CurrentY > max_num_vertical_images) CurrentY = max_num_vertical_images;


                    if (login.is_cache_images)     //  read view data to array
                    {
                        string[] src_fns = GenerateSubViewsFnPaths(login.view_config_path, src_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);
                        string[] dst_fns = GenerateSubViewsFnPaths(login.view_config_path, dis_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);

                        source_views = LoadLightFieldViewImages(src_fns);
                        distortion_images = LoadLightFieldViewImages(dst_fns);

                        int left_view_index = mapping_hori_veri_to_array_index(left_image_id, CurrentY, max_num_horizontal_images, max_num_vertical_images);
                        int right_view_index = mapping_hori_veri_to_array_index(right_image_id, CurrentY, max_num_horizontal_images, max_num_vertical_images);
                        pictureBox1.Image = source_views[left_view_index];
                        pictureBox2.Image = distortion_images[left_view_index];
                        pictureBox3.Image = source_views[right_view_index];
                        pictureBox4.Image = distortion_images[right_view_index];

                    }
                    else
                    {
                        pic1_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + CurrentY.ToString() + "_" + left_image_id.ToString() + "." + login.picture_format;
                        pic2_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + CurrentY.ToString() + "_" + left_image_id.ToString() + "." + login.picture_format;
                        pic3_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + CurrentY.ToString() + "_" + right_image_id.ToString() + "." + login.picture_format;
                        pic4_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + CurrentY.ToString() + "_" + right_image_id.ToString() + "." + login.picture_format;

                        pictureBox1.ImageLocation = pic1_image;
                        pictureBox2.ImageLocation = pic2_image;
                        pictureBox3.ImageLocation = pic3_image;
                        pictureBox4.ImageLocation = pic4_image;
                    }

                    xPos = e.X; yPos = e.Y;
                }
            }
        }

        private void pictureBox2_MouseMove(object sender, MouseEventArgs e)
        {
            int left_image_id, right_image_id;
            if (MoveFlag)
            {
                ButtonFlag = false; //如果移动则不需要

                StepX = (e.X - xPos) / MouseRateDivder;
                StepY = (e.Y - yPos) / MouseRateDivder;
                if (System.Math.Abs(StepX) >= 1 || System.Math.Abs(StepY) >= 1)
                {

                    CurrentX -= StepX;
                    if (CurrentX < 1)
                    {
                        CurrentX = 1;
                        left_image_id = 1;
                        right_image_id = login.num_disparity_distance + 1;
                    }
                    else if ((CurrentX + login.num_disparity_distance) > max_num_horizontal_images)
                    {
                        CurrentX = max_num_horizontal_images - login.num_disparity_distance;
                        left_image_id = CurrentX;
                        right_image_id = max_num_horizontal_images;
                    }
                    else
                    {
                        left_image_id = CurrentX;
                        right_image_id = CurrentX + login.num_disparity_distance;
                    }

                    CurrentY -= StepY;
                    if (CurrentY < 1) CurrentY = 1;
                    if (CurrentY > max_num_vertical_images) CurrentY = max_num_vertical_images;


                    if (login.is_cache_images)     //  read view data to array
                    {
                        string[] src_fns = GenerateSubViewsFnPaths(login.view_config_path, src_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);
                        string[] dst_fns = GenerateSubViewsFnPaths(login.view_config_path, dis_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);

                        source_views = LoadLightFieldViewImages(src_fns);
                        distortion_images = LoadLightFieldViewImages(dst_fns);

                        int left_view_index = mapping_hori_veri_to_array_index(left_image_id, CurrentY, max_num_horizontal_images, max_num_vertical_images);
                        int right_view_index = mapping_hori_veri_to_array_index(right_image_id, CurrentY, max_num_horizontal_images, max_num_vertical_images);
                        pictureBox1.Image = source_views[left_view_index];
                        pictureBox2.Image = distortion_images[left_view_index];
                        pictureBox3.Image = source_views[right_view_index];
                        pictureBox4.Image = distortion_images[right_view_index];

                    }
                    else
                    {
                        pic1_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + CurrentY.ToString() + "_" + left_image_id.ToString() + "." + login.picture_format;
                        pic2_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + CurrentY.ToString() + "_" + left_image_id.ToString() + "." + login.picture_format;
                        pic3_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + CurrentY.ToString() + "_" + right_image_id.ToString() + "." + login.picture_format;
                        pic4_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + CurrentY.ToString() + "_" + right_image_id.ToString() + "." + login.picture_format;

                        pictureBox1.ImageLocation = pic1_image;
                        pictureBox2.ImageLocation = pic2_image;
                        pictureBox3.ImageLocation = pic3_image;
                        pictureBox4.ImageLocation = pic4_image;
                    }

                    xPos = e.X; yPos = e.Y;
                }
            }
        }

        private void pictureBox3_MouseMove(object sender, MouseEventArgs e)
        {
            int left_image_id, right_image_id;
            if (MoveFlag)
            {
                ButtonFlag = false; //如果移动则不需要

                StepX = (e.X - xPos) / MouseRateDivder;
                StepY = (e.Y - yPos) / MouseRateDivder;
                if (System.Math.Abs(StepX) >= 1 || System.Math.Abs(StepY) >= 1)
                {

                    CurrentX -= StepX;
                    if (CurrentX < 1)
                    {
                        CurrentX = 1;
                        left_image_id = 1;
                        right_image_id = login.num_disparity_distance + 1;
                    }
                    else if ((CurrentX + login.num_disparity_distance) > max_num_horizontal_images)
                    {
                        CurrentX = max_num_horizontal_images - login.num_disparity_distance;
                        left_image_id = CurrentX;
                        right_image_id = max_num_horizontal_images;
                    }
                    else
                    {
                        left_image_id = CurrentX;
                        right_image_id = CurrentX + login.num_disparity_distance;
                    }

                    CurrentY -= StepY;
                    if (CurrentY < 1) CurrentY = 1;
                    if (CurrentY > max_num_vertical_images) CurrentY = max_num_vertical_images;


                    if (login.is_cache_images)     //  read view data to array
                    {
                        string[] src_fns = GenerateSubViewsFnPaths(login.view_config_path, src_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);
                        string[] dst_fns = GenerateSubViewsFnPaths(login.view_config_path, dis_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);

                        source_views = LoadLightFieldViewImages(src_fns);
                        distortion_images = LoadLightFieldViewImages(dst_fns);

                        int left_view_index = mapping_hori_veri_to_array_index(left_image_id, CurrentY, max_num_horizontal_images, max_num_vertical_images);
                        int right_view_index = mapping_hori_veri_to_array_index(right_image_id, CurrentY, max_num_horizontal_images, max_num_vertical_images);
                        pictureBox1.Image = source_views[left_view_index];
                        pictureBox2.Image = distortion_images[left_view_index];
                        pictureBox3.Image = source_views[right_view_index];
                        pictureBox4.Image = distortion_images[right_view_index];

                    }
                    else
                    {
                        pic1_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + CurrentY.ToString() + "_" + left_image_id.ToString() + "." + login.picture_format;
                        pic2_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + CurrentY.ToString() + "_" + left_image_id.ToString() + "." + login.picture_format;
                        pic3_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + CurrentY.ToString() + "_" + right_image_id.ToString() + "." + login.picture_format;
                        pic4_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + CurrentY.ToString() + "_" + right_image_id.ToString() + "." + login.picture_format;

                        pictureBox1.ImageLocation = pic1_image;
                        pictureBox2.ImageLocation = pic2_image;
                        pictureBox3.ImageLocation = pic3_image;
                        pictureBox4.ImageLocation = pic4_image;
                    }

                    xPos = e.X; yPos = e.Y;
                }
            }
        }

        private void pictureBox4_MouseMove(object sender, MouseEventArgs e)
        {
            int left_image_id, right_image_id;
            if (MoveFlag)
            {
                ButtonFlag = false; //如果移动则不需要

                StepX = (e.X - xPos) / MouseRateDivder;
                StepY = (e.Y - yPos) / MouseRateDivder;
                if (System.Math.Abs(StepX) >= 1 || System.Math.Abs(StepY) >= 1)
                {

                    CurrentX -= StepX;
                    if (CurrentX < 1)
                    {
                        CurrentX = 1;
                        left_image_id = 1;
                        right_image_id = login.num_disparity_distance + 1;
                    }
                    else if ((CurrentX + login.num_disparity_distance) > max_num_horizontal_images)
                    {
                        CurrentX = max_num_horizontal_images - login.num_disparity_distance;
                        left_image_id = CurrentX;
                        right_image_id = max_num_horizontal_images;
                    }
                    else
                    {
                        left_image_id = CurrentX;
                        right_image_id = CurrentX + login.num_disparity_distance;
                    }

                    CurrentY -= StepY;
                    if (CurrentY < 1) CurrentY = 1;
                    if (CurrentY > max_num_vertical_images) CurrentY = max_num_vertical_images;


                    if (login.is_cache_images)     //  read view data to array
                    {
                        string[] src_fns = GenerateSubViewsFnPaths(login.view_config_path, src_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);
                        string[] dst_fns = GenerateSubViewsFnPaths(login.view_config_path, dis_view_path, max_num_vertical_images, max_num_horizontal_images, login.picture_format);

                        source_views = LoadLightFieldViewImages(src_fns);
                        distortion_images = LoadLightFieldViewImages(dst_fns);

                        int left_view_index = mapping_hori_veri_to_array_index(left_image_id, CurrentY, max_num_horizontal_images, max_num_vertical_images);
                        int right_view_index = mapping_hori_veri_to_array_index(right_image_id, CurrentY, max_num_horizontal_images, max_num_vertical_images);
                        pictureBox1.Image = source_views[left_view_index];
                        pictureBox2.Image = distortion_images[left_view_index];
                        pictureBox3.Image = source_views[right_view_index];
                        pictureBox4.Image = distortion_images[right_view_index];

                    }
                    else
                    {
                        pic1_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + CurrentY.ToString() + "_" + left_image_id.ToString() + "." + login.picture_format;
                        pic2_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + CurrentY.ToString() + "_" + left_image_id.ToString() + "." + login.picture_format;
                        pic3_image = login.view_config_path + "\\" + src_view_path + "\\" + src_view_path + "_" + CurrentY.ToString() + "_" + right_image_id.ToString() + "." + login.picture_format;
                        pic4_image = login.view_config_path + "\\" + dis_view_path + "\\" + dis_view_path + "_" + CurrentY.ToString() + "_" + right_image_id.ToString() + "." + login.picture_format;

                        pictureBox1.ImageLocation = pic1_image;
                        pictureBox2.ImageLocation = pic2_image;
                        pictureBox3.ImageLocation = pic3_image;
                        pictureBox4.ImageLocation = pic4_image;
                    }

                    xPos = e.X; yPos = e.Y;
                }
            }
        }

    }
}
