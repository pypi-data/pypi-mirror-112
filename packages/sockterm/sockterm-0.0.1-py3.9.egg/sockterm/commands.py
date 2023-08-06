import sys
from sockterm import socketio_client
from sockterm.socketio_client import sio
from sockterm.state import state

class Commands:
    def connect(self, url):
        """
        Connect to specified SocketIO server.
        """
        sio.disconnect()
        sio.connect(url)

    def disconnect(self):
        """
        Disconnect from current SocketIO server.
        """
        sio.disconnect()
        return "Disconnected!"

    def subscribe(self, event, namespace=None):
        """
        Subscribe to an event.
        """
        if not state.connected:
            return "Connect to a server first!"

        sio.on(
            event,
            lambda data: socketio_client.receive_message(event, namespace, data),
            namespace=namespace
        )
        if namespace is None:
            namespace = "/"

        return f"Subscribed to event {event} on namespace [{namespace}]"

    def unsubscribe(self, event, namespace=None):
        """
        Stop subscribing to an event.
        """
        if not state.connected:
            return "Connect to a server first!"

        sio.on(
            event,
            lambda data: None,
            namespace=namespace
        )
        if namespace is None:
            namespace = "/"

        return f"Unsubscribed from event {event} on namespace [{namespace}]"

    def emit(self, event, data, namespace=None):
        """
        Emit a message to an event.
        """
        if not state.connected:
            return "Connect to a server first!"

        # Subscribe to responses
        sio.on(
            event,
            lambda data: socketio_client.receive_message(event, namespace, data),
            namespace=namespace
        )

        sio.emit(
            event,
            data,
            namespace=namespace
        )

    def call(self, event, data, namespace=None):
        """
        Emit a message and wait for a response.
        """
        if not state.connected:
            return "Connect to a namespace first!"

        # Subscribe to responses
        sio.on(
            event,
            lambda data: socketio_client.receive_message(event, namespace, data),
            namespace=namespace
        )

        sio.call(
            event,
            data,
            namespace=namespace
        )

    def exit(self):
        """
        Quit the CLI.
        """
        print("Bye!")
        sys.exit(0)
