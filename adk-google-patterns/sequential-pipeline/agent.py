from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from .tools import pdf_parser, regex_extractor, summary_engine


MODEL_NAME = "gemini-2.5-flash-lite"


# Step 1: Parse the PDF
parser = LlmAgent(
    name="ParserAgent",
    model=MODEL_NAME,
    instruction="Parse raw PDF and extract text.",
    tools=[pdf_parser],
    output_key="raw_text" 
)

# Step 2: Extract structured data
extractor = LlmAgent(
    name="ExtractorAgent",
    model=MODEL_NAME,
    instruction="Extract structured data from {raw_text}.",
    tools=[regex_extractor],
    output_key="structured_data"
)

# Step 3: Summarize
summarizer = LlmAgent(
    name="SummarizerAgent",
    model=MODEL_NAME,
    instruction="Generate summary from {structured_data}.",
    tools=[summary_engine]
)

# Orchestrate the Assembly Line
pipeline = SequentialAgent(
    name="PDFProcessingPipeline",
    sub_agents=[parser, extractor, summarizer]
)


root_agent = pipeline