#!python

from pathlib import Path
import argparse as ap
import sys
from typing import Union, List
from dpanonymize import dtype_module_dict
import dpanonymize as dpanon

'''
dpanonymize is designed to be executed from lochness, but this simple shell
executable script is added to use PII removal functionalities of dpanonymize
from shell.
'''

def lock_file(in_file: Union[Path, str],
              out_file: Union[Path, str],
              datatype: str) -> None:
    '''Remove PII using information from a file

    Requirements:
        - in_file: input file path, Path or str
        - out_file: path to save the PII removed file, Path or str
        - datatype: datatype that this in_file belongs to, str
            - 'survey', 'video', 'audio', 'actigraphy', 'mri', 'eeg'
    '''
    module = dtype_module_dict.get(datatype)
    module.remove_pii(in_file, out_file)


def lock_directory(in_dir: Union[Path, str],
                   out_dir: Union[Path, str],
                   datatype: str) -> None:
    '''Remove PII from all files under a directory

    Requirements:
        - in_file: input directory path, Path or str
        - out_file: directory to save the PII removed file, Path or str
        - datatype: datatype that all of the files belongs to, str
            - 'survey', 'video', 'audio', 'actigraphy', 'mri', 'eeg'
    '''
    module = dtype_module_dict.get(datatype)

    for in_file in Path(in_dir).glob('*'):
        if in_file.is_file():
            out_file = Path(out_dir) / in_file.name
            module.remove_pii(in_file, out_file)


def parse_args(argv):
    '''Parse inputs coming from the terminal'''
    parser = ap.ArgumentParser(description='dpanonymize: PII remover')

    parser.add_argument('-p', '--phoenix_root',
                        type=str,
                        help='Root of PHOENIX directory. If this option is '
                             'given, -i, -o, -d, -od are ignored')
    parser.add_argument('-b', '--bids', action='store_true',
                        help='Option to use if the PHOENIX is in BIDS')
    parser.add_argument('-i', '--in_file', help='A file to remove PII from')
    parser.add_argument('-o', '--out_file',
                        help='PII removed output file path')
    parser.add_argument('-d', '--in_dir',
                        help='A directory to remove PII from')
    parser.add_argument('-od', '--out_dir',
                        help='PII removed output dir path')
    parser.add_argument('-dt', '--datatype',
                        help='Datatype to remove PII (applies to -p, -i).')

    args = parser.parse_args(argv)

    if args.in_file and args.datatype is None:
        parser.error('--in_file and --datatype always appear together')

    if args.in_dir and args.datatype is None:
        parser.error('--in_file and --datatype always appear together')
    
    return args


def dpanonymize(args):
    if args.phoenix_root:
        in_dict = {'phoenix_root': args.phoenix_root, 'BIDS': args.bids}
        dpanon.lock_lochness(in_dict, args.datatype)

    else:
        if args.in_file:
            lock_file(args.in_file, args.out_file, args.datatype)

        if args.in_dir:
            lock_directory(args.in_dir, args.out_dir, args.datatype)


if __name__ == '__main__':
    parser, args = parse_args(sys.argv[1:])
    dpanonymize(args)
