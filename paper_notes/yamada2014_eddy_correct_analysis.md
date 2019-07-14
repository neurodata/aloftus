# Efficacy of Distortion Correction on Diffusion Imaging: Comparison of FSL Eddy and Eddy_Correct Using 30 and 60 Directions Diffusion Encoding

## introduction
- looking at difference between `eddy` and `eddy_correct`
- eddy current
    - source of geometric distortion
    - lots of possible solutions
        - correct: multireference, field map with point-spread function mapping, k-space traversal
        - compensate: post-processing registration, twice-refocused spin echo, linear response theory characterization of eddy current field
        - k-space traversal + method of Bowtell : both susceptibility and eddu current correction
- there are a bunch of other reasons the images can be out of sync with each other too
- eddy_correct
    - corrected eddu current-induced bullshit, but didn't mitigate susceptibility-induced distortion or signal pileup
- topup / eddy
    - estimate both susceptibility and eddy current induced bullshit and correct them both

- present study
    - compare diffusion-derived FA values of
        - non-distortion corrected images
        - images correct with `eddy_correct`
        - image corrected with `eddy` and `topup`
    - do this voxel-wise with Tract-Based Spatial Statistics (TBSS)

## methods
- acquisition
    - they grabbed 10 reasonably-healthy homies from hospitals 
    - scanned the homies with reasonable parameters
- image processing
    - turned dicom scans into niftis
        - used `dcm2nii`
    - use `eddy_correct`, and `toppup`/`eddy` on those bad boys
    - FSL's `dtifit` used to make FA images
- statistical analysis
    - permutation-based tests with FSL `randomize_parallel`
        - 50,000 permutations
        - threshold-free cluster enhancement option
    - lots of paired t-tests
    - that's pretty much it

## results
- they looked at it with their eyeballs and thought eddy and topup looked better