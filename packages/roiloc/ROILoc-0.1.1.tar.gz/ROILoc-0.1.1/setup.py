# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roiloc']

package_data = \
{'': ['*'], 'roiloc': ['MNI/*', 'MNI/cerebra/*', 'MNI/icbm152/*']}

install_requires = \
['antspyx>=0.2.7,<0.3.0',
 'importlib-resources>=5.2.0,<6.0.0',
 'nibabel>=3.2.1,<4.0.0',
 'pandas>=1.3.0,<2.0.0',
 'rich>=10.5.0,<11.0.0']

entry_points = \
{'console_scripts': ['roiloc = roiloc.roiloc:start']}

setup_kwargs = {
    'name': 'roiloc',
    'version': '0.1.1',
    'description': 'A simple package to center and crop T1w & T2w MRIs around a given region of interest by its name.',
    'long_description': '=================\nWelcome to ROILoc\n=================\n\nROILoc is a registration-based ROI locator, based on the MNI152 09c Sym template, and the CerebrA Atlas. It\'ll center and crop T1 or T2 MRIs around a given ROI.\n\n.. image:: https://raw.githubusercontent.com/clementpoiret/ROILoc/main/example.png\n  :width: 400\n  :alt: Example: using ROILoc for Hippocampus\n  \nIf the results aren\'t correct, please consider performing BET/Skull Stripping on your subject\'s MRI beforehand, then pass ``-b True`` afterward.\nYou can use FSL or ANTs to perform BET. I personnally also had great and fast results from `deepbrain <https://github.com/iitzco/deepbrain>`_ which depends on TensorFlow 1.X.\n\nIt requires the following packages:\n\n- ANTs (Can be a system installation or anaconda installation),\n- ANTsPyX,\n- importlib_resources,\n- NiBabel,\n- Pandas,\n- Rich.\n\nusage: roiloc [-h] -p PATH -i INPUTPATTERN [-r ROI] -c CONTRAST [-b BET] [-t TRANSFORM] [-m MARGIN [MARGIN ...]] [--mask MASK]\n\narguments::\n\n  -h, --help            show this help message and exit\n  -p PATH, --path PATH  <Required> Input images path.\n  -i INPUTPATTERN, --inputpattern INPUTPATTERN\n                        <Required> Pattern to find input images in input path\n                        (e.g.: `**/*t1*.nii.gz`).\n  -r ROI, --roi ROI     ROI included in CerebrA. See\n                        `roiloc/MNI/cerebra/CerebrA_LabelDetails.csv` for more\n                        details. Default: \'Hippocampus\'.\n  -c CONTRAST, --contrast CONTRAST\n                        <Required> Contrast of the input MRI. Can be `t1` or\n                        `t2`.\n  -b BET, --bet BET     Boolean to choose if we use the BET version of the\n                        MNI152 template.\n  -t TRANSFORM, --transform TRANSFORM\n                        Type of registration. See `https://antspy.readthedocs.\n                        io/en/latest/registration.html` for the complete list\n                        of options. Default: `AffineFast`\n  -m MARGIN [MARGIN ...], --margin MARGIN [MARGIN ...]\n                        Margin to add around the bounding box in voxels. It\n                        has to be a list of 3 integers, to control the margin\n                        in the three axis. Default: [8,8,2]\n  --mask MASK           Pattern for brain tissue mask to improve registration\n                        (e.g.: `**/sub_*bet_mask.nii.gz`). If providing a BET\n                        mask, please also pass `-b True` to use a BET MNI\n                        template.\n\n\nExample:\n********\n\nLet\'s say I have a main database folder, containing one subfolder for each subject. In all those subjects folders, all of them have a t2w mri called ``tse.nii.gz`` and a brain mask call ``brain_mask.nii``.\n\nTherefore, to extract both left and right hippocampi (``Hippocampus``), I can run: \n\n``roiloc -p "~/Datasets/MemoDev/ManualSegmentation/" -i "**/tse.nii.gz" -r "hippocampus" -c "t2" -b True -t "AffineFast" -m 8 8 2 --mask "*brain_mask.nii``\n\n\nSupported Registrations\n***********************\n\n(Taken from ANTsPyX\'s doc)\n\n- ``Translation``: Translation transformation.\n- ``Rigid``: Rigid transformation: Only rotation and translation.\n- ``Similarity``: Similarity transformation: scaling, rotation and translation.\n- ``QuickRigid``: Rigid transformation: Only rotation and translation. May be useful for quick visualization fixes.\n- ``DenseRigid``: Rigid transformation: Only rotation and translation. Employs dense sampling during metric estimation.\n- ``BOLDRigid``: Rigid transformation: Parameters typical for BOLD to BOLD intrasubject registration.\n- ``Affine``: Affine transformation: Rigid + scaling.\n- ``AffineFast``: Fast version of Affine.\n- ``BOLDAffine``: Affine transformation: Parameters typical for BOLD to BOLD intrasubject registration.\n- ``TRSAA``: translation, rigid, similarity, affine (twice). please set regIterations if using this option. this would be used in cases where you want a really high quality affine mapping (perhaps with mask).\n- ``ElasticSyN``: Symmetric normalization: Affine + deformable transformation, with mutual information as optimization metric and elastic regularization.\n- ``SyN``: Symmetric normalization: Affine + deformable transformation, with mutual information as optimization metric.\n- ``SyNRA``: Symmetric normalization: Rigid + Affine + deformable transformation, with mutual information as optimization metric.\n- ``SyNOnly``: Symmetric normalization: no initial transformation, with mutual information as optimization metric. Assumes images are aligned by an inital transformation. Can be useful if you want to run an unmasked affine followed by masked deformable registration.\n- ``SyNCC``: SyN, but with cross-correlation as the metric.\n- ``SyNabp``: SyN optimized for abpBrainExtraction.\n- ``SyNBold``: SyN, but optimized for registrations between BOLD and T1 images.\n- ``SyNBoldAff``: SyN, but optimized for registrations between BOLD and T1 images, with additional affine step.\n- ``SyNAggro``: SyN, but with more aggressive registration (fine-scale matching and more deformation). Takes more time than SyN.\n- ``TVMSQ``: time-varying diffeomorphism with mean square metric\n- ``TVMSQC``: time-varying diffeomorphism with mean square metric for very large deformation\n\n\nSupported ROIs\n**************\n\n- Caudal Anterior Cingulate,\n- Caudal Middle Frontal,\n- Cuneus,\n- Entorhinal,\n- Fusiform,\n- Inferior Parietal,\n- Inferior temporal,\n- Isthmus Cingulate,\n- Lateral Occipital,\n- Lateral Orbitofrontal,\n- Lingual,\n- Medial Orbitofrontal,\n- Middle Temporal,\n- Parahippocampal,\n- Paracentral,\n- Pars Opercularis,\n- Pars Orbitalis,\n- Pars Triangularis,\n- Pericalcarine,\n- Postcentral,\n- Posterior Cingulate,\n- Precentral,\n- Precuneus,\n- Rostral Anterior Cingulate,\n- Rostral Middle Frontal,\n- Superior Frontal,\n- Superior Parietal,\n- Superior Temporal,\n- Supramarginal,\n- Transverse Temporal,\n- Insula,\n- Brainstem,\n- Third Ventricle,\n- Fourth Ventricle,\n- Optic Chiasm,\n- Lateral Ventricle,\n- Inferior Lateral Ventricle,\n- Cerebellum Gray Matter, \n- Cerebellum White Matter,\n- Thalamus,\n- Caudate,\n- Putamen,\n- Pallidum,\n- Hippocampus,\n- Amygdala,\n- Accumbens Area,\n- Ventral Diencephalon,\n- Basal Forebrain,\n- Vermal lobules I-V,\n- Vermal lobules VI-VII,\n- Vermal lobules VIII-X.\n',
    'author': 'Clément POIRET',
    'author_email': 'poiret.clement@outlook.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
