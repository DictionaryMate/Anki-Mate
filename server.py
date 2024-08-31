from textual_serve.server import Server

server = Server("python -m src.main", host="0.0.0.0", port=8080)
server.serve()
