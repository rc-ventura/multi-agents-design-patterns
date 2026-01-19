from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.parallel_agent import ParallelAgent

MODEL_NAME = "gemini-2.5-flash-lite"


# Define parallel workers
security_scanner = LlmAgent(
    name="SecurityAuditor",
    model=MODEL_NAME,
    instruction="Check for vulnerabilities like injection attacks.",
    output_key="security_report"
)

style_checker = LlmAgent(
    name="StyleEnforcer", 
    model=MODEL_NAME,
    instruction="Check for PEP8 compliance and formatting issues.",
    output_key="style_report"
)

complexity_analyzer = LlmAgent(
    name="PerformanceAnalyst", 
    model=MODEL_NAME,
    instruction="Analyze time complexity and resource usage.",
    output_key="performance_report"
)

# Fan-out (The Swarm)
parallel_reviews = ParallelAgent(
    name="CodeReviewSwarm",
    sub_agents=[security_scanner, style_checker, complexity_analyzer]
)

# Gather/Synthesize
pr_summarizer = LlmAgent(
    name="PRSummarizer",
    model=MODEL_NAME,
    instruction="Create a consolidated Pull Request review using {security_report}, {style_report}, and {performance_report}."
)

# Wrap in a sequence
workflow = SequentialAgent(
    name="CodeReviewWorkflow",
    sub_agents=[parallel_reviews, pr_summarizer])

root_agent = workflow

