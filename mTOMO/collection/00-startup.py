import nslsii

# See docstring for nslsii.configure_base() for more details
nslsii.configure_base(get_ipython().user_ns,'xpdd', pbar=False, bec=True,
                      magics=True, mpl=True, epics_context=False, configure_logging=False)

# db.reg.set_root_map({'/direct/XF28ID1':'/direct/XF28ID2'})

# At the end of every run, verify that files were saved and
# print a confirmation message.
# from bluesky.callbacks.broker import verify_files_saved, post_run
# RE.subscribe(post_run(verify_files_saved, db),'stop')

# Uncomment the following lines to turn on verbose messages for
# debugging.
# import logging
# ophyd.logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)

RE.md['facility'] = 'NSLS-II'
RE.md['group'] = 'XPD'
RE.md['beamline_id'] = '28-ID-D'

