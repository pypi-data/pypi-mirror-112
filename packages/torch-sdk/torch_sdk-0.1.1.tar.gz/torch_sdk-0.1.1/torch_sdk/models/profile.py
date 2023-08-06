class Profile:

    def __init__(self):
        pass


class AutoProfileConfiguration:

    def __init__(self, assemblyId, assemblyName, createdAt, updatedAt, enabled, schedule, parallelizationCount, id=None,
                 includeList=None, excludeList=None, **kwargs):
        self.assemblyId = assemblyId
        self.assemblyName = assemblyName
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.enabled = enabled
        self.schedule = schedule
        self.parallelizationCount = parallelizationCount
        self.id = id
        if isinstance(includeList, list):
            self.includeList = list(includeList)
        else:
            self.includeList = includeList

        if isinstance(excludeList, dict):
            self.excludeList = list(excludeList)
        else:
            self.excludeList = excludeList

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"AutoProfileConfiguration({self.__dict__})"
