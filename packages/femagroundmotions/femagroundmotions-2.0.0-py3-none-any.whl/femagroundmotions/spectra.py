"""Calculate response spectra for the ground motions using OpenSees."""
import dataclasses
import importlib.resources
import multiprocessing as mp
from datetime import datetime

import numpy as np
import pandas as pd
import opswrapper as ops
import xarray as xr


@dataclasses.dataclass
class ResponseSpectrumBuilder(ops.analysis.OpenSeesAnalysis):
    """
    Parameters
    ----------
    ground_motions : pd.DataFrame
        Dataframe the contains the parsed ground motions.
    T : array_like
        1-d array of periods in seconds
    m : float, optional
        Mass of the structure in kg (default: 1.0)
    z : float, optional
        Percent of critical damping to apply (default: 0.05)
    Fy : float, optional
        Yield strength of the structure (default: inf)
    a : float, optional
        Strain-hardening factor (default: 0.01)
    """
    ground_motions: pd.DataFrame
    T: np.ndarray
    m: float = 1.0
    z: float = 0.05
    Fy: float = float('inf')
    a: float = 0.01

    def __post_init__(self):
        self.T = np.atleast_1d(self.T)
        if self.T.ndim != 1:
            raise ValueError('T must be interpretable as a 1-d array')

        super().__init__()

    #-------------------------------------------------
    # Units
    #-------------------------------------------------
    u_time = 's'
    u_disp = 'm'
    u_accel = 'm/s^2'
    u_force = 'N'
    g0 = 9.80665

    #-------------------------------------------------
    # Analyses
    #-------------------------------------------------
    def run_analysis(self, record, component, echo=None):
        """Generate response spectrum for a specific ground motion.
        
        Parameters
        ----------
        record : int
            The record ID to select
        component : {'a', 'b'}
            Which direction component to select
        echo : bool, optional
            Whether to echo OpenSees output to the console. If None, fall back
            to the `echo_output` setting (default: None)
        """
        scratch_file = self.create_scratch_filer()
        files = {
            'input': scratch_file('input.tcl'),
            'output': scratch_file('output.dat'),
            'gm': scratch_file('gm.acc'),
        }

        # Loading
        gm = self.ground_motions.loc[record, component]

        # Generate script
        template = importlib.resources.read_text(
            'femagroundmotions', 'sdof-response-spectrum.tcl.in')
        periods = [format(_T, 'g') for _T in self.T]
        script = template % {
            # Header
            'timestamp': datetime.now().ctime(),
            'units.force': self.u_force,
            'units.length': self.u_disp,
            'units.time': self.u_time,

            # Ground motions
            'gm.dt': gm.DT / 2,
            'gm.file': files['gm'].as_posix(),

            # Structure
            'm': self.m,
            'z': self.z,
            'Fy': self.Fy,
            'a': self.a,
            'periods': ops.utils.tcllist(periods),

            # Output
            'file.output': files['output'].as_posix(),
        }

        # Write inputs and run analysis
        accel = subdivide(gm.RecordedAcceleration, 1)
        np.savetxt(files['gm'], accel * self.m * self.g0)

        with open(files['input'], 'w') as f:
            f.write(script)

        process = self.run_opensees(files['input'], echo=echo)
        if process.returncode != 1:
            raise RuntimeError('OpenSees exited unexpectedly.')

        # Read results
        data = np.loadtxt(files['output'], ndmin=2)
        umax = data[:, 0]
        u = data[:, 1]
        up = data[:, 2]
        amax = data[:, 3]
        tamax = data[:, 4]

        if self.delete_files:
            for path in files.values():
                path.unlink(missing_ok=True)

        ωn = 2 * np.pi / self.T
        pa = umax * ωn**2 / self.g0

        results = xr.Dataset(
            data_vars={
                'disp_max': ('period', umax),
                'disp_final': ('period', u),
                'disp_resid': ('period', up),
                'accel_max': ('period', amax),
                'accel_max_time': ('period', tamax),
                'pseudo_accel': ('period', pa),
            },
            coords={
                'period': self.T,
                'record': record,
                'component': component,
            },
        )

        results.period.attrs['units'] = self.u_time
        results.disp_max.attrs['units'] = self.u_disp
        results.disp_final.attrs['units'] = self.u_disp
        results.disp_resid.attrs['units'] = self.u_disp
        results.accel_max.attrs['units'] = self.u_accel
        results.accel_max_time.attrs['units'] = self.u_time
        results.pseudo_accel.attrs['units'] = 'g0'

        return results.expand_dims(['record', 'component'])

    def run_all(self, parallel=False, num_cpus=4, echo=None):
        """Generate response spectra for all the ground motions.

        Parameters
        ----------
        parallel : bool, optional
            Whether to run analyses in parallel using the multiprocessing
            module (default: False)
        num_cpus : int, optional
            How many processes to use in the multiprocessing Pool if `parallel`
            is True (default: 4)
        echo : bool, optional
            Whether to echo OpenSees output to the console. If None, fall back
            to the `echo_output` setting (default: None)
        """
        if parallel:
            with mp.Pool(num_cpus) as p:
                results = p.starmap(self.run_analysis,
                                    self.ground_motions.index)
        else:
            results = []
            for record, component in self.ground_motions.index:
                results.append(self.run_analysis(record, component, echo=echo))

        results = xr.merge(results, combine_attrs='drop_conflicts')
        return results


def subdivide(a, n):
    a = np.asanyarray(a)
    if a.ndim != 1:
        raise ValueError('subdivide only works on 1d arrays')
    xp = np.arange(a.size)
    yp = a
    x = np.linspace(0, xp[-1], a.size * (n + 1) - n)
    return np.interp(x, xp, yp)
