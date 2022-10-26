from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

student_data = {'13':'3.3',
                '25':'4.0',
                '17':'3.7',
                '41':'2.7'}

firstname_dict = {'13':'Jim',
                 '25':'Davey',
                 '17':'Michael',
                 '41':'Max'}

lastname_dict = {'13':'Hopper',
                '25':'Jones',
                '17':'Scott',
                '41':'Miller'}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.log_message("Incoming GET request...")
        try:
            index = parse_qs(self.path[2:])['index'][0]

        except:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")
            return
        if index in student_data.keys():
            self.send_response_to_client(200, student_data[index])
            self.wfile.write(str("\n").encode())
            self.wfile.write(str(firstname_dict[index]).encode())
            self.wfile.write(str("\n").encode())
            self.wfile.write(str(lastname_dict[index]).encode())
        else:
            self.send_response_to_client(400, 'Index not found')
            self.log_message("Index not found")

    def do_POST(self):
        self.log_message('Incoming POST request...')
        data = parse_qs(self.path[2:])
        try:
            student_data[data['index'][0]] = data['gpa'][0]
            firstname_dict[data['index'][0]] = data ['first_name'][0]
            lastname_dict[data['index'][0]] = data['last_name'][0]
            self.send_response_to_client(200, firstname_dict)
        except KeyError:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")
             
    def send_response_to_client(self, status_code, data):
        # Send OK status
        self.send_response(status_code)
        # Send headers
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
     
        # Send the response
        self.wfile.write(str(data).encode())
 
server_address = ('127.0.0.1', 8080)
http_server = HTTPServer(server_address, RequestHandler)
http_server.serve_forever()