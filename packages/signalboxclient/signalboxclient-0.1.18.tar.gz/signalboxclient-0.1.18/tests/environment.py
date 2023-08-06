from dotenv import dotenv_values

config = dotenv_values(".local.env")

api_key = config.get('api_key_admin')
host = config.get('host')
port = config.get('port')

print('using admin role')
print('host is ', host)
print('port is ', port)