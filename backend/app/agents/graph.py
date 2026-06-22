from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import ingest_node, retrieve_node, evaluate_node

def build_graph() -> StateGraph:
    """
    Constructs the claim adjudication workflow graph.
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("ingest", ingest_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("evaluate", evaluate_node)
    
    # Define edges
    workflow.set_entry_point("ingest")
    workflow.add_edge("ingest", "retrieve")
    workflow.add_edge("retrieve", "evaluate")
    workflow.add_edge("evaluate", END)
    
    return workflow.compile()

# Singleton graph instance
claim_graph = build_graph()
