import os
from utils import cut_volume_single_tiff

# Root of slice folder and the resulted folders
dir_data = r"/mnt/drive2/Ying/HFD/BigNeuron/gold166/tiffs/"
slice_folder_name = "1201_01_s06b_L36_Sum_ch2"
# set the patch size and overlap size between patches
patch_size = [300, 300, 300] 
patch_overlap = [10, 10, 10]

parameters = {}
parameters["file_format"] = "Nifti"
parameters["dataset"] = {}
parameters["dataset"]["channelname"] = ""
parameters['dataset']['sourcefolder'] = os.path.join(dir_data, slice_folder_name)
parameters['dataset']['localfolder'] = os.path.join(dir_data, slice_folder_name + "local")
parameters['dataset']['syncfolder'] =  os.path.join(dir_data, slice_folder_name + "sync")
parameters['dataset']['cachefolder'] = os.path.join(dir_data, slice_folder_name+ "cache")
parameters['dataset']['downsampling'] = 'None'
parameters['partitioning'] = {}
parameters['partitioning']['patch_size'] = patch_size
parameters['partitioning']['patch_overlap'] = patch_overlap
parameters['partitioning']['safe_cache'] = False
parameters['advanced'] = {}
parameters['advanced']['empty_patches'] = [] 
cut_volume_single_tiff.cut_volume(parameters)

