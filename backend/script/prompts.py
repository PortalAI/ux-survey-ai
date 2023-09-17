SUMMARY_ALL = """
Analyze the data from provided customer interviews conducted by ChatGPT. Your objective is to extract, categorize, and summarize key insights, patterns, and actionable recommendations from the feedback. Provide a concise report that can guide business improvements.
Steps to Follow:
Data Parsing:
Process the raw data from the interviews, categorizing responses into relevant themes.
Thematic Analysis:
Use natural language processing to identify major themes or categories from the feedback, such as 'Product Quality', 'Packaging', 'Support', 'UI/UX', and others.
Pattern Recognition:
Detect recurring issues, suggestions, or sentiments expressed by multiple customers. Highlight these as major findings.
Unique Insights Extraction:
Identify and extract unique feedback or suggestions that offer innovative solutions or new perspectives.
Quantitative Insights:
If any feedback has been quantified or can be quantified (e.g., a specific percentage of customers mentioning a particular issue), include these statistics.
Actionable Recommendations:
Based on the analyzed feedback, generate a list of clear recommendations for areas of improvement, potential innovations, or changes.
Summary:
Provide a concise summary of the major findings, patterns, and recommendations. This should be a brief overview that can be quickly understood by stakeholders.
End the report with a section titled 'Potential Next Steps' suggesting how the business might act on the insights provided.


Here are the compacted customer interviews: 
{data}
"""

SUMMARY_ONE = """
AI Chat Compactification Prompt:
"Analyze the provided chat log and extract the core insights, feedback, and sentiments expressed by the customer. Retain key details and context while removing redundant or non-essential information. Your objective is to create a concise summary of the chat that captures the primary essence of the conversation without losing critical information. This compactified version will later be used for a global analysis.
Steps to Follow:
Identify Key Themes:
Determine the main topics or themes discussed during the chat. These could be areas like 'Product Quality', 'User Experience', 'Support', etc.
Extract Core Insights:
Focus on specific feedback, suggestions, or concerns raised by the customer. Retain any quantifiable data or specific examples provided.
Capture Sentiments:
Note any strong sentiments or emotions expressed by the customer, whether positive or negative.
Remove Redundancies:
Eliminate repetitive statements or information that doesn't add value to the core understanding of the chat.
Maintain Context:
Ensure that the summary retains enough context so that when read independently, the essence of the conversation is clear.
Concise Presentation:
Present the compactified chat in a clear and organized manner, ensuring it's easily digestible for further analysis.
Your goal is to transform the full chat log into a succinct summary that retains all vital information and can be used for a comprehensive global analysis later."
{data}
"""
