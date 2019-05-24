# Glass brain connectome
import nibabel as nib
import numpy as np
from fury import actor, window, colormap, ui
from dipy.tracking.streamline import Streamlines
import random
import sys

if __name__ == "__main__":
    streamlines_mni = str(sys.argv[1])
    ch2bet = "/Users/alex/Dropbox/NeuroData/ndmg_atlases/mask/MNI152NLin6_res-2x2x2_T1w_descr-brainmask.nii.gz"
    # ch2bet =  "/Users/derekpisner/Applications/PyNets/build/lib/pynets/templates/ch2better.nii.gz"
    atlas = "/Users/alex/Dropbox/NeuroData/ndmg_atlases/label/desikan_space-MNI152NLin6_res-2x2x2.nii.gz"
    r = window.Renderer()

    template_img = nib.load(ch2bet)
    template_img_data = template_img.get_data()
    template_actor = actor.contour_from_roi(
        template_img_data, color=(50, 50, 50), opacity=0.1
    )
    r.add(template_actor)

    atlas_img = nib.load(atlas)
    atlas_img_data = atlas_img.get_data()

    streamlines_mni_in = nib.streamlines.load(streamlines_mni).streamlines
    streamlines_actor = actor.line(
        streamlines_mni_in,
        colormap.create_colormap(
            np.zeros([len(streamlines_mni_in)]), name="Greys_r", auto=True
        ),
        lod_points=10000,
        depth_cue=True,
        linewidth=0.2,
        fake_tube=True,
        opacity=0.3,
    )
    r.add(streamlines_actor)

    roi_colors = np.random.rand(int(np.max(atlas_img_data)), 3)
    parcel_contours = []
    i = 0
    for roi in np.unique(atlas_img_data)[1:36]:
        parcel_contours.append(
            actor.contour_from_roi(
                atlas_img_data == roi, color=roi_colors[i], opacity=0.4
            )
        )
        i = i + 1

    for vol_actor in parcel_contours:
        r.add(vol_actor)

    window.show(r)
