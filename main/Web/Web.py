import picoweb
import _thread
import logging

# Logging initialisation
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__file__)

app = picoweb.WebApp(__name__)

class Web:
    def __init__(self, hostname):
        log.info("Initialising Web")
        self.hostname = hostname
        app.run(debug=True, host=self.hostname)
        log.info("Web crashed")
        # _thread.start_new_thread(self.run, ())
    
    # def run(self):
    #     print("1")
        
    #     print("2")
        
@app.route("/")
def Index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite(b"Static image 2: <img src='static/dht.jpg'><br />")
    htmlFile = open('/main/web_files/index.html', 'r')
    for line in htmlFile:
        yield from resp.awrite(line)

@app.route("/log")
def Log(req, resp):
    yield from picoweb.start_response(resp)
    htmlFile = open('/main/web_files/log.html', 'r')
    for line in htmlFile:
        yield from resp.awrite(line + "</br>")

# @app.route("/web_files/dht.jpg")
# def squares(req, resp):
#     yield from resp.awrite(b"Static image: <img src='dht.jpg'><br />")