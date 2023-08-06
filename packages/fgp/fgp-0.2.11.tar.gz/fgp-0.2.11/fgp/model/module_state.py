import json


class ModuleState:
    dateCreated: int = None
    lastUpdated: int = None
    runId: int = None
    status: str = None
    version: str = None

    @classmethod
    def from_api_response(cls, d: dict) -> 'ModuleState':
        doc: dict = json.loads(d.get('doc', None))
        return cls.from_dict(doc)

    @classmethod
    def from_dict(cls, d: dict) -> 'ModuleState':
        ret = cls()
        for k in d.keys():
            setattr(ret, k, d.get(k))
        return ret