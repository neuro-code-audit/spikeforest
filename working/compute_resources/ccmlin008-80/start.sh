#!/bin/bash
set -e

module load matlab

export MLPROCESSORS_FORCE_RUN=FALSE

export NUM_WORKERS=2
export MKL_NUM_THREADS=$NUM_WORKERS
export NUMEXPR_NUM_THREADS=$NUM_WORKERS
export OMP_NUM_THREADS=$NUM_WORKERS

export DISPLAY=""
RESOURCE_NAME=${1:-ccmlin008-80}
COLLECTION=spikeforest
KACHERY_NAME=kbucket

compute-resource-start $RESOURCE_NAME \
	--allow_uncontainerized  \
	--collection $COLLECTION --kachery_name $KACHERY_NAME \
        --srun_opts "-c 2 -n 80 -p ccm"

#compute-resource-start ccmlin008-80 \
#	--allow_uncontainerized  \
#	--collection $COLLECTION --kachery_name $KACHERY_NAME \
#        --parallel 1

