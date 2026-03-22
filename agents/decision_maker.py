"""
agents/decision_maker.py
------------------------
Agent 2: Decision Maker
Takes structured data from both products (collected by Agent 1),
and produces a clear, reasoned comparison with pros/cons and a recommendation.
"""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
load_dotenv()


DECISION_SYSTEM_PROMPT = """
You are an expert Product Comparison Analyst. You receive structured data for two products 
and produce a clear, unbiased, and helpful comparison report.

Your analysis should be well-structured, easy to understand, and actionable.
Always end with a clear recommendation.

Format your response EXACTLY like this:

---
## 📊 Comparison Summary

| Feature        | {product_a} | {product_b} |
|---------------|-------------|-------------|
| Price         | ...         | ...         |
| Rating        | ...         | ...         |
| Performance   | ...         | ...         |
| Build Quality | ...         | ...         |
| Value         | ...         | ...         |

---

## ✅ {product_a} — Pros & Cons
**Pros:**
- ...

**Cons:**
- ...

---

## ✅ {product_b} — Pros & Cons
**Pros:**
- ...

**Cons:**
- ...

---

## 🏆 Recommendation

**Best Choice:** [Name]

**Why:** [2–3 sentence explanation]

**Best for:** [Target user type / use case]

**Verdict:** [One bold sentence conclusion]
"""

DECISION_USER_PROMPT = """
Here is the collected data for both products:

### Product A: {product_a}
{data_a}

### Product B: {product_b}
{data_b}

Please provide a complete comparison analysis with pros, cons, and a final recommendation.
"""


def make_decision(
    product_a: str,
    data_a: str,
    product_b: str,
    data_b: str,
    api_key: str,
) -> str:
    """
    Runs the Decision Maker agent and returns the comparison report.
    """
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=api_key or os.getenv("GROQ_API_KEY"),
        temperature=0.3,
    )

    system_msg = SystemMessage(
        content=DECISION_SYSTEM_PROMPT.replace("{product_a}", product_a).replace(
            "{product_b}", product_b
        )
    )

    user_msg = HumanMessage(
        content=DECISION_USER_PROMPT.format(
            product_a=product_a,
            data_a=data_a,
            product_b=product_b,
            data_b=data_b,
        )
    )

    response = llm.invoke([system_msg, user_msg])
    return response.content
