import picoweb
import _thread
import os 
print(os.getcwd())
app = picoweb.WebApp(__name__)

class Web:
    def __init__(self, hostname):
        self.hostname = hostname
        _thread.start_new_thread(self.run, ())
    
    def run(self):
        app.run(debug=True, host=self.hostname)
        

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite(b"Static image 2: <img src='static/dht.jpg'><br />")
    htmlFile = open('/main/web_files/index.html', 'r')
    for line in htmlFile:
      yield from resp.awrite(line)

# @app.route("/web_files/dht.jpg")
# def squares(req, resp):
#     yield from resp.awrite(b"Static image: <img src='dht.jpg'><br />")