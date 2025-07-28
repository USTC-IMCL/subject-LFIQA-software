import sys
sys.path.append('./Utils')
sys.path.append('./Widgets')

import PlayList
import Config_Form
import ExpDataIO
import ExpInfo


if __name__ == '__main__':
    # playlist = PlayList.PlayList()
    # playlist.show()
    config_file="./Experiment_Jsons/DSCS_PC_Refine_base.json"
    exp_setting=ExpDataIO.GetConfigExpSetting(config_file)

    all_scoring_lfi=ExpInfo.TwoFolderLFIInfo("/home/heathcliff/Downloads/Serpentine_Left_Reference/two_folder/test",exp_setting.input_video_type_str,in_mode="test")

    scoring_num=all_scoring_lfi.GetLFINum()

    grading_num=exp_setting.grading_num
    grading_scales=exp_setting.grading_scales

    all_scores=[i%grading_num for i in range(scoring_num)]

    PlayList.MakeDSCSPCList(all_scoring_lfi,)