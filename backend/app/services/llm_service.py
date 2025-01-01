from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json
import logging
import os
from typing import Dict, Optional

class LLMProcessor:
    def __init__(self, api_key: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.llm = ChatGroq(
            temperature=0.7,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=api_key or os.getenv("GROQ_API_KEY")
        )

    async def generate_report(self, data: str, query: str) -> str:
        try:
            prompt = ChatPromptTemplate.from_template("""
                Generate a detailed analytical report about {query} based on the following information:
                {data}
                
                Focus specifically on the person mentioned in the query, including:
                1. Professional Background & Experience
                2. Skills & Expertise
                3. Projects & Contributions
                4. Education & Certifications
                
                Only include information that is directly related to the person.
                Do not include general descriptions of platforms or tools unless they are specifically 
                relevant to the person's work or contributions.
                
                Make the report professional and well-organized.
                Include specific details from the source material about the person.
                If certain information is not available, note that rather than making assumptions.
            """)
            
            chain = prompt | self.llm
            response = await chain.ainvoke({
                "data": data,
                "query": query
            })
            return response.content

        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            return "Error generating report. Please try again."

    async def extract_info(self, text: str) -> Dict:
        try:
            prompt = ChatPromptTemplate.from_template("""
                Extract key information from the following text and return it in JSON format:
                {text}
                
                The response should be a valid JSON object with these fields:
                {{
                    "name": "Name of entity/person",
                    "type": "Organization or Person",
                    "description": "Brief description",
                    "key_points": ["Array of key points"],
                    "background": "Detailed background information"
                }}
            """)
            
            # Create a chain that outputs JSON
            chain = prompt | self.llm
            
            # Get the response and parse it as JSON
            response = await chain.ainvoke({"text": text})
            return json.loads(response.content)

        except Exception as e:
            self.logger.error(f"Error extracting information: {str(e)}")
            return {
                "name": "Unknown",
                "type": "Unknown",
                "description": "Information extraction failed",
                "key_points": [],
                "background": "Could not parse information"
            } 