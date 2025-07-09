### For SELMA3D2025: volume cutting - cutting tif slices into 3D patches 

The original large 3D light-sheet microscopy images provided in SELMA2025 are saved as TIFF slices. Participants who need to crop them into smaller 3D patches for model training can use this repository, which is adapted from the pipeline of our [SCP-Nano](https://github.com/erturklab/SCP-Nano/) project. The resulting 3D patches will be saved as NIFTI files.


#### How to implement it?
1. Install Anaconda and python.
2. Clone this repository to your device and install the required libraries by: 

   `pip install -r requirements.txt`
3. In [main_cutting.py](./main_cutting.py), set the variable `dir_data` to the parent folder contianing the TIFF series folder, and set `slice_folder_name` to the name of the folder with TIFF series.

4. Adjust `patch_size` and `patch_overlap` as needed.

5. Run `main_cutting.py`



