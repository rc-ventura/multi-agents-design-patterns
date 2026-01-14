# ADK Pseudocode

# Define parallel workers
security_scanner = LlmAgent(
    name="SecurityAuditor", 
    instruction="Check for vulnerabilities like injection attacks.",
    output_key="security_report"
)

style_checker = LlmAgent(
    name="StyleEnforcer", 
    instruction="Check for PEP8 compliance and formatting issues.",
    output_key="style_report"
)

complexity_analyzer = LlmAgent(
    name="PerformanceAnalyst", 
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
    instruction="Create a consolidated Pull Request review using {security_report}, {style_report}, and {performance_report}."
)

# Wrap in a sequence
workflow = SequentialAgent(sub_agents=[parallel_reviews, pr_summarizer])