# mcpadapt/crewai_adapter.py

class CrewAIAdapter:
    """Minimal adapter to satisfy MCPAdapt integration."""
    
    def preprocess_arguments(self, args: dict):
        return args

    def postprocess_result(self, result: dict):
        return result
