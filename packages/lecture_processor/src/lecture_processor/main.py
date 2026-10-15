import base64
import json
from pathlib import Path

from lecture_processor.graph.graph import State

s = State.model_validate(json.loads(Path("./full_output.json").read_text()))
print(s.lecture_summary)
for res in s.results:
    if res.kind == "derivation":
        
    