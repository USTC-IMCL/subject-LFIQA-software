namespace position_save_excel
{
    partial class Form1
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.listView1 = new System.Windows.Forms.ListView();
            this.columnHeader1 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            this.columnHeader2 = ((System.Windows.Forms.ColumnHeader)(new System.Windows.Forms.ColumnHeader()));
            //this.button1 = new System.Windows.Forms.Button();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.To_assess = new System.Windows.Forms.Button();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.button2 = new System.Windows.Forms.Button();
            //this.pictureBox2 = new System.Windows.Forms.PictureBox();
            //this.trackBar1 = new System.Windows.Forms.TrackBar();
            //this.trackBar2 = new System.Windows.Forms.TrackBar();
            //this.textBox1 = new System.Windows.Forms.TextBox();
            //this.textBox2 = new System.Windows.Forms.TextBox();
            //this.textBox3 = new System.Windows.Forms.TextBox();
            //this.textBox4 = new System.Windows.Forms.TextBox();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            //((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).BeginInit();
            //((System.ComponentModel.ISupportInitialize)(this.trackBar1)).BeginInit();
            //((System.ComponentModel.ISupportInitialize)(this.trackBar2)).BeginInit();
            this.SuspendLayout();
            // 
            // listView1
            // 
            this.listView1.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.columnHeader1,
            this.columnHeader2});
            this.listView1.Location = new System.Drawing.Point(100, 532);
            this.listView1.Name = "listView1";
            this.listView1.Size = new System.Drawing.Size(10, 10);
            this.listView1.TabIndex = 0;
            this.listView1.UseCompatibleStateImageBehavior = false;
            this.listView1.View = System.Windows.Forms.View.Tile;
            // 
            // columnHeader1
            // 
            this.columnHeader1.Text = "X";
            // 
            // columnHeader2
            // 
            this.columnHeader2.Text = "Y";
            // 
            // button1
            // 
            //this.button1.BackColor = System.Drawing.Color.White;
            //this.button1.Location = new System.Drawing.Point(127, 532);
            //this.button1.Name = "button1";
            //this.button1.Size = new System.Drawing.Size(101, 23);
            //this.button1.TabIndex = 1;
            //this.button1.Text = "Send to Excel";
            //this.button1.UseVisualStyleBackColor = false;
            //this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // pictureBox1
            // 
            this.pictureBox1.BackColor = System.Drawing.SystemColors.ButtonShadow;
            this.pictureBox1.Location = new System.Drawing.Point(322, 68);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(1672, 434);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox1.TabIndex = 3;
            this.pictureBox1.TabStop = false;
            this.pictureBox1.MouseClick += new System.Windows.Forms.MouseEventHandler(this.Form1_MouseClick);
            this.pictureBox1.MouseDown += new System.Windows.Forms.MouseEventHandler(this.pictureBox1_MouseDown);
            this.pictureBox1.MouseMove += new System.Windows.Forms.MouseEventHandler(this.pictureBox1_MouseMove);
            this.pictureBox1.MouseUp += new System.Windows.Forms.MouseEventHandler(this.pictureBox1_MouseUp);
            // 
            // To_assess
            // 
            this.To_assess.BackColor = System.Drawing.Color.White;
            this.To_assess.ImageAlign = System.Drawing.ContentAlignment.TopLeft;
            this.To_assess.Location = new System.Drawing.Point(1130, 532);
            this.To_assess.Name = "To_assess";
            this.To_assess.Size = new System.Drawing.Size(89, 46);
            this.To_assess.TabIndex = 10;
            this.To_assess.Text = "OK";
            this.To_assess.UseVisualStyleBackColor = false;
            this.To_assess.Click += new System.EventHandler(this.To_assess_Click);
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(1130, 12);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(89, 39);
            this.button2.TabIndex = 11;
            this.button2.Text = "exit";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click_1);
            // 
            // pictureBox2
            // 
            //this.pictureBox2.BackColor = System.Drawing.SystemColors.ButtonShadow;
            //this.pictureBox2.Location = new System.Drawing.Point(553, 68);
            //this.pictureBox2.Name = "pictureBox2";
            //this.pictureBox2.Size = new System.Drawing.Size(625, 434);
            //this.pictureBox2.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            //this.pictureBox2.TabIndex = 12;
            //this.pictureBox2.TabStop = false;
            // 
            // trackBar1
            // 
            //this.trackBar1.Location = new System.Drawing.Point(304, 497);
            //this.trackBar1.Name = "trackBar1";
            //this.trackBar1.Size = new System.Drawing.Size(625, 45);
            //this.trackBar1.TabIndex = 13;
            //this.trackBar1.Scroll += new System.EventHandler(this.trackBar1_Scroll);
            // 
            // trackBar2
            // 
            //this.trackBar2.Location = new System.Drawing.Point(127, 28);
            //this.trackBar2.Name = "trackBar2";
            //this.trackBar2.Orientation = System.Windows.Forms.Orientation.Vertical;
            //this.trackBar2.Size = new System.Drawing.Size(45, 434);
            //this.trackBar2.TabIndex = 15;
            //this.trackBar2.Scroll += new System.EventHandler(this.trackBar2_Scroll);
            // 
            // textBox1
            // 
            //this.textBox1.Location = new System.Drawing.Point(302, 535);
            //this.textBox1.Name = "textBox1";
            //this.textBox1.Size = new System.Drawing.Size(100, 21);
            //this.textBox1.TabIndex = 16;
            // 
            // textBox2
            // 
            //this.textBox2.Location = new System.Drawing.Point(480, 539);
            //this.textBox2.Name = "textBox2";
            //this.textBox2.Size = new System.Drawing.Size(100, 21);
            //this.textBox2.TabIndex = 17;
            // 
            // textBox3
            // 
            //this.textBox3.Location = new System.Drawing.Point(636, 542);
            //this.textBox3.Name = "textBox3";
            //this.textBox3.Size = new System.Drawing.Size(100, 21);
            //this.textBox3.TabIndex = 18;
            // 
            // textBox4
            // 
            //this.textBox4.Location = new System.Drawing.Point(811, 538);
            //this.textBox4.Name = "textBox4";
            //this.textBox4.Size = new System.Drawing.Size(100, 21);
            //this.textBox4.TabIndex = 19;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.Black;
            this.ClientSize = new System.Drawing.Size(1231, 590);
            //this.Controls.Add(this.textBox4);
            //this.Controls.Add(this.textBox3);
            //this.Controls.Add(this.textBox2);
            //this.Controls.Add(this.textBox1);
            //this.Controls.Add(this.trackBar2);
            //this.Controls.Add(this.trackBar1);
            //this.Controls.Add(this.pictureBox2);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.To_assess);
            this.Controls.Add(this.pictureBox1);
            //this.Controls.Add(this.button1);
            this.Controls.Add(this.listView1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form1_FormClosing);
            this.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.Form1_KeyPress);
            this.MouseClick += new System.Windows.Forms.MouseEventHandler(this.Form1_MouseClick);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            //((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).EndInit();
            //((System.ComponentModel.ISupportInitialize)(this.trackBar1)).EndInit();
            //((System.ComponentModel.ISupportInitialize)(this.trackBar2)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ListView listView1;
        private System.Windows.Forms.ColumnHeader columnHeader1;
        private System.Windows.Forms.ColumnHeader columnHeader2;
        //private System.Windows.Forms.Button button1;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Button To_assess;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.PictureBox pictureBox2;
        private System.Windows.Forms.TrackBar trackBar1;
        private System.Windows.Forms.TrackBar trackBar2;
        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.TextBox textBox2;
        private System.Windows.Forms.TextBox textBox3;
        private System.Windows.Forms.TextBox textBox4;
    }
}

