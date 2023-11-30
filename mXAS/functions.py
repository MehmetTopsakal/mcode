import os, sys, datetime
import glob, linecache, shutil
import numpy as np
import xarray as xr

from larch.io import read_ascii, read_athena
from larch.xafs import find_e0, pre_edge, autobk, xftf
from larch import Group
import larch

from copy import deepcopy
from datatree import DataTree


def get_fl(pattern, mode=["ISS"]):
    """
    This function searches files in a directory and sorts by experiment start time
    """

    fl_in = []
    fl = sorted(glob.glob(pattern))

    for e, f in enumerate(fl):
        try:
            if mode[0] == "ISS":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[2], l.split()[3]), "%m/%d/%Y_%H:%M:%S"
                )
            if mode[0] == "ISS_old":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[3], l.split()[4]), "%m/%d/%Y_%H:%M:%S"
                )
            elif mode[0] == "ISS_2021_3":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[2], l.split()[3]), "%m/%d/%Y_%H:%M:%S"
                )
            elif mode[0] == "QAS":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[3], l.split()[4]), "%m/%d/%Y_%H:%M:%S"
                )
            elif mode[0] == "BMM":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    l, "# Scan.start_time: %Y-%m-%dT%H:%M:%S\n"
                )
            elif mode[0] == "12BM":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(l, "#D %a %b %d %H:%M:%S %Y \n")
            elif mode[0] == "20ID":
                l = linecache.getline(f, mode[1]).split()
                dt = datetime.datetime.strptime(
                    "%s_%s_%s" % (l[9], l[10], l[11][0:2]), "%m/%d/%Y_%I:%M:%S_%p"
                )

            fl_in.append([dt.timestamp(), dt, f])

        except Exception as exc:
            print(exc)
            print("Unable to read %s" % (f))

    # sort by timestamp
    fl_in.sort(key=lambda x: x[0])
    fl_out = [[i[1].isoformat(), i[2]] for e, i in enumerate(fl_in)]

    return fl_out


def read_as_ds(
    fl_in,
    mode="ISS",
    sdd_cols=[9, 9 + 4, 9 + 4 + 4, 9 + 4 + 4 + 4],
    Eshift=0,
    imin=0,
    imax=-1,
    plot=True,
    legend=False,
    plot_ref=True,
    plot_fluo=True,
    xlim=None,
    cut=0,
):
    Es = []
    MUs_f = []
    MUs_r = []

    d0 = np.loadtxt(fl_in[0][1], unpack=True)

    read_data = []
    for i in fl_in:
        d = np.loadtxt(i[1], unpack=True)
        if mode == "ISS":
            MUs_f.append(d[4] / d[1])
            MUs_r.append(-np.log(d[3] / d[2]))
            Es.append(d[0])
        elif mode == "ISS_SDD":
            MUs_f.append(
                -(d[sdd_cols[0]] + d[sdd_cols[1]] + d[sdd_cols[2]] + d[sdd_cols[3]])
                / d[1]
            )
            MUs_r.append(-np.log(d[3] / d[2]))
            Es.append(d[0])
        elif mode == "QAS":
            # MUs_f.append(d[1]/d[2])
            # MUs_r.append(np.log(d[1]/d[3]))
            MUs_f.append(d[4] / d[1])
            MUs_r.append(-np.log(d[2] / d[1]))
            Es.append(d[0])
        elif mode == "BMM":
            MUs_f.append(d[3])
            # MUs_r.append(-np.log(d[6]/d[4]))
            MUs_r.append(-np.log(d[6] / d[5]))
            Es.append(d[0])
        elif mode == "12BM":
            MUs_f.append(d[9] / d[2])
            MUs_r.append(d[7] / d[2])
            Es.append(d[0])
        elif mode == "20ID_98":
            MUs_f.append(d[9] / d[8])
            # MUs_r.append(d[9]/d[8]) #for compatibility issues
            Es.append(d[0])
        elif mode == "20ID_186":
            MUs_f.append(d[18] / d[6])
            # MUs_r.append(d[18]/d[6]) #for compatibility issues
            Es.append(d[0])
        elif mode == "20ID_128":
            MUs_f.append(d[12] / d[8])
            # MUs_r.append(d[12]/d[8]) #for compatibility issues
            Es.append(d[0])
        elif mode == "20ID_108":
            MUs_f.append(d[10] / d[8])
            # MUs_r.append(d[10]/d[8]) #for compatibility issues
            Es.append(d[0])
        elif mode == "20ID_65ref":
            MUs_f.append(-np.log(d[6] / d[5]))
            MUs_r.append(-np.log(d[6] / d[5]))
            Es.append(d[0])

    if plot:
        if plot_fluo and plot_ref:
            fig = plt.figure(figsize=(12, 6), dpi=96)
            ax_f = fig.add_subplot(1, 2, 1)
            ax_r = fig.add_subplot(1, 2, 2)
        elif plot_fluo and not plot_ref:
            fig = plt.figure(figsize=(8, 6), dpi=96)
            ax_f = fig.add_subplot(1, 1, 1)
        elif plot_ref and not plot_fluo:
            fig = plt.figure(figsize=(8, 6), dpi=96)
            ax_r = fig.add_subplot(1, 1, 1)

        if plot_fluo:
            for e, i in enumerate(MUs_f):
                ax_f.plot(
                    Es[e], i, label=fl_in[e][1] + " (ind:%d time:%s)" % (e, fl_in[e][0])
                )
            ax_f.set_xlabel("E (eV)")
            ax_f.set_ylabel("$\mu(E)$")
            ax_f.set_title("Fluoresence")
            ax_f.axvline(x=Es[e][imin], linestyle="--", color="k")
            ax_f.axvline(x=Es[e][imax], linestyle="--", color="k")
            ax_f.set_xlim(xlim)

        if plot_ref:
            for e, i in enumerate(MUs_r):
                ax_r.plot(
                    Es[e], i, label=fl_in[e][1] + " (ind:%d time:%s)" % (e, fl_in[e][0])
                )
            ax_r.set_xlabel("E (eV)")
            ax_r.set_ylabel("$\mu(E)$")
            ax_r.set_title("Reference")
            ax_r.axvline(x=Es[e][imin], linestyle="--", color="k")
            ax_r.axvline(x=Es[e][imax], linestyle="--", color="k")
            ax_r.set_xlim(xlim)

        if legend:
            if plot_ref:
                ax_r.legend(fontsize=8, loc="best", frameon=False)
            if plot_fluo:
                ax_f.legend(fontsize=8, loc="best", frameon=False)

    # for spectra that have different length (usually ISS data)

    E = Es[0][: len(d0[0]) - cut] + Eshift

    ds = xr.Dataset()
    try:
        arr_f = np.array([i[: len(d0[0]) - cut] for i in MUs_f])
        da_f = xr.DataArray(
            data=arr_f[:, imin:imax],
            coords=[np.arange(len(fl_in)), E[imin:imax]],
            dims=["scan_num", "energy"],
        )
        da_f.scan_num.attrs["files"] = fl_in
        ds["mu_fluo"] = deepcopy(da_f)

        try:
            arr_r = np.array([i[: len(d0[0]) - cut] for i in MUs_r])
            da_r = xr.DataArray(
                data=arr_r[:, imin:imax],
                coords=[np.arange(len(fl_in)), E[imin:imax]],
                dims=["scan_num", "energy"],
            )
            da_r.scan_num.attrs["files"] = fl_in
            ds["mu_ref"] = deepcopy(da_r)
        except:
            pass

    except Exception as exc:
        print(exc)
        print("Unable to create dataset. Something is wrong")
        if plot_fluo and legend:
            ax_f.legend(fontsize=8, loc="best", frameon=False)
            ax_f.set_xlim(xlim)
        if plot_ref and legend:
            ax_r.legend(fontsize=8, loc="best", frameon=False)
            ax_r.set_xlim(xlim)

    return ds


def deglitch(da_in, fl_in, glitches, plot=True):
    Is_new = []
    for i in da_in:
        Enew, Inew = i.energy.values.copy(), i.values.copy()
        for g in glitches:
            Etmp = [
                Enew[e]
                for e, s in enumerate(Enew)
                if (s < float(g.split(":")[0]) or s > float(g.split(":")[1]))
            ]
            Itmp = [
                Inew[e]
                for e, s in enumerate(Enew)
                if (s < float(g.split(":")[0]) or s > float(g.split(":")[1]))
            ]
            Enew, Inew = np.array(Etmp), np.array(Itmp)
        Is_new.append(Inew)
    Is_new = np.array(Is_new)
    da_dg = xr.DataArray(
        data=Is_new,
        coords=[np.arange(Is_new.shape[0]), Enew],
        dims=["scan_num", "energy"],
    )
    da_dg.scan_num.attrs["files"] = da_in.scan_num.attrs["files"]

    if plot:
        fig = plt.figure(figsize=(10, 4))
        ax = fig.add_subplot(1, 2, 1)
        for e, i in enumerate(da_dg):
            i.plot.line("-", ms=1, ax=ax, label=fl_in[e][1])
        for e, i in enumerate(da_in):
            i.plot.line("--o", ms=1, ax=ax)
        ax.set_title(None)
        ax.set_xlabel("E (eV)")
        ax.set_ylabel("$\mu(E)$")
        ax.legend(fontsize=5, ncol=1, bbox_to_anchor=(1.1, 0.99))
        for g in glitches:
            ax.axvline(x=float(g.split(":")[0]), lw=0.2)
            ax.axvline(x=float(g.split(":")[1]), lw=0.2)
        plt.tight_layout()

    return da_dg


def normalize_and_flatten(
    da_in,
    e0=None,
    pre1=None,
    pre2=None,
    nvict=2,
    norm1=None,
    norm2=None,
    rbkg=1.0,
    kweight=1,
    kmin=2,
    kmax=10,
    dk=0.1,
    window="hanning",
    ave_method="mean",
    xlim=None,
    plot=True,
    figsize=(12, 7),
    show_edge_regions=True,
    show_raw=True,
    raw_plot_axes=[0.25, 0.25, 0.2, 0.45],
    legend=False,
    show_std=True,
):
    # create dataset
    ds = xr.Dataset()

    # first average all
    if ave_method == "mean":
        ave = da_in.mean(axis=0)
    elif ave_method == "median":
        ave = da_in.median(axis=0)
    else:
        ave = da_in.mean(axis=0)

    # pre_edge parameters
    if e0 is None:
        e0 = find_e0(ave.energy.values, ave.values)

    if pre1 is None:
        pre1 = -round(e0 - da_in.energy.values[1])
    if pre2 is None:
        pre2 = round(pre1 / 3)

    if norm2 is None:
        norm2 = round(da_in.energy.values[-2] - e0)
    if norm1 is None:
        norm1 = round(norm2 / 3)

    ds.attrs["e0"] = e0
    ds.attrs["pre1"] = pre1
    ds.attrs["pre2"] = pre2
    ds.attrs["nvict"] = nvict
    ds.attrs["norm1"] = norm1
    ds.attrs["norm2"] = norm2

    # normalize and flatten each spectra individually
    mus = np.zeros((da_in.shape[0], da_in.shape[1]))
    norms = np.zeros((da_in.shape[0], da_in.shape[1]))
    flats = np.zeros((da_in.shape[0], da_in.shape[1]))
    for e, i in enumerate(da_in):
        group = Group(
            energy=da_in.energy.values, mu=da_in.isel(scan_num=e).values, filename=None
        )
        pre_edge(
            group,
            e0=e0,
            pre1=pre1,
            pre2=pre2,
            nvict=nvict,
            norm1=norm1,
            norm2=norm2,
            group=group,
        )
        mus[e, :] = group.mu
        norms[e, :] = group.norm
        flats[e, :] = group.flat
    da_mus = xr.DataArray(
        data=mus,
        coords=[np.arange(norms.shape[0]), da_in.energy.values],
        dims=["scan_num", "energy"],
    )
    ds["mus"] = deepcopy(da_mus)
    da_norms = xr.DataArray(
        data=norms,
        coords=[np.arange(norms.shape[0]), da_in.energy.values],
        dims=["scan_num", "energy"],
    )
    ds["norms"] = deepcopy(da_norms)
    da_flats = xr.DataArray(
        data=flats,
        coords=[np.arange(norms.shape[0]), da_in.energy.values],
        dims=["scan_num", "energy"],
    )
    ds["flats"] = deepcopy(da_flats)

    # first average , then normalize
    if ave_method == "mean":
        group_ave1 = Group(
            energy=da_mus.energy.values, mu=da_mus.mean(axis=0).values, filename=None
        )
    elif ave_method == "median":
        group_ave1 = Group(
            energy=da_mus.energy.values, mu=da_mus.median(axis=0).values, filename=None
        )
    else:
        group_ave1 = Group(
            energy=da_mus.energy.values, mu=da_mus.mean(axis=0).values, filename=None
        )
    pre_edge(
        group_ave1,
        e0=e0,
        pre1=pre1,
        pre2=pre2,
        norm1=norm1,
        norm2=norm2,
        group=group_ave1,
    )

    ds["mu1"] = xr.DataArray(
        data=group_ave1.mu, coords=[group_ave1.energy], dims=["energy"]
    )
    ds["flat1"] = xr.DataArray(
        data=group_ave1.flat, coords=[group_ave1.energy], dims=["energy"]
    )
    ds["norm1"] = xr.DataArray(
        data=group_ave1.norm, coords=[group_ave1.energy], dims=["energy"]
    )

    # first normalize , then average
    if ave_method == "mean":
        da = da_norms.mean(axis=0)
        group_ave2 = Group(energy=da.energy.values, mu=da.values, filename=None)
        pre_edge(
            group_ave2,
            e0=e0,
            pre1=pre1,
            pre2=pre2,
            norm1=norm1,
            norm2=norm2,
            group=group_ave2,
        )
    elif ave_method == "median":
        da = da_norms.median(axis=0)
        group_ave2 = Group(energy=da.energy.values, mu=da.values, filename=None)
        pre_edge(
            group_ave2,
            e0=e0,
            pre1=pre1,
            pre2=pre2,
            norm1=norm1,
            norm2=norm2,
            group=group_ave2,
        )
    else:
        da = da_norms.mean(axis=0)
        group_ave2 = Group(energy=da.energy.values, mu=da.values, filename=None)
        pre_edge(
            group_ave2,
            e0=e0,
            pre1=pre1,
            pre2=pre2,
            norm1=norm1,
            norm2=norm2,
            group=group_ave2,
        )

    ds["mu2"] = xr.DataArray(
        data=group_ave2.mu, coords=[group_ave2.energy], dims=["energy"]
    )
    ds["flat2"] = xr.DataArray(
        data=group_ave2.flat, coords=[group_ave2.energy], dims=["energy"]
    )
    ds["norm2"] = xr.DataArray(
        data=group_ave2.norm, coords=[group_ave2.energy], dims=["energy"]
    )

    if plot:
        fig = plt.figure(figsize=figsize, dpi=96)

        ax = fig.add_subplot(1, 2, 1)
        for e, i in enumerate(da_flats):
            i.plot.line("-", ms=1, ax=ax)
        if show_std:
            (da_flats.std(axis=0) - 0.1).plot(ax=ax)

        ax.set_xlim(xlim)
        ax.set_title(None)
        ax.set_xlabel("Energy (eV)")
        ax.set_ylabel("Normalized and flattened $\mu(E)$")
        ax.axvline(x=e0 + pre1, lw=0.2)
        ax.axvline(x=e0 + pre2, lw=0.2)
        ax.axvline(x=norm1 + e0, lw=0.2)
        ax.axvline(x=norm2 + e0, lw=0.2)
        ax.axvline(x=e0, lw=0.2)

        if show_edge_regions:
            ax = fig.add_axes([0.20, 0.2, 0.12, 0.3])
            ax.plot(group_ave1.energy, group_ave1.flat, "-r", lw=2)
            ax.plot(group_ave2.energy, group_ave1.flat, "--b", lw=2)
            ax.set_xlim([e0 - 20, e0])
            ax.set_ylim(top=0.5)
            ax.set_title("pre-edge")
            ax.set_yticklabels([])

            ax = fig.add_axes([0.34, 0.2, 0.12, 0.3])
            ax.plot(group_ave1.energy, group_ave1.flat, "-r", lw=2)
            ax.plot(group_ave2.energy, group_ave1.flat, "--b", lw=2)
            ax.set_xlim([e0, e0 + 20])
            ax.set_ylim(bottom=0.5)
            ax.set_title("post-edge")
            ax.set_yticklabels([])

        elif show_raw:
            ax = fig.add_axes(raw_plot_axes)

            for e, i in enumerate(da_mus):
                i.plot.line(
                    "-",
                    ms=1,
                    ax=ax,
                    label=da_in.scan_num.attrs["files"][e][1].split("/")[-1],
                )
            ax.set_title(None)
            ax.set_xlabel(None)
            ax.set_ylabel("$\mu(E)$")

            if legend:
                ax.legend(fontsize=6)

            plt.gca().spines["top"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)

        plt.tight_layout()

    try:
        autobk(group_ave1, rbkg=rbkg, kweight=kweight)
        xftf(group_ave1, kmin=kmin, kmax=kmax, dk=dk, kwindow=window)
        autobk(group_ave2, rbkg=rbkg, kweight=kweight)
        xftf(group_ave2, kmin=kmin, kmax=kmax, dk=dk, kwindow=window)

        ds.attrs["rbkg"] = rbkg
        ds.attrs["kweight"] = kweight
        ds.attrs["kmin"] = kmin
        ds.attrs["kmax"] = kmax
        ds.attrs["dk"] = dk
        ds.attrs["window"] = window

        da = xr.DataArray(data=group_ave1.chir_mag, coords=[group_ave1.r], dims=["R"])
        ds["chir_mag1"] = deepcopy(da)
        da = xr.DataArray(
            data=group_ave1.k * group_ave1.k * group_ave1.chi,
            coords=[group_ave1.k],
            dims=["k"],
        )
        ds["k2chi1"] = deepcopy(da)

        da = xr.DataArray(data=group_ave2.chir_mag, coords=[group_ave2.r], dims=["R"])
        ds["chir_mag2"] = deepcopy(da)
        da = xr.DataArray(
            data=group_ave2.k * group_ave2.k * group_ave2.chi,
            coords=[group_ave2.k],
            dims=["k"],
        )
        ds["k2chi2"] = deepcopy(da)

        if plot:
            ax = fig.add_subplot(1, 2, 2)
            ax.plot(group_ave1.r, group_ave1.chir_mag, "-r", lw=2)
            ax.plot(group_ave2.r, group_ave2.chir_mag, "--b", lw=2)
            ax.set_xlim([0, 7])
            ax.set_xlabel("$\it{R}$ ($\AA$)")
            ax.set_ylabel("|$\chi$ ($\it{R}$)| ($\AA^{-3}$)")
            ax.set_title(
                "rbkg=%.2f, kmin=%.2f, kmax=%.2f \nkweight=%.2f, dk=%.2f, kwindow=%s"
                % (rbkg, kmin, kmax, kweight, dk, window),
                fontsize=9,
            )

            ax = fig.add_axes([0.77, 0.60, 0.2, 0.3])
            ax.plot(group_ave1.k, group_ave1.k * group_ave1.k * group_ave1.chi, "-r")
            ax.plot(group_ave2.k, group_ave2.k * group_ave2.k * group_ave2.chi, "--b")
            ax.axvline(x=kmin, linestyle=":", color="k")
            ax.axvline(x=kmax, linestyle=":", color="k")
            ax.set_xlabel("$\it{k}$ ($\AA^{-1}$)")
            ax.set_ylabel("$\it{k^{2}}$ $\chi$ ($\it{k}$) ($\AA^{-2}$)")

            plt.gca().spines["top"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)

            plt.tight_layout()

    except Exception as exc:
        print(exc)
        pass

    return ds


import os, sys, datetime
import glob, linecache, shutil
import numpy as np
import xarray as xr

from larch.io import read_ascii, read_athena
from larch.xafs import find_e0, pre_edge, autobk, xftf
from larch import Group
import larch

from copy import deepcopy
from datatree import DataTree


def get_fl(pattern, mode=["ISS"]):
    """
    This function searches files in a directory and sorts by experiment start time
    """

    fl_in = []
    fl = sorted(glob.glob(pattern))

    for e, f in enumerate(fl):
        try:
            if mode[0] == "ISS":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[2], l.split()[3]), "%m/%d/%Y_%H:%M:%S"
                )
            if mode[0] == "ISS_old":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[3], l.split()[4]), "%m/%d/%Y_%H:%M:%S"
                )
            elif mode[0] == "ISS_2021_3":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[2], l.split()[3]), "%m/%d/%Y_%H:%M:%S"
                )
            elif mode[0] == "QAS":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[3], l.split()[4]), "%m/%d/%Y_%H:%M:%S"
                )
            elif mode[0] == "BMM":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    l, "# Scan.start_time: %Y-%m-%dT%H:%M:%S\n"
                )
            elif mode[0] == "12BM":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(l, "#D %a %b %d %H:%M:%S %Y \n")
            elif mode[0] == "20ID":
                l = linecache.getline(f, mode[1]).split()
                dt = datetime.datetime.strptime(
                    "%s_%s_%s" % (l[9], l[10], l[11][0:2]), "%m/%d/%Y_%I:%M:%S_%p"
                )

            fl_in.append([dt.timestamp(), dt, f])

        except Exception as exc:
            print(exc)
            print("Unable to read %s" % (f))

    # sort by timestamp
    fl_in.sort(key=lambda x: x[0])
    fl_out = [[i[1].isoformat(), i[2]] for e, i in enumerate(fl_in)]

    return fl_out


def read_as_ds(
    fl_in,
    mode="ISS",
    sdd_cols=[9, 9 + 4, 9 + 4 + 4, 9 + 4 + 4 + 4],
    Eshift=0,
    imin=0,
    imax=-1,
    plot=True,
    legend=False,
    plot_ref=True,
    plot_fluo=True,
    xlim=None,
    cut=0,
):
    Es = []
    MUs_f = []
    MUs_r = []

    d0 = np.loadtxt(fl_in[0][1], unpack=True)

    read_data = []
    for i in fl_in:
        d = np.loadtxt(i[1], unpack=True)
        if mode == "ISS":
            MUs_f.append(d[4] / d[1])
            MUs_r.append(-np.log(d[3] / d[2]))
            Es.append(d[0])
        elif mode == "ISS_SDD":
            MUs_f.append(
                -(d[sdd_cols[0]] + d[sdd_cols[1]] + d[sdd_cols[2]] + d[sdd_cols[3]])
                / d[1]
            )
            MUs_r.append(-np.log(d[3] / d[2]))
            Es.append(d[0])
        elif mode == "QAS":
            # MUs_f.append(d[1]/d[2])
            # MUs_r.append(np.log(d[1]/d[3]))
            MUs_f.append(d[4] / d[1])
            MUs_r.append(-np.log(d[2] / d[1]))
            Es.append(d[0])
        elif mode == "BMM":
            MUs_f.append(d[3])
            # MUs_r.append(-np.log(d[6]/d[4]))
            MUs_r.append(-np.log(d[6] / d[5]))
            Es.append(d[0])
        elif mode == "12BM":
            MUs_f.append(d[9] / d[2])
            MUs_r.append(d[7] / d[2])
            Es.append(d[0])
        elif mode == "20ID_98":
            MUs_f.append(d[9] / d[8])
            # MUs_r.append(d[9]/d[8]) #for compatibility issues
            Es.append(d[0])
        elif mode == "20ID_186":
            MUs_f.append(d[18] / d[6])
            # MUs_r.append(d[18]/d[6]) #for compatibility issues
            Es.append(d[0])
        elif mode == "20ID_128":
            MUs_f.append(d[12] / d[8])
            # MUs_r.append(d[12]/d[8]) #for compatibility issues
            Es.append(d[0])
        elif mode == "20ID_108":
            MUs_f.append(d[10] / d[8])
            # MUs_r.append(d[10]/d[8]) #for compatibility issues
            Es.append(d[0])
        elif mode == "20ID_65ref":
            MUs_f.append(-np.log(d[6] / d[5]))
            MUs_r.append(-np.log(d[6] / d[5]))
            Es.append(d[0])

    if plot:
        if plot_fluo and plot_ref:
            fig = plt.figure(figsize=(12, 6), dpi=96)
            ax_f = fig.add_subplot(1, 2, 1)
            ax_r = fig.add_subplot(1, 2, 2)
        elif plot_fluo and not plot_ref:
            fig = plt.figure(figsize=(8, 6), dpi=96)
            ax_f = fig.add_subplot(1, 1, 1)
        elif plot_ref and not plot_fluo:
            fig = plt.figure(figsize=(8, 6), dpi=96)
            ax_r = fig.add_subplot(1, 1, 1)

        if plot_fluo:
            for e, i in enumerate(MUs_f):
                ax_f.plot(
                    Es[e], i, label=fl_in[e][1] + " (ind:%d time:%s)" % (e, fl_in[e][0])
                )
            ax_f.set_xlabel("E (eV)")
            ax_f.set_ylabel("$\mu(E)$")
            ax_f.set_title("Fluoresence")
            ax_f.axvline(x=Es[e][imin], linestyle="--", color="k")
            ax_f.axvline(x=Es[e][imax], linestyle="--", color="k")
            ax_f.set_xlim(xlim)

        if plot_ref:
            for e, i in enumerate(MUs_r):
                ax_r.plot(
                    Es[e], i, label=fl_in[e][1] + " (ind:%d time:%s)" % (e, fl_in[e][0])
                )
            ax_r.set_xlabel("E (eV)")
            ax_r.set_ylabel("$\mu(E)$")
            ax_r.set_title("Reference")
            ax_r.axvline(x=Es[e][imin], linestyle="--", color="k")
            ax_r.axvline(x=Es[e][imax], linestyle="--", color="k")
            ax_r.set_xlim(xlim)

        if legend:
            if plot_ref:
                ax_r.legend(fontsize=8, loc="best", frameon=False)
            if plot_fluo:
                ax_f.legend(fontsize=8, loc="best", frameon=False)

    # for spectra that have different length (usually ISS data)

    E = Es[0][: len(d0[0]) - cut] + Eshift

    ds = xr.Dataset()
    try:
        arr_f = np.array([i[: len(d0[0]) - cut] for i in MUs_f])
        da_f = xr.DataArray(
            data=arr_f[:, imin:imax],
            coords=[np.arange(len(fl_in)), E[imin:imax]],
            dims=["scan_num", "energy"],
        )
        da_f.scan_num.attrs["files"] = fl_in
        ds["mu_fluo"] = deepcopy(da_f)

        try:
            arr_r = np.array([i[: len(d0[0]) - cut] for i in MUs_r])
            da_r = xr.DataArray(
                data=arr_r[:, imin:imax],
                coords=[np.arange(len(fl_in)), E[imin:imax]],
                dims=["scan_num", "energy"],
            )
            da_r.scan_num.attrs["files"] = fl_in
            ds["mu_ref"] = deepcopy(da_r)
        except:
            pass

    except Exception as exc:
        print(exc)
        print("Unable to create dataset. Something is wrong")
        if plot_fluo and legend:
            ax_f.legend(fontsize=8, loc="best", frameon=False)
            ax_f.set_xlim(xlim)
        if plot_ref and legend:
            ax_r.legend(fontsize=8, loc="best", frameon=False)
            ax_r.set_xlim(xlim)

    return ds


def deglitch(da_in, fl_in, glitches, plot=True):
    Is_new = []
    for i in da_in:
        Enew, Inew = i.energy.values.copy(), i.values.copy()
        for g in glitches:
            Etmp = [
                Enew[e]
                for e, s in enumerate(Enew)
                if (s < float(g.split(":")[0]) or s > float(g.split(":")[1]))
            ]
            Itmp = [
                Inew[e]
                for e, s in enumerate(Enew)
                if (s < float(g.split(":")[0]) or s > float(g.split(":")[1]))
            ]
            Enew, Inew = np.array(Etmp), np.array(Itmp)
        Is_new.append(Inew)
    Is_new = np.array(Is_new)
    da_dg = xr.DataArray(
        data=Is_new,
        coords=[np.arange(Is_new.shape[0]), Enew],
        dims=["scan_num", "energy"],
    )
    da_dg.scan_num.attrs["files"] = da_in.scan_num.attrs["files"]

    if plot:
        fig = plt.figure(figsize=(10, 4))
        ax = fig.add_subplot(1, 2, 1)
        for e, i in enumerate(da_dg):
            i.plot.line("-", ms=1, ax=ax, label=fl_in[e][1])
        for e, i in enumerate(da_in):
            i.plot.line("--o", ms=1, ax=ax)
        ax.set_title(None)
        ax.set_xlabel("E (eV)")
        ax.set_ylabel("$\mu(E)$")
        ax.legend(fontsize=5, ncol=1, bbox_to_anchor=(1.1, 0.99))
        for g in glitches:
            ax.axvline(x=float(g.split(":")[0]), lw=0.2)
            ax.axvline(x=float(g.split(":")[1]), lw=0.2)
        plt.tight_layout()

    return da_dg


def normalize_and_flatten(
    da_in,
    e0=None,
    pre1=None,
    pre2=None,
    nvict=2,
    norm1=None,
    norm2=None,
    rbkg=1.0,
    kweight=1,
    kmin=2,
    kmax=10,
    dk=0.1,
    window="hanning",
    ave_method="mean",
    xlim=None,
    plot=True,
    figsize=(12, 7),
    show_edge_regions=True,
    show_raw=True,
    raw_plot_axes=[0.25, 0.25, 0.2, 0.45],
    legend=False,
    show_std=True,
):
    # create dataset
    ds = xr.Dataset()

    # first average all
    if ave_method == "mean":
        ave = da_in.mean(axis=0)
    elif ave_method == "median":
        ave = da_in.median(axis=0)
    else:
        ave = da_in.mean(axis=0)

    # pre_edge parameters
    if e0 is None:
        e0 = find_e0(ave.energy.values, ave.values)

    if pre1 is None:
        pre1 = -round(e0 - da_in.energy.values[1])
    if pre2 is None:
        pre2 = round(pre1 / 3)

    if norm2 is None:
        norm2 = round(da_in.energy.values[-2] - e0)
    if norm1 is None:
        norm1 = round(norm2 / 3)

    ds.attrs["e0"] = e0
    ds.attrs["pre1"] = pre1
    ds.attrs["pre2"] = pre2
    ds.attrs["nvict"] = nvict
    ds.attrs["norm1"] = norm1
    ds.attrs["norm2"] = norm2

    # normalize and flatten each spectra individually
    mus = np.zeros((da_in.shape[0], da_in.shape[1]))
    norms = np.zeros((da_in.shape[0], da_in.shape[1]))
    flats = np.zeros((da_in.shape[0], da_in.shape[1]))
    for e, i in enumerate(da_in):
        group = Group(
            energy=da_in.energy.values, mu=da_in.isel(scan_num=e).values, filename=None
        )
        pre_edge(
            group,
            e0=e0,
            pre1=pre1,
            pre2=pre2,
            nvict=nvict,
            norm1=norm1,
            norm2=norm2,
            group=group,
        )
        mus[e, :] = group.mu
        norms[e, :] = group.norm
        flats[e, :] = group.flat
    da_mus = xr.DataArray(
        data=mus,
        coords=[np.arange(norms.shape[0]), da_in.energy.values],
        dims=["scan_num", "energy"],
    )
    ds["mus"] = deepcopy(da_mus)
    da_norms = xr.DataArray(
        data=norms,
        coords=[np.arange(norms.shape[0]), da_in.energy.values],
        dims=["scan_num", "energy"],
    )
    ds["norms"] = deepcopy(da_norms)
    da_flats = xr.DataArray(
        data=flats,
        coords=[np.arange(norms.shape[0]), da_in.energy.values],
        dims=["scan_num", "energy"],
    )
    ds["flats"] = deepcopy(da_flats)

    # first average , then normalize
    if ave_method == "mean":
        group_ave1 = Group(
            energy=da_mus.energy.values, mu=da_mus.mean(axis=0).values, filename=None
        )
    elif ave_method == "median":
        group_ave1 = Group(
            energy=da_mus.energy.values, mu=da_mus.median(axis=0).values, filename=None
        )
    else:
        group_ave1 = Group(
            energy=da_mus.energy.values, mu=da_mus.mean(axis=0).values, filename=None
        )
    pre_edge(
        group_ave1,
        e0=e0,
        pre1=pre1,
        pre2=pre2,
        norm1=norm1,
        norm2=norm2,
        group=group_ave1,
    )

    ds["mu1"] = xr.DataArray(
        data=group_ave1.mu, coords=[group_ave1.energy], dims=["energy"]
    )
    ds["flat1"] = xr.DataArray(
        data=group_ave1.flat, coords=[group_ave1.energy], dims=["energy"]
    )
    ds["norm1"] = xr.DataArray(
        data=group_ave1.norm, coords=[group_ave1.energy], dims=["energy"]
    )

    # first normalize , then average
    if ave_method == "mean":
        da = da_norms.mean(axis=0)
        group_ave2 = Group(energy=da.energy.values, mu=da.values, filename=None)
        pre_edge(
            group_ave2,
            e0=e0,
            pre1=pre1,
            pre2=pre2,
            norm1=norm1,
            norm2=norm2,
            group=group_ave2,
        )
    elif ave_method == "median":
        da = da_norms.median(axis=0)
        group_ave2 = Group(energy=da.energy.values, mu=da.values, filename=None)
        pre_edge(
            group_ave2,
            e0=e0,
            pre1=pre1,
            pre2=pre2,
            norm1=norm1,
            norm2=norm2,
            group=group_ave2,
        )
    else:
        da = da_norms.mean(axis=0)
        group_ave2 = Group(energy=da.energy.values, mu=da.values, filename=None)
        pre_edge(
            group_ave2,
            e0=e0,
            pre1=pre1,
            pre2=pre2,
            norm1=norm1,
            norm2=norm2,
            group=group_ave2,
        )

    ds["mu2"] = xr.DataArray(
        data=group_ave2.mu, coords=[group_ave2.energy], dims=["energy"]
    )
    ds["flat2"] = xr.DataArray(
        data=group_ave2.flat, coords=[group_ave2.energy], dims=["energy"]
    )
    ds["norm2"] = xr.DataArray(
        data=group_ave2.norm, coords=[group_ave2.energy], dims=["energy"]
    )

    if plot:
        fig = plt.figure(figsize=figsize, dpi=96)

        ax = fig.add_subplot(1, 2, 1)
        for e, i in enumerate(da_flats):
            i.plot.line("-", ms=1, ax=ax)
        if show_std:
            (da_flats.std(axis=0) - 0.1).plot(ax=ax)

        ax.set_xlim(xlim)
        ax.set_title(None)
        ax.set_xlabel("Energy (eV)")
        ax.set_ylabel("Normalized and flattened $\mu(E)$")
        ax.axvline(x=e0 + pre1, lw=0.2)
        ax.axvline(x=e0 + pre2, lw=0.2)
        ax.axvline(x=norm1 + e0, lw=0.2)
        ax.axvline(x=norm2 + e0, lw=0.2)
        ax.axvline(x=e0, lw=0.2)

        if show_edge_regions:
            ax = fig.add_axes([0.20, 0.2, 0.12, 0.3])
            ax.plot(group_ave1.energy, group_ave1.flat, "-r", lw=2)
            ax.plot(group_ave2.energy, group_ave1.flat, "--b", lw=2)
            ax.set_xlim([e0 - 20, e0])
            ax.set_ylim(top=0.5)
            ax.set_title("pre-edge")
            ax.set_yticklabels([])

            ax = fig.add_axes([0.34, 0.2, 0.12, 0.3])
            ax.plot(group_ave1.energy, group_ave1.flat, "-r", lw=2)
            ax.plot(group_ave2.energy, group_ave1.flat, "--b", lw=2)
            ax.set_xlim([e0, e0 + 20])
            ax.set_ylim(bottom=0.5)
            ax.set_title("post-edge")
            ax.set_yticklabels([])

        elif show_raw:
            ax = fig.add_axes(raw_plot_axes)

            for e, i in enumerate(da_mus):
                i.plot.line(
                    "-",
                    ms=1,
                    ax=ax,
                    label=da_in.scan_num.attrs["files"][e][1].split("/")[-1],
                )
            ax.set_title(None)
            ax.set_xlabel(None)
            ax.set_ylabel("$\mu(E)$")

            if legend:
                ax.legend(fontsize=6)

            plt.gca().spines["top"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)

        plt.tight_layout()

    try:
        autobk(group_ave1, rbkg=rbkg, kweight=kweight)
        xftf(group_ave1, kmin=kmin, kmax=kmax, dk=dk, kwindow=window)
        autobk(group_ave2, rbkg=rbkg, kweight=kweight)
        xftf(group_ave2, kmin=kmin, kmax=kmax, dk=dk, kwindow=window)

        ds.attrs["rbkg"] = rbkg
        ds.attrs["kweight"] = kweight
        ds.attrs["kmin"] = kmin
        ds.attrs["kmax"] = kmax
        ds.attrs["dk"] = dk
        ds.attrs["window"] = window

        da = xr.DataArray(data=group_ave1.chir_mag, coords=[group_ave1.r], dims=["R"])
        ds["chir_mag1"] = deepcopy(da)
        da = xr.DataArray(
            data=group_ave1.k * group_ave1.k * group_ave1.chi,
            coords=[group_ave1.k],
            dims=["k"],
        )
        ds["k2chi1"] = deepcopy(da)

        da = xr.DataArray(data=group_ave2.chir_mag, coords=[group_ave2.r], dims=["R"])
        ds["chir_mag2"] = deepcopy(da)
        da = xr.DataArray(
            data=group_ave2.k * group_ave2.k * group_ave2.chi,
            coords=[group_ave2.k],
            dims=["k"],
        )
        ds["k2chi2"] = deepcopy(da)

        if plot:
            ax = fig.add_subplot(1, 2, 2)
            ax.plot(group_ave1.r, group_ave1.chir_mag, "-r", lw=2)
            ax.plot(group_ave2.r, group_ave2.chir_mag, "--b", lw=2)
            ax.set_xlim([0, 7])
            ax.set_xlabel("$\it{R}$ ($\AA$)")
            ax.set_ylabel("|$\chi$ ($\it{R}$)| ($\AA^{-3}$)")
            ax.set_title(
                "rbkg=%.2f, kmin=%.2f, kmax=%.2f \nkweight=%.2f, dk=%.2f, kwindow=%s"
                % (rbkg, kmin, kmax, kweight, dk, window),
                fontsize=9,
            )

            ax = fig.add_axes([0.77, 0.60, 0.2, 0.3])
            ax.plot(group_ave1.k, group_ave1.k * group_ave1.k * group_ave1.chi, "-r")
            ax.plot(group_ave2.k, group_ave2.k * group_ave2.k * group_ave2.chi, "--b")
            ax.axvline(x=kmin, linestyle=":", color="k")
            ax.axvline(x=kmax, linestyle=":", color="k")
            ax.set_xlabel("$\it{k}$ ($\AA^{-1}$)")
            ax.set_ylabel("$\it{k^{2}}$ $\chi$ ($\it{k}$) ($\AA^{-2}$)")

            plt.gca().spines["top"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)

            plt.tight_layout()

    except Exception as exc:
        print(exc)
        pass

    return ds



def read_files(
    pattern = None,
    fl_in = None,
    mode=["ISS",56],
    exclude_these=[],
    labels_str=None,
    plot_mus=True,
    plot_channels=False,
    plot_filenames=True,
    sdd=False,
    sdd_cols=[9, 9 + 4, 9 + 4 + 4, 9 + 4 + 4 + 4],
    return_dt = True,
    verbose = False,
):
    """
    This function searches files in a directory and sorts by experiment start time
    """

    reads = []

    if fl_in is not None:
        fl = fl_in
        pattern = ''
    else:
        fl = sorted(glob.glob(pattern))

    for e, f in enumerate(fl):
        if verbose:
            print('reading %s'%(f))
        try:
            # read file
            d = np.loadtxt(f, unpack=True)

            if mode[0] == "ISS":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[2], l.split()[3][:8]), "%m/%d/%Y_%H:%M:%S"
                )
            if mode[0] == "ISS_old":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[3], l.split()[4][:8]), "%m/%d/%Y_%H:%M:%S"
                )
            elif mode[0] == "ISS_2021_3":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[2], l.split()[3][:8]), "%m/%d/%Y_%H:%M:%S"
                )
            elif mode[0] == "QAS":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    "%s_%s" % (l.split()[3], l.split()[4]), "%m/%d/%Y_%H:%M:%S"
                )
            elif mode[0] == "BMM":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(
                    l, "# Scan.start_time: %Y-%m-%dT%H:%M:%S\n"
                )
            elif mode[0] == "12BM":
                l = linecache.getline(f, mode[1])
                dt = datetime.datetime.strptime(l, "#D %a %b %d %H:%M:%S %Y \n")
            elif mode[0] == "20ID":
                l = linecache.getline(f, mode[1]).split()
                dt = datetime.datetime.strptime(
                    "%s_%s_%s" % (l[9], l[10], l[11][0:2]), "%m/%d/%Y_%I:%M:%S_%p"
                )

            reads.append([dt.timestamp(), dt.isoformat(), f, d])

        except Exception as exc:
            if verbose:
                print(exc)
                print("Unable to read %s" % (f))
            else:
                pass

    # sort by timestamp
    reads.sort(key=lambda x: x[0])

    reads = [i for j, i in enumerate(reads) if j not in exclude_these]

    if labels_str is None:
        # figure out columns label from first file
        f0 = open(reads[0][2], "r")
        for e, line in enumerate(f0):
            if line.startswith("#"):
                last_comment_line = e
        col_labels_line = linecache.getline(reads[0][2], last_comment_line + 1).replace(
            "#", ""
        )
        col_labels = col_labels_line.split()

    else:
        col_labels = labels_str.replace("#", "").split()

    col_energy = col_labels.index("energy")
    col_i0 = col_labels.index("i0")
    col_it = col_labels.index("it")
    col_ir = col_labels.index("ir")
    col_if = col_labels.index("iff")

    if plot_channels:

        mosaic = """
                ABE
                CDE
                """
        fig = plt.figure(figsize=(8, 6),layout="constrained",dpi=128)
        axes = fig.subplot_mosaic(mosaic)

        # ax = fig.add_subplot(2, 4, 1)
        ax = axes["A"]
        for i in reads:
            if verbose:
                print("%s [%d,%.2f,%.2f]" % (i[2].split('/')[-1][-30:], e, i[3][0][0], i[3][0][-1]))
            ax.plot(i[3][col_energy], i[3][col_i0])
        ax.set_ylabel("I$_0$")

        # ax = fig.add_subplot(2, 4, 2)
        ax = axes["B"]
        for i in reads:
            ax.plot(i[3][col_energy], i[3][col_it])
        ax.set_ylabel("I$_t$")

        # ax = fig.add_subplot(2, 4, 5)
        ax = axes["C"]
        for i in reads:
            ax.plot(i[3][col_energy], i[3][col_ir])
        ax.set_xlabel("Energy, eV")
        ax.set_ylabel("I$_r$")

        # ax = fig.add_subplot(2, 4, 6)
        ax = axes["D"]
        for i in reads:
            ax.plot(i[3][col_energy], i[3][col_if])
        ax.set_ylabel("I$_{ff}$")
        ax.set_xlabel("Energy, eV")


        ax = axes["E"]

        ax.axis("off")
        ax.set_title(pattern.split('/')[-1],fontsize=10)
        dy = 1 / len(reads)
        if plot_filenames:
            for e, i in enumerate(reads):
                ax.text(
                    -0.3,
                    e * dy,
                    "%s [%d,%.2f,%.2f]" % (i[2].split('/')[-1][-30:], e, i[3][0][0], i[3][0][-1]),
                    color="C%d" % (e % 10),
                    transform=ax.transAxes,
                    fontsize=6,
                )

        plt.tight_layout()

        if sdd:
            fig = plt.figure(figsize=(4,4))
            ax = fig.add_subplot(1, 1, 1)
            for i in reads:
                for e, c in enumerate(sdd_cols):
                    ax.plot(i[3][col_energy], i[3][c], color="C%s" % e)

            plt.tight_layout()

    if plot_mus:
        fig = plt.figure(figsize=(10,4),dpi=128)

        ax = fig.add_subplot(1, 4, 1)
        for i in reads:
            ax.plot(i[3][col_energy], -np.log(i[3][col_it] / i[3][col_i0]))
        # ax.set_ylabel('$\mu_{transmission}$')
        ax.set_xlabel("Energy, eV")
        ax.set_title("Transmission")

        ax = fig.add_subplot(1, 4, 2)
        for i in reads:
            ax.plot(i[3][col_energy], -np.log(i[3][col_ir] / i[3][col_it]))
        # ax.set_ylabel('$\mu_{reference}$')
        ax.set_xlabel("Energy, eV")
        ax.set_title("Reference")

        ax = fig.add_subplot(1, 4, 3)
        if sdd:
            for i in reads:
                ax.plot(i[3][col_energy],(-(np.array([i[3][s] for s in sdd_cols]).mean(axis=0))/i[3][col_i0]))
        else:
            for i in reads:
                ax.plot(i[3][col_energy], (i[3][col_if] / i[3][col_i0]))
        ax.set_xlabel("Energy, eV")
        # ax.set_ylabel('$\mu_{fluorescence}$')
        if sdd:
            ax.set_title("Fluorescence (SDD)")
        else:
            ax.set_title("Fluorescence")


        if plot_filenames:
            ax = fig.add_subplot(1, 4, 4)
            ax.axis("off")
            dy = 1 / len(reads)
            for e, i in enumerate(reads):
                ax.text(
                    -0.2,
                    e * dy,
                    "%s [%d,%.2f,%.2f]" % (i[2].split('/')[-1][-30:], e, i[3][0][0], i[3][0][-1]),
                    color="C%d" % (e % 10),
                    transform=ax.transAxes,
                    fontsize=6,
                )

        plt.tight_layout()

    if return_dt:
        try:
            E = np.array([i[3][col_energy] for i in reads]).mean(axis=0)

            mus_trans = np.array([-np.log(i[3][col_it] / i[3][col_i0]) for i in reads])
            mus_ref = np.array([-np.log(i[3][col_ir] / i[3][col_it]) for i in reads])
            if sdd:
                mus_fluo = np.array([(-(np.array([i[3][s] for s in sdd_cols]).mean(axis=0))/i[3][col_i0]) for i in reads])
            else:
                mus_fluo = np.array([(i[3][col_if] / i[3][col_i0]) for i in reads])

            ds_dict = {}
            for d in [
                [mus_trans, "transmission"],
                [mus_ref, "reference"],
                [mus_fluo, "fluoresence"],
            ]:
                ds = xr.Dataset()
                ds["mus"] = xr.DataArray(
                    data=d[0], coords=[np.arange(len(reads)), E], dims=["scan_num", "energy"])
                ds_dict[d[1]] = ds
            dt = DataTree.from_dict(ds_dict)
            dt.attrs["files"] = [i[2] for i in reads]
            dt.attrs["sdd"] = str(sdd)
            dt.attrs["mode"] = mode
            dt.attrs["pattern"] = pattern
            if sdd:
                dt.attrs["sdd_cols"] = sdd_cols

            return dt
        except Exception as exc:
            print(exc)
            print('\n Unable to get dt, something is wrong...\nreturning reads')
            return reads
    else:
        return reads


def process_ds(
    ds_in,
    e0=None,
    glitches=[],
    pre1=None,
    pre2=None,
    norm1=None,
    norm2=None,
    nvict=2,
    rbkg=1.15,
    kweight=2,
    kmin=2,
    kmax=10,
    dk=0.1,
    window="hanning",
    plot_raw=True,
):
    if e0 is None:
        e0 = find_e0(ds_in.energy.values, ds_in.mus.mean(axis=0).values)

    if glitches is not None or []:
        Is_new = []
        for i in ds_in.mus:
            Enew, Inew = i.energy.values.copy(), i.values.copy()
            for g in glitches:
                Etmp = [
                    Enew[e]
                    for e, s in enumerate(Enew)
                    if (s < float(g.split(":")[0]) or s > float(g.split(":")[1]))
                ]
                Itmp = [
                    Inew[e]
                    for e, s in enumerate(Enew)
                    if (s < float(g.split(":")[0]) or s > float(g.split(":")[1]))
                ]
                Enew, Inew = np.array(Etmp), np.array(Itmp)
            Is_new.append(Inew)
        Is_new = np.array(Is_new)
        da_mus = xr.DataArray(
            data=Is_new,
            coords=[np.arange(Is_new.shape[0]), Enew],
            dims=["scan_num", "energy"],
        )
    else:
        da_mus = ds_in.mus

    # pre_edge and normalization parameters
    if pre1 is None:
        pre1 = -round(e0 - da_mus.energy.values[1])
    if pre2 is None:
        pre2 = round(pre1 / 3)
    if norm2 is None:
        norm2 = round(da_mus.energy.values[-2] - e0)
    if norm1 is None:
        norm1 = round(norm2 / 3)

    flats = []
    for d in da_mus:
        group = Group(energy=da_mus.energy.values, mu=d.values, filename=None)
        pre_edge(
            group,
            e0=e0,
            pre1=pre1,
            pre2=pre2,
            norm1=norm1,
            norm2=norm2,
            nvict=nvict,
            group=group,
        )
        flats.append(group.flat)
    flats = np.array(flats)
    da_flats = xr.DataArray(
        data=flats,
        coords=[np.arange(da_mus.shape[0]), da_mus.energy.values],
        dims=["scan_num", "energy"],
    )



    group = Group(
        energy=da_flats.energy.values, mu=da_flats.mean(axis=0).values, filename=None
    )
    pre_edge(
        group,
        e0=e0,
        pre1=pre1,
        pre2=pre2,
        norm1=norm1,
        norm2=norm2,
        nvict=nvict,
        group=group,
    )

    ds = xr.Dataset()
    ds["mu"] = xr.DataArray(data=group.mu, coords=[group.energy], dims=["energy"])
    ds["mus"] = da_mus
    ds["norm"] = xr.DataArray(data=group.norm, coords=[group.energy], dims=["energy"])
    ds["flat"] = xr.DataArray(data=group.flat, coords=[group.energy], dims=["energy"])
    ds["dmude"] = xr.DataArray(data=group.dmude, coords=[group.energy], dims=["energy"])
    ds["pre_edge"] = xr.DataArray(
        data=group.pre_edge, coords=[group.energy], dims=["energy"]
    )
    ds["post_edge"] = xr.DataArray(
        data=group.post_edge, coords=[group.energy], dims=["energy"]
    )
    # ds.attrs['pre_edge_details'] = group.pre_edge_details.__dict__

    ds.attrs["e0"] = e0
    ds.attrs["pre1"] = pre1
    ds.attrs["pre2"] = pre2
    ds.attrs["nvict"] = nvict
    ds.attrs["norm1"] = norm1
    ds.attrs["norm2"] = norm2

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 2, 1)
    ax.plot(group.energy, group.flat, color="k", lw=2)

    ax.axvline(
        group.pre_edge_details.pre1 + group.e0, linewidth=0.3, color="k", linestyle="--"
    )
    ax.axvline(
        group.pre_edge_details.pre2 + group.e0, linewidth=0.3, color="k", linestyle="--"
    )
    ax.axvline(group.e0, linewidth=0.3, color="k", linestyle="--")
    ax.axvline(
        group.pre_edge_details.norm1 + group.e0,
        linewidth=0.3,
        color="k",
        linestyle="--",
    )
    ax.axvline(
        group.pre_edge_details.norm2 + group.e0,
        linewidth=0.3,
        color="k",
        linestyle="--",
    )
    ax.set_ylabel("$\mu(E)$")
    ax.set_xlabel("Energy, eV")

    if plot_raw:
        ax_in = fig.add_axes([0.27, 0.18, 0.18, 0.35])
        # ax_in.plot(group0.energy, group0.mu, color="k", lw=1)
        # ax_in.plot(group0.energy, group0.pre_edge, lw=0.5)
        # ax_in.plot(group0.energy, group0.post_edge, lw=0.5)
        for m in ds_in.mus:
            m.plot(ax=ax_in)
        ax_in.set_title(None)
        ax_in.set_xlabel(None)
        ax_in.set_ylabel(None)
        if glitches is not None or []:
            for g in glitches:
                ax_in.axvline(
                    x=float(g.split(":")[0]),
                    linewidth=0.2,
                    color="k",
                    linestyle="--",
                    alpha=0.5,
                )
                ax_in.axvline(
                    x=float(g.split(":")[1]),
                    linewidth=0.2,
                    color="k",
                    linestyle="--",
                    alpha=0.5,
                )

    try:
        autobk(group, rbkg=rbkg, kweight=kweight)
        xftf(group, kmin=kmin, kmax=kmax, dk=dk, kwindow=window)
        ds["bkg"] = xr.DataArray(data=group.bkg, coords=[group.energy], dims=["energy"])

        # if plot_raw:
        #     ds["bkg"].plot(ax=ax_in,color='r')
        #     ds["pre_edge"].plot(ax=ax_in,color='r')
        #     ds["post_edge"].plot(ax=ax_in,color='r')

        ds.attrs["rbkg"] = rbkg
        ds.attrs["kweight"] = kweight
        ds.attrs["kmin"] = kmin
        ds.attrs["kmax"] = kmax
        ds.attrs["dk"] = dk
        ds.attrs["window"] = window

        ds["chir_mag"] = xr.DataArray(data=group.chir_mag, coords=[group.r], dims=["r"])
        ds["chir_re"] = xr.DataArray(data=group.chir_re, coords=[group.r], dims=["r"])
        ds["chir_im"] = xr.DataArray(data=group.chir_im, coords=[group.r], dims=["r"])

        ds["kwin"] = xr.DataArray(data=group.kwin, coords=[group.k], dims=["k"])
        ds["k2chi"] = xr.DataArray(
            data=group.k * group.k * group.chi, coords=[group.k], dims=["k"]
        )

        ax = fig.add_subplot(1, 2, 2)
        ax.plot(group.r, group.chir_mag, "-b", lw=2)

        ax.set_xlim([0, 7])
        ax.set_xlabel("$\it{R}$ ($\AA$)")
        ax.set_ylabel("|$\chi$ ($\it{R}$)| ($\AA^{-3}$)")
        ax.set_title(
            "rbkg=%.2f, kmin=%.2f, kmax=%.2f \nkweight=%.2f, dk=%.2f, kwindow=%s"
            % (rbkg, kmin, kmax, kweight, dk, window),
            fontsize=9,
        )

        ax = fig.add_axes([0.77, 0.57, 0.2, 0.3])
        ax.plot(group.k, group.k * group.k * group.chi, "-r")
        ax.axvline(x=kmin, linestyle=":", color="k")
        ax.axvline(x=kmax, linestyle=":", color="k")
        ax.set_xlabel("$\it{k}$ ($\AA^{-1}$)")
        ax.set_ylabel("$\it{k^{2}}$ $\chi$ ($\it{k}$) ($\AA^{-2}$)")

    except Exception as exc:
        print(exc)
        print("Unable to get xftf")

    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.tight_layout()

    return ds

