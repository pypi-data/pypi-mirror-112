# sockterm

A CLI terminal client for Socket.IO.

## Usage

Run `sockterm` to start the CLI. You should see a prompt: `sockterm>`

Type `connect {url}` to connect to a Socket.IO server.
For instance, to connect to a local Socket.IO server over WebSockets
on port 5000, type `connect ws://localhost:5000`.

To emit a message to the server, type `emit {event} {data}`. For example,
to emit a JSON message to the `hi_mom` event, type
`emit hi_mom '{ "mom": "hi" }'`. Note the single quotes.

You can also "call" an endpoint on the server by using `call {event} {data}`.
This is functionally the same as emit, but will block until the server
responds. It's useful for determining whether your requests are getting through
properly.

You can subscribe to a topic by typing `subscribe {event}`. This will output messages
on an event indefinitely. To stop the output, hit Ctrl+C until the output stops.
(Proper stoppage will be implemented later.)

Help can be shown by typing --help on any command, or by itself.

All publish/subscribe commands above accept an optional namespace argument.
To publish/subscribe on a non-default namespace, add `--namespace {namespace}`
to the command.
