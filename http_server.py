import socket
import sys
import requests

def response_ok(body=b"This is a minimal response", mimetype=b"text/plain"):
    """
    returns a basic HTTP response
    Ex:
        response_ok(
            b"<html><h1>Welcome:</h1></html>",
            b"text/html"
        ) ->
        b'''
        HTTP/1.1 200 OK\r\n
        Content-Type: text/html\r\n
        \r\n
        <html><h1>Welcome:</h1></html>\r\n
        '''
    """
    return b"\r\n".join([
        b"HTTP/1.1 200 OK",
        b"Content-Type: text/plain" +mimetype,
        b"",
        body
    ])


def parse_request(request):
     return request.split("\r\n")[0].split(" ")[1]


def response_method_not_allowed():
    """Returns a 405 Method Not Allowed response"""
    return b"\r\n".join([b"HTTP/1.1 405 405 Method Not Allowed,
                         b"Content-Type: text/plain", b"",
                         b"This is a minimal response", ])


def response_not_found():
    """Returns a 404 Not Found response"""
    method, uri, version = request.split("\r\n")[0].split(" ")

    if method != "GET":
        raise NotImplementedError

    return uri
    

def resolve_uri(uri):
    """
    This method should return appropriate content and a mime type.

    If the requested URI is a directory, then the content should be a
    plain-text listing of the contents with mimetype `text/plain`.

    If the URI is a file, it should return the contents of that file
    and its correct mimetype.

    If the URI does not map to a real location, it should raise an
    exception that the server can catch to return a 404 response.

    Ex:
        resolve_uri('/a_web_page.html') -> (b"<html><h1>North Carolina...",
                                            b"text/html")

        resolve_uri('/images/sample_1.png')
                        -> (b"A12BCF...",  # contents of sample_1.png
                            b"image/png")

        resolve_uri('/') -> (b"images/, a_web_page.html, make_type.py,...",
                             b"text/plain")

        resolve_uri('/a_page_that_doesnt_exist.html') -> Raises a NameError

    """

    # TODO: Raise a NameError if the requested content is not present
    # under webroot.

    # TODO: Fill in the appropriate content and mime_type give the URI.
    # See the assignment guidelines for help on "mapping mime-types", though
    # you might need to create a special case for handling make_time.py
    content = b"not implemented"
    mime_type = b"not implemented"

    return content, mime_type


def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                request = ''
                while True:
                    data = conn.recv(16)
                    request += data.decode('utf8')
                    if len(data) < 1024:
                        break

                    # Now we have a "request"
                    # TODO: fulfill the request
                    try:
                        uri = parse_request(request)
                    except NotImplementedError:
                        response = response_method_not_allowed
                    else:
                        # Do some work in here
                        # to produce the correct body and correct mimetype
                        # based on the uri
                        response = response_ok(body=uri.encode(), mimetype=b"text/plain")

                    conn.sendall(response)

                    #print('received "{0}"'.format(data), file=log_buffer)
                    #if data:
                    #    print('sending data back to client', file=log_buffer)
                    #    conn.sendall(data)
                    #else:
                    #    msg = 'no more data from {0}:{1}'.format(*addr)
                    #    print(msg, log_buffer)
                    #    break
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)


