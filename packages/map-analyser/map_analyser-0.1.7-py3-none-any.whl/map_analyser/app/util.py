import os.path as path


def read_config(file_name):
    config_file = path.abspath(file_name)
    if not path.isfile(config_file):
        config_file = path.join(path.dirname(path.dirname(path.dirname(__file__))), file_name)
    config = {}
    with open(config_file, 'r') as f:
        for l in f.readlines():
            l = l.split('#')[0]
            l = l.strip()
            if len(l) == 0:
                continue
            try:
                key, value = l.split(',')
                key, value = key.strip(), int(value.strip())
            except:
                continue
            config[key] = value

    return config
