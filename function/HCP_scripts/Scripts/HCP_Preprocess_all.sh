#!/bin/bash
sub="$1" 
wd="/mnt/d/HCPPipeline/HCP_analysis/DLH/Pre/Images"

# Freesurfer
./PreFreeSurferPipelineBatch.sh --runlocal --Subject=${sub} --StudyFolder=${wd}
./FreeSurferPipelineBatch.sh --runlocal --Subject=${sub} --StudyFolder=${wd}
./PostFreeSurferPipelineBatch.sh --runlocal --Subject=${sub} --StudyFolder=${wd}
cp -r "../Images/${sub}" "../Images/${sub}_after_PostFS"

# fMRI+FIX
./GenericfMRIVolumeProcessingPipelineBatch.sh --runlocal --Subject=${sub} --StudyFolder=${wd}
./GenericfMRISurfaceProcessingPipelineBatch.sh --runlocal --Subject=${sub} --StudyFolder=${wd}
./IcaFixProcessingBatch.sh --runlocal --Subject=${sub} --StudyFolder=${wd}
./PostFixBatch.sh --runlocal --Subjlist=${sub} --StudyFolder=${wd}
cp -r "../Images/${sub}" "../Images/${sub}_after_PostFix"

# MSM+reFIX
./MSMAllPipelineBatch.sh --runlocal --Subjlist=${sub} --StudyFolder=${wd}
./DeDriftAndResamplePipelineBatch.sh --runlocal --Subjlist=${sub} --StudyFolder=${wd}
cp -r "../Images/${sub}" "../Images/${sub}_after_DeDrift"