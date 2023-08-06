from dg_ai_platform.example import HelloWorld

from dg_ai_platform.dg_platform import CaldronAI

ca = CaldronAI(HelloWorld, pid="97c683d44bd8320c6a9fa74134c9a2bb", public_key="aa8bd78952c2d677032d1598f990e86b")

ca.run()