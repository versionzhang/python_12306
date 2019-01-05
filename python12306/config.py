import os
import yaml
import namedtupled


def parsing_config():
    """
    解析yaml
    :return: s  字典
    """
    path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(path, 'r') as f:
        s = yaml.load(f)
    return s


Config = namedtupled.map(parsing_config())

