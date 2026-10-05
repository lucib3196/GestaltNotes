from lecture_processor.graph.graph import State
from pathlib import Path
import json
import base64
s = State.model_validate(json.loads(Path("./full_output.json").read_text()))
content = s.sections[0].document.content

pdf_bytes = base64.b64decode(content, validate=True)

Path("section.pdf").write_bytes(pdf_bytes)