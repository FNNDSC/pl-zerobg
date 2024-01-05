#!/usr/bin/env python
import os
import shutil
import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from typing import Callable

import numpy as np
import nibabel as nib

from tqdm.contrib.concurrent import process_map, thread_map

from chris_plugin import chris_plugin, PathMapper, helpers

__version__ = '1.0.0'

DISPLAY_TITLE = r"""
       _                          _           
      | |                        | |          
 _ __ | |______ _______ _ __ ___ | |__   __ _ 
| '_ \| |______|_  / _ \ '__/ _ \| '_ \ / _` |
| |_) | |       / /  __/ | | (_) | |_) | (_| |
| .__/|_|      /___\___|_|  \___/|_.__/ \__, |
| |                                      __/ |
|_|                                     |___/ 
"""


parser = ArgumentParser(description='Set the background intensity of MRI volumes to zero.',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-t', '--thresholds', required=False, type=str,
                    default='.nii.gz:37.0',
                    help='A filename glob and background intensity threshold. Multiple pairs should be comma-separated,'
                         ' i.e. GLOB1:THRESHOLD1,GLOB2:THRESHOLD2,...')
parser.add_argument('-J', '--threads', type=int, default=0,
                    help='Number of threads to use for parallel jobs. '
                         'Pass 0 to use number of visible CPUs.')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')


@chris_plugin(
    parser=parser,
    title='Zero MRI Background',
    category='MRI',              # ref. https://chrisstore.co/plugins
    min_memory_limit='4Gi',      # supported units: Mi, Gi
    min_cpu_limit='4000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE, flush=True)

    mapper = PathMapper.file_mapper(inputdir, outputdir)
    nproc = options.threads if options.threads else len(os.sched_getaffinity(0))
    threshold_map = {k: float(v) for k, v in helpers.parse_csv_as_dict(options.thresholds).items()}
    results = thread_map(curry_zerobg(threshold_map), mapper, max_workers=nproc, total=mapper.count(), maxinterval=0.1)

    # raise exceptions, if any
    for _ in results:
        pass


def curry_zerobg(threshold_map: dict[str, float]) -> Callable[[tuple[Path, Path]], bool]:
    return lambda t: zerobg(t[0], t[1], threshold_map)


def zerobg(input: Path, output: Path, threshold_map: dict[str, float]) -> bool:
    threshold = next((v for k, v in threshold_map.items() if input.name.endswith(k)), None)
    if threshold is None:
        shutil.copy(input, output)
        return True

    vol = nib.load(input)
    data = vol.get_fdata()
    result = np.where(data <= threshold, 0, data)
    output_vol = vol.__class__(result, vol.affine, header=vol.header)
    nib.save(output_vol, output)


if __name__ == '__main__':
    main()
