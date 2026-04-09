"""
Export services for Notion and Google Docs
"""
from notion_client import Client
from typing import Dict, List, Optional
from datetime import datetime
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class NotionExportService:
    """Export campaigns and email sequences to Notion"""
    
    def __init__(self, notion_api_key: str = None):
        self.notion_key = notion_api_key or os.getenv("NOTION_API_KEY")
        if self.notion_key:
            self.client = Client(auth=self.notion_key)
        else:
            self.client = None
    
    def create_campaign_page(self, database_id: str, campaign_data: Dict) -> Optional[str]:
        """Create a new Notion page for a campaign"""
        if not self.client:
            raise ValueError("Notion API key not configured")
        
        try:
            page = self.client.pages.create(
                parent={"database_id": database_id},
                properties={
                    "title": {
                        "title": [{"text": {"content": campaign_data.get("company", "Campaign")}}]
                    },
                    "Goal": {
                        "rich_text": [{"text": {"content": campaign_data.get("goal", "")}}]
                    },
                    "Status": {
                        "select": {"name": campaign_data.get("status", "Active")}
                    },
                    "Opportunity Score": {
                        "number": campaign_data.get("opportunity_score", 0)
                    },
                    "Created": {
                        "date": {"start": datetime.utcnow().isoformat()}
                    }
                }
            )
            return page["id"]
        except Exception as e:
            print(f"Error creating Notion page: {e}")
            return None
    
    def add_email_sequence_to_page(self, page_id: str, emails: List[Dict]) -> bool:
        """Add email sequence to an existing Notion page"""
        if not self.client:
            raise ValueError("Notion API key not configured")
        
        try:
            blocks = []
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Email Sequence"}}]
                }
            })
            
            for idx, email in enumerate(emails, 1):
                blocks.extend([
                    {
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [{"type": "text", "text": {"content": f"Email {idx}: {email.get('subject', '')}"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "callout",
                        "callout": {
                            "rich_text": [{"type": "text", "text": {"content": f"Confidence: {email.get('confidence_score', 0)}/100"}}],
                            "icon": {"emoji": "⭐"}
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": email.get("body", "")}}]
                        }
                    }
                ])
            
            # Append blocks to page
            self.client.blocks.children.append(page_id, {"children": blocks})
            return True
        except Exception as e:
            print(f"Error adding email sequence to Notion: {e}")
            return False
    
    def add_objections_to_page(self, page_id: str, objections: List[Dict]) -> bool:
        """Add objection handling guide to Notion page"""
        if not self.client:
            raise ValueError("Notion API key not configured")
        
        try:
            blocks = [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "Objection Handling Guide"}}]
                    }
                }
            ]
            
            for obj in objections:
                blocks.extend([
                    {
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [{"type": "text", "text": {"content": obj.get("objection", "")}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "callout",
                        "callout": {
                            "rich_text": [{"type": "text", "text": {"content": f"Likelihood: {obj.get('likelihood_percentage', 0)}%"}}],
                            "icon": {"emoji": "🎯"}
                        }
                    },
                    {
                        "object": "block",
                        "type": "heading_4",
                        "heading_4": {
                            "rich_text": [{"type": "text", "text": {"content": "Response"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": obj.get("response", "")}}]
                        }
                    }
                ])
            
            self.client.blocks.children.append(page_id, {"children": blocks})
            return True
        except Exception as e:
            print(f"Error adding objections to Notion: {e}")
            return False


class GoogleDocsExportService:
    """Export campaigns and email sequences to Google Docs"""
    
    def __init__(self, credentials: Credentials = None):
        self.credentials = credentials
        self.service = None
        if credentials:
            self.service = build("docs", "v1", credentials=credentials)
    
    def create_campaign_document(self, campaign_data: Dict) -> Optional[str]:
        """Create a new Google Doc for a campaign"""
        if not self.service:
            raise ValueError("Google Docs service not configured")
        
        try:
            document = {
                "title": f"{campaign_data.get('company')} - Campaign"
            }
            
            doc = self.service.documents().create(body=document).execute()
            doc_id = doc.get("documentId")
            
            # Add initial content
            self._add_campaign_content(doc_id, campaign_data)
            
            return doc_id
        except HttpError as e:
            print(f"Error creating Google Doc: {e}")
            return None
    
    def _add_campaign_content(self, doc_id: str, campaign_data: Dict) -> bool:
        """Add campaign data to document"""
        try:
            requests = [
                {
                    "insertText": {
                        "text": f"{campaign_data.get('company')} - Sales Campaign\n\n"
                    }
                },
                {
                    "updateTextStyle": {
                        "range": {
                            "startIndex": 0,
                            "endIndex": len(f"{campaign_data.get('company')} - Sales Campaign\n\n")
                        },
                        "textStyle": {
                            "bold": True,
                            "fontSize": {"magnitude": 28, "unit": "pt"}
                        },
                        "fields": "bold,fontSize"
                    }
                },
                {
                    "insertText": {
                        "text": f"Goal: {campaign_data.get('goal', 'N/A')}\n"
                    }
                },
                {
                    "insertText": {
                        "text": f"Opportunity Score: {campaign_data.get('opportunity_score', 0)}/100\n"
                    }
                },
                {
                    "insertText": {
                        "text": f"Created: {datetime.utcnow().isoformat()}\n\n"
                    }
                }
            ]
            
            self.service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": requests}
            ).execute()
            
            return True
        except HttpError as e:
            print(f"Error adding content to Google Doc: {e}")
            return False
    
    def add_email_sequence(self, doc_id: str, emails: List[Dict]) -> bool:
        """Add email sequence to Google Doc"""
        if not self.service:
            raise ValueError("Google Docs service not configured")
        
        try:
            requests = [
                {
                    "insertText": {
                        "text": "\n\nEmail Sequence\n"
                    }
                }
            ]
            
            for idx, email in enumerate(emails, 1):
                requests.extend([
                    {
                        "insertText": {
                            "text": f"\nEmail {idx}: {email.get('subject', '')}\n"
                        }
                    },
                    {
                        "insertText": {
                            "text": f"Confidence Score: {email.get('confidence_score', 0)}/100\n"
                        }
                    },
                    {
                        "insertText": {
                            "text": f"Personalization: {email.get('personalization_score', 0)}/10\n\n"
                        }
                    },
                    {
                        "insertText": {
                            "text": f"{email.get('body', '')}\n"
                        }
                    }
                ])
            
            self.service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": requests}
            ).execute()
            
            return True
        except HttpError as e:
            print(f"Error adding email sequence: {e}")
            return False
    
    def add_objections_guide(self, doc_id: str, objections: List[Dict]) -> bool:
        """Add objection handling guide to Google Doc"""
        if not self.service:
            raise ValueError("Google Docs service not configured")
        
        try:
            requests = [
                {
                    "insertText": {
                        "text": "\n\nObjection Handling Guide\n"
                    }
                }
            ]
            
            for obj in objections:
                requests.extend([
                    {
                        "insertText": {
                            "text": f"\n{obj.get('objection', '')}\n"
                        }
                    },
                    {
                        "insertText": {
                            "text": f"Likelihood: {obj.get('likelihood_percentage', 0)}%\n"
                        }
                    },
                    {
                        "insertText": {
                            "text": f"Response: {obj.get('response', '')}\n\n"
                        }
                    }
                ])
            
            self.service.documents().batchUpdate(
                documentId=doc_id,
                body={"requests": requests}
            ).execute()
            
            return True
        except HttpError as e:
            print(f"Error adding objections guide: {e}")
            return False
