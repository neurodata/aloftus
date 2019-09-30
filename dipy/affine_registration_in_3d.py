#%%
import numpy as np
import nibabel as nib
from dipy.core.gradients import gradient_table
from dipy.io import read_bvals_bvecs
from dipy.viz import regtools
from dipy.data import fetch_stanford_hardi, read_stanford_hardi
from dipy.data.fetcher import fetch_syn_data, read_syn_data
from dipy.align.imaffine import (transform_centers_of_mass,
                                 AffineMap,
                                 MutualInformationMetric,
                                 AffineRegistration)

from dipy.align.transforms import (TranslationTransform3D,
                                   RigidTransform3D,
                                   AffineTransform3D)

from matplotlib import pyplot as plt
#%%
# Fetch b0 volume
b0 = nib.load("/Users/alex/.ndmg_data/output/sub-0025864/ses-1/dwi/preproc/0_B0.nii.gz")
bvals, bvecs = read_bvals_bvecs("/Users/alex/.ndmg_data/output/sub-0025864/ses-1/dwi/preproc/bval.bval", "/Users/alex/.ndmg_data/output/sub-0025864/ses-1/dwi/preproc/bvec_scaled.bvec")
gtab = gradient_table(bvals, bvecs, atol=1.0)

static = np.squeeze(b0.get_data())
print(f"static ndim: {static.ndim}")
static_grid2world = b0.affine

# moving image
t1w = nib.load('/Users/alex/.ndmg_data/output/sub-0025427/ses-1/anat/preproc/t1w_brain.nii.gz')
b0_corrected = nib.load('/Users/alex/.ndmg_data/output/sub-0025427/ses-1/dwi/preproc/nodif_B0.nii.gz')
moving = np.array(b0_corrected.get_data())
print(f"moving ndim: {moving.ndim}")
moving_grid2world = b0_corrected.affine

#%%
identity = np.eye(4); identity
affine_map = AffineMap(identity, static.shape, static_grid2world, moving.shape, moving_grid2world)
resampled = affine_map.transform(moving)

regtools.overlay_slices(static, resampled, None, 0, "Static", "Moving", "resampled_0.png")
regtools.overlay_slices(static, resampled, None, 1, "Static", "Moving", "resampled_1.png")
regtools.overlay_slices(static, resampled, None, 2, "Static", "Moving", "resampled_2.png")

#%%

# get center-of-mass of the two images, then translate on top of static image
c_of_mass = transform_centers_of_mass(static, static_grid2world, moving, moving_grid2world)
transformed = c_of_mass.transform(moving)

# visualize
regtools.overlay_slices(static, transformed, None, 0, "Static", "Transformed", "resampled_0.png")
regtools.overlay_slices(static, transformed, None, 1, "Static", "Transformed", "resampled_1.png")
regtools.overlay_slices(static, transformed, None, 2, "Static", "Transformed", "resampled_2.png")

#%%
# using an affine registration with Mutual Information Metric
nbins = 32
sampling_prob = None
metric = MutualInformationMetric(nbins, sampling_prob)
level_iters = [10000, 1000, 100]
sigmas = [3.0, 1.0, 0.0]
factors = [4, 2, 1]

affreg = AffineRegistration(metric=metric, level_iters=level_iters, sigmas=sigmas, factors=factors)
transform = TranslationTransform3D()
params0 = None
starting_affine = c_of_mass.affine
translation = affreg.optimize(static, moving, transform, params0, static_grid2world, moving_grid2world, starting_affine=starting_affine)
transformed = translation.transform(moving)

# visualize
regtools.overlay_slices(static, transformed, None, 0, "Static", "Transformed", "resampled_0.png")
regtools.overlay_slices(static, transformed, None, 1, "Static", "Transformed", "resampled_1.png")
regtools.overlay_slices(static, transformed, None, 2, "Static", "Transformed", "resampled_2.png")

#%%
# using a rigid transform
transform = RigidTransform3D()
params0 = None
starting_affine = translation.affine
rigid = affreg.optimize(static, moving, transform, params0, static_grid2world, moving_grid2world, starting_affine=starting_affine)
transformed = rigid.transform(moving)

regtools.overlay_slices(static, transformed, None, 0, "Static", "Transformed", "resampled_0.png")
regtools.overlay_slices(static, transformed, None, 1, "Static", "Transformed", "resampled_1.png")
regtools.overlay_slices(static, transformed, None, 2, "Static", "Transformed", "resampled_2.png")

#%%
# with a full affine transform
transform = AffineTransform3D()
params0 = None
starting_affine = rigid.affine
affine = affreg.optimize(static, moving, transform, params0, static_grid2world, moving_grid2world, starting_affine=starting_affine)
transformed = affine.transform(moving)

regtools.overlay_slices(static, transformed, None, 0, "Static", "Transformed", "resampled_0.png")
regtools.overlay_slices(static, transformed, None, 1, "Static", "Transformed", "resampled_1.png")
regtools.overlay_slices(static, transformed, None, 2, "Static", "Transformed", "resampled_2.png")

