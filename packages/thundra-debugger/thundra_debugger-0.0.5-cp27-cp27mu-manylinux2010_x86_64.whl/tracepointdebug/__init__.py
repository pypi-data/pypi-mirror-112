import atexit

from . import cdbg_native
from .broker.broker_manager import BrokerManager
from .tracepoint.trace_point_manager import TracePointManager


def start():
    cdbg_native.InitializeModule(None)
    _broker_manager = BrokerManager().instance()
    tpm = TracePointManager(broker_manager=_broker_manager)
    _broker_manager.initialize()
    atexit.register(tpm.remove_all_trace_points)
