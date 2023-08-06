from tracardi_plugin_sdk.domain.console import Console


class ActionRunner:

    debug = False
    event = None
    session = None
    profile = None
    flow = None
    flow_history = None
    console = Console()

    async def run(self, **kwargs):
        pass
