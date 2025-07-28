import json
from ExpInfo import LFIFeatures,ComparisonType,ExpSetting,SaveFormat,VideoSaveTypeDict

def GetConfigExpSetting(config_file):
    all_config=json.load(config_file)
    exp_config=all_config['Exp_Info']

    exp_keys=list(exp_config.keys())
    disp_type=exp_config["Display_Type"]
    threed_type=exp_config["ThreeD_Type"]
    view_change_type=exp_config["View_Changing"]
    refocusing_type=exp_config["Refocusing"]
    cmp_type=exp_config["Comparison"]
    save_format_type=exp_config["Save_Format"]

    all_lfi_features=[]

    disp_type=disp_type.lower()
    threed_type=threed_type.lower()
    if disp_type == '2d':
        all_lfi_features.append(LFIFeatures.TwoD)
    if disp_type == '3d':
        if threed_type == "lr" or threed_type =="leftright":
            all_lfi_features.append(LFIFeatures.Stereo_horizontal)
        if threed_type == "ud" or threed_type =="updown":
            all_lfi_features.append(LFIFeatures.Stereo_vertical)
        if threed_type == "full" or threed_type =="fullfield":
            all_lfi_features.append(LFIFeatures.Stereo_full)

    view_change_type=view_change_type.lower()
    if view_change_type == "active":
        all_lfi_features.append(LFIFeatures.Active_ViewChanging) 
    if view_change_type == "passive":
        all_lfi_features.append(LFIFeatures.Passive_ViewChanging)
    if view_change_type == "none":
        all_lfi_features.append(LFIFeatures.None_ViewChanging)
    
    refocusing_type=refocusing_type.lower()
    if refocusing_type == "active":
        all_lfi_features.append(LFIFeatures.Active_Refocusing)
    if refocusing_type == "passive":
        all_lfi_features.append(LFIFeatures.Passive_Refocusing)
    if refocusing_type == "none":
        all_lfi_features.append(LFIFeatures.None_Refocusing)
    
    if LFIFeatures.None_Refocusing in all_lfi_features and LFIFeatures.None_ViewChanging in all_lfi_features:
        return None

    cmp_type_str=cmp_type.lower()
    if "double" in cmp_type_str:
        cmp_type=ComparisonType.DoubleStimuli
    if "single" in cmp_type_str:
        cmp_type=ComparisonType.SingleStimuli
    if "pair" in cmp_type_str:
        cmp_type=ComparisonType.PairComparison
    if "dscs" in cmp_type_str:
        if "base" in cmp_type_str:
            cmp_type=ComparisonType.DSCS_PC_BASE
        if "ccg" in cmp_type_str:
            cmp_type=ComparisonType.DSCS_PC_CCG
        
    if LFIFeatures.Active_Refocusing in all_lfi_features or LFIFeatures.Passive_Refocusing in all_lfi_features:
        all_lfi_features.append(LFIFeatures.Refocusing)
    
    save_format_type=save_format_type.lower()
    if save_format_type == "csv":
        save_format=SaveFormat.CSV
    if save_format_type == "excel":
        save_format=SaveFormat.Excel

    exp_setting=ExpSetting(all_lfi_features,cmp_type,save_format)
    
    if "Two_Folder_Mode" in exp_keys:
        exp_setting.two_folder_mode=exp_config["Two_Folder_Mode"]
    if "Auto_Play" in exp_keys:
        exp_setting.auto_play=exp_config["Auto_Play"]
    if "Loop_Times" in exp_keys:
        exp_setting.loop_times=exp_config["Loop_Times"]
    if "FPS" in exp_keys:
        exp_setting.fps=exp_config["FPS"]
    
    if "Input_Type" in exp_keys:
        input_types=exp_config["Input_Type"]
        input_types=input_types.split(";")
        for v_type in input_types:
            exp_setting.AddInputVideoType(v_type)
    else:
        for v_type in VideoSaveTypeDict.keys():
            exp_setting.AddInputVideoType(v_type)
    
    if "Score_Names" in exp_keys:
        exp_setting.score_names=exp_config["Score_Names"]
    if "Score_Levels" in exp_keys:
        cur_score_levels=exp_config["Score_Levels"]
        if type(cur_score_levels) == int:
            cur_score_levels=[cur_score_levels]*len(exp_setting.score_names)
        exp_setting.score_levels=cur_score_levels
    if "Score_Values" in exp_keys:
        cur_score_values=exp_config["Score_Values"]
        if isinstance(cur_score_values[0],int):
            cur_score_values=[cur_score_values]*len(exp_setting.score_names)
        exp_setting.score_values=cur_score_values
    else:
        cur_score_values=[]
        for score_level in exp_setting.score_levels:
            cur_score_values.append([score_level-i for i in range(score_level)])
        exp_setting.score_values=cur_score_values
    
    if "Score_Definition" in exp_keys:
        score_definition=exp_config["Score_Definition"]
        if type(score_definition[0]) == str:
            score_definition=[score_definition]*len(exp_setting.score_names)
        exp_setting.score_definition=score_definition
        for i in range(len(exp_setting.score_names)):
            if len(exp_setting.score_definition[i]) != exp_setting.score_levels[i]:
                exp_setting.score_definition=None
                break
    
    if "High_Quality_Only" in exp_keys:
        exp_setting.high_quality_only=exp_config["High_Quality_Only"]
    
    exp_setting.grading_num=exp_setting.score_levels[0]
    exp_setting.grading_scales=exp_setting.score_values[0]
    
    if cmp_type==ComparisonType.PairComparison and (not exp_setting.two_folder_mode):
        if "PairWise_List" not in exp_keys:
            return None
        else:
            exp_setting.pair_wise_dict=exp_config["PairWise_List"]
    exp_setting.skip_preprocessing=exp_config["Skip_Preprocessing"]

    if "Auto_Transition" in exp_keys:
        exp_setting.auto_transition=exp_config["Auto_Transition"]
    
    if "Pause_Allowed" in exp_keys:
        exp_setting.pause_allowed=exp_config["Pause_Allowed"]
    
    if "Passive_Control_Backend" in exp_keys:
        exp_setting.passive_control_backend=exp_config["Passive_Control_Backend"]

    if "First_Loop_Skip_Allowed" in exp_keys:
        exp_setting.first_loop_skip=exp_config["First_Loop_Skip_Allowed"]
    
    if "Skip_Hint_Text" in exp_keys:
        exp_setting.skip_hint_text=exp_config["Skip_Hint_Text"]
    
    if "Table_Font_Size" in exp_keys:
        exp_setting.table_font_size=exp_config["Table_Font_Size"]
    
    if "Hint_Font_Size" in exp_keys:
        exp_setting.hint_text_font_size=exp_config["Hint_Font_Size"]
    
    if "Allow_Undistinguishable" in exp_keys:
        exp_setting.allow_undistinguishable=exp_config["Allow_Undistinguishable"]

    return exp_setting