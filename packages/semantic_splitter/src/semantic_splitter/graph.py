from langgraph.graph import END, START, StateGraph

from .nodes import analyze, chunk, finalize, prepare
from .state import InputState, SegmentationContext, State


def build_graph():
    builder = StateGraph(
        state_schema=State, input_schema=InputState, context_schema=SegmentationContext
    )
    builder.add_node("prepare", prepare)
    builder.add_node("analyze", analyze)
    builder.add_node("chunk", chunk)
    builder.add_node("finalize", finalize)

    builder.add_edge(START, "prepare")
    builder.add_edge("prepare", "analyze")
    builder.add_edge("analyze", "chunk")
    builder.add_edge("chunk", "finalize")
    builder.add_edge("finalize", END)
    return builder.compile()
