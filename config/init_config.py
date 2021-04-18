from configparser import ConfigParser

config = ConfigParser()

config['basic'] ={
    'startup' : 'true',
    'productive' : '100'
}
config['files'] = {
    'location' : ''
}

with open('./config.ini', 'w') as f:
    config.write(f)