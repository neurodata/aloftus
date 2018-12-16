# Output files for ndmg : master branch

## ndmg-d individual-level pipeline

- fibers : for every subject, for every session, contains a .npz file with tractography information.

- graphs : For every subject, for every session and parcellation, contains edgelist output.

- qa : Quality assurance output.
    - fibers : Empty
    - reg : For every subject, for every session, contains .png images that show the registration.
    - tensors : For every subject, for every session, contains .png images that show the tensor estimation.

- reg : For each subject, for each session, contains .nii.gz files with aligned images.

- tensors : 
    - For each subject, for each session, contains a .nii.gz file with tensor estimation.
    - For each subject, for each session, contains a numpy compressed array (.npz) file with tensor estimation.

- temp :
    - For each subject, for each session, contains temporary .nii.gz files, .ecclog files, and .mat files
