"""Ground motions in HDF5 format, with BLOSC compression.

File structure:

    records/
        <tabular data>
    groundmotions/
        <tabular data>
    _timeseries/
        <recordID>/<component>/Time
        <recordID>/<component>/RecordedAcceleration
        <recordID>/<component>/NormalizedAcceleration
"""
import typing as t

import h5py
import hdf5plugin
import pandas as pd

__all__ = [
    'from_hdf5',
    'to_hdf5',
]


def to_hdf5(filename, records: pd.DataFrame, groundmotions: pd.DataFrame):
    tableopts = dict(complib='blosc', complevel=9, format='table')

    records.to_hdf(filename, 'records', mode='w', **tableopts)

    #--------------------------------------------
    # Modify groundmotions so pytables is happy
    #--------------------------------------------
    gm = groundmotions.copy()
    timeseries = pd.DataFrame(
        {
            'Time': gm.pop('Time'),
            'RecordedAcceleration': gm.pop('RecordedAcceleration'),
            'NormalizedAcceleration': gm.pop('NormalizedAcceleration'),
        },
        index=gm.index,
    )
    gm.to_hdf(filename, 'groundmotions', mode='a', **tableopts)

    #------------------------------------------
    # Store the time series-es elsewhere
    #------------------------------------------
    compression = hdf5plugin.Blosc(clevel=9)
    with h5py.File(filename, mode='a') as h5:
        ts_group = h5.create_group('_timeseries')
        for ts in timeseries.itertuples():
            recID = ts.Index[0]
            compID = ts.Index[1]

            def create_dataset(name, data):
                ts_group.create_dataset(f'{recID}/{compID}/{name}',
                                        data=data,
                                        **compression)

            create_dataset('Time', ts.Time)
            create_dataset('RecordedAcceleration', ts.RecordedAcceleration)
            create_dataset('NormalizedAcceleration', ts.NormalizedAcceleration)


def from_hdf5(filename) -> t.Tuple[pd.DataFrame, pd.DataFrame]:
    records = pd.read_hdf(filename, 'records')
    groundmotions = pd.read_hdf(filename, 'groundmotions')

    timeseries = pd.DataFrame(
        columns=['Time', 'RecordedAcceleration', 'NormalizedAcceleration'],
        index=groundmotions.index,
    )
    with h5py.File(filename) as h5:
        for recID, compID in groundmotions.index:
            group = h5['_timeseries'][str(recID)][compID]
            timeseries.loc[(recID, compID), 'Time'] = group['Time'][()]
            timeseries.loc[
                (recID, compID),
                'RecordedAcceleration'] = group['RecordedAcceleration'][()]
            timeseries.loc[
                (recID, compID),
                'NormalizedAcceleration'] = group['NormalizedAcceleration'][()]

    groundmotions = pd.concat([groundmotions, timeseries], axis='columns')

    return records, groundmotions
