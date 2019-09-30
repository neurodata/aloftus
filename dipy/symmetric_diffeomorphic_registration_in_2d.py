#%%
import nibabel as nib
import numpy as np
from dipy.data import get_fnames
from dipy.align.imwarp import SymmetricDiffeomorphicRegistration
from dipy.align.metrics import SSDMetric, CCMetric
import dipy.align.imwarp as imwarp
from dipy.viz import regtools
from dipy.segment.mask import median_otsu


#%%
fname_moving = get_fnames("reg_o")
fname_static = get_fnames("reg_c")

moving = np.load(fname_moving)
static = np.load(fname_static)

regtools.overlay_images(static, moving, "Static", "Overlay", "Moving", 'input_images.png')

#%%

# Sum of Squared Differences metric
dim = static.ndim
metric = SSDMetric(dim)

level_iters = [200, 100, 50, 25]
sdr = SymmetricDiffeomorphicRegistration(metric, level_iters, inv_iter=50)

mapping = sdr.optimize(static, moving)

# plot diffeomorphic map
regtools.plot_2d_diffeomorphic_map(mapping, 10, 'diffeomorphicmap.png')

#%%
warped_static = mapping.transform_inverse(static, "linear")
regtools.overlay_images(warped_static, moving, "Warped Static", "Overlay", "Moving", "inverse_warp_result.png")
regtools.overlay_images(static, moving, "Static", "Overlay", "Moving", 'input_images.png')

#%%
def callback_CC(sdr, status):
    if status == imwarp.RegistrationStages.SCALE_END:

        # get the current images from the metric
        wmoving = sdr.metric.moving_image
        wstatic = sdr.metric.static_image

        # draw the images on top of each other with different colors
        regtools.overlay_images(wmoving, wstatic, 'Warped moving', 'Overlay', 'Warped Static')

t1w = nib.load('/Users/alex/.ndmg_data/input/sub-0025427/ses-1/anat/sub-0025427_ses-1_T1w.nii.gz')
b0 = nib.load('/Users/alex/.ndmg_data/output/sub-0025427/ses-1/dwi/preproc/nodif_B0.nii.gz')
data = np.array(b0.get_data(), dtype=np.float64)

b0_mask, mask = median_otsu(data, median_radius=4, numpass=4)

#%%
# plot brain segmentation
regtools.plot_slices(data)
regtools.plot_slices(b0_mask)

#%%
# grab a couple slices for registration
static = b0_mask[..., 40]
moving = b0_mask[..., 38]

# Instantiate Cross Correlation metric
sigma_diff = 3.0
radius = 4
metric = CCMetric(2, sigma_diff, radius)

level_iters = [100, 50, 25]
sdr = SymmetricDiffeomorphicRegistration(metric, level_iters)
sdr.callback = callback_CC

mapping = sdr.optimize(static, moving)
warped = mapping.transform(moving)

#%%
# plot
regtools.overlay_images(static, moving, "Static", "Overlay", "Moving", "t1_slices_input.png")

#%%
inv_warped = mapping.transform_inverse(static)
regtools.overlay_images(inv_warped, moving, "Warped static", "Overlay", "Moving", "t1_slices_res2.png")

#%%
regtools.plot_2d_diffeomorphic_map(mapping, 5, "diffeomorphic_map_b0s.png")
