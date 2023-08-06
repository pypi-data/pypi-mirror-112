from dg_ai_platform.example import ExampleTask
from dg_ai_platform.dg_platform import CaldronAI

ca = CaldronAI('pid', 'pky', ExampleTask)
ca.run()