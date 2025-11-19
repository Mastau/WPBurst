class WPBurstModule:
    """
    Base class for all WPBurst modules.
    """
    name = "undefined"
    description = "No description"

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def run(self):
        raise NotImplementedError("Each module need implement run().")

