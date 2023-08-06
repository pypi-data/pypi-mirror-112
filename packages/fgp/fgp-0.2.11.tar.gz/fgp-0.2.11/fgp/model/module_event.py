class ModuleEvent:
    dateCreated: int = None
    eventName: str = None
    eventType: str = None
    runId: int = None
    version: str = None
    lastUpdated: int = None

    @classmethod
    def from_dict(cls, d: dict) -> 'ModuleEvent':
        ret = cls()
        for k in d.keys():
            setattr(ret, k, d.get(k))
        return ret
