#!/bin/bash
set -e

export NUM_WORKERS=2
export MKL_NUM_THREADS=$NUM_WORKERS
export NUMEXPR_NUM_THREADS=$NUM_WORKERS
export OMP_NUM_THREADS=$NUM_WORKERS

export DISPLAY=""

COLLECTION=spikeforest
SHARE_ID=69432e9201d0

../../../bin/compute-resource-start ccmlin008-test \
	--allow_uncontainerized --parallel 4  \
	--collection $COLLECTION --share_id $SHARE_ID