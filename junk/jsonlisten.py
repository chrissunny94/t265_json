from jsocket import Client, Server


host = 'localhost'
port = '8000'

# Client code:
client = Client()
client.connect(host, port).send({'some_list': [123, 456]})
response = client.recv()
# response now is {'data': {'some_list': [123, 456]}}
client.close()


# Server code:
server = Server(host, port)
server.accept()
data = server.recv()
# data now is: {'some_list': [123, 456]}

while(True):
  print(server.recv())

server.send({'data': data}).close()
