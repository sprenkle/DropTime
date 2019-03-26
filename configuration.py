import json


class Configuration:

    def __init__(self, config_file):
        self.configuration_dict = dict();
        with open(config_file) as json_file:
            data = json.load(json_file)
            configuration = data['configuration']
        self.configuration = configuration

    def get_value(self, section, key):
        return self.configuration[section][key]


if __name__ == "__main__":
    conf = Configuration("debug_config.json")
    print(conf.get_value('tag_api', 'url'))
