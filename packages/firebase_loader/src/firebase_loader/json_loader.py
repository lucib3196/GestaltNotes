import json
from collections.abc import Callable, Iterator
from typing import Any
from google.cloud.storage import Bucket, Blob

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

JsonParser = Callable[[Any], Iterator[Document]]


class FirebaseJsonLoader(BaseLoader):
    def __init__(
        self,
        bucket: Bucket,
        *,
        prefix: str,
        parser: JsonParser,
    ):
        self.bucket = bucket
        self.prefix = prefix
        self.parser = parser

    def lazy_load(self) -> Iterator[Document]:
        for blob in self.bucket.list_blobs(prefix=self.prefix):
            if not blob.name.endswith(".json"):
                continue

            source = f"gs://{self.bucket.name}/{blob.name}"

            try:
                payload = json.loads(blob.download_as_bytes())

                for index, document in enumerate(self.parser(payload)):
                    yield Document(
                        page_content=document.page_content,
                        metadata={
                            **document.metadata,
                            "source": source,
                            "generation": str(blob.generation),
                            "record_index": index,
                        },
                    )
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(f"Could not parse JSON document at {source}") from exc


if __name__ == "__main__":
    print("Hi")
    # from firebase_admin import initialize_app
    # from firebase_admin import credentials
    # from firebase_admin import storage
    # from pathlib import Path

    # cred = credentials.Certificate(
    #     Path(
    #         r"/home/lberm/projects/gestalt/GestaltNotes/backend/FIREBASE_CRED.json"
    #     )
    # )
    # initialize_app(cred,{"storageBucket": "gestaltnotes.firebasestorage.app"})

    # def parser(data: Any) -> Iterator[Document]:
    #     print("Reading data", data)
    #     yield Document(
    #         page_content="",
    #         metadata={
    #             "note_id": str(123),
    #             "title": str("title"),
    #         },
    #     )

    # for doc in FirebaseJsonLoader(
    #     bucket=storage.bucket("gestaltnotes.firebasestorage.app"),
    #     prefix="",
    #     parser=parser,
    # ).lazy_load():
    #     print(doc)
