from matplotlib.gridspec import GridSpec
import requests
import PIL
import io
import pprint
import tifffile


def ds_saver(ds, save_to, save_str="_", zlib=False, add_time=True, dtype="float32"):
    comp = dict(zlib=zlib, dtype=dtype)
    encoding = {var: comp for var in ds.data_vars}
    if add_time:
        ds_path = "%s/%s_%s.nc" % (
            save_to,
            ds.attrs["time"].replace("/", "").replace(" ", "").replace(":", ""),
            save_str,
        )
    else:
        ds_path = "%s/%s.nc" % (
            save_to,
            save_str,
        )        
    ds.to_netcdf(ds_path, encoding=encoding)
    return ds_path


def axis_reader(axis_url = 'http://10.67.217.123/axis-cgi/jpg/image.cgi'):
    import requests
    import PIL
    import io
    rqsts=requests.get(axis_url, proxies=None)
    axis_img = np.asarray(PIL.Image.open(io.BytesIO(rqsts.content)))
    da_axis = xr.DataArray(data=axis_img,
                dims=['axis_y', 'axis_x', 'axis_rgb'])
    da_axis.attrs = {'axis_time':time.time()}
    return da_axis


def count_reader(uid,uid_dark=None,include_axis=True,save_ds=False):
    md_user = raw[uid]._item["attributes"]["metadata"]["start"]["md_user"]
    ds_raw = raw[uid]["primary"].read()

    ds = xr.Dataset()

    if uid_dark == 'none':
        uid_dark = None


    if uid_dark is not None:
        ds_raw_dark = raw[uid_dark]["primary"].read()
        md_user_dark = raw[uid_dark]._item["attributes"]["metadata"]["start"]["md_user"]

        for d in raw[uid_dark]._item["attributes"]["metadata"]["start"]["detectors"]:
            if d == "xs3":
                ds["xrf_dark"] = ds_raw_dark.xs3_channel01_data.mean(dim=("time"))
                ds["xrf_dark"].attrs = {
                    "%s_acq_time" % d: md_user_dark["detectors"]["%s_acq_time" % d],
                    "%s_exposure" % d: md_user_dark["detectors"]["%s_exposure" % d],
                }
            elif d == "prosilica":
                ds["%s_img_dark" % d] = xr.DataArray(
                    data=ds_raw_dark["%s_image" % d]
                    .mean(dim=("time"))
                    .mean(axis=0)
                    .astype("float32"),
                    dims=["%s_y" % d, "%s_x" % d, "%s_z" % d],
                    attrs={
                        "%s_acq_time" % d: md_user_dark["detectors"]["%s_acq_time" % d],
                        "%s_exposure" % d: md_user_dark["detectors"]["%s_exposure" % d],
                        "%s_num_exposures"
                        % d: md_user_dark["detectors"]["%s_num_exposures" % d],
                    },
                )
            else:
                ds["%s_img_dark" % d] = xr.DataArray(
                    data=ds_raw_dark["%s_image" % d]
                    .mean(dim=("time"))
                    .mean(axis=0)
                    .astype("float32"),
                    dims=["%s_y" % d, "%s_x" % d],
                    attrs={
                        "%s_acq_time" % d: md_user_dark["detectors"]["%s_acq_time" % d],
                        "%s_exposure" % d: md_user_dark["detectors"]["%s_exposure" % d],
                        "%s_num_exposures"
                        % d: md_user_dark["detectors"]["%s_num_exposures" % d],
                    },
                )

    for d in raw[uid]._item["attributes"]["metadata"]["start"]["detectors"]:
        if d == "xs3":
            ds["xrf"] = ds_raw.xs3_channel01_data.mean(dim=("time"))
            ds["xrf"].attrs = {
                "%s_acq_time" % d: md_user["detectors"]["%s_acq_time" % d],
                "%s_exposure" % d: md_user["detectors"]["%s_exposure" % d],
            }
        elif d == "prosilica":
            ds["%s_img" % d] = xr.DataArray(
                data=ds_raw["%s_image" % d]
                .mean(dim=("time"))
                .mean(axis=0)
                .astype("float32"),
                dims=["%s_y" % d, "%s_x" % d, "%s_z" % d],
                attrs={
                    "%s_acq_time" % d: md_user["detectors"]["%s_acq_time" % d],
                    "%s_exposure" % d: md_user["detectors"]["%s_exposure" % d],
                    "%s_num_exposures"
                    % d: md_user["detectors"]["%s_num_exposures" % d],
                },
            )
        else:
            ds["%s_img" % d] = xr.DataArray(
                data=ds_raw["%s_image" % d]
                .mean(dim=("time"))
                .mean(axis=0)
                .astype("float32"),
                dims=["%s_y" % d, "%s_x" % d],
                attrs={
                    "%s_acq_time" % d: md_user["detectors"]["%s_acq_time" % d],
                    "%s_exposure" % d: md_user["detectors"]["%s_exposure" % d],
                    "%s_num_exposures"
                    % d: md_user["detectors"]["%s_num_exposures" % d],
                },
            )

    if include_axis:
        ds["axis"] = axis_reader()

    ds.attrs = md_user

    ds.attrs = ds.attrs | ds.attrs["detectors"]
    del ds.attrs["detectors"]

    ds.attrs["uid"] = uid
    if uid_dark is None:
        ds.attrs["uid_dark"] = "none"
    else:
        ds.attrs["uid_dark"] = raw[uid_dark]._item["attributes"]["metadata"]["start"]["uid"]

    if save_ds:
        return ds_saver(
            ds,
            md_user["save_to"],
            save_str=md_user["save_name"],
            zlib=False,
            dtype="float32",
        )
    else:
        return ds











def scan_reader(uid,uid_dark=None,include_axis=True,save_ds=False):
    md_user = raw[uid]._item["attributes"]["metadata"]["start"]["md_user"]
    ds_raw = raw[uid]["primary"].read()

    ds = xr.Dataset()

    if uid_dark == 'none':
        uid_dark = None

    print(uid_dark)
    if uid_dark is not None:
        ds_raw_dark = raw[uid_dark]["primary"].read()
        for d in raw[uid_dark]._item["attributes"]["metadata"]["start"]["detectors"]:
            if d == "xs3":
                ds["xrf_dark"] = ds_raw_dark.xs3_channel01_data.mean(dim=("time"))
            elif d == "prosilica":
                ds["%s_img_dark" % d] = xr.DataArray(
                    data=ds_raw_dark["%s_image" % d]
                    .mean(dim=("time"))
                    .mean(axis=0)
                    .astype("float32"),
                    dims=["%s_y" % d, "%s_x" % d, "%s_z" % d],
                )
            else:
                ds["%s_img_dark" % d] = xr.DataArray(
                    data=ds_raw_dark["%s_image" % d]
                    .mean(dim=("time"))
                    .mean(axis=0)
                    .astype("float32"),
                    dims=["%s_y" % d, "%s_x" % d],
                )


    
    for d in raw[uid]._item["attributes"]["metadata"]["start"]["detectors"]:
        if d == "xs3":
            ds["xrfs"] = xr.DataArray(
                data=ds_raw.xs3_channel01_data.values,
                dims = [md_user["motor"],'bin_count']
            )
        elif d == "prosilica":
            ds["%s_imgs" % d] = xr.DataArray(
                data=ds_raw["%s_image" % d]
                .mean(dim='dim_0')
                .astype("float32").values,
                dims=[md_user["motor"], "%s_y" % d, "%s_x" % d, "%s_z" % d],
            )
            ds["%s_stats1" % d] = xr.DataArray(
                data=ds_raw["%s_stats1_total" % d]
                .astype("float32").values,
                dims=[md_user["motor"]],
            )
        else:
            ds["%s_imgs" % d] = xr.DataArray(
                data=ds_raw["%s_image" % d]
                .mean(dim='dim_0')
                .astype("float32").values,
                dims=[md_user["motor"], "%s_y" % d, "%s_x" % d],
                coords=[ds_raw[md_user["motor"]],ds_raw.dim_1,ds_raw.dim_2] 
                
            )
            ds["%s_stats1" % d] = xr.DataArray(
                data=ds_raw["%s_stats1_total" % d]
                .astype("float32").values,
                dims=[md_user["motor"]],
            )
    
    if include_axis:
        ds["axis"] = axis_reader()

    ds.attrs = md_user

    ds.attrs = ds.attrs | ds.attrs["detectors"]
    del ds.attrs["detectors"]
     

    ds.attrs["uid"] = uid
    if uid_dark is None:
        ds.attrs["uid_dark"] = "none"
    else:
        ds.attrs["uid_dark"] = raw[uid_dark]._item["attributes"]["metadata"]["start"]["uid"]

    if save_ds:
        return ds_saver(
            ds,
            md_user["save_to"],
            save_str=md_user["save_name"],
            zlib=False,
            dtype="float32",
        )
    else:
        return ds

























# def plotter_visible(ds, robust=True, robust0=True):
#     try:
#         with xr.open_dataset(ds) as ds:
#             ds.load()
#     except:
#         ds = ds

#     fig = plt.figure(constrained_layout=True, figsize=(12, 12), dpi=96)

#     gs1 = GridSpec(3, 2, width_ratios=(1.0, 0.8), figure=fig)

#     gsc = 0

#     try:
#         x, y, s = [ds.attrs["prosilica_lx"], ds.attrs["prosilica_ly"], 200]

#         ax = fig.add_subplot(gs1[gsc, 0])
#         ds["prosilica_img"].plot.imshow(
#             robust=robust0, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
#         )

#         ax.axvline(x=x, color="r", linestyle="--", alpha=0.8)
#         ax.axhline(y=(1752 - y), color="r", linestyle="--", alpha=0.8)

#         ax.set_title(
#             "mBaseX=%.3f mTopX=%.3f mTopZ=%.3f mPhi=%.3f"
#             % (
#                 ds.attrs["mBaseX"],
#                 ds.attrs["mTopX"],
#                 ds.attrs["mTopY"],
#                 ds.attrs["mPhi"],
#             )
#         )
#         ax.set_aspect("equal")

#         ax = fig.add_subplot(gs1[gsc, 1])
#         ds["prosilica_img"].sel(prosilica_y=slice((1752 - y) - s, (1752 - y) + s)).sel(
#             prosilica_x=slice(x - s, x + s)
#         ).plot.imshow(
#             robust=True, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
#         )

#         ax.axvline(x=s, color="r", linestyle="--", alpha=0.8)
#         ax.axhline(y=s, color="r", linestyle="--", alpha=0.8)
#         ax.set_aspect("equal")
#         ax.set_xlabel(None)
#         ax.set_ylabel(None)
#         ax.set_title("[%d/%d/%d]" % (x, y, s))

#         gsc = gsc + 1

#     except:
#         pass

#     try:
#         x, y, s = [ds.attrs["blackfly_lx"], ds.attrs["blackfly_ly"], 200]

#         ax = fig.add_subplot(gs1[gsc, 0])
#         ds["blackfly_img"].plot.imshow(
#             robust=robust0, yincrease=True, ax=ax, add_colorbar=False, cmap="Greys_r"
#         )

#         ax.axvline(x=x, color="r", linestyle="--", alpha=0.8)
#         ax.axhline(y=(2048 - y), color="r", linestyle="--", alpha=0.8)

#         ax.set_title(
#             "mBaseY=%.3f mTopY=%.3f " % (ds.attrs["mBaseY"], ds.attrs["mTopY"])
#         )
#         ax.set_aspect("equal")

#         ax = fig.add_subplot(gs1[gsc, 1])
#         ds["blackfly_img"].sel(blackfly_y=slice((2048 - y) - s, (2048 - y) + s)).sel(
#             blackfly_x=slice(x - s, x + s)
#         ).plot.imshow(
#             robust=True, yincrease=True, ax=ax, add_colorbar=False, cmap="Greys_r"
#         )

#         ax.axvline(x=s, color="r", linestyle="--", alpha=0.8)
#         ax.axhline(y=s, color="r", linestyle="--", alpha=0.8)
#         ax.set_aspect("equal")
#         ax.set_xlabel(None)
#         ax.set_ylabel(None)
#         ax.set_title("[%d/%d/%d]" % (x, y, s))

#         gsc = gsc + 1

#     except:
#         pass

#     try:
#         x, y, s = [ds.attrs["emergent_lx"], ds.attrs["emergent_ly"], 200]

#         ax = fig.add_subplot(gs1[gsc, 0])
#         ds["emergent_img"].plot.imshow(
#             robust=robust0, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
#         )

#         ax.axvline(x=x, color="r", linestyle="--", alpha=0.8)
#         ax.axhline(y=(3000 - y), color="r", linestyle="--", alpha=0.8)
#         ax.set_aspect("equal")

#         ax = fig.add_subplot(gs1[gsc, 1])
#         ds["emergent_img"].sel(emergent_y=slice((3000 - y) - s, (3000 - y) + s)).sel(
#             emergent_x=slice(x - s, x + s)
#         ).plot.imshow(
#             robust=True, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
#         )

#         ax.axvline(x=s, color="r", linestyle="--", alpha=0.8)
#         ax.axhline(y=s, color="r", linestyle="--", alpha=0.8)
#         ax.set_aspect("equal")
#         ax.set_xlabel(None)
#         ax.set_ylabel(None)
#         ax.set_title("[%d/%d/%d]" % (x, y, s))

#         gsc = gsc + 1
#     except:
#         pass

#     try:
#         x, y, s = [ds.attrs["alliedvision_lx"], ds.attrs["alliedvision_ly"], 200]

#         ax = fig.add_subplot(gs1[gsc, 0])
#         ds["alliedvision_img"].plot.imshow(
#             robust=robust0, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
#         )

#         ax.axvline(x=x, color="r", linestyle="--", alpha=0.8)
#         ax.axhline(y=(2848 - y), color="r", linestyle="--", alpha=0.8)

#         ax.set_title(
#             "mBaseY=%.3f mTopY=%.3f " % (ds.attrs["mBaseY"], ds.attrs["mTopY"])
#         )
#         ax.set_aspect("equal")

#         ax = fig.add_subplot(gs1[gsc, 1])
#         ds["alliedvision_img"].sel(
#             alliedvision_y=slice((2848 - y) - s, (2848 - y) + s)
#         ).sel(alliedvision_x=slice(x - s, x + s)).plot.imshow(
#             robust=True, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
#         )

#         ax.axvline(x=s, color="r", linestyle="--", alpha=0.8)
#         ax.axhline(y=s, color="r", linestyle="--", alpha=0.8)
#         ax.set_aspect("equal")
#         ax.set_xlabel(None)
#         ax.set_ylabel(None)
#         ax.set_title("[%d/%d/%d]" % (x, y, s))

#         gsc = gsc + 1
#     except:
#         pass


def plotter_dexela(ds):
    fig = plt.figure(constrained_layout=True, figsize=(8, 8), dpi=96)

    # gs1 = GridSpec(1, 2, width_ratios=(1, 0.5), figure=fig)
    # ax = fig.add_subplot(gs1[0, 0])
    
    ax = fig.add_subplot(1,1,1)
    try:
        da = ds["dexela_img"] - ds["dexela_img_dark"]
    except:
        da = ds["dexela_img"]

    da.T.plot.imshow(
        robust=True,
        yincrease=False,
        ax=ax,
        add_colorbar=True,
        cmap="Greys_r",
        vmin=None,
        vmax=None,
        cbar_kwargs=dict(orientation="horizontal", pad=0.02, shrink=0.4, label=None),
    )
    ax.set_aspect("equal")
    ax.set_xlabel("pixel_x")
    ax.set_ylabel("pixel_y")
    ax.set_title(
        "user_note=%s\nuid=%s\nuid_dark=%s"
        % (ds.attrs["user_note"], ds.attrs["uid"], ds.attrs["uid_dark"])
    )
    ax.set_xlabel(
        "[acq_time=%.2f/exposure=%.2f]"
        % (
            ds.attrs["dexela_acq_time"],
            ds.attrs["dexela_exposure"],
        )
    )

    # try:
    #     da_xrf = ds["xrf"]
    #     ax = fig.add_subplot(gs1[0, 1])
    #     da_xrf.plot(ax=ax)
    #     ax.set_ylabel(None)
    # except:
    #     pass







def plot_bf_alignmnet(ds):

    try:
        with xr.open_dataset(ds) as ds:
            ds.load()
    except:
        ds = ds

    fig = plt.figure(constrained_layout=True, figsize=(12,4), dpi=96)
    
    x, y, s = [ds.attrs["blackfly_lx"], ds.attrs["blackfly_ly"], 200]
    
    ax = fig.add_subplot(1,3,1)
    ds["blackfly_img"].plot.imshow(
        robust=False, yincrease=True, ax=ax, add_colorbar=False, cmap="Greys_r"
    )
    ax.axvline(x=(2448 - x), color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=(y), color="r", linestyle="--", alpha=0.8)
    ax.set_aspect("equal")
    ax.set_title(ds.attrs["uid"])
    
    ax = fig.add_subplot(1,3,2)
    ds["blackfly_img"].sel(blackfly_y=slice((y) - s, (y) + s)).sel(
        blackfly_x=slice(2448 - x - s, 2448 - x + s)
    ).plot.imshow(
        robust=True, yincrease=True, ax=ax, add_colorbar=False, cmap="Greys_r"
    )
    ax.axvline(x=s, color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=s, color="r", linestyle="--", alpha=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    
    ax = fig.add_subplot(1,3,3)
    x, y, s = 1126, 1036, 50 
    x, y, s = 1718, 2048-285, 250  
    ds["blackfly_img"].sel(blackfly_y=slice((y) - s, (y) + s)).sel(
        blackfly_x=slice(2448 - x - s, 2448 - x + s)
    ).plot.imshow(
        robust=False, yincrease=True, ax=ax, add_colorbar=False, cmap="Greys_r"
    )
    ax.axvline(x=s, color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=s, color="r", linestyle="--", alpha=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel(None)
    ax.set_ylabel(None)

    return





def plot_bf_and_em(ds):

    try:
        with xr.open_dataset(ds) as ds:
            ds.load()
    except:
        ds = ds


    
    fig = plt.figure(constrained_layout=True, figsize=(8,8), dpi=96)



    
    x, y, s = [ds.attrs["blackfly_lx"], ds.attrs["blackfly_ly"], 100]
    
    ax = fig.add_subplot(2,2,1)
    ds["blackfly_img"].plot.imshow(
        robust=False, yincrease=True, ax=ax, add_colorbar=False, cmap="Greys_r"
    )
    ax.axvline(x=(2448 - x), color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=(y), color="r", linestyle="--", alpha=0.8)
    ax.set_aspect("equal")
    ax.set_title(
        "%s \n mBaseX=%.3f mBaseY=%.3f " % (ds.attrs["uid"],ds.attrs["mBaseX"], ds.attrs["mBaseY"])
    )

    ax = fig.add_subplot(2,2,2)
    ds["blackfly_img"].sel(blackfly_y=slice((y) - s, (y) + s)).sel(
        blackfly_x=slice(2448 - x - s, 2448 - x + s)
    ).plot.imshow(
        robust=True, yincrease=True, ax=ax, add_colorbar=False, cmap="Greys_r"
    )

    ax.axvline(x=s, color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=s, color="r", linestyle="--", alpha=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_title("[%d/%d/%d]" % (x, y, s))





    x, y, s = [ds.attrs["emergent_lx"], ds.attrs["emergent_ly"], 100]
    ax = fig.add_subplot(2,2,3)
    ds["emergent_img"].plot.imshow(
        robust=True, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
    )

    ax.axvline(x=x, color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=(3000 - y), color="r", linestyle="--", alpha=0.8)
    ax.set_title(
        "mTopY=%.3f mPhi=%.3f " % (ds.attrs["mTopY"], ds.attrs["mPhi"])
    )

    ax = fig.add_subplot(2,2,4)
    ds["emergent_img"].sel(emergent_y=slice((3000 - y) - s, (3000 - y) + s)).sel(
        emergent_x=slice(x - s, x + s)
    ).plot.imshow(
        robust=True, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
    )
    ax.axvline(x=s, color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=s, color="r", linestyle="--", alpha=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_title("[%d/%d/%d]" % (x, y, s))

    return


def plot_ps_and_em(ds):

    try:
        with xr.open_dataset(ds) as ds:
            ds.load()
    except:
        ds = ds


    
    fig = plt.figure(constrained_layout=True, figsize=(8,8), dpi=96)



    
    x, y, s = [ds.attrs["prosilica_lx"], ds.attrs["prosilica_ly"], 100]
    
    ax = fig.add_subplot(2,2,1)
    ds["prosilica_img"].plot.imshow(
        robust=True, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
    )

    ax.axvline(x=x, color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=(1752 - y), color="r", linestyle="--", alpha=0.8)
    ax.set_aspect("equal")
    ax.set_title(
        "%s \n mBaseX=%.3f mBaseY=%.3f " % (ds.attrs["uid"],ds.attrs["mBaseX"], ds.attrs["mBaseY"])
    )

    ax = fig.add_subplot(2,2,2)
    ds["prosilica_img"].sel(prosilica_y=slice((1752 - y) - s, (1752 - y) + s)).sel(
        prosilica_x=slice(x - s, x + s)
    ).plot.imshow(
        robust=True, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
    )

    ax.axvline(x=s, color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=s, color="r", linestyle="--", alpha=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_title("[%d/%d/%d]" % (x, y, s))





    x, y, s = [ds.attrs["emergent_lx"], ds.attrs["emergent_ly"], 100]
    ax = fig.add_subplot(2,2,3)
    ds["emergent_img"].plot.imshow(
        robust=True, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
    )

    ax.axvline(x=x, color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=(3000 - y), color="r", linestyle="--", alpha=0.8)
    ax.set_title(
        "mTopY=%.3f mPhi=%.3f " % (ds.attrs["mTopX"], ds.attrs["mPhi"])
    )

    ax = fig.add_subplot(2,2,4)
    ds["emergent_img"].sel(emergent_y=slice((3000 - y) - s, (3000 - y) + s)).sel(
        emergent_x=slice(x - s, x + s)
    ).plot.imshow(
        robust=True, yincrease=False, ax=ax, add_colorbar=False, cmap="Greys_r"
    )
    ax.axvline(x=s, color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=s, color="r", linestyle="--", alpha=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_title("[%d/%d/%d]" % (x, y, s))

    return



def plot_av(ds):

    try:
        with xr.open_dataset(ds) as ds:
            ds.load()
    except:
        ds = ds

    fig = plt.figure(constrained_layout=True, figsize=(9,8), dpi=96)

    x, y, s = [ds.attrs["alliedvision_lx"], ds.attrs["alliedvision_ly"], 100]


    ax = fig.add_subplot(2,2,4)
    ds["alliedvision_img"].plot.imshow(
        robust=False, yincrease=True, ax=ax, add_colorbar=False, cmap="Greys_r"
    )
    ax.axvline(x=x, color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=(2848 - y), color="r", linestyle="--", alpha=0.8)
    # ax.set_title("[%d/%d/%d]" % (x, y, s))
    
    ax.set_aspect("equal")
    


    ax = fig.add_subplot(2,2,2)
    ds["alliedvision_img"].sel(
        alliedvision_y=slice((2848 - y) - s, (2848 - y) + s)).sel(alliedvision_x=slice(x - s, x + s)).mean(dim='alliedvision_x').plot(y='alliedvision_y',yincrease=False,ax=ax)
    ax.set_ylim([0,2*s])
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    
    ax = fig.add_subplot(2,2,3)
    ds["alliedvision_img"].sel(alliedvision_y=slice((2848 - y) - s, (2848 - y) + s)).sel(alliedvision_x=slice(x - s, x + s)).mean(dim='alliedvision_y').plot(ax=ax)
    ax.set_xlim([0,2*s])
    ax.set_xlabel(None)
    ax.set_ylabel(None)
   
    ax = fig.add_subplot(2,2,1)
    ds["alliedvision_img"].sel(
        alliedvision_y=slice((2848 - y) - s, (2848 - y) + s)
    ).sel(alliedvision_x=slice(x - s, x + s)).plot.imshow(
        robust=False, yincrease=True, ax=ax, add_colorbar=False, cmap="Greys_r"
    )

    ax.axvline(x=s, color="r", linestyle="--", alpha=0.8)
    ax.axhline(y=s, color="r", linestyle="--", alpha=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_xlim([0,2*s])
    ax.set_ylim([0,2*s])    

    
    return





def ds_getter(uid,include_axis=False,save_ds=True,plot=True):

    md_user = raw[uid]._item["attributes"]["metadata"]["start"]["md_user"]
    if md_user['type'] == 'count':
        ds = count_reader(uid,md_user['uid_dark'],include_axis=include_axis,save_ds=save_ds)
        if plot:
            if md_user['plot_hint'] == 'bf_alignmnet_check':
                plot_bf_alignmnet(ds)
            if md_user['plot_hint'] == 'bf_and_em':
                plot_bf_and_em(ds)
            if md_user['plot_hint'] == 'ps_and_em':
                plot_ps_and_em(ds)
            if md_user['plot_hint'] == 'av-count':
                plot_av(ds)
    return ds









