# core
import os
import signal

# community
from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get('/cdn-cgi/trace', response_class = PlainTextResponse)
def onTest(req:Request):
  return f"""ip={req.client.host}
visit_scheme={req.url.scheme}
uag={req.headers['User-Agent']}
"""

@app.get('/shutdown')
def onShutdown():
  os.kill(os.getpid(), signal.SIGTERM)