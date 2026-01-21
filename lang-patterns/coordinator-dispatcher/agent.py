import operator
import os
import json
from dotenv import load_dotenv
from typing import Annotated, TypedDict, Dict, Any, Optional
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from tools import billing_system_db, diagnostic_tool, knowledge_base, invoice_generator

# Setup paths dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

MODEL_NAME = "gpt-4o-mini"

# State
class SupportState(TypedDict):
    user_query: str
    intent: str
    customer_name: Optional[str]
    amount_invoice: Optional[float]
    final_result: str

# LLM
#llm = ChatGoogleGenerativeAI(model=MODEL_NAME)
llm = ChatOpenAI(model=MODEL_NAME)

# Nodes
def coordinator_node(state: SupportState):
    """Analyze user intent. Route billing issues to BillingSpecialist and bugs to TechSupportSpecialist."""
    
    prompt = f"""
    You are a Support Coordinator.
    
    Task:
    1. Analyze the User Request.
    2. Classify intent into ONE of: ['billing', 'technical', 'general'].
    3. Extract 'customer_name' and 'amount_invoice' if present in the text.
    
    - If the user says "ola", "oi", "hello", or chats without a specific task, intent is 'general'.
    - If the user asks about invoices, payments, or money, intent is 'billing'.
    - If the user reports a bug, error, or system failure, intent is 'technical'.

    Output strictly in JSON format:
    {{
        "intent": "billing" | "technical" | "general",
        "customer_name": "name" or null,
        "amount_invoice": 100.0 or null,
        "reply": "Your response to the user if intent is general" or null
    }}
    
    User Request: {state['user_query']}
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        content = response.content.strip().replace("```json", "").replace("```", "")
        data = json.loads(content)
        intent = data.get("intent", "general").lower()
        new_name = data.get("customer_name")
        new_amount = data.get("amount_invoice")
        reply = data.get("reply")
        
        # Merge state
        name = new_name if new_name else state.get("customer_name")
        amount = new_amount if new_amount else state.get("amount_invoice")
        
    except Exception as e:
        print(f"DEBUG: JSON Parse Error: {e}")
        intent = "general"
        name = state.get("customer_name")
        amount = state.get("amount_invoice")
        reply = "I didn't understand. Could you rephrase?"

    return {
        "intent": intent, 
        "customer_name": name, 
        "amount_invoice": amount, 
        "final_result": reply if intent == "general" else state.get("final_result")
    }

def billing_node(state: SupportState):
    """Handle billing inquiries and invoices."""
    query = state["user_query"]
    customer_name = state.get("customer_name")
    amount_invoice = state.get("amount_invoice")
    
    if not customer_name or not amount_invoice:
        return {"final_result": "Please provide the Customer Name and Invoice Amount so I can proceed."}
    
    billing_info = billing_system_db(query)
    invoice = invoice_generator(customer_name, amount_invoice)
    return {"final_result": f"{billing_info}\n{invoice}"}
    
def technical_node(state: SupportState):
    """Troubleshoot technical issues."""
    issue = state["user_query"]
    diagnostics = diagnostic_tool(issue)
    kb = knowledge_base(issue)
    return {"final_result": f"{diagnostics}\n{kb}"}

def route_intent(state: SupportState):
    """Route based on intent."""
    intent = state["intent"]
    if intent in ["billing", "technical"]:
        return intent
    return "general"

# Graph
workflow = StateGraph(SupportState)

# Add nodes
workflow.add_node("coordinator", coordinator_node)
workflow.add_node("billing", billing_node)
workflow.add_node("technical", technical_node)

# Add edges
workflow.add_edge(START, "coordinator")

# Conditional Routing
workflow.add_conditional_edges(
    "coordinator", 
    route_intent,
    {
        "billing": "billing",
        "technical": "technical",
        "general": END
    }
)

workflow.add_edge("billing", END)
workflow.add_edge("technical", END)

# Compile
app = workflow.compile()

# Show workflow
DIR = "lang-patterns/coordinator-dispatcher"
graph_image = app.get_graph().draw_mermaid_png()
workflow_path = os.path.join(BASE_DIR, "workflow.png")
with open(workflow_path, "wb") as f:
    f.write(graph_image)
    print(f"📸 Graph saved as '{workflow_path}'")




# Chat Starting ...
print("\n💬 CHAT INICIADO")
print("Tente: 'Quero uma fatura', responda o nome, depois mude para 'Minha internet caiu'.")
print("Digite 'sair' para encerrar.\n")

session_state = {
        "user_query": "",
        "intent": "",
        "customer_name": None,
        "amount_invoice": None,
        "final_result": ""
    }

while True:
    user_input = input("👤 Usuário: ")
    if user_input.lower() == "sair":
        break

    # Update state
    session_state["user_query"] = user_input
    
    result = app.invoke(session_state)
    session_state = result

    print("🤖 Agent: ", result["final_result"])