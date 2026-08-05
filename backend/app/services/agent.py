from app.tools import TOOLS


class AgentService:

    def __init__(self):
        self.tools = TOOLS


    def list_tools(self):
        return list(self.tools.keys())


agent_service = AgentService()