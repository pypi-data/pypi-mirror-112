import json
from requests import get as request_get
from requests import post as request_post
from flask import Flask, request
from threading import Thread
from time import sleep

class server:
    running = True
    class Web:
        def run(self):
            app = Flask("Web")
            @app.route("/appinfo")
            def get_info():
                return {
                    "width": self.AppWidth,
                    "height": self.AppHeight,
                    "fps": self.AppFPS
                }
            @app.route("/var", methods=["POST"])
            def get_variable():
                name = str(json.loads(request.data).get("name"))
                data = json.loads(request.data).get("data")
                if not data == None:
                    self.variables[name] = data
                return {
                    name: self.variables[name]
                }

            try:
                self.webScript(self, app)
            except:
                pass
                
            app.debug = False
            app.run(host=self.host, port=self.port)
    def __init__(self, Host, Port, AppWidth, AppHeight, AppFPS, UpdateScript, **others):
        self.host = str(Host)
        self.port = str(Port)
        self.updateScript = UpdateScript
        self.AppWidth = int(AppWidth)
        self.AppHeight = int(AppHeight)
        self.AppFPS = int(AppFPS)
        if not others.get("WebScript") == None:
            self.webScript = others.get("WebScript")
            others.pop("WebScript")
        if not others.get("InitScript") == None:
            self.initScript = others.get("InitScript")
            others.pop("InitScript")
        self.variables = others["variables"]
        self.frame_count = 0
        try:
            self.initScript(self)
        except:
            pass
        Thread(target = self.Web.run, args=(self,)).start()
        Thread(target = self.run()).start()

    def run(self):
        while self.running:
            self.update()
            self.frame_count += 1
            sleep(1 / self.AppFPS)

    def update(self):
        self.updateScript(self)

class client:
    def __init__(self, Host, Port):
        self.server = "http://" + str(Host) + ":" + str(Port)
        app = self.appinfo()
        self.width = app["width"]
        self.height = app["height"]
        self.fps = app["fps"]
    
    def var(self, Variable, **Options):
        if Options.get("Value") == None:
            data = request_post(self.server + "/var", json={"name": str(Variable)}).json()
        else:
            data = request_post(self.server + "/var", json={"name": str(Variable), "data": Options.get("Value")}).json()
        if not data.get(str(Variable)) == None:
            return data[str(Variable)]
        else:
            print(data["error"])
            raise
    def post(self, Route, json):
        data = request_post(self.server + str(Route), json=json).json()
        return data

    def get(self, Route):
        data = request_get(self.server + str(Route)).json()
        return data

    def appinfo(self):
        data = request_get(self.server + "/appinfo").json()
        return data