from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from functions import getMovement

hostName = 'localhost'  # Imposta l'hostname
serverPort = 12347

class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/getmovement':
            self.handle_get_movement()

    def handle_get_movement(self):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            content_len = int(self.headers.get('content-length'))
            post_body = self.rfile.read(content_len)

            try:
                request_data = json.loads(post_body.decode('utf-8'))
                if 'user_prompt' in request_data:
                    user_prompt = request_data['user_prompt']
                    result = getMovement(user_prompt)
                    response_data = {'movement': result}  
                    self.wfile.write(json.dumps(response_data).encode('utf-8'))
                else:
                    response = {'error': 'Richiesta non valida'}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
            except json.JSONDecodeError as e:
                response = {'error': f"Errore nella richiesta: {str(e)}"}
                self.wfile.write(json.dumps(response).encode('utf-8'))

    def handle_404(self):
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {'error': 'Endpoint non trovato'}
        self.wfile.write(json.dumps(response).encode('utf-8'))

if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")    