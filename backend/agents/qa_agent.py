"""
Quality Assurance Agent - Confidence Score and Quality Feedback
Reviews generated emails and provides scores with specific feedback
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, List
import json

class ConfidenceScoreAgent:
    """Reviews email quality and provides confidence scores"""
    
    def __init__(self, groq_api_key: str = None):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=groq_api_key,
            temperature=0.3  # Lower temp for consistent scoring
        )
    
    def review_email(self, email_subject: str, email_body: str, 
                     company: str, prospect_info: Dict = None) -> Dict:
        """
        Review an email and provide quality scores and feedback
        
        Returns:
            {
                "overall_score": 75,
                "subject_line_score": 7,
                "body_quality_score": 8,
                "personalization_score": 6,
                "call_to_action_score": 8,
                "issues_found": [...],
                "recommendations": [...],
                "feedback": {...}
            }
        """
        prompt = ChatPromptTemplate.from_template("""You are an expert sales email quality reviewer. 
        Analyze this email and provide detailed quality feedback.
        
        Company: {company}
        Prospect Info: {prospect_info}
        
        Subject Line: {subject}
        Email Body:
        {body}
        
        Score the following on a scale of 0-10 (for personalization)/ 0-100 (for overall):
        1. Overall email quality (0-100)
        2. Subject line effectiveness (0-10)
        3. Body copy quality (0-10)
        4. Personalization level (0-10) 
        5. Call-to-action strength (0-10)
        
        Identify specific issues:
        - Subject line problems
        - Weak personalization elements
        - Missing or unclear CTAs
        - Tone issues
        - Length problems
        
        Provide 3-5 specific, actionable recommendations with examples.
        
        Format your response as JSON with this exact structure:
        {{
            "overall_score": <number>,
            "subject_line_score": <number>,
            "body_quality_score": <number>,
            "personalization_score": <number>,
            "call_to_action_score": <number>,
            "subject_feedback": "<specific feedback>",
            "body_feedback": "<specific feedback>",
            "personalization_feedback": "<specific feedback>",
            "cta_feedback": "<specific feedback>",
            "issues_found": [
                {{"issue": "<issue description>", "severity": "high|medium|low"}},
            ],
            "recommendations": [
                {{"recommendation": "<specific action>", "example": "<example text>"}},
            ]
        }}""")
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "company": company,
                "prospect_info": json.dumps(prospect_info or {}),
                "subject": email_subject,
                "body": email_body
            })
            
            # Parse JSON response
            response_text = result.content
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            
            return self._default_score()
        except Exception as e:
            print(f"Error in confidence scoring: {e}")
            return self._default_score()
    
    def _default_score(self) -> Dict:
        """Return default score structure"""
        return {
            "overall_score": 50,
            "subject_line_score": 5,
            "body_quality_score": 5,
            "personalization_score": 5,
            "call_to_action_score": 5,
            "issues_found": [],
            "recommendations": []
        }


class ObjectionHandlerAgent:
    """Generates pre-responses to likely objections"""
    
    def __init__(self, groq_api_key: str = None):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=groq_api_key,
            temperature=0.5
        )
    
    def generate_objection_responses(self, company: str, goal: str, 
                                    analysis: Dict = None) -> List[Dict]:
        """
        Generate the 3 most likely objections and pre-written responses
        
        Returns:
            [
                {
                    "objection": "That's too expensive",
                    "likelihood_percentage": 85,
                    "response": "Pre-written response...",
                    "approach": "value-focused",
                    "alternatives": ["Alternative response 1", "Alternative response 2"]
                },
                ...
            ]
        """
        prompt = ChatPromptTemplate.from_template("""You are a sales expert who helps reps handle objections.
        Analyze this sales scenario and generate the 3 MOST LIKELY objections the prospect will raise.
        
        Company Being Approached: {company}
        Sales Goal: {goal}
        Additional Context: {context}
        
        For each of the 3 most likely objections:
        1. State the objection clearly
        2. Estimate likelihood percentage (0-100)
        3. Write a compelling response that addresses the objection
        4. Suggest the best approach (empathetic, logical, social_proof, value-focused)
        5. Provide 2 alternative responses the rep can use
        
        Focus on common objections in B2B sales:
        - Budget/Price concerns
        - "Not the right time" 
        - "We already have a solution"
        - "Need to think about it"
        - "We don't have anyone who needs this"
        
        Format as JSON:
        [
            {{
                "objection": "<the objection>",
                "likelihood_percentage": <0-100>,
                "context": "<why this objection is likely>",
                "triggers": ["<trigger 1>", "<trigger 2>"],
                "response": "<primary response>",
                "approach": "<approach type>",
                "alternatives": ["<alt response 1>", "<alt response 2>"]
            }},
        ]""")
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "company": company,
                "goal": goal,
                "context": json.dumps(analysis or {})
            })
            
            # Parse JSON response
            response_text = result.content
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            
            return []
        except Exception as e:
            print(f"Error in objection handling: {e}")
            return []
