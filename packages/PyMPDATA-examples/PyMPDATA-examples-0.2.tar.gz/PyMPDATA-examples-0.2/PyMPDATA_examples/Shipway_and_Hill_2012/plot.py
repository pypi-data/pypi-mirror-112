from .formulae import convert_to, si
import numpy as np
from matplotlib import pyplot


def plot(var, mult, label, output, range=None, threshold=None, cmap='copper', rasterized=False, figsize=None):
    lines = {3: ':', 6: '--', 9: '-', 12: '-.'}

    dt = output['t'][1] - output['t'][0]
    dz = output['z'][1] - output['z'][0]
    tgrid = np.concatenate(((output['t'][0] - dt / 2,), output['t'] + dt / 2))
    zgrid = np.concatenate(((output['z'][0] - dz / 2,), output['z'] + dz / 2))
    convert_to(zgrid, si.km)

    fig = pyplot.figure(constrained_layout=True, figsize=figsize)
    gs = fig.add_gridspec(25, 5)
    ax1 = fig.add_subplot(gs[:-1, 0:3])
    data = output[var]*mult
    if threshold is not None:
        data[data < threshold] = np.nan
    mesh = ax1.pcolormesh(tgrid, zgrid,
                          data,
                          cmap=cmap, rasterized=rasterized,
                          vmin=None if range is None else range[0],
                          vmax=None if range is None else range[1]
    )

    ax1.set_xlabel('time [s]')
    ax1.set_xticks([k * si.minutes for k in lines.keys()])
    ax1.set_ylabel('z [km]')
    ax1.grid()

    cbar = fig.colorbar(mesh, fraction=.05, location='top')
    cbar.set_label(label)

    ax2 = fig.add_subplot(gs[:-1, 3:], sharey=ax1)
    ax2.set_xlabel(label)
    ax2.grid()
    if range is not None:
        ax2.set_xlim(range)

    last_t = -1
    for i, t in enumerate(output['t']):
        x, z = output[var][:, i]*mult, output['z'].copy()
        convert_to(z, si.km)
        params = {'color': 'black'}
        for line_t, line_s in lines.items():
            if last_t < line_t * si.minutes <= t:
                params['ls'] = line_s
                ax2.plot(x, z, **params)
                ax1.axvline(t, **params)
        last_t = t

