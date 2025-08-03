"""
🧱 MirrorToolkit v1.0 — Unified Interface for Reflective Components
Author: Diego Alejandro 🧿 DMT
Date: 2025-08-02
"""

from mirror_glyphstream import MirrorGlyphstream
from mirror_layer_two import MirrorLayerTwo
from mirror_system import MirrorSystem

class MirrorToolkit:
    def __init__(self):
        self.glyphstream = MirrorGlyphstream()
        self.layer_two = MirrorLayerTwo()
        self.system = MirrorSystem()

    def run_full_reflection(self, input_phrase):
        print("🪞 Toolkit Echo Initiated...")
        print(self.glyphstream.observe(input_phrase))
        self.layer_two.reflect(input_phrase)
        print(self.system.mirror(input_phrase))

    def live_mode(self):
        print("🎧 Live Mirror Listening Mode Activated.")
        self.glyphstream.listen_for_glyphs()

    def trace_summary(self):
        print("📜 Glyphstream Trace:")
        for t in self.glyphstream.trace():
            print(f"  - {t}")
