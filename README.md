# subject-LFIQA-software Version 2.3

This is IMCL software for subjective light field image quality assessment. It has been remade with Qt (PySide6).

The software can be used for subjective light field image quality assessment (LFIQA) . As proposed in our JPEG proposal [1], the LF images features differs LFIQA from the traditional 2D image evaluation. Thus before your experiment, you need to decide which feature you want to evaluate and how to display them to your subjects.

The features include:
- Stereo parallax 
- Moving parallax
- refocusing

The display type, 2D or 3D, decides the stereo parallax feature. The moving parallax and refocusing features can be explored with mouse moving and clicking and we call it the active mode. A pseudo sequence generated with views or refocusing images can also be used and that's called a passive mode.

## New feature
MPV is used as backend for passive mode.

## How to Run
As the project is implemented with Python, you may run it from the scripts. But I recommend to use the compiled binary file that we released.  

If you want a passive light field image feature (i.e. passive view changing or passive refocusing), then make sure you have installed the ffmpeg in your system. For windows system you can download the portable **ffmpeg [here](https://github.com/GyanD/codexffmpeg/releases/tag/2023-09-29-git-40aa451154)**. The ffmpeg path should be added into system environment.

1. Run from scripts
   
   Python 3.9+ is recomended.
   Before running it some python modules should be installed. 
   
   ```
   pip install PySide6 xlsxwriter xlsxreader openpyxl numpy opencv-python
   ```
   Download and unpack the source code. Enter the folder and run it with
   
   ```
   python LFIQoE.py
   ```
   
2. (Recommended) Alternatively, you can download the [binary file](https://github.com/USTC-IMCL/subject-LFIQA-software/releases/tag/V2.0). Put it to anywhere you like and double click it.


**If you want a refocusing feature, please put the lambda file and the depth map in each folder. The lambda file is only for the dense light field image. The module for sparse light field images need to be further implemented.**

## Configuration
Click the Project->New button to create a new experiment. 

![image](https://github.com/USTC-IMCL/subject-LFIQA-software/assets/9655283/533d0341-1a55-4f6b-8805-35e58cb802f5)

Please use the Json file to configure your experiment. An example is shown below:

```
{
    "Training":[
        {
            "Name":"Bikes",
            "Width": 625 ,
            "Height": 434,
            "Angular_Height": 11,
            "Angular_Width": 11,
            "Type":"Dense",
            "Angular_Format":"XY",
            "SRC":"C:/Users/ZSY/Downloads/Bikes/Ori",
            "HRC":
            [ 
                {
                    "Distortion_Type":"HEVC",
                    "Distortion_Level":1,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/HEVC/1"
                },
                {
                    "Distortion_Type":"HEVC",
                    "Distortion_Level":2,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/HEVC/2"
                },
                {
                    "Distortion_Type":"HEVC",
                    "Distortion_Level":3,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/HEVC/3"
                },
                {
                    "Distortion_Type":"HEVC",
                    "Distortion_Level":4,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/HEVC/4"
                },
                {
                    "Distortion_Type":"HEVC",
                    "Distortion_Level":5,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/HEVC/5"
                },
                {
                    "Distortion_Type":"JPEG",
                    "Distortion_Level":"1",
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/JPEG/1"
                },
                {
                    "Distortion_Type":"JPEG",
                    "Distortion_Level":"2",
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/JPEG/2"
                },
                {
                    "Distortion_Type":"JPEG",
                    "Distortion_Level":3,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/JPEG/3"
                },
                {
                    "Distortion_Type":"JPEG",
                    "Distortion_Level":"4",
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/JPEG/4"
                },
                {
                    "Distortion_Type":"JPEG",
                    "Distortion_Level":"5",
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/JPEG/5"
                }
            ]
        }
    ],
    "Test":[
        {
            "Name":"Bikes",
            "Width": 625 ,
            "Height": 434,
            "Angular_Height": 11,
            "Angular_Width": 11,
            "Type":"Dense",
            "Angular_Format":"XY",
            "SRC":"C:/Users/ZSY/Downloads/Bikes/Ori",
            "HRC":
            [ 
                {
                    "Distortion_Type":"HEVC",
                    "Distortion_Level":1,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/HEVC/1"
                },
                {
                    "Distortion_Type":"HEVC",
                    "Distortion_Level":2,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/HEVC/2"
                },
                {
                    "Distortion_Type":"HEVC",
                    "Distortion_Level":3,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/HEVC/3"
                },
                {
                    "Distortion_Type":"HEVC",
                    "Distortion_Level":4,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/HEVC/4"
                },
                {
                    "Distortion_Type":"HEVC",
                    "Distortion_Level":5,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/HEVC/5"
                },
                {
                    "Distortion_Type":"JPEG",
                    "Distortion_Level":"1",
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/JPEG/1"
                },
                {
                    "Distortion_Type":"JPEG",
                    "Distortion_Level":"2",
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/JPEG/2"
                },
                {
                    "Distortion_Type":"JPEG",
                    "Distortion_Level":3,
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/JPEG/3"
                },
                {
                    "Distortion_Type":"JPEG",
                    "Distortion_Level":"4",
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/JPEG/4"
                },
                {
                    "Distortion_Type":"JPEG",
                    "Distortion_Level":"5",
                    "Distortion_Path":"C:/Users/ZSY/Downloads/Bikes/dist/JPEG/5"
                }
            ]
        }
    ],
    "Exp_Info":{
        "Display_Type":"2D", (2D or 3D)
        "Score_Levels":5, (not used yet)
        "ThreeD_Type":"LeftRight", (LeftRight, UpDown or Full)
        "View_Changing":"Active", (Active, passive or None)
        "Refocusing":"Active", (Active, passive or None)
        "Comparison":"DoubleStimuli", (can be DoubleStimuli, SingleStimulous or PairComparison)
        "Save_Format":"CSV", (CSV or Excel)
        "PairWise_Path":"PairWise.json", (Your path to the pair list json)
        "Skip_Preprocessing": false 
    }
}
```

The configuration file must contain 3 keys: training, test and Exp_Info. The training and test describe your light field images (SRCs and HRCs). You need to denote the distortion type, distortion level and distortion path for each HRC. The distoriton level can be a string or an int number. The distortion path should be the root folder of the HRC, which means all possible views or passive videos should be in this folder (may be in a certain subfolder).

If you want a pair comparison, set the comparison to paircomparison. A pair list json example is shown below. It describes 3 pairs for training and 3 pairs for test.

```
{
    "training":
    {
        "0":
        {
            "lfi_name": "Bikes",
            "left": "HEVC",
            "left_level": 1,
            "right":"JPEG",
            "right_level": "2"
        }
        ,
        "1":
        {
            "lfi_name": "Bikes",
            "left": "HEVC",
            "left_level": 3,
            "right":"JPEG",
            "right_level": 3
        },
        "2":
        {
            "lfi_name": "Bikes",
            "left": "HEVC",
            "left_level": 3,
            "right":"JPEG",
            "right_level": "2"
        }
    },
    "test":
    {
        "0":
        {
            "lfi_name": "Bikes",
            "left": "HEVC",
            "left_level": 1,
            "right":"JPEG",
            "right_level": 3
        }
        ,
        "1":
        {
            "lfi_name": "Bikes",
            "left": "HEVC",
            "left_level": 5,
            "right":"JPEG",
            "right_level": "2"
        },
        "2":
        {
            "lfi_name": "Bikes",
            "left": "HEVC",
            "left_level": 3,
            "right":"JPEG",
            "right_level": "4" 
        }
    }
}
```

## Preprocessing

Click the Run -> Preprocessing to generate images or videos for your experiments.

![image](https://github.com/USTC-IMCL/subject-LFIQA-software/assets/9655283/9382d20f-a4d3-400b-95de-130e99f8b8b4)

Note that now the refocusing module only supports light field images captured by Lytro. But the extension for different rigs will be supported in the future.

If you use a passive feature for your experiment, you may find a .mp4 file in the folder. It is generated by concating show views. To make sure a **view synchronization**, we stiching the comparing views into one single frame and compress it with ffmpeg **losslessly**. The views order or the focusing moving order is fixed now (but can be extended).

## Custom preprocessing

Sometimes you may want to preprocess it manually. Then keep the skip_preprocessing to true. Then organize your folder as following:

```
├── SRC-distortion-path
│   └── show_views
|      └── xxx_yyy.png (stitched views)
|      └── view.mp4 (your passive video)
│   └── show_refocusing
|      └── depth_value.png (stitched refocusing image)
|      └── refocus.mp4 (your passive video)
|   └── training
|      └── PairComparison_{Your_pair_key_in_the_pair_list_json}
│         └── show_views
|            └── xxx_yyy.png (stitched views)
|            └── view.mp4 (your passive video)
│         └── show_refocusing
|            └── depth_value.png (stitched refocusing image)
|            └── refocus.mp4 (your passive video)
|      └── PairComparison_.....
|   └── test
|      └── PairComparison_{Your_pair_key_in_the_pair_list_json}
│         └── show_views
|            └── xxx_yyy.png (stitched views)
|            └── view.mp4 (your passive video)
│         └── show_refocusing
|            └── depth_value.png (stitched refocusing image)
|            └── refocus.mp4 (your passive video)
|      └── PairComparison_.....
.......
```

Please organize the folder based on your experiment and you do not need to generate all the folders above. For example, if you use a passive view changing only configuration, then you just need a show_views folder and put the view.mp4 in it.

## How to evaluate

This section explains the operation to evaluate the light field image.

0. Start your training or test

1.Use the Run -> Start training or Run -> Start test to start your evaluation experiment. Note that the training stage won't record your subjects' name -- the training stage should try to teach the subjects, not to record their socres.


2. Active view changing
   
   Use a right click (any position is fine) to start the view changing. Then you can change the view by moving mouse. Note that we use a right click to "wake up" the view changing instead of using the hover directly. This avoids subjects to take a border view as the first-glance view and can make sure that each subject starts from the same view (e.g. the center view).
    
3. Active refocusing
   
  
  Use a left clicing (any positin within the view) to select where you want to focus. This will close the active view changing.
      
3. Passive feature
   
   Just left clicking the view then the video begins playing.

4. Pair comparison
   
   Use a left or right arrow to select the better one. Note once you press the key, it records your choice and show the next page.

5. Scoring
   
   Use left or right arrow te select the scring table and the number key to offer you evaluation score.
   
   ![image](https://github.com/USTC-IMCL/subject-LFIQA-software/assets/9655283/c169c84d-11d6-4247-acec-69ebaa872fab)

6. Next page
   
   Use enter key to get next page when you have finished exploring the light field immage (except the pair-wise comparison mode).

## Postprocessing

  Click the Run -> Post Processing button to start the post processing. The project will record all your subjects so you just need to click the button. It will calculate the PLCC between each subjects and others' mean scores.

## Compile to exe file

   If you want to revise the source code and compile it manually, use the pyinstaller:

   ```
   pyinstaller --onefile -w -p ./UI -p ./Widgets --add-data "your/path/to/ffmpeg;./" LFIQoE.py
   ```

## Acknowledgement

We follow the BSD license.

Any problem or quesition please email me: zsy7788@mail.ustc.edu.cn. Any new issue for this project is welcome.
