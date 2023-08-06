class Device:
    uuid: str = None
    name: str = None
    type: str = None
    description: str = None

    @classmethod
    def from_api_response(cls, d):
        ret = cls()
        ret.uuid = d.get('deviceKey', {}).get('id')
        ret.name = d.get('name')
        ret.type = d.get('type')
        ret.description = d.get('description')
        return ret
