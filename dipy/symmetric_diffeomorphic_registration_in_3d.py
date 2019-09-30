#%%
import os.path

import numpy as np
import nibabel as nib
from dipy.core.gradients import gradient_table
from dipy.io import read_bvals_bvecs

from dipy.align.imwarp import SymmetricDiffeomorphicRegistration
from dipy.align.imwarp import DiffeomorphicMap
from dipy.align.metrics import CCMetric
from dipy.align.imaffine import AffineMap

from dipy.viz import regtools

from dipy.segment.mask import median_otsu

#%%

# static image
b0_static = nib.load("/Users/alex/.ndmg_data/output/sub-0025864/ses-1/dwi/preproc/nodif_b0.nii.gz")
bvals_static, bvecs_static = read_bvals_bvecs("/Users/alex/.ndmg_data/output/sub-0025864/ses-1/dwi/preproc/bval.bval", "/Users/alex/.ndmg_data/output/sub-0025864/ses-1/dwi/preproc/bvec_scaled.bvec")
gtab_static = gradient_table(bvals_static, bvecs_static, atol=1.0)

static = np.squeeze(b0_static.get_data())
print(f"static ndim: {static.ndim}")
static_grid2world = b0_static.affine

# moving image
t1w_moving = nib.load('/Users/alex/.ndmg_data/output/sub-0025427/ses-1/anat/preproc/t1w_brain.nii.gz')
b0_moving = nib.load('/Users/alex/.ndmg_data/output/sub-0025427/ses-1/dwi/preproc/nodif_B0.nii.gz')
moving = np.array(b0_moving.get_data())
print(f"moving ndim: {moving.ndim}")
moving_grid2world = b0_moving.affine

#%%
# skull-strip both b0's
static, static_mask = median_otsu(static, median_radius=4, numpass=4)
moving, moving_mask = median_otsu(moving, median_radius=4, numpass=4)

static_affine = b0_static.affine
moving_affine = b0_moving.affine

#%%

# plot skull-stripping job
regtools.plot_slices(static)
regtools.plot_slices(moving)

#%%
pre_align = np.array([[1.02783543e+00, -4.83019053e-02, -6.07735639e-02, -2.57654118e+00],
                      [4.34051706e-03, 9.41918267e-01, -2.66525861e-01, 3.23579799e+01],
                      [5.34288908e-02, 2.90262026e-01, 9.80820307e-01, -1.46216651e+01],
                      [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

affine_map = AffineMap(pre_align, static.shape, static_affine, moving.shape, moving_affine)
resampled = affine_map.transform(moving)

regtools.overlay_slices(static, resampled, None, 1, "Static", "Moving", "input3d.png")

#%%
metric = CCMetric(3)
level_iters = [10, 10, 5]
sdr = SymmetricDiffeomorphicRegistration(metric, level_iters)
mapping = sdr.optimize(static, moving, static_affine, moving_affine, pre_align)
warped_moving = mapping.transform(moving)
regtools.overlay_slices(static, warped_moving, None, 1, "Static", "Warped moving", "input3d.png")

#%%
warped_static = mapping.transform_inverse(static)
regtools.overlay_slices(warped_static, moving, None, 1, "Warped static", "Moving", "warped_static.png")