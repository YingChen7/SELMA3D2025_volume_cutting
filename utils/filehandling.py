import os 
import cv2 
import numpy as np
import pickle
import nibabel as nib
from pathlib import Path

def psave(path, variable):
    '''
    psave(path, variable)
    
    Takes a variable (given as string with its name) and saves it to a file as specified in the path.
    The path must at least contain the filename (no file ending needed), and can also include a 
    relative or an absolute folderpath, if the file is not to be saved to the current working directory.
    '''
    if not path.endswith('.pickledump'):
        path += '.pickledump'
    
    folderpath = Path(path).parent
    folderpath.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(variable, f, protocol=4)


def pload(path):
    '''
    variable = pload(path)
    
    Loads a variable from a file that was specified in the path. The path must at least contain the 
    filename (no file ending needed), and can also include a relative or an absolute folderpath, if 
    the file is not to located in the current working directory.
    '''
    if not path.endswith('.pickledump'):
        path += '.pickledump'
        
    p = Path(path)

    # Convert to absolute path if needed
    if not p.is_absolute():
        p = (Path.cwd() / p).resolve()
    with open(p, 'rb') as f:
        return pickle.load(f)


def estimateVolSize(pathtofolders,folderlist):
    ''' 
    Estimates size of stack of images from arbitrary number of folders where each folder 
    corresponds to one channel. Expects each file per folder to be grayscale
     
    Returns string with size in GB, dimensionality (n_y,n_x,n_z,n_c), and bitdepth, where
    
     * n_y is the height of a single image
     * n_x is the width of a single image
     * n_z is the number of images per folder
     * n_c is the number of folders
    '''

    print("Path for volume size estimation: {} {}".format(pathtofolders, folderlist))
    n_c = len(folderlist)
    base_path = Path(pathtofolders)
    if n_c > 1:
        folder = base_path / folderlist[0]
    else:
        folder = base_path
        
    filelist = os.listdir(folder)
    n_z = len(filelist)
    path = folder / filelist[0]
    print("Path : {}".format(path))
    image = cv2.imread(path,2)
    if image is None:
        raise ValueError(f"Failed to read image: {path}")
    
    (n_y,n_x) = image.shape
    bitdepth =  image.dtype.itemsize * 8

    size = int(n_y*n_x*n_z*n_c*bitdepth / 8 / 1024**3)
    return (size,(n_y,n_x,n_z,n_c),bitdepth)


def writeNifti(path,volume,compress=False):
    '''
    writeNifti(path,volume)
    
    Takes a Numpy volume, converts it to the Nifti1 file format, and saves it to file under
    the specified path. 
    '''
    path = Path(path)

    # Add extension if missing
    if compress:
        if not path.name.endswith('.nii.gz'):
            path = path.with_suffix('.nii.gz')
    else:
        if not path.name.endswith('.nii'):
            path = path.with_suffix('.nii')

    path.parent.mkdir(parents=True, exist_ok=True)
    # Save volume with adjusted orientation
    # --> Swap X and Y axis to go from (y,x,z) to (x,y,z)
    # --> Show in RAI orientation (x: right-to-left, y: anterior-to-posterior, z: inferior-to-superior)
    affmat = np.eye(4)
    affmat[0,0] = affmat[1,1] = -1
    NiftiObject = nib.Nifti1Image(np.swapaxes(volume,0,1), affine=affmat)

    nib.save(NiftiObject,path)


def readNifti(path,reorient=None):
    '''
    volume = readNifti(path)
    
    Reads in the NiftiObject saved under path and returns a Numpy volume.
    This function can also read in .img files (ANALYZE format).
    '''
    path = Path(path)
    
    # Add extension if missing
    if not (path.suffix in ['.nii', '.img']):
        path = path.with_suffix('.nii')
        
    if path.is_file():
        final_path = path
    elif path.with_suffix(path.suffix + '.gz').is_file():
        final_path = path.with_suffix(path.suffix + '.gz')
    else:
        raise FileNotFoundError(f"No file found at: {path}")

    NiftiObject = nib.load(str(final_path))   
    # Load volume and adjust orientation from (x,y,z) to (y,x,z)
    volume = np.swapaxes(NiftiObject.dataobj,0,1)


    if reorient == 'uCT_Rosenhain' and path.suffix == '.img':
        # Special reorientation for Rosenhain dataset
        volume = np.swapaxes(volume, 0, 2)  # swap y and z
        volume = np.flip(volume, 0)         # head at y=0
        volume = np.flip(volume, 2)         # belly at x=0

    return volume
