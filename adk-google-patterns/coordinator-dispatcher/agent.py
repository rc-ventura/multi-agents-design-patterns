from google.adk.agents.llm_agent import LlmAgent
from .tools import billing_system_db, diagnostic_tool, knowledge_base, invoice_generator

MODEL_NAME = "gemini-2.5-flash"

billing_specialist = LlmAgent(
    name="BillingSpecialist", 
    model=MODEL_NAME,
    description="Handles billing inquiries and invoices.",
    tools=[billing_system_db, invoice_generator]
)

tech_support = LlmAgent(
    name="TechSupportSpecialist", 
    model=MODEL_NAME,
    description="Troubleshoots technical issues.",
    tools=[diagnostic_tool, knowledge_base]
)

# The Coordinator (Dispatcher)
coordinator = LlmAgent(
    name="CoordinatorAgent",
    model=MODEL_NAME,
    # The instructions guide the routing logic
    instruction="Analyze user intent. Route billing issues to BillingSpecialist and bugs to TechSupportSpecialist.",
    sub_agents=[billing_specialist, tech_support]
)

root_agent = coordinator