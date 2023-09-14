import json
import os
import datetime
import magic
from http.server import BaseHTTPRequestHandler, HTTPServer
from processing import Processor


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(405)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        message = "405 Method Not Allowed"
        self.wfile.write(bytes(message, "utf8"))


    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        file_content = self.rfile.read(content_length)

        mime_type = magic.from_buffer(file_content, mime=True)
        if mime_type == 'application/pdf':

            temporary_file_name = '/tmp/upload_' + str(datetime.datetime.now())
            file = open(temporary_file_name, 'wb')
            file.write(file_content)
            file.close()

            processor = Processor(temporary_file_name)
            result = processor.process()

            if os.path.isfile(temporary_file_name):
                os.remove(temporary_file_name)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(result.json(), "utf8"))

        else:
            self.send_response(415)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            message = json.dumps(
                {'Error': 'Only "application/pdf" files are accepted.'},
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
            self.wfile.write(bytes(message, "utf8"))


try:

    with HTTPServer(('', 8000), RequestHandler) as server:
        server.serve_forever()

except KeyboardInterrupt:
    server.server_close()
