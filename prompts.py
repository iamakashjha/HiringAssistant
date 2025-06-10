"""
Prompt templates for the TalentScout Hiring Assistant chatbot.
"""

INITIAL_GREETING = """Hello! I'm the TalentScout Hiring Assistant. I'm here to help gather some initial information about you and assess your technical skills. 
Let's start with some basic information. Please provide your:
1. Full Name
2. Email Address
3. Phone Number
4. Years of Experience
5. Desired Position(s)
6. Current Location

You can provide this information in any format you prefer."""

TECH_STACK_PROMPT = """Great! Now, could you please list your technical skills? Include:
- Programming languages
- Frameworks
- Databases
- Tools and technologies
- Any other relevant technical skills

Please be specific about your proficiency level in each technology."""

TECHNICAL_QUESTION_PROMPT = """Based on the candidate's tech stack: {tech_stack}
Generate 3-5 technical questions that assess their proficiency in these technologies.
Focus on practical knowledge and problem-solving abilities.
Make the questions challenging but appropriate for their stated experience level of {years_experience} years.

Format the questions as a numbered list."""

FOLLOW_UP_PROMPT = """Based on the candidate's previous answer: {previous_answer}
Generate a follow-up question that:
1. Probes deeper into their understanding
2. Challenges their assumptions
3. Explores real-world application of their knowledge

Keep the question focused and relevant to their tech stack."""

CONVERSATION_END = """Thank you for your time! I've gathered all the necessary information. 
A member of our recruitment team will review your profile and get back to you within 2-3 business days.
Is there anything else you'd like to know before we end this conversation?"""

ERROR_HANDLING = """I apologize, but I didn't quite understand that. Could you please:
1. Rephrase your response
2. Provide the information in a clearer format
3. Or let me know if you need clarification on what information I'm looking for"""

def get_tech_questions_prompt(tech_stack: str, years_experience: int) -> str:
    """Generate a prompt for technical questions based on tech stack and experience."""
    return TECHNICAL_QUESTION_PROMPT.format(
        tech_stack=tech_stack,
        years_experience=years_experience
    )

def get_follow_up_prompt(previous_answer: str) -> str:
    """Generate a follow-up question prompt based on previous answer."""
    return FOLLOW_UP_PROMPT.format(previous_answer=previous_answer) 