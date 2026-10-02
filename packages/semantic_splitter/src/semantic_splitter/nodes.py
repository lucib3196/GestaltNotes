from langgraph.runtime import Runtime

from .state import SegmentationContext, State


def prepare(state: State, runtime: Runtime[SegmentationContext]) -> None:
    print("Preparing Document... ")


def analyze(state: State, runtime: Runtime[SegmentationContext]) -> None:
    print("Analyzing Document... ")


def chunk(state: State, runtime: Runtime[SegmentationContext]) -> None:
    print("Chunking Pages..")


def finalize(state: State, runtime: Runtime[SegmentationContext]) -> None:
    print("Finalizing....")
