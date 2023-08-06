import queue
import socketio
import click
from sockterm.state import state

sio = socketio.Client()
state.connected = False

def quit_output(event, namespace):
    if event is not None:
        sio.on(
            event,
            lambda data: None,
            namespace=namespace
        )

@sio.event
def connect():
    state.connected = True
    print("Connected!")

@sio.event
def disconnect():
    state.connected = False
    print("Disconnected!")

def receive_message(event, namespace, data):
    global current_event
    global current_namespace
    if namespace is None:
        namespace_hr = "/"
    else:
        namespace_hr = namespace
    current_event = event
    current_namespace = namespace
    print(f"[{namespace_hr}][{event}] {data}")
