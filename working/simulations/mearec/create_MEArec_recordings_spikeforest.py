#!/usr/bin/env python

import MEArec as mr
from pprint import pprint
from pathlib import Path
from copy import deepcopy
import shutil
import os
import numpy as np
import mlprocessors as mlpr
from mountaintools import client as mt
import mtlogging


@mtlogging.log(root=True)
def main():
    templates_path = 'sha1dir://95dba567b5168bacb480411ca334ffceb96b8c19.2019-06-11.templates'
    recordings_path = 'recordings_out'

    tempgen_tetrode = templates_path + '/templates_tetrode.h5'
    tempgen_neuronexus = templates_path + '/templates_neuronexus.h5'
    tempgen_neuropixels = templates_path + '/templates_neuropixels.h5'
    tempgen_neuronexus_drift = templates_path + '/templates_neuronexus_drift.h5'

    noise_level = [10, 20]
    duration = 20  # change this to 600
    bursting = [False, True]
    nrec = 2
    ei_ratio = 0.8
    rec_dict = {
        'tetrode': {
            'ncells': [10, 20], 'tempgen': tempgen_tetrode, 'drifting': False
        },
        'neuronexus': {
            'ncells': [10, 20, 40], 'tempgen': tempgen_neuronexus, 'drifting': False
        },
        'neuropixels': {
            'ncells': [20, 40, 60], 'tempgen': tempgen_neuropixels, 'drifting': False
        },
        'neuronexus_drift': {
            'ncells': [10, 20, 40], 'tempgen': tempgen_neuronexus_drift, 'drifting': True
        }
    }

    # optional: if drifting change drift velocity
    # recording_params['recordings']['drift_velocity] = ...

    # Generate and save recordings
    if os.path.exists(recordings_path):
        shutil.rmtree(recordings_path)
    os.mkdir(recordings_path)

    SJH = mlpr.SlurmJobHandler(working_dir='tmp1')
    with mlpr.JobQueue(job_handler=SJH):
        for rec_type in rec_dict.keys():
            study_set_name = 'synth_mearec_{}'.format(rec_type)
            os.mkdir(recordings_path + '/' + study_set_name)
            params = dict()
            params['duration'] = duration
            params['drifting'] = rec_dict[rec_type]['drifting']
            # reduce minimum distance for dense recordings
            params['min_dist'] = 15
            for ncells in rec_dict[rec_type]['ncells']:
                # changing number of cells
                n_exc = int(ei_ratio * 10)   # intentionally replaced nrec by 10 here
                params['n_exc'] = n_exc
                params['n_inh'] = ncells - n_exc
                for n in noise_level:
                    # changing noise level
                    params['noise_level'] = n
                    for b in bursting:
                        bursting_str = ''
                        if b:
                            bursting_str = '_bursting'
                        study_name = 'synth_mearec_{}_noise{}_K{}{}'.format(rec_type, n, ncells, bursting_str)
                        os.mkdir(recordings_path + '/' + study_set_name + '/' + study_name)
                        for i in range(nrec):
                            # set random seeds
                            params['seed'] = i  # intentionally doing it this way

                            # changing bursting and shape modulation
                            print('Generating', rec_type, 'recording with', ncells, 'noise level', n, 'bursting', b)
                            params['bursting'] = b
                            params['shape_mod'] = b
                            result0 = GenerateMearecRecording.execute(**params, templates_in=rec_dict[rec_type]['tempgen'], recording_out=dict(ext='.h5'))
                            out_fname = recordings_path + '/' + study_set_name + '/' + study_name + '/' + '{}.h5'.format(i)
                            print('Writing {}'.format(out_fname))
                            mt.realizeFile(path=result0.outputs['recording_out'], dest_path=out_fname)


class GenerateMearecRecording(mlpr.Processor):
    # input file
    templates_in = mlpr.Input(description='.h5 file containing templates')

    # output file
    recording_out = mlpr.Output()

    # recordings params
    drifting = mlpr.BoolParameter()
    noise_level = mlpr.FloatParameter()
    bursting = mlpr.BoolParameter()
    shape_mod = mlpr.BoolParameter()

    # spiketrains params
    duration = mlpr.FloatParameter()
    n_exc = mlpr.IntegerParameter()
    n_inh = mlpr.IntegerParameter()

    # templates params
    min_dist = mlpr.FloatParameter()

    # seed
    seed = mlpr.IntegerParameter()

    def run(self):
        recordings_params = deepcopy(mr.get_default_recordings_params())

        recordings_params['recordings']['drifting'] = self.drifting
        recordings_params['recordings']['noise_level'] = self.noise_level
        recordings_params['recordings']['bursting'] = self.bursting
        recordings_params['recordings']['shape_mod'] = self.shape_mod
        recordings_params['recordings']['seed'] = self.seed

        recordings_params['spiketrains']['duration'] = self.duration
        recordings_params['spiketrains']['n_exc'] = self.n_exc
        recordings_params['spiketrains']['n_inh'] = self.n_inh
        recordings_params['spiketrains']['seed'] = self.seed

        recordings_params['templates']['min_dist'] = self.min_dist
        recordings_params['templates']['seed'] = self.seed

        # this is needed because mr.load_templates requires the file extension
        templates_fname = self.templates_in + '.h5'
        shutil.copyfile(self.templates_in, templates_fname)
        tempgen = mr.load_templates(Path(templates_fname))

        recgen = mr.gen_recordings(params=recordings_params, tempgen=tempgen, verbose=False)
        mr.save_recording_generator(recgen, self.recording_out)
        del recgen

if __name__ == "__main__":
    main()
