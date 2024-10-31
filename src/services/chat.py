from typing import List, Dict, Optional
from datetime import datetime, timezone
from src.llm.engine import llm_engine
from src.llm.prompts.templates import prompt_templates
from src.db.mongodb import chat_collection
from src.db.vector import vector_store
import uuid

class ChatService:
    def __init__(self):
        self.llm = llm_engine
        self.templates = prompt_templates
        self.max_context_messages = 10

    def get_current_time(self) -> datetime:
        """Get current UTC time with timezone information"""
        return datetime.now(timezone.utc)

    async def create_conversation(self, user_id: str) -> Dict:
        """Create a new conversation"""
        try:
            conversation_id = str(uuid.uuid4())
            current_time = self.get_current_time()
            
            conversation = {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "messages": [],
                "created_at": current_time,
                "updated_at": current_time,
                "status": "active",
                "metadata": {
                    "total_messages": 0,
                    "last_user_message_time": None,
                    "last_assistant_message_time": None
                }
            }
            
            # Insert the document
            await chat_collection.insert_one(conversation)
            
            # Return the conversation without the _id field
            conversation.pop('_id', None)
            return conversation
            
        except Exception as e:
            raise Exception(f"Error creating conversation: {str(e)}")

    async def add_message(self, conversation_id: str, role: str, content: str) -> Dict:
        """Add a message to the conversation"""
        try:
            current_time = self.get_current_time()
            
            message = {
                "message_id": str(uuid.uuid4()),
                "role": role,
                "content": content,
                "timestamp": current_time
            }
            
            # Prepare update data
            update_data = {
                "$push": {"messages": message},
                "$set": {
                    "updated_at": current_time,
                },
                "$inc": {"metadata.total_messages": 1}
            }
            
            # Update last message time based on role
            if role == "user":
                update_data["$set"]["metadata.last_user_message_time"] = current_time
            elif role == "assistant":
                update_data["$set"]["metadata.last_assistant_message_time"] = current_time
            
            # Perform the update
            result = await chat_collection.find_one_and_update(
                {"conversation_id": conversation_id},
                update_data,
                return_document=True
            )
            
            if not result:
                raise Exception(f"Conversation not found: {conversation_id}")
            
            return message
            
        except Exception as e:
            raise Exception(f"Error adding message: {str(e)}")

    async def get_conversation_history(self, conversation_id: str, limit: int = 50) -> List[Dict]:
        """Get conversation history"""
        try:
            conversation = await chat_collection.find_one(
                {"conversation_id": conversation_id}
            )
            
            if not conversation:
                raise Exception(f"Conversation not found: {conversation_id}")
            
            messages = conversation.get("messages", [])
            return messages[-limit:] if messages else []
            
        except Exception as e:
            raise Exception(f"Error getting conversation history: {str(e)}")

    async def generate_response(
        self,
        conversation_id: str,
        user_message: str,
        use_knowledge_base: bool = True
    ) -> Dict:
        """Generate response to user message"""
        try:
            # Add user message first
            await self.add_message(conversation_id, "user", user_message)
            
            # Get recent conversation history
            history = await self.get_conversation_history(
                conversation_id, 
                limit=self.max_context_messages
            )
            
            # Initialize system prompt
            system_prompt = self.templates.CUSTOMER_SERVICE_PROMPT
            
            # Add knowledge base context if enabled
            if use_knowledge_base:
                try:
                    search_results = vector_store.search(user_message)
                    relevant_docs = search_results.get("documents", [])
                    if relevant_docs:
                        context = "\n".join(relevant_docs)
                        system_prompt = self.templates.get_knowledge_base_prompt(context)
                except Exception as e:
                    print(f"Knowledge base search failed: {str(e)}")
            
            # Convert history to message format
            messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]
            
            # Generate response
            response = await self.llm.generate_response(
                messages=messages,
                system_prompt=system_prompt
            )
            
            # Add assistant response
            await self.add_message(conversation_id, "assistant", response)
            
            return {"response": response}
            
        except Exception as e:
            error_msg = self.templates.get_error_response(str(e))
            await self.add_message(conversation_id, "assistant", error_msg)
            return {"response": error_msg}

    async def end_conversation(self, conversation_id: str) -> Dict:
        """End/Archive a conversation"""
        try:
            current_time = self.get_current_time()
            
            result = await chat_collection.find_one_and_update(
                {"conversation_id": conversation_id},
                {
                    "$set": {
                        "status": "archived",
                        "archived_at": current_time,
                        "updated_at": current_time
                    }
                },
                return_document=True
            )
            
            if not result:
                raise Exception(f"Conversation not found: {conversation_id}")
                
            return {"message": "Conversation archived successfully"}
            
        except Exception as e:
            raise Exception(f"Error ending conversation: {str(e)}")

    async def get_active_conversations(self, user_id: str) -> List[Dict]:
        """Get all active conversations for a user"""
        try:
            cursor = chat_collection.find(
                {
                    "user_id": user_id,
                    "status": "active"
                }
            )
            conversations = await cursor.to_list(length=None)
            return [
                {
                    "conversation_id": conv["conversation_id"],
                    "created_at": conv["created_at"],
                    "updated_at": conv["updated_at"],
                    "total_messages": conv["metadata"]["total_messages"]
                }
                for conv in conversations
            ]
        except Exception as e:
            raise Exception(f"Error getting active conversations: {str(e)}")

# Create chat service instance
chat_service = ChatService()