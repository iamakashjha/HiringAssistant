# TalentScout Hiring Assistant

An intelligent chatbot designed to assist in the initial screening of candidates for TalentScout, a fictional recruitment agency specializing in technology placements.

## Features

- Interactive chat interface using Streamlit
- Intelligent candidate information gathering
- Dynamic technical question generation based on tech stack
- Context-aware conversation handling
- Secure data handling and privacy compliance

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd talentscout-hiring-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Interact with the chatbot by:
   - Providing your personal information
   - Specifying your tech stack
   - Answering technical questions
   - Using "exit" or "quit" to end the conversation

## Technical Details

### Libraries Used
- Streamlit: Frontend interface
- OpenAI: Language model integration
- Python-dotenv: Environment variable management
- Pandas: Data handling

### Architecture
The application follows a modular architecture with the following components:
- `app.py`: Main application entry point
- `chatbot.py`: Core chatbot logic and conversation handling
- `prompts.py`: Prompt templates and management
- `utils.py`: Utility functions and helpers

### Prompt Design
The chatbot uses carefully crafted prompts to:
1. Gather candidate information systematically
2. Generate relevant technical questions based on tech stack
3. Maintain conversation context
4. Handle edge cases and unexpected inputs

## Data Privacy
- All candidate data is handled in compliance with GDPR
- No personal information is stored permanently
- Data is processed in-memory during the session only

## Challenges & Solutions

### Challenge 1: Context Management
Solution: Implemented a conversation history tracking system that maintains context while preventing memory leaks.

### Challenge 2: Dynamic Question Generation
Solution: Created a flexible prompt template system that adapts to various tech stacks and experience levels.

### Challenge 3: User Experience
Solution: Designed an intuitive interface with clear instructions and feedback mechanisms.

## Contributing
Feel free to submit issues and enhancement requests!

## License
This project is licensed under the MIT License - see the LICENSE file for details. 