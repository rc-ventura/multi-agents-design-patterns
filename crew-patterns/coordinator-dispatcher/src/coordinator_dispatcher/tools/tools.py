from crewai.tools import tool

@tool("Billing System DB")
def billing_system_db(query: str) -> str:
    """
    Queries the billing system database for invoice or payment information.
    
    Args:
        query: The search query or invoice ID.
        
    Returns:
        Billing information string.
    """
    return f"Mock Billing DB Result for '{query}': Invoice #9999 paid on 2023-12-01. Balance: $20.00."


@tool("Diagnostic Tool")
def diagnostic_tool(issue: str) -> str:
    """
    Runs system diagnostics to troubleshoot technical issues.
    
    Args:
        issue: Description of the technical issue.
        
    Returns:
        Diagnostic report.
    """
    return f"Mock Diagnostic Report for '{issue}': System latency normal. No packet loss detected. Suggest clearing cache."


@tool("Knowledge Base")
def knowledge_base(query: str) -> str:
    """
    Searches the technical support knowledge base for articles and solutions.
    
    Args:
        query: The topic or error message to search for.
        
    Returns:
        Relevant knowledge base articles.
    """
    return f"Mock Knowledge Base Result for '{query}': Article 1, Article 2."

@tool("Invoice Generator")
def invoice_generator(customer_name: str, amount: float) -> str:
    """
    Generates a new invoice for a customer.
    
    Args:
        customer_name: Name of the customer.
        amount: The amount to be billed.
        
    Returns:
        Confirmation message with the new invoice ID.
    """
    return f"Mock Invoice Generator: Created Invoice #10001 for {customer_name} with amount ${amount}."
