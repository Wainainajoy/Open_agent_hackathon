try:
    from . import agent  # ADK loads the agent from here
except ImportError:  # lets sample_demo.py run without google-adk installed
    pass
