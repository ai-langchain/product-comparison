"""
agents/data_collector.py
------------------------
Agent 1: Data Collector
Uses modern LCEL-based agent (LangChain 0.3+)
"""



from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from tools.product_fetcher import fetch_product_data
from dotenv import load_dotenv
load_dotenv()


SYSTEM_PROMPT = """You are a Product Data Collector Agent. Your job is to gather 
detailed, structured information about a product using your knowledge.

Return a structured report with these exact sections:
- **Product Name**: 
- **Category**: 
- **Price Range**: (e.g., ₹15,000 – ₹20,000 or $200 – $250)
- **Key Specifications**: (bullet list of 5–8 specs)
- **User Ratings**: (out of 5, with brief sentiment)
- **Availability**: (Online/Offline/Both)
- **Target Audience**: 
"""


def collect_product_data(product_name: str, api_key: str = None) -> str:
    """
    Uses ChatGroq directly to collect structured product data.
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=api_key or os.getenv("GROQ_API_KEY"),
        temperature=0.2,
    )

    # Try to fetch web snippet first
    try:
        web_data = fetch_product_data.invoke(product_name)
    except Exception:
        web_data = ""

    user_content = f"""Research this product and return a structured profile.

Product: {product_name}

Additional web context (if available):
{web_data}

Now return the full structured profile."""

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ])

    return response.content