from bluesky.callbacks.zmq import Publisher
from xpdan.vend.callbacks import CallbackBase

raw_publisher = Publisher(glbl['inbound_proxy_address'], prefix=b'raw')
#RE.subscribe(lambda *x: raw_publisher(*x))
xrun.subscribe(lambda *x: raw_publisher(*x))
