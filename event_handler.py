from openai import AssistantEventHandler
from typing_extensions import override

class StreamlitAssistantEventHandler(AssistantEventHandler):
    def __init__(self, container):
        super().__init__()
        self.container = container
        self.message_placeholder = container.empty()
        self.full_response = ""
        
    @override
    def on_text_created(self, text) -> None:
        self.full_response = ""
        self.message_placeholder.markdown("▌")
    
    @override
    def on_text_delta(self, delta, snapshot):
        self.full_response += delta.value
        self.message_placeholder.markdown(self.full_response + "▌")
    
    @override
    def on_text_done(self, text) -> None:
        self.message_placeholder.markdown(self.full_response)
        
    @override
    def on_tool_call_created(self, tool_call):
        self.message_placeholder.markdown(f"Using tool: {tool_call.type}...")
        
    @override
    def on_exception(self, exception: Exception):
        self.message_placeholder.error(f"Error: {str(exception)}")
        
    @override
    def on_end(self):
        return self.full_response
