class TracePointConfig(object):

    def __init__(self, trace_point_id, file=None, line=None, client=None, cond=None, expire_duration=None, expire_hit_count=None,
                 file_hash=None, disabled=False, tracing_enabled=False):
        self.trace_point_id = trace_point_id
        self.file = file
        self.file_hash = file_hash
        self.line = line
        self.client = client
        self.cond = cond
        self.expire_duration = expire_duration
        self.expire_hit_count = expire_hit_count
        self.disabled = disabled
        self.tracing_enabled = tracing_enabled

    def to_json(self):
        return {
            "id": self.trace_point_id,
            "fileName": self.file,
            "lineNo": self.line,
            "expireSecs": self.expire_duration,
            "client": self.client,
            "expireCount": self.expire_hit_count,
            "disabled": self.disabled,
            "tracingEnabled": self.tracing_enabled
        }
