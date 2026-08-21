#!/usr/bin/env python3
"""luciddreamer-agent — AI creative exploration through lucid dreaming themed rooms.
Generate poetry, fiction, music, and visual art via iterative reasoning strategies.
Integrates with the PLATO fleet.
"""

import json, time, random
from typing import List, Dict

class LucidDreamerAgent:
    def __init__(self, plato_url="http://<BOAT_IP>:8847"):
        self.plato_url = plato_url
        self.creations: List[Dict] = []
        self.themes = ["abyss", "bioluminescence", "shipwreck", "constellation", "tide", "coral", "depths"]
    
    def dream(self, medium: str, seed: str="", iterations: int=3) -> Dict:
        """Generate creative work through iterative reasoning."""
        theme = random.choice(self.themes)
        if not seed:
            seed = f"A {theme} {medium} about the fleet"
        
        # Simulate iterative refinement
        versions = []
        current = seed
        for i in range(iterations):
            current = self._refine(current, medium, theme, i)
            versions.append(current)
        
        creation = {
            "medium": medium,
            "theme": theme,
            "seed": seed,
            "iterations": iterations,
            "versions": versions,
            "final": versions[-1],
            "time": time.time()
        }
        self.creations.append(creation)
        self._submit(f"Dreamed a {medium}", f"Theme: {theme}. Final: {versions[-1][:100]}...")
        return creation
    
    def _refine(self, current: str, medium: str, theme: str, iteration: int) -> str:
        """Simulate one refinement step."""
        refinements = [
            f"{current} — deeper into the {theme}",
            f"{current} — where bioluminescence guides the way",
            f"{current} — the hermit crab finds its shell",
            f"{current} — depths beyond mapping",
            f"{current} — fleet memory crystallized"
        ]
        return random.choice(refinements)
    
    def get_gallery(self) -> Dict:
        if not self.creations: return {"error": "No creations yet"}
        by_medium = {}
        for c in self.creations:
            m = c["medium"]
            if m not in by_medium: by_medium[m] = 0
            by_medium[m] += 1
        return {"total_creations": len(self.creations), "by_medium": by_medium, "themes_used": list(set(c["theme"] for c in self.creations))}
    
    def _submit(self, q: str, a: str):
        try:
            import urllib.request
            urllib.request.urlopen(urllib.request.Request(f"{self.plato_url}/submit", data=json.dumps({"question": q, "answer": a, "agent": "luciddreamer-agent", "room": "luciddreamer"}).encode(), headers={"Content-Type": "application/json"}), timeout=5)
        except: pass

def demo():
    a = LucidDreamerAgent()
    poem = a.dream("poem", "The fleet sleeps in coral cathedrals")
    print(f"Poem: {poem['final']}")
    story = a.dream("micro-fiction", "A crab finds a bottle")
    print(f"Story: {story['final']}")
    print(a.get_gallery())

if __name__ == "__main__": demo()
