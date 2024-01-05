#!/usr/bin/env python

from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from tqdm.contrib.concurrent import process_map

from chris_plugin import chris_plugin, PathMapper

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
parser.add_argument('-t', '--threshold', required=False, type=str,
                    default='.nii.gz:37',
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
    category='',                 # ref. https://chrisstore.co/plugins
    min_memory_limit='1Gi',      # supported units: Mi, Gi
    min_cpu_limit='1000m',       # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0              # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE, flush=True)

    mapper = PathMapper.file_mapper(inputdir, outputdir, glob=options.pattern, suffix='.count.txt')
    for input_file, output_file in mapper:
        # The code block below is a small and easy example of how to use a ``PathMapper``.
        # It is recommended that you put your functionality in a helper function, so that
        # it is more legible and can be unit tested.
        data = input_file.read_text()
        frequency = data.count(options.word)
        output_file.write_text(str(frequency))


if __name__ == '__main__':
    main()
