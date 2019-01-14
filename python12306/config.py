import os
import yaml
import namedtupled


def parsing_config():
    """
    解析yaml
    :return: s  字典
    """
    path = os.path.join(os.getcwd(), 'config.yaml')
    with open(path, 'r', encoding='utf-8') as f:
        s = yaml.load(f)
    return s


Config = namedtupled.map(parsing_config())
