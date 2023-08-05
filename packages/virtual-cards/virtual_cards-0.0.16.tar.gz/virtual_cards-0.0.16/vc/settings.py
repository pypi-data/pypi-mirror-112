class Settings(object):
    _config = {}

    def __init__(self, conf_dict):
        self._config = conf_dict

    def update_config(self, **kwargs):
        self._config.update(kwargs)

    def __getattr__(self, item):
        if item == "_config":
            return self._config
        # elif item == "update_config":
        #     return self.update_config
        return self._config.get(item)

    def __getitem__(self, item):
        return self._config[item]

    def __setitem__(self, key, value):
        if key == "_config":
            super().__setattr__(key, value)
        else:
            self._config[key] = value

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
