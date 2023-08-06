from tracardi_plugin_sdk.domain.console import Console


class ActionRunner:
    id = None
    debug = False
    event = None
    session = None
    profile = None
    flow = None
    flow_history = None
    console = None

    def __new__(cls, *args, **kwargs):
        o = super(ActionRunner, cls).__new__(cls, *args, **kwargs)
        o.console = Console()

    async def run(self, **kwargs):
        pass
