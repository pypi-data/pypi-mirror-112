# DPANONYMIZE

`dpanonymize` is a PII removal tool for given data types. It's mainly designed
to work with `lochness` on a PHOENIX structured data, but it also has
functionalities to take separate file and folder with predefined datatype.



TO BE UPDATED

## Contents
1. [Installation](#installation)
2. [How to run](#how_to_run)
3. [Documentation](http://docs.neuroinfo.org/lochness/en/latest/)


## Installation

Just use `pip`

```
pip install dpanonymize
```


For most recent DPACC-lochness

```
pip install git+https://github.com/AMP-SCZ/dpanonymize
```


For debugging

```
cd ~
git clone https://github.com/AMP-SCZ/dpanonymize
pip install -r ~/dpanonymize/requirements.txt

export PATH=${PATH}:~/dpanonymize/scripts  # add to ~/.bashrc
export PYTHONPATH=${PYTHONPATH}:~/dpanonymize  # add to ~/.bashrc
```


## Running test


```
cd dpanonymize/tests
bash dpanonymize_test.sh
```


## How to run

- Execute PII removal from `lochness`(`sync.py`)

- Execute PII removal on a PHOENIX folder
```
# apply PII removal in all datatypes
dpanon.py --phoenix_root /path/to/PHOENIX

# or you can also select which datatype to apply PII removal
dpanon.py --phoenix_root /path/to/PHOENIX --datatype actigraphy
dpanon.py --phoenix_root /path/to/PHOENIX --datatype survey
```

- Execute PII removal on a single file
```
dpanon.py \
    --in_file /path/to/survey/file \
    --out_file /path/to/PII_removed/file \
    --datatype survey
```

- Execute PII removal on a directory where there are multiple files of same data type
    - This applies PII removal on all files under the given directory.
```
dpanon.py \
    --in_dir /path/to/survey/directory \
    --out_dir /path/to/PII_removed/directory \
    --datatype survey
```



## Documentation
