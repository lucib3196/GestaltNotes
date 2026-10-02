from .graph import InputState, SegmentationContext, build_graph

if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke(
        input=InputState(file="MyFile"), context=SegmentationContext(prompt="MyPrompt")
    )
