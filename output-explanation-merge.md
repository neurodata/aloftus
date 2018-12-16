# Output files for ndmg : Eric's branch

## ndmg-d individual-level pipeline

- anat : Contains nothing?
    - preproc : Empty
    - registered : Empty

- dwi : 
    - fiber : For each subject, for each session, contains .npz (Numpy compressed) files for tractography estimation.
    - preproc : Empty
    - registered : For each subject, for each session, contains .nii.gz files with registered brains aligned with MNI152 space.
    - roi-connectomes : The final output. For every parcellation, for each subject, for each session, contains edgelists.
    - tensor : For each subject, for each session, contains .npz files for tensor estimation.
    - voxel-connectomes : Empty

 - qa : Quality assurance.
    - roi-connectomes : For each parcellation, contains pickle files which provide overall statistics.
    - sub folders: Each subject folder contains all quality assurance for that subject, for registration, tensor estimation, tractography, and graph generation.

- tmp : Contains temporary files for every subject.
    - For each subject, for each session, contains temporary masking files.
    - sub folders: Each subject folder contains a full copy of the folders in the ndmg individual level pipeline. Any temporary files for that subject go into these folders.
