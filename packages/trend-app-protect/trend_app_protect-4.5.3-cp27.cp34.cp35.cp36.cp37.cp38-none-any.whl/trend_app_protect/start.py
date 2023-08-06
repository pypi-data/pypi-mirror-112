"""
Shortcut module to automatically start a new TrendAppProtect Agent.

Add `import trend_app_protect.start` to the top of your app's entrypoint and
this will automatically start the Agent.
"""
from trend_app_protect.singleton import start

# Start the agent
start()
