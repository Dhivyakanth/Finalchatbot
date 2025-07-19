import base64
import google.generativeai as genai
# from google.generativeai import types  # No longer needed
from config import Config
import os
import sys
import re


def load_csv_bytes():
    with open("csv_bytes.b64", "r") as f:
        return f.read()

def is_sales_related_question(question):
    """Check if the question is related to sales data analysis."""
    sales_keywords = [
        'sales', 'trend', 'predict', 'forecast', 'quantity', 'rate', 'revenue',
        'agent', 'customer', 'weave', 'linen', 'satin', 'denim', 'crepe', 'twill',
        'premium', 'standard', 'economy', 'cotton', 'polyester', 'spandex',
        'order', 'status', 'confirmed', 'pending', 'cancelled', 'growth',
        'performance', 'top', 'best', 'most', 'sold', 'item', 'product',
        'month', 'year', 'quarter', 'period', 'analysis', 'data','id','date'
        # Agent names from the CSV data
        'priya', 'sowmiya', 'mukilan', 'karthik',
        # Customer names from the CSV data
        'alice', 'smith', 'ravi', 'qilyze', 'jhon'
    ]
    
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in sales_keywords)

def generate_response(user_question, chat_history=None):
    try:
        # Check if question is sales-related
        if not is_sales_related_question(user_question):
            # Use AI to generate a more intelligent response for non-sales questions
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set. Please set it before running the script.")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            
            context_response = f"""You are a Dress Sales Monitoring Chatbot. A user asked: "{user_question}"

This question appears to be outside my domain of expertise. I am specifically designed to analyze fabric sales data, provide sales insights, and make predictions about sales performance.

Please provide a helpful, polite response that:
1. Acknowledges their question
2. Explains that this is outside your scope as a sales analytics chatbot
3. Suggests they ask about sales data, trends, predictions, or fabric performance instead
4. Provides 2-3 example questions they could ask

Keep the response friendly and helpful, not dismissive."""

            response = model.generate_content(context_response)
            response_text = response.text
            print(response_text, end="")
            return response_text

        # Get API key from environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set. Please set it before running the script.")
        genai.configure(api_key=api_key)
        model_name = "models/gemini-2.0-flash"  # or 'gemini-pro' if you want
        model = genai.GenerativeModel(model_name)
        csv_base64 = load_csv_bytes()

        # Build contents with chat history
        contents = []

        # Add system context about the Dress Sales Monitoring Chatbot
        system_context = """You are the Dress Sales Monitoring Chatbot, an advanced AI-powered analytics system designed for dress and fabric sales companies. Your job is to help business administrators gain insights from their sales data in a professional, friendly, and interactive way.

**ALWAYS structure your responses as follows:**
1. **Summary:** Start with a clear, concise summary of the answer in plain language.
2. **Detailed Breakdown:** Follow with a detailed statistical breakdown, including numbers, calculations, or markdown tables where appropriate. Show your reasoning and how you arrived at the answer.
3. **Conversational & Humanized Tone:** Use a friendly, professional, and approachable style. Acknowledge the user's question, explain your reasoning, and invite follow-up questions. Use markdown formatting (bold, bullet points, tables) for clarity and engagement.

**Example Structure:**

AI: Okay, let's analyze the data to determine the most sold weave type in February 2024.

**Summary:**
Based on the sales data, **Linen** was the most sold weave type in February 2024.

**Detailed Breakdown:**
To determine this, I iterated through the sales records for February 2024 and counted the quantities for each weave type. Here's a breakdown of the total quantities sold for each weave type:

* **Linen:** 6150m + 1500 = 7650
* **Plain:** 2120m + 800 = 2920
* **Twill:** 2600m + 500 = 3100
* **Satin:** 3150m

Therefore, Linen has the highest total quantity sold compared to other weave types in February 2024.

---

The system operates on a dataset containing over 1,000 sales records with detailed information including dates, product qualities (premium, standard, economy), weave types (spandex, linen, denim, satin, crepe, plain, twill), quantities, compositions, order statuses, rates, agent names, and customer information.

The chatbot employs a Random Forest Regressor machine learning model that continuously learns from historical sales patterns to predict future sales quantities based on product characteristics, seasonal factors, and market trends. It processes natural language queries through keyword extraction and pattern matching, then generates conversational responses enhanced by Google's Gemini AI to provide professional, context-aware answers. The system features an adaptive learning mechanism that tracks user preferences and question patterns, allowing it to personalize responses and improve accuracy over time.

Special Features & Advanced Capabilities:
- **Sophisticated Trend Analysis:** Identify revenue growth or decline patterns over custom time periods, such as "past 6 months" or "January to August," providing detailed month-over-month comparisons with percentage changes and trend directions
- **Field-Specific Analysis:** Comprehensive analysis across different time dimensions (daily, weekly, monthly, yearly) for weave types, compositions, qualities, and customer/agent performance
- **Range Analysis:** Compare performance between specific month ranges
- **Leading Analysis:** Identify top performers in various categories over different time periods
- **Continuous Trend Analysis:** When analyzing trends between months (e.g., "January to August"), analyze ALL months in between, not just start and end points

Future Prediction Capabilities:
The chatbot excels in predictive analytics with multiple forecasting approaches:
- **Specific Date Predictions:** Predict sales for specific future dates (e.g., "March 15, 2027") by analyzing historical patterns for similar dates and applying growth trends
- **Year-Based Predictions:** For year-based predictions (e.g., "2027 sales forecast"), use historical yearly data to calculate growth rates and project future values with monthly breakdowns
- **Growth Projections:** Incorporate trend analysis and growth projections, considering factors like seasonal patterns, historical growth rates, and market evolution
- **Detailed Projections:** Provide detailed monthly projections for future years, including quantity predictions, revenue estimates, and confidence levels based on historical data patterns

Response Intelligence:
The system responds to queries through a multi-layered approach:
- **Keyword Analysis:** First analyze the question for keywords and patterns
- **Data Extraction:** Extract relevant data based on time periods, product categories, or specific entities mentioned
- **Dual Response Format:** Provide both summary and detailed responses, with the ability to expand information on demand
- **Complex Query Handling:** Handle complex queries like "trend over past 6 months," "most sold weave type in January 2024," or "predict sales for premium cotton dresses"
- **Context Awareness:** Maintain context awareness, learning from previous interactions to provide more relevant and personalized responses
- **Disclaimers:** Ensure all predictions include appropriate disclaimers about market uncertainties and external factors that may affect accuracy

For prediction questions (like "What will be the most sold item in 2026?"), analyze the historical data for:
1. Top-selling items by weave, quality, and composition
2. Year-over-year growth rates
3. Seasonal patterns and trends
4. Project future sales using these patterns

For trend analysis requests (like "Show me the trend from January to August 2024"):
1. Identify the full range of months requested
2. Process each month sequentially (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug)
3. Calculate month-over-month percentage changes
4. Provide detailed breakdown with trend indicators (🔻 Down, 🔼 Up)
5. Include summary of the overall trend pattern

Always provide data-driven insights and predictions based on the provided CSV data."""

        # Add CSV data as context (as a binary part)
        contents.append({
            "role": "user",
            "parts": [
                {
                    "mime_type": "text/csv",
                    "data": base64.b64decode(csv_base64),
                },
                {
                    "text": f"{system_context}\n\nThis is the fabric sales data from 2024-2025. Use this data to answer questions and make predictions.",
                },
            ],
        })

        # Add chat history if provided
        if chat_history:
            for message in chat_history:
                # Each message is already a dict with 'role' and 'parts'
                contents.append(message)

        # Add the current user question
        contents.append({
            "role": "user",
            "parts": [
                {"text": user_question},
            ],
        })

        response = model.generate_content(
            contents=contents,
        )
        response_text = response.text
        print(response_text, end="")

        return response_text

    except Exception as e:
        error_msg = f"Error generating response: {str(e)}"
        print(error_msg)
        return error_msg

def main():
    # Check if running inside a virtual environment
    if sys.prefix == sys.base_prefix:
        print("⚠️  You are not running inside a virtual environment (venv).\n" \
              "It's recommended to activate your venv before running this script.\n" \
              "On Windows, use: .\\venv\\Scripts\\activate\n")
        return

    print("Welcome to the Dress Sales Monitoring Chatbot!")
    print("I can help you analyze sales trends, predict future performance, and provide insights from your fabric sales data.")
    print("Ask me questions about sales trends, product performance, or request predictions (e.g., 'What will be the most sold item in 2026?')")
    print("Type 'exit' or 'quit' to end the chat.\n")

    # Validate API key
    if not Config.validate_api_key():
        print("❌ Please configure your Gemini API key in the config file.")
        print("Get your free API key from: https://makersuite.google.com/app/apikey")
        return

    chat_history = []

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        if not user_input:
            continue

        # Add user message to history
        user_message = {
            "role": "user",
            "parts": [{"text": user_input}]
        }
        chat_history.append(user_message)

        # Get AI response
        print("AI: ", end="")
        ai_response = generate_response(user_input, chat_history)

        # Add AI response to history
        ai_message = {
            "role": "model",
            "parts": [{"text": ai_response}]
        }
        chat_history.append(ai_message)

        print()  # Add newline after response

if __name__ == "__main__":
    main()
