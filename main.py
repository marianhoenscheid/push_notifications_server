# Konfiguration
auth_file = "path/to/serviceAccountKey.json"
key_file = "path/to/key.pem"
cert_file = "path/to/cert.pem"
port = 8000

# Bibliotheken
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import firebase_admin
from firebase_admin import credentials, messaging
import ssl

def send_notification(id, notification_title, notification_body, notification_image=''):
    message = messaging.Message(
        notification=messaging.Notification(
            title=notification_title,
            body=notification_body,
            image=notification_image,
        ),
        token=id,
    )

    response = messaging.send(message)
    return response


def send(self):
    content_length = int(self.headers['Content-Length'])
    body = self.rfile.read(content_length)
    data = json.loads(body.decode("utf-8"))
    token = data["token"]
    title = data["title"]
    body = data["body"]
    if "img_url" in data:
        image = data["img_url"]
    else:
        image = ""
    message_id = send_notification(token, title, body, image)
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b'{"id":"')
    self.wfile.write(bytes(message_id, 'utf-8'))
    self.wfile.write(b'"}')


def register(self):
    content_length = int(self.headers['Content-Length'])
    body = self.rfile.read(content_length)
    data = json.loads(body.decode("utf-8"))
    with open('clients.txt') as json_file:
        clients = json.load(json_file)
    clients[data["client_name"]] = {
        'token': data["token"]
    }
    with open('clients.txt', 'w') as outfile:
        json.dump(clients, outfile)
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b'saved')


if __name__ == '__main__':
    cred = credentials.Certificate(auth_file)
    firebase_admin.initialize_app(cred)


    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/clients":
                self.send_response(200)
                self.end_headers()
                with open('clients.txt') as json_file:
                    clients = json.load(json_file)
                self.wfile.write(bytes(json.dumps(clients), 'utf-8'))

            else:
                self.send_response(405)
                self.end_headers()
                self.wfile.write(b'not allowed')

        def do_POST(self):
            if self.path == "/send":
                send(self)
            elif self.path == "/register":
                register(self)
            else:
                self.send_response(405)
                self.end_headers()


    httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile=key_file,
                                   certfile=cert_file,
                                   server_side=True)
    httpd.serve_forever()
