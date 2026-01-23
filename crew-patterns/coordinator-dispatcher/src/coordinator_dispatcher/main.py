#!/usr/bin/env python
import sys
import json
from pydantic import BaseModel, Field
from typing import Optional
from crewai.flow.flow import Flow, listen, start, router
from crewai import LLM

from coordinator_dispatcher.crews.billing_crew.billing_crew import BillingCrew
from coordinator_dispatcher.crews.tech_support_crew.tech_support_crew import TechSupportCrew

# Schema
class IntentResult(BaseModel):
    intent: str = Field(..., description="The classification: 'billing', 'technical', or 'general'.")
    customer_name: Optional [str] = Field(None, description="The Extracted name of the customer")
    amount_invoice: Optional [float] = Field(None, description="The Extracted amount of the invoice")
    reply: Optional[str] = Field(None, description="Friendly reply if intent is general")

# State
class SupportState(BaseModel):
    user_query: str = ""
    intent_result: Optional[IntentResult] = None
    final_result: str = ""
    

# Flow
class CoordinatorFlow(Flow[SupportState]):
    @start()
    def route_intent(self):
        """
        Analyze the user's request and route to the appropriate crew
        """
        print(f"🔍 Analyzing request: {self.state.user_query}")

        # agent coordinator
        llm = LLM(
            model="gpt-4o-mini",
            response_format=IntentResult
        )

        response = llm.call(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a Support Coordinator. Output ONLY JSON."
                },
                {
                    "role": "user", 
                    "content": f"""
                    Analyze this request: '{self.state.user_query}'
                    
                    Classify into ONE category:
                    - 'billing' (invoices, payments, money)
                    - 'technical' (bugs, errors, system failure)
                    - 'general' (greetings, others)
                    
                    Extract 'customer_name' and 'amount_invoice' if present.
                    """
                }
            ]
        )
        
        self.state.intent_result = response
        
        if self.state.intent_result.intent == "general":
            self.state.final_result = self.state.intent_result.reply

        print(f"🚦 Routing to: {self.state.intent_result.intent}")
        return self.state.intent_result.intent


    @router(route_intent)
    def route_node(self):
        """
        Route the flow to the appropriate crew based on the intent
        """
        intent = self.state.intent_result.intent
        
        if intent == "billing":
            return "billing_branch"
        elif intent == "technical":
            return "technical_branch"
        elif intent == "general":
            return "general_branch"
    
    @listen("billing_branch")
    def run_billing_crew(self):
        """
        Run the billing crew
        """
        print("💰 Activating Billing Crew")

        inputs= {
            "query": self.state.user_query,
            "customer_name": self.state.intent_result.customer_name,
            "amount_invoice": self.state.intent_result.amount_invoice
        }
       
        result = BillingCrew().crew().kickoff(inputs=inputs) 
        
        self.state.final_result = result.raw
    
    @listen("technical_branch")
    def run_tech_support_crew(self):
        """
        Run the tech support crew
        """
        print("🛠️ Activating Tech Crew")
        result = TechSupportCrew().crew().kickoff(inputs={"query": self.state.user_query})
        self.state.final_result = result.raw


    @listen("general_branch")
    def run_general_crew(self):
        """
        Run the general crew
        """
        print("General response")
        if not self.state.final_result:
            self.state.final_result = "How can I help you today?"

def plot():
    """Generate a visualization of the flow """
    flow = CoordinatorFlow()
    flow.plot("coordinator_flow")
    print("Flow plotted successfully.")

def kickoff():
    """ Run the flow """
    print("🤖 Coordinator Dispatcher System Initialized")
    print("Type 'exit', 'quit' or 'sair' to stop.")
    
    while True:
        try:
            query = input("\n👤 Enter your request: ")
            if query.lower() in ['exit', 'quit', 'sair']:
                print("� Exiting...")
                break
                
            if not query.strip():
                continue
                
            print(f"🚀 Processing: '{query}'")
            flow = CoordinatorFlow()
            flow.kickoff(inputs={"user_query": query})
            print(f"🏁 Final Result: {flow.state.final_result}")
            
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    kickoff()
