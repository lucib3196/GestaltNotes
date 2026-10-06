from multimodal_llm import MultiModalLLM
from semantic_splitter.utils import to_serializable

from .model import Derivation

if __name__ == "__main__":
    import json
    from pathlib import Path

    from document_processing.converter import PDF2ImageConverter
    from dotenv import load_dotenv
    from langchain.chat_models import init_chat_model

    load_dotenv()
    model = init_chat_model(
        model_provider="google_genai",
        model="gemini-2.5-flash",
    )
    file = Path("lecture_processor/extract_derivations/output.pdf").resolve()

    result = MultiModalLLM(model).invoke(
        prompt="Extract the derivation in the image. For any math equations use latext delimited by $$ for block level math and $ for inline level math ",
        images=PDF2ImageConverter().convert(file),
        mime_type="image/png",
        output_model=Derivation,
    )
    print("RESULT\n", result)
    Path("./output.json").write_text(json.dumps(to_serializable(result)))
    der = Derivation.model_validate(json.loads(Path("./output.json").read_text()))
    print(der.as_string())
