import setuptools

pkg_name = "spikeforest2"

setuptools.setup(
    name=pkg_name,
    version="0.1.0",
    author="Jeremy Magland",
    author_email="jmagland@flatironinstitute.org",
    description="Spike sorting validation and comparison system",
    url="https://github.com/magland/spikeforest2",
    packages=[
        'vdomr',
        'spikeforest_batch_run',
        'spikeextractors','spikewidgets','spiketoolkit',
        'mlprocessors',
        'kbucket','pairio','fasteners',
        'spikeforest',
        'pillow','pandas','h5py','scipy'
    ],
    install_requires=[
        'numpy',
        'matplotlib',
        'requests'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    )
)