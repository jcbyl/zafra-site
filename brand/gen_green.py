#!/usr/bin/env python3
"""Zafra emblems, Areito-seal style: gold engraving on deep forest green field.
Round medallion compositions only (no square plates). 8 renders, 4 concepts."""
import os, json, time, urllib.request

FAL_KEY = [l.split("=",1)[1].strip() for l in open(os.path.expanduser("~/.hermes/.env")) if l.startswith("FAL_KEY=")][0]
TMP = "/tmp/zafra-fal"
os.makedirs(TMP, exist_ok=True)

BASE = ("Vintage engraved circular medallion emblem, fine metallic gold "
        "copper-plate etching and cross-hatching on a deep dark forest green "
        "field, {scene}, ornate thin gold circular border, perfectly round "
        "composition filling the frame, antique trading company seal, "
        "no text, no letters, no words")

CONCEPTS = [
    ("g1", BASE.format(scene="radiant sun with rays rising over layered mountain ridges, coffee branch with red cherries across the foreground")),
    ("g2", BASE.format(scene="mountain landscape encircled by a wreath of coffee branches with leaves and cherries")),
    ("g3", BASE.format(scene="crossed sugar cane stalks and coffee branches beneath a rising sun, harvest motif")),
    ("g4", BASE.format(scene="terraced plantation hillsides with a winding path and sun on the horizon")),
]

def gen(seed):
    prompt = CONCEPTS[i][1] if False else None

results = []
for name, prompt in CONCEPTS:
    for k in range(2):
        seed = 4000 + hash((name, k)) % 90000
        body = json.dumps({
            "prompt": prompt, "image_size": "square_hd",
            "num_inference_steps": 28, "guidance_scale": 3.5, "seed": seed,
        }).encode()
        req = urllib.request.Request(
            "https://fal.run/fal-ai/flux/dev", data=body,
            headers={"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as r:
            img = r.read()
        fn = os.path.join(TMP, f"{name}{k+1}.jpg")
        open(fn, "wb").write(img)
        print(name, k+1, "seed", seed, len(img), "bytes")
        results.append(fn)

print("DONE", len(results))
