import operator
from dotenv import load_dotenv
from typing import Annotated, TypedDict, Dict, Any
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END


from tools import pdf_parser, regex_extractor, summary_engine

load_dotenv()
MODEL_NAME = "gemini-2.5-flash-lite"

# State
class SequentialState(TypedDict):
    file_path: str
    raw_text: str
    structured_data: Dict[str, Any]
    final_summary: str

# LLM
llm = ChatGoogleGenerativeAI(model=MODEL_NAME)

# Nodes
def parser_node(state: SequentialState):
    """Step 1: Parse the PDF using the existing tool."""
    file_path = state["file_path"]
    text = pdf_parser(file_path)
    return {"raw_text": text}

def extractor_node(state: SequentialState):
    """Step 2: Extract structured data using the existing tool."""
    text = state["raw_text"]
    data = regex_extractor(text)
    return {"structured_data": data}

def summarizer_node(state: SequentialState):
    """Step 3: Summarize using the existing tool."""
    data = state["structured_data"]
    summary = summary_engine(data)

    prompt = f"""Create a professional summary of this invoice data.
    
    Invoice Data: {data}
    """

    reponse = llm.invoke([HumanMessage(content=prompt)])
    return {"final_summary": reponse.content}

# Graph
workflow = StateGraph(SequentialState)

# Add nodes
workflow.add_node("parser", parser_node)
workflow.add_node("extractor", extractor_node)
workflow.add_node("summarizer", summarizer_node)

# Add edges
workflow.add_edge(START, "parser",)
workflow.add_edge("parser", "extractor")
workflow.add_edge("extractor", "summarizer")
workflow.add_edge("summarizer", END)

# Compile
app = workflow.compile()

# Show workflow
DIR = "lang-patterns/sequential-pipeline"
graph_image = app.get_graph().draw_mermaid_png()
with open(f"{DIR}/workflow.png", "wb") as f:
    f.write(graph_image)
print("📸 Graph saved as 'workflow.png'")


# Invoke
result = app.invoke({"file_path": f"{DIR}/invoice.pdf"})
print("🚀 Running Pipeline...")
print("\nStage 1: Parser")
print(result["raw_text"])
print("\nStage 2: Extractor")
print(result["structured_data"])
print("\nStage 3: Summarizer")
print(result["final_summary"])
