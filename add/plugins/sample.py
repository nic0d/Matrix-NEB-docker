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
