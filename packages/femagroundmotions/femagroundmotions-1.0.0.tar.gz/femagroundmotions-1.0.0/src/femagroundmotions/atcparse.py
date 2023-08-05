from pathlib import Path

import numpy as np
import pandas as pd


def parse_nearfield_filename(filename):
    path = Path(filename)
    eq_id = path.name.split('_')[1][1:1 + 7]
    rsn = int(eq_id[2:2 + 4])
    comp = int(eq_id[-1])
    return eq_id, rsn, comp


def load_metadata(filename, sheet) -> pd.DataFrame:
    md = pd.read_excel(filename, sheet, index_col='ID')
    return md


def empty_ground_motions(records: pd.DataFrame):
    gm_a = _empty_half_ground_motions(records, 'A')
    gm_b = _empty_half_ground_motions(records, 'B')
    gm = pd.concat([gm_a, gm_b],
                   keys=['a', 'b'],
                   names=['ComponentID', 'RecordID'])
    # Reorder and resort because ComponentID gets added to the outside
    gm = gm.reorder_levels(['RecordID', 'ComponentID']).sort_index()

    return gm


def _empty_half_ground_motions(records: pd.DataFrame, component: str):
    gm = pd.DataFrame(
        columns=[
            'RecordSequenceNumber',
            'ComponentName',
            'NumPoints',
            'DT',
            'Time',
            'RecordedAcceleration',
            'NormalizationFactor',
            'NormalizedAcceleration',
        ],
        index=records.index,
    )
    gm['RecordSequenceNumber'] = records['RecordSequenceNumber']
    gm['NormalizationFactor'] = records['NormalizationFactor']
    gm['ComponentName'] = records[f'Component{component}'].astype(str)
    return gm


class AtcParser():
    def __init__(self, directory):
        self.directory = Path(directory).resolve()
        self.metafile = self.directory / 'atcmetadata.xlsx'

    def load_metadata(self, dataset):
        return load_metadata(self.metafile, dataset)

    def _load_nearfield_timeseries(self, gm_row):
        """
        Parameters
        ----------
        gm_row : tuple
            tuple from empty_ground_motions().itertuples()
        """
        gmdir = self.directory / 'nearfield'

        rsn = gm_row.RecordSequenceNumber
        alpha_comp = gm_row.Index[1]
        comp = 1 if alpha_comp == 'a' else 2
        eq_id = f'82{rsn:04d}{comp}'

        with open(gmdir / f'DtFile_({eq_id}).txt') as f:
            dt = float(f.read().strip())
        with open(gmdir / f'NumPointsFile_({eq_id}).txt') as f:
            npts = int(f.read().strip())
        data = np.loadtxt(gmdir / f'SortedEQFile_({eq_id}).txt')

        return dt, npts, data

    def _load_farfield_timeseries(self, gm_row):
        """
        Parameters
        ----------
        gm_row : tuple
            tuple from empty_ground_motions().itertuples()
        """
        gmdir = self.directory / 'farfield'

        recID = gm_row.Index[0]
        compID = gm_row.Index[1]
        tsID = f'{recID:02d}{compID}'

        with open(gmdir / f'{tsID}_dt.txt') as f:
            dt = float(f.read().strip())
        with open(gmdir / f'{tsID}_npts.txt') as f:
            npts = int(f.read().strip())
        data = np.loadtxt(gmdir / f'{tsID}_acc.txt')

        return dt, npts, data

    def build(self, dataset):
        load_ts_dispatch = {
            'farfield': self._load_farfield_timeseries,
            'nearfield_pulse': self._load_nearfield_timeseries,
            'nearfield_no_pulse': self._load_nearfield_timeseries,
        }

        records = self.load_metadata(dataset)
        load_timeseries = load_ts_dispatch[dataset]
        groundmotions = empty_ground_motions(records)

        for gm in groundmotions.itertuples():
            dt, npts, data = load_timeseries(gm)
            groundmotions.at[gm.Index, 'DT'] = dt
            groundmotions.at[gm.Index, 'NumPoints'] = npts
            groundmotions.at[gm.Index, 'Time'] = np.arange(npts) * dt
            groundmotions.at[gm.Index, 'RecordedAcceleration'] = data
            NF = gm.NormalizationFactor
            groundmotions.at[gm.Index, 'NormalizedAcceleration'] = NF * data

        groundmotions = groundmotions.infer_objects()

        # h5file = self.directory / f'{dataset}.hdf5'
        # records.to_hdf(h5file, 'records', mode='w')
        # groundmotions.to_hdf(h5file, 'groundmotions', mode='a')
        return records, groundmotions
