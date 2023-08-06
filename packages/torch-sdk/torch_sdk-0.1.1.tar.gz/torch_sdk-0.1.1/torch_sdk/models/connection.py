class ConnectionType:

    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"ConnectionType({self.__dict__})"


class AnalysisPipeline:

    def __init__(self, id, name, accessKey, createdAt, updatedAt, url, externalUrl, description, hbaseEnabled, hdfsEnabled,
                 hiveEnabled, **kwargs):
        self.name = name
        self.accessKey = accessKey
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.url = url
        self.id = id
        self.externalUrl = externalUrl
        self.description = description
        self.hbaseEnabled = hbaseEnabled
        self.hdfsEnabled = hdfsEnabled
        self.hiveEnable = hiveEnabled

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"AnalysisPipeline({self.__dict__})"
