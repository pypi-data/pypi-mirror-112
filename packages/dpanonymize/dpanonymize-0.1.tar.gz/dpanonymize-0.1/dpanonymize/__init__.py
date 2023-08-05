
from pathlib import Path
import os
import re
from typing import Union, List
import dpanonymize.survey as SURVEY
import dpanonymize.actigraphy as ACTIGRAPHY
import dpanonymize.mri as MRI
import dpanonymize.video as VIDEO
import dpanonymize.audio as AUDIO


dtype_module_dict = {
    'survey': SURVEY,
    'actigraphy': ACTIGRAPHY,
    'mri': MRI,
    'interviews': VIDEO,
    'audio': AUDIO,
    'video': VIDEO
}


class FileInPhoenixBIDS(object):
    '''PHOENIX file class used to grab file information'''
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.subject = self.file_path.parent.name
        self.dtype = self.file_path.parent.parent.parent.name
        self.study = self.file_path.parent.parent.parent.parent.name
        self.general_path = re.sub('/PROTECTED/', '/GENERAL/',
                                   str(self.file_path))

    def anonymize(self) -> None:
        '''Remove PII from the fileInPhoenix object

        Key arguments:
            - self: It should have following attributes
                - self.file_path: path of the file, Path.
                - self.dtype: type of the data, str.
                - self.general_path: path of the target GENERAL path, Path.
                eg) self.file_path = 'PATH/PROTECTED/PATH/TO/FILE'
                    self.dtype = 'survey'
                    fileInPhoenix.general_path = 'PATH/GENERAL/PATH/TO/FILE'
        '''
        print(self.dtype)
        module = dtype_module_dict.get(self.dtype)
        module.remove_pii(self.file_path, self.general_path)

    def __repr__(self):
        return f"<{self.file_path.name}>"


class FileInPhoenix(FileInPhoenixBIDS):
    '''NON-BIDS PHOENIX file class used to grab file information'''
    def __init__(self, file_path):
        super().__init__(file_path)
        self.dtype = self.file_path.parent.parent.name
        self.subject = self.file_path.parent.parent.name


def get_file_objects_from_phoenix(root_dir: Union[Path, str],
                                  BIDS: bool) -> List[FileInPhoenix]:
    '''Search all files under phoenix and get a list of FileInPhoenix objects

    Key Arguments
        - root_dir: root of PHOENIX directory structure to search files
                          from, Path or str.
        - BIDS: True if the PHOENIX is in BIDS structure, bool.
    '''
    protected_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            full_path = Path(root) / file
            if BIDS:
                protected_files.append(FileInPhoenixBIDS(full_path))
            else:
                protected_files.append(FileInPhoenix(full_path))

    return protected_files


def get_file_objects_from_module(root_dir: Union[Path, str],
                                 module: str,
                                 BIDS: bool) -> List[FileInPhoenix]:
    '''Search all files under phoenix and get a list of FileInPhoenix objects

    Key Arguments:
        - root_dir: root of PHOENIX directory structure to search files
                          from, Path or str.
        - module: name of the module to remove PII from, str.
        - BIDS: True if the PHOENIX is in BIDS structure, bool.
    '''
    module_dirs = list(root_dir.glob(f'*/{module}')) if BIDS else \
        list(root_dir.glob(f'*/*/{module}'))

    protected_files = []
    for module_dir in module_dirs:
        protected_files += get_file_objects_from_phoenix(module_dir, BIDS)

    return protected_files


def lock_lochness(Lochness: 'Lochness', module: str = None) -> None:
    '''Lock PII using information from Lochness object

    Requirements:
        - Lochness: Lochness object from lochness.config.load
                    It needs to have 'phoenix_root' (str) and 'BIDS' (bool).
                    eg) Lochness['phoenix_root'] = '/PATH/TO/PHOENIX'
                        Lochness['BIDS'] = True
    '''
    phoenix_root = Path(Lochness['phoenix_root'])
    protected_root = phoenix_root / 'PROTECTED'
    bids = Lochness['BIDS'] if 'BIDS' in Lochness else False

    file_object_list = get_file_objects_from_phoenix(protected_root, bids) \
        if module is None else \
        get_file_objects_from_module(protected_root, module, bids)

    for file_object in file_object_list:
        file_object.anonymize()


