# pyxel_server
A simple to use API for integration between your [Pyxel](https://github.com/kitao/pyxel) games with servers. 

![Preview](https://github.com/FloppiDisk/pyxserver/blob/main/preview.gif?raw=true)

# Usage
## Code
### client.py
```python
import pyxel_server
import pyxel

class App:
    def __init__(self):
        self.client = pyxel_server.client("127.0.0.1", "5000")
        pyxel.init(self.client.width, self.client.height, fps=self.client.fps)
        self.text = "Client text"
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.text = self.client.var("text")

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, round(self.client.height / 2), self.text, 7)

App()
```
### server.py
```python
import pyxel_server

def update(self):
  self.variables["text"] = str(self.frame_count)
  
variables = {
    "text": "Server Text"
}

pyxel_server.server("127.0.0.1", "5000", 256, 144, 24, update, variables=variables)
```
## What will happen
When you press space in the client, it will get the server's text variable and the text on the screen will change to the server's `frame_count`.  
## What are they doing
### client.py
1. Imports necessary modules.  
* `__init__()`  
  1. Initializes the client with the server `Host` and `Port` by getting necessary information including the width and height of the client.  
    2. Initializes pyxel application with the client's recieved `self.client.width` and `self.client.height`.  
    3. Sets local variable called `text` with some text.  
    4. Runs pyxel application.  
* `update()`  
  1. Checks if the space bar is pressed  
    1. If pressed, it will set the local `text` variable to the server's `text` variable  
* `draw()`  
  1. Clears screen  
  2. Draws text from local `text` variable  
### server.py
1. Imports necessary modules.  
2. Creates a dictionary with needed variables for the server.  
3. Initializes the server to run on `Host` and `Port`, sets default pyxel `AppWidth`, `AppHeight` and `AppFPS`,  
    server `update()` function to run local `update()`,  
    and server variables with the `variables` dictionary.  
* `update()`  
  1. Sets server variable `text` to the current `frame_count`.  
# Reference
Note: `pyxel_server`'s intended features are not fully implemented yet.
## Server
* `server(Host, Port, AppWidth, AppHeight, AppFPS, UpdateScript, [WebScript], [InitScript], [Variables])`  
Initializes the server and runs it.  
`Host`: The ip or domain of the server. e.g. `Host="127.0.0.1"`  
`Port`: The port to be opened in the `Host`. e.g. `Port="5000"`  
`AppWidth`: The width of the client's window when connected. e.g. `AppWidth=256`  
`AppHeight`: The height of the client's window when connected. e.g. `AppHeight=144`  
`AppFPS`: The FPS of the client's window when connected. e.g. `AppFPS=24`  
`UpdateScript`: The function to run every 1/`AppFPS`. e.g. `UpdateScript=update`  
  Note: The function must have the parameter `self`.  
`WebScript`: The custom flask events and routes. e.g. `WebScript=web`  
  Note: The function must have the parameter `self` & `app`.  
`InitScript`: The custom initialization function that will be called when `server()` is called. e.g. `InitScript=init`  
  Note: The function must have the parameter `self`.  
`Variables`: A dictionary of variables needed. e.g. `Variables={"Name": "Value"}`  
## Client
* `client(Host, Port)`  
Initializes the client with necessary information.  
`Host`: The ip or domain of the server. e.g. `Host="127.0.0.1"`  
`Port`: The port to be opened in the `Host`. e.g. `Port="5000"`  
  Note: You must run this command before anything that needs to use the `client` class.  
* `var(Variable, [Value])`  
Returns & optionaly changes a variable from the server.  
`Variable`: The variable name e.g. `Variable="Name"`  
`Value`: The value of variable e.g. `Value="Value"`  
  Note: The variable will be changed before it returns.  
* `post(Route, json)`  
Posts data to a specified route and returns json back.  
`Route`: The path to post e.g. `Route="/var"`  
`json`: The json to post to the `Route` e.g. `json={"Name": "Value"}`  
* `get(Route)`  
Gets data from a specified route  
`Route`: The path to post e.g. `Route="/var"`  
