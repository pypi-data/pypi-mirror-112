import os

def ReadConfig(file_name):
    CONFIG_FILE = os.path.abspath(file_name)
    C = {}
    with open(CONFIG_FILE, 'r') as f:
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
            C[key] = value

    return C
