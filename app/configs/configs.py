import json
import os


class Configs:
    @classmethod
    def get_configs(cls) -> dict[str, dict]:
        configs_path = os.path.join(os.getcwd(), 'app', 'configs')
        configs = [i for i in os.listdir(configs_path) if '.json' in i]
        parsed_configs = {}
        print(configs)
        for config in configs:
            with open(os.path.join(configs_path, config), 'r') as file:
                parsed_configs[config.replace('.json', '')] = json.loads(file.read())
        return parsed_configs