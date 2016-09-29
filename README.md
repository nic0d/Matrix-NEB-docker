# Develop Matrix bots using NEB

This document describes the setup of a Matrix bot based on NEB and running as a Docker container. NEB is an open source project to create a generic bot extendable through plugins. It is developed in Python and comes with some sample plugins. More documentation on NEB is available on [https://github.com/matrix-org/Matrix-NEB].

## Prerequisites

* Docker installed
* Matrix server running
* User account (standard) created in the Matrix server for the bot, with the associated *access token* (the access token can be found in the user account information in the Matrix web console under Settings > Information)

## Setup & Docker image creation

* Get the project code

```
git clone https://github.com/nic0d/Matrix-NEB-docker.git
cd Matrix-NEB-docker
```
* Create & edit configuration of the bot (./add/neb.conf). See neb.conf.sample.

```
{
    "url": "<synapse server url>",
    "user": "<bot user name> (eg: @NEB:matrix.org)",
    "token": "<token of the bot user>",
    "admins": ["<list of account that have admin rights (in the context of NEB bot)."]    
}
```
| Parameter   | Description |
| ----------- | ----------- |
| url         | URL of the matrix server |
| user        | User in the Matrix server that is used by the bot |
| token       | Access token of the Matrix user. It can be found in the user account information |
| admins      | List of accounts that will have *bot admin* rights, e.g. to invite the bot to a room.

* Docker image creation

```
docker build -t nic0d/matrix-neb-docker .
...
Successfully built <id>
```

## Run

```
docker run -it --rm -P -e GOOGLE_API_KEY=XXXXX nic0d/matrix-neb-docker:latest

2016-07-19 12:04:06,291 INFO:   ===== NEB initialising =====
2016-07-19 12:04:06,291 INFO: Loading config from /app/neb.conf
2016-07-19 12:04:06,292 DEBUG: Setting up plugins...
2016-07-19 12:04:06,292 DEBUG: add_plugin <class 'plugins.time_utils.TimePlugin'>
2016-07-19 12:04:06,292 DEBUG: add_plugin <class 'plugins.b64.Base64Plugin'>
2016-07-19 12:04:06,292 DEBUG: add_plugin <class 'plugins.guess_number.GuessNumberPlugin'>
2016-07-19 12:04:06,292 DEBUG: add_plugin <class 'plugins.TAIBot.TAIBot'>
2016-07-19 12:04:06,294 INFO: Running NebHookServer
2016-07-19 12:04:06,304 INFO:  * Running on http://0.0.0.0:8500/ (Press CTRL+C to quit)
2016-07-19 12:04:06,312 INFO: Startidocker run -it --rm -P dumontn/neb-tai:0.0.1ng new HTTP connection (1): matrix.tai.org
2016-07-19 12:04:06,366 DEBUG: "GET /_matrix/client/api/v1/initialSync?access_token=<token>&limit=1 HTTP/1.1" 200 None
2016-07-19 12:04:06,370 DEBUG: Notifying plugins of initial sync results
2016-07-19 12:04:06,370 INFO: Listening for incoming events.
2016-07-19 12:04:06,372 INFO: Starting new HTTP connection (1): matrix.tai.org
```

NB: The google graph commands requires a Google API key, which is given as a environment variable.

The following additional options might be useful:

| Option | Description |
| ------ | ----------- |
| --rm  | Useful when testing, but delete the container once it is stopped. |
| --add-host server_name:IP | Add a static name resolution in the /etc/hosts of the container. It is useful when the matrix server is not properly declared in DNS |
| -v host-dir:container-dir | Mount a volume from the host in the container. Can be used as a shared folder, or to store the code of the application being edited. |
| --entrypoint /bin/sh | Override the entrypoint of the container. Instead of starting the NEB application it starts a shell in the container, which allows to check different things (eg: dns resolution, existence of files, configurations, etc). The application can then be started using python neb.py -c conf_file

## Test the bot

Use a Matrix client to invite the bot user (eg: @NEB:matrix.org) to a room. Then try some of the commands provided by the default plugins, such as:

```
!tai graph beatles
```

## Add a new command

NEB proposes a simple way to add new commands. It defines an interface (./neb/plugins.PluginInterface) and base class (./neb/plugins.Plugin).
Adding a new command consists in:

1. Create a class extending Plugin
2. Define the name of the command
3. Define the command methods and parameters
4. Import and declare the command in the main

Here is an example of a simple Hello world command.

./add/plugins/sample.py
```python
from neb.plugins import Plugin
class SampleBot(Plugin):
    """Sample bot extension.
    sample hello <text>: Say hello to <text>
    """

    name="sample"

    def cmd_hello(self, event, *args):
        """sample hello <text>: Say hello to <text>"""

        to = event["content"]["body"][13:]

        result = "Hello %s !" % to
        print result
        return result
```

Declaration in ./add/neb.py
```python
...
from plugins.sample import SampleBot
...

def main(config):
    ...
    plugins = [
        ...
        TAIBot,
        SampleBot
    ]
    ...
```

## Next steps

Explore other capabilities of the Plugin Interface such as Webhook. (not implemented in the base class, but implemented in some commands (e.g. JIRA, GitHub)).
