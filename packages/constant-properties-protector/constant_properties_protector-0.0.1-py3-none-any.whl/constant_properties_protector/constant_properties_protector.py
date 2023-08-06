class CPP:
    def __init__(self, protecteds):
        self.__protecteds = protecteds
        
    def __getattribute__(self, attribute):
        if attribute in ['__getattribute__','_CPP__protecteds','__dict__']:
            return object.__getattribute__(self, attribute)
        if attribute in self.__protecteds:
            return object.__getattribute__(self, '_'+attribute)
        return object.__getattribute__(self, attribute)
        
    def __setattr__(self, attribute, value):
        if '_CPP__protecteds' in self.__dict__:
            if attribute in self.__protecteds:
                raise Exception(f'Can not modify constant property: {attribute}')
        return object.__setattr__(self, attribute, value)