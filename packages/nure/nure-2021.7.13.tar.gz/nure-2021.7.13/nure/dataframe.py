import concurrent.futures
import os
from typing import Dict, List, Union

import numpy as np
import pandas as pd
from pandas.io.parsers import TextFileReader

from .code import LabelCoder

_DEFAULT_N_WORKERS_ = os.cpu_count() or 4


def parallelize_dataframe(dataframe, func,
                          executor: concurrent.futures.Executor = None,
                          n_workers=_DEFAULT_N_WORKERS_, use_process=False):
    # check if exe is provided
    if executor is None:
        if use_process:
            my_executor = concurrent.futures.ProcessPoolExecutor(max_workers=n_workers)
        else:
            my_executor = concurrent.futures.ThreadPoolExecutor(max_workers=n_workers)
    else:
        my_executor = executor

    splits = np.array_split(dataframe, n_workers)
    processed_splits = my_executor.map(func, splits)

    # if is my exe, then shutdown
    if executor is None:
        my_executor.shutdown()

    return pd.concat(processed_splits)


def encode_dataframe(dataframe: pd.DataFrame, columns: Union[List[str], Dict[str, LabelCoder]]):
    if not isinstance(columns, dict):
        columns = {cname: LabelCoder() for cname in columns}

    dataframe = dataframe.assign(**{
        cname: encoder.encode(dataframe[cname].values) for cname, encoder in columns.items()
    })

    return dataframe, columns


def decode_dataframe(dataframe: pd.DataFrame, columns: Dict[str, LabelCoder]):
    dataframe = dataframe.assign(**{
        cname: encoder.decode(dataframe[cname].values) for cname, encoder in columns.items()
    })

    return dataframe


def read_csv_and_encode(filepath, encode_columns: Union[List[str], Dict[str, LabelCoder]], chunksize: int = None, **kargs):
    if chunksize is None:
        dataframe = pd.read_csv(filepath, **kargs)
        dataframe, encode_columns = encode_dataframe(dataframe, encode_columns)
        return dataframe, encode_columns

    dataframe_chunks = []
    with pd.read_csv(filepath, iterator=True, chunksize=chunksize, ** kargs) as reader:
        reader: TextFileReader
        for dataframe in reader:
            dataframe, encode_columns = encode_dataframe(dataframe, encode_columns)
            dataframe_chunks.append(dataframe)

    ignore_index = ('index_col' not in kargs) or (not kargs['index_col'])
    dataframe: pd.DataFrame = pd.concat(dataframe_chunks, ignore_index=ignore_index)
    return dataframe, encode_columns


def decode_and_write_csv(filepath, dataframe: pd.DataFrame, encode_columns: Dict[str, LabelCoder], chunksize: int = None, **kargs):
    if chunksize is None:
        chunksize = len(dataframe)

    dataframe_list = np.array_split(dataframe, range(chunksize, len(dataframe), chunksize))
    dataframe = decode_dataframe(dataframe_list[0], encode_columns)
    dataframe.to_csv(filepath, **kargs)

    for dataframe in dataframe_list[1:]:
        dataframe = decode_dataframe(dataframe, encode_columns)
        dataframe.to_csv(filepath, header=False, mode='a', **kargs)
