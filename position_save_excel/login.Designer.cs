using System;
using System.Windows.Forms;

namespace position_save_excel
{
    partial class login
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }


        private void DataConfigSetting_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                //data_config_path = openFileDialog.FileName;
                dataConfigLabel.Text = openFileDialog.FileName; 
            }
        }

        private void PicConfigSetting_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();

            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                //picture_fold_path = folderBrowserDialog.SelectedPath;
                pictureConfigLabel.Text = folderBrowserDialog.SelectedPath; 
            }
        }

        private void DepConfigSetting_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();

            if (folderBrowserDialog.ShowDialog() == DialogResult.OK)
            {
                //depth_fold_path = folderBrowserDialog.SelectedPath;
                depthConfigLabel.Text = folderBrowserDialog.SelectedPath; 
            }
        }


        private void ComboBox_SelectedIndexChange(object sender, EventArgs e)
        { 
            display_mode = this.displayComboBox.GetItemText(this.displayComboBox.SelectedItem);
        }

        private void ComboBox_IsCacheImageIndexChange(object sender, EventArgs e)
        {
            is_cache_string = this.isCacheComboBox.GetItemText(this.isCacheComboBox.SelectedItem);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            //  username 
            this.label1 = new System.Windows.Forms.Label();
            this.textBox1 = new System.Windows.Forms.TextBox();
            //  numHorizontalImages
            this.label2 = new System.Windows.Forms.Label();
            this.numHorizontalImages = new System.Windows.Forms.NumericUpDown();
            ((System.ComponentModel.ISupportInitialize)(this.numHorizontalImages)).BeginInit();
            //  numVerticalImages
            this.label3 = new System.Windows.Forms.Label();
            this.numVerticalImages = new System.Windows.Forms.NumericUpDown();
            ((System.ComponentModel.ISupportInitialize)(this.numVerticalImages)).BeginInit();
            //  disparity distance
            this.disparityDistance = new System.Windows.Forms.Label();
            this.numOfDisparity = new System.Windows.Forms.NumericUpDown();
            //  angular distance 
            this.angularDistance = new System.Windows.Forms.Label();
            this.angularSpeed = new NumericUpDown();
            // data config 
            this.dataConfigLabel = new System.Windows.Forms.TextBox();
            this.DataConfig = new System.Windows.Forms.Button();
            //  picture config
            this.PicturesConfig = new Button();
            this.pictureConfigLabel = new TextBox();
            //  depth config
            this.DepthConfig = new Button();
            this.depthConfigLabel = new TextBox();  
            //  picture format
            this.picFormatLabel  = new Label();
            this.picFormatText = new TextBox();
            //  display mode
            this.displayMode = new Label();
            this.displayComboBox = new ComboBox();  
            //  is cache image
            this.isCacheLabel = new Label();
            this.isCacheComboBox = new ComboBox();
            //  image height and width
            this.imageHeight = new Label();
            this.imageWidth = new Label();
            this.numImageHeight = new NumericUpDown();
            this.numImageWidth = new NumericUpDown();

            //  table layout panel init
            this.tableLayoutPanel = new System.Windows.Forms.TableLayoutPanel();

            this.NEXT = new System.Windows.Forms.Button();
            this.groupBox1 = new System.Windows.Forms.GroupBox();

            //this.tableLayoutPanel.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.SuspendLayout();

            //
            //  table layout init config
            //
            this.tableLayoutPanel.ColumnCount = 2;
            this.tableLayoutPanel.RowCount  = 10;
            //this.tableLayoutPanel.Height    = this.tableLayoutPanel.RowCount * 40;
            this.tableLayoutPanel.Dock      = DockStyle.Fill;
            this.tableLayoutPanel.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(SizeType.Percent, 50));
            this.tableLayoutPanel.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(SizeType.Percent, 50));
            //this.tableLayoutPanel.RowStyles.Add(new System.Windows.Forms.RowStyle(SizeType.Percent, 25));
            //this.tableLayoutPanel.RowStyles.Add(new System.Windows.Forms.RowStyle(SizeType.Percent, 25));
            //this.tableLayoutPanel.RowStyles.Add(new System.Windows.Forms.RowStyle(SizeType.Percent, 25));
            //this.tableLayoutPanel.RowStyles.Add(new System.Windows.Forms.RowStyle(SizeType.Percent, 25));
            this.tableLayoutPanel.Controls.Add(this.label1, 0, 0);
            this.tableLayoutPanel.Controls.Add(this.textBox1, 1, 0);
            this.tableLayoutPanel.Controls.Add(this.label2, 0, 1);
            this.tableLayoutPanel.Controls.Add(this.numHorizontalImages, 1,1);
            this.tableLayoutPanel.Controls.Add(this.label3, 0, 2);
            this.tableLayoutPanel.Controls.Add(this.numVerticalImages, 1, 2);
            this.tableLayoutPanel.Controls.Add(this.disparityDistance, 0, 3);
            this.tableLayoutPanel.Controls.Add(this.numOfDisparity, 1, 3);
            this.tableLayoutPanel.Controls.Add(this.angularDistance, 0, 4);
            this.tableLayoutPanel.Controls.Add(this.angularSpeed, 1, 4);
            this.tableLayoutPanel.Controls.Add(this.DataConfig, 0, 5);
            this.tableLayoutPanel.Controls.Add(this.dataConfigLabel, 1, 5);
            this.tableLayoutPanel.Controls.Add(this.PicturesConfig, 0, 6);
            this.tableLayoutPanel.Controls.Add(this.pictureConfigLabel, 1, 6);
            this.tableLayoutPanel.Controls.Add(this.DepthConfig, 0, 7);
            this.tableLayoutPanel.Controls.Add(this.depthConfigLabel, 1, 7);
            this.tableLayoutPanel.Controls.Add(this.picFormatLabel, 0, 8);
            this.tableLayoutPanel.Controls.Add(this.picFormatText, 1, 8);
            this.tableLayoutPanel.Controls.Add(this.displayMode, 0, 9);
            this.tableLayoutPanel.Controls.Add(this.displayComboBox, 1, 9);
            this.tableLayoutPanel.Controls.Add(this.imageHeight, 0, 10);
            this.tableLayoutPanel.Controls.Add(this.numImageHeight,1, 10);
            this.tableLayoutPanel.Controls.Add(this.imageWidth, 0, 11);
            this.tableLayoutPanel.Controls.Add(this.numImageWidth,1, 11);
            this.tableLayoutPanel.Controls.Add(this.isCacheLabel, 0, 12);
            this.tableLayoutPanel.Controls.Add(this.isCacheComboBox, 1, 12);
            // 
            // username input 
            // 
            this.label1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.TabIndex = 0;
            this.label1.Text = "userName";
            this.textBox1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.textBox1.TabIndex = 1;

            // 
            // numHorizontalImages
            // 
            this.label2.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.TabIndex = 0;
            this.label2.Text = "numHorizontalImages";
            this.numHorizontalImages.Font = new System.Drawing.Font("Times New Roman", 14F);
            this.numHorizontalImages.Maximum = new decimal(new int[] { 999, 0, 0, 0});
            this.numHorizontalImages.Minimum = new decimal(new int[] { 1, 0, 0, 0});
            this.numHorizontalImages.Name = "numHorizontalImages";
            this.numHorizontalImages.TabIndex = 3;
            this.numHorizontalImages.Value = new decimal(new int[] { 8, 0, 0, 0});

            // 
            // numVerticalImages
            // 
            this.label3.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.TabIndex = 0;
            this.label3.Text = "numVerticalImages";
            this.numVerticalImages.Font = new System.Drawing.Font("Times New Roman", 14F);
            this.numVerticalImages.Maximum = new decimal(new int[] { 999, 0, 0, 0 });
            this.numVerticalImages.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            this.numVerticalImages.Name = "numVerticalImages";
            this.numVerticalImages.TabIndex = 4;
            this.numVerticalImages.Value = new decimal(new int[] { 9, 0, 0, 0 });
            // 
            // disparity distance
            // 
            this.disparityDistance.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.disparityDistance.AutoSize = true;
            this.disparityDistance.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.disparityDistance.Text = "stereoImageDistance";
            this.numOfDisparity.Font = new System.Drawing.Font("Times New Roman", 14F);
            this.numOfDisparity.Maximum = new decimal(new int[] { 999, 0, 0, 0 });
            this.numOfDisparity.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            this.numOfDisparity.Value = new decimal(new int[] { 1, 0, 0, 0 });
            // 
            // angular distance
            // 
            this.angularDistance.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.angularDistance.AutoSize = true;
            this.angularDistance.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.angularDistance.Text = "viewChangeDistance";
            this.angularSpeed.Font = new System.Drawing.Font("Times New Roman", 14F);
            this.angularSpeed.Maximum = new decimal(new int[] { 5000, 0, 0, 0 });
            this.angularSpeed.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            this.angularSpeed.Value = new decimal(new int[] { 30, 0, 0, 0 });


            // 
            // NEXT
            // 
            this.NEXT.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.NEXT.Location = new System.Drawing.Point(89, 167);
            this.NEXT.Name = "NEXT";
            this.NEXT.Size = new System.Drawing.Size(75, 23);
            this.NEXT.TabIndex = 2;
            this.NEXT.Text = "NEXT";
            this.NEXT.UseVisualStyleBackColor = true;
            this.NEXT.Click += new System.EventHandler(this.NEXT_Click);
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.NEXT);
            //this.groupBox1.Controls.Add(this.DataConfig);
            //this.groupBox1.Controls.Add(this.textBox1);
            //this.groupBox1.Controls.Add(this.label1);
            //this.groupBox1.Controls.Add(this.label2);
            //this.groupBox1.Controls.Add(this.label3);
            //this.groupBox1.Controls.Add(this.numHorizontalImages);
            //this.groupBox1.Controls.Add(this.numVerticalImages);
            //this.groupBox1.Controls.Add(this.dataConfigLabel);
            this.groupBox1.Controls.Add(this.tableLayoutPanel);
            this.groupBox1.Location = new System.Drawing.Point(116, 97);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(354, 223);
            this.groupBox1.TabIndex = 3;
            this.groupBox1.TabStop = false;

            // 
            // dataConfigLabel
            // 
            this.dataConfigLabel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.dataConfigLabel.Text = "path_of_input_data_txt";
            this.dataConfigLabel.Font = new System.Drawing.Font("Times New Roman", 14F);
            //this.dataConfigLabel.Size = new System.Drawing.Size(89, 23);
            this.dataConfigLabel.TabIndex = 5;
            this.DataConfig.AutoSize = true;
            this.DataConfig.Name = "DataConfig";
            this.DataConfig.TabIndex = 2;
            this.DataConfig.Text = "DataConfig";
            this.DataConfig.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.DataConfig.UseVisualStyleBackColor = true;
            this.DataConfig.Click += DataConfigSetting_Click;
            // 
            // picture config label
            // 
            this.pictureConfigLabel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.pictureConfigLabel.Text = "root_fold_of_images";
            this.pictureConfigLabel.Font = new System.Drawing.Font("Times New Roman", 14F);
            this.pictureConfigLabel.TabIndex = 5;
            this.PicturesConfig.AutoSize = true;
            this.PicturesConfig.TabIndex = 2;
            this.PicturesConfig.Text = "PicturesConfig";
            this.PicturesConfig.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.PicturesConfig.UseVisualStyleBackColor = true;
            this.PicturesConfig.Click += PicConfigSetting_Click;
            // 
            // depth config label
            // 
            this.depthConfigLabel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.depthConfigLabel.Text = "root_fold_of_depthmap";
            this.depthConfigLabel.Font = new System.Drawing.Font("Times New Roman", 14F);
            this.depthConfigLabel.TabIndex = 5;
            this.DepthConfig.AutoSize = true;
            this.DepthConfig.TabIndex = 2;
            this.DepthConfig.Text = "DepthConfig";
            this.DepthConfig.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.DepthConfig.UseVisualStyleBackColor = true;
            this.DepthConfig.Click += DepConfigSetting_Click;
            //
            //  picture format
            //
            this.picFormatLabel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.picFormatLabel.AutoSize = true;
            this.picFormatLabel.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.picFormatLabel.TabIndex = 0;
            this.picFormatLabel.Text = "imageFormat";
            this.picFormatText.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.picFormatText.TabIndex = 1;
            this.picFormatText.Text = "bmp";

            //
            //  display mode 
            //  
            this.displayMode.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.displayMode.AutoSize = true;
            this.displayMode.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.displayMode.TabIndex = 0;
            this.displayMode.Text = "displayMode";
            this.displayComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
            this.displayComboBox.Items.AddRange(new string[] {"3D", "2D" });
            this.displayComboBox.SelectedIndexChanged += ComboBox_SelectedIndexChange;
            this.displayComboBox.SelectedIndex = 0;

            //
            //  is cache image selection
            //  
            this.isCacheLabel.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.isCacheLabel.AutoSize = true;
            this.isCacheLabel.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.isCacheLabel.TabIndex = 0;
            this.isCacheLabel.Text = "isCacheAllViews(Requires a lot of memory and is prone to memory leaks)";
            this.isCacheComboBox.DropDownStyle= ComboBoxStyle.DropDownList;
            this.isCacheComboBox.Items.AddRange(new string[] { "No", "Yes" });
            this.isCacheComboBox.SelectedIndexChanged += ComboBox_IsCacheImageIndexChange;
            this.isCacheComboBox.SelectedIndex = 0;

            //  
            //  image height and width
            //
            this.imageHeight.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.imageHeight.AutoSize = true;
            this.imageHeight.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.imageHeight.Text = "imageHeight";
            this.numImageHeight.Font = new System.Drawing.Font("Times New Roman", 14F);
            this.numImageHeight.Maximum = new decimal(new int[] { 9999, 0, 0, 0 });
            this.numImageHeight.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            this.numImageHeight.Value = new decimal(new int[] { 434, 0, 0, 0 });

            this.imageWidth.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
            | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.imageWidth.AutoSize = true;
            this.imageWidth.Font = new System.Drawing.Font("Times New Roman", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.imageWidth.Text = "imageWidth";
            this.numImageWidth.Font = new System.Drawing.Font("Times New Roman", 14F);
            this.numImageWidth.Maximum = new decimal(new int[] { 9999, 0, 0, 0 });
            this.numImageWidth.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            this.numImageWidth.Value = new decimal(new int[] { 625, 0, 0, 0 });
            // 
            // login
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1430, 920);
            this.Controls.Add(this.groupBox1);
            this.Name = "login";
            this.Text = "login";
            ((System.ComponentModel.ISupportInitialize)(this.numHorizontalImages)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numVerticalImages)).EndInit();
            //this.tableLayoutPanel.ResumeLayout(false);
            //this.tableLayoutPanel.PerformLayout();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        //  username
        private System.Windows.Forms.Label label1;  
        private System.Windows.Forms.TextBox textBox1;
        //  numHorizontalImages
        private System.Windows.Forms.Label label2;  
        private System.Windows.Forms.NumericUpDown numHorizontalImages;
        //  numVerticalImages
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown numVerticalImages;

        //  data config 
        private System.Windows.Forms.Button DataConfig;
        private System.Windows.Forms.TextBox dataConfigLabel;
        //private string data_config_path;

        //  picture fold path config
        private System.Windows.Forms.Button PicturesConfig;
        private System.Windows.Forms.TextBox pictureConfigLabel;
        //private string picture_fold_path;

        //  depth fold path config
        private System.Windows.Forms.Button DepthConfig;
        private System.Windows.Forms.TextBox depthConfigLabel;
        //private string depth_fold_path;

        //  disparity distance
        private System.Windows.Forms.Label disparityDistance;
        private System.Windows.Forms.NumericUpDown numOfDisparity;

        //  Angular view change distance
        private System.Windows.Forms.Label angularDistance;
        private System.Windows.Forms.NumericUpDown angularSpeed;

        //  picture format
        private Label picFormatLabel;
        private TextBox picFormatText;

        //  display mode
        private Label displayMode;
        private ComboBox displayComboBox;
        private string display_mode;

        //  image height and width
        private Label imageHeight;
        private Label imageWidth;
        private NumericUpDown numImageHeight;
        private NumericUpDown numImageWidth;

        //  is cache image
        private Label isCacheLabel;
        private ComboBox isCacheComboBox;
        private string is_cache_string;
        
        //  item box and next button
        private System.Windows.Forms.Button NEXT;
        private System.Windows.Forms.GroupBox groupBox1;


        


        //  table layout panel
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel;
    }
}