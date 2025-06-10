"""
Core chatbot logic for the TalentScout Hiring Assistant.
"""

import os
from typing import Dict, List, Optional
import openai
from dotenv import load_dotenv
from prompts import (
    INITIAL_GREETING,
    TECH_STACK_PROMPT,
    get_tech_questions_prompt,
    get_follow_up_prompt,
    CONVERSATION_END,
    ERROR_HANDLING
)
from utils import (
    parse_candidate_info,
    is_conversation_ending,
    format_tech_stack
)

# Initialize OpenAI client with API key
openai.api_key = "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"

class HiringAssistant:
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.candidate_info: Dict = {}
        self.current_state = "greeting"
        self.tech_stack: Optional[str] = None
        self.technical_questions: List[str] = []
        self.current_question_index = 0
        self.required_info = {
            "name": False,
            "email": False,
            "phone": False,
            "experience": False,
            "position": False,
            "location": False
        }
        self.first_interaction = True

    def get_ai_response(self, prompt: str, system_prompt: str = None) -> str:
        """Get response from OpenAI API."""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting AI response: {e}")
            return ERROR_HANDLING

    def get_natural_response(self, user_input: str, context: str) -> str:
        """Get a natural, conversational response from the LLM."""
        system_prompt = """You are a friendly and professional hiring assistant. 
        Your goal is to gather information from candidates in a natural, conversational way.
        Be warm and engaging while maintaining professionalism.
        If you need more information, ask for it naturally without being too formal.
        Always acknowledge what the user has shared before asking for more information.
        If the user just says 'hi' or similar greetings, respond warmly and guide them to share their information."""
        
        prompt = f"""Context: {context}
        User's last message: {user_input}
        Please respond in a natural, conversational way while gathering the required information."""
        
        return self.get_ai_response(prompt, system_prompt)

    def process_message(self, user_input: str) -> str:
        """Process user input and return appropriate response."""
        # Check for conversation ending
        if is_conversation_ending(user_input):
            return CONVERSATION_END

        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_input})

        # Handle first interaction
        if self.first_interaction:
            self.first_interaction = False
            return "Hello! I'm your AI hiring assistant. I'd love to learn more about you. Could you please share your name and what position you're interested in?"

        # Process based on current state
        if self.current_state == "greeting":
            # Parse candidate information
            info = parse_candidate_info(user_input)
            
            # Update required info status
            if info.get("email"):
                self.required_info["email"] = True
                self.candidate_info["email"] = info["email"]
            if info.get("phone"):
                self.required_info["phone"] = True
                self.candidate_info["phone"] = info["phone"]
            if info.get("years_experience"):
                self.required_info["experience"] = True
                self.candidate_info["years_experience"] = info["years_experience"]
            if info.get("name"):
                self.required_info["name"] = True
                self.candidate_info["name"] = info["name"]
            if info.get("position"):
                self.required_info["position"] = True
                self.candidate_info["position"] = info["position"]
            if info.get("location"):
                self.required_info["location"] = True
                self.candidate_info["location"] = info["location"]
            
            # Check if we have all required information
            missing_info = [k for k, v in self.required_info.items() if not v]
            
            if missing_info:
                # Create context for natural response
                context = f"""Current information gathered:
                {', '.join([f'{k}: {v}' for k, v in self.candidate_info.items()])}
                Still need: {', '.join(missing_info)}"""
                
                return self.get_natural_response(user_input, context)
            else:
                self.current_state = "tech_stack"
                return TECH_STACK_PROMPT

        elif self.current_state == "tech_stack":
            self.tech_stack = user_input
            formatted_stack = format_tech_stack(user_input)
            
            # Generate technical questions
            prompt = get_tech_questions_prompt(
                tech_stack=", ".join(formatted_stack),
                years_experience=self.candidate_info.get("years_experience", 0)
            )
            questions = self.get_ai_response(prompt)
            self.technical_questions = questions.split("\n")
            self.current_state = "technical_questions"
            return self.technical_questions[0]

        elif self.current_state == "technical_questions":
            # Generate follow-up question
            follow_up_prompt = get_follow_up_prompt(user_input)
            follow_up = self.get_ai_response(follow_up_prompt)
            
            self.current_question_index += 1
            if self.current_question_index >= len(self.technical_questions):
                self.current_state = "conclusion"
                return CONVERSATION_END
            
            return follow_up + "\n\n" + self.technical_questions[self.current_question_index]

        else:
            return ERROR_HANDLING

    def get_initial_greeting(self) -> str:
        """Get the initial greeting message."""
        return "👋 Welcome to TalentScout! I'm your AI hiring assistant. I'm here to help you through the application process. How can I assist you today?" 