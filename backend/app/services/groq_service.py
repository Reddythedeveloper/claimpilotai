import os
import time
import logging
from typing import Type, TypeVar, Any, Dict, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from groq import InternalServerError, RateLimitError, APITimeoutError

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class GroqService:
    def __init__(self, model_name: str = None, temperature: float = 0.0):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is missing")
            
        self.model_name = model_name or os.getenv("GROQ_MODEL_PRIMARY", "llama3-70b-8192")
        self.temperature = temperature
        
        self.llm = ChatGroq(
            api_key=self.api_key,
            model_name=self.model_name,
            temperature=self.temperature,
            max_retries=3,
            timeout=30.0,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((InternalServerError, RateLimitError, APITimeoutError))
    )
    def invoke_structured(self, prompt: str, schema: Type[T], system_prompt: Optional[str] = None) -> T:
        """
        Invokes the Groq model and enforces a Pydantic structured output.
        Includes logging for latency and automatic retries.
        """
        start_time = time.time()
        
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))
        
        # Enforce structured output via Groq's tool-calling/JSON mode
        structured_llm = self.llm.with_structured_output(schema)
        
        try:
            logger.info(f"Invoking Groq structured output (model={self.model_name})")
            result = structured_llm.invoke(messages)
            latency = time.time() - start_time
            logger.info(f"Groq API call completed in {latency:.2f} seconds")
            return result
            
        except Exception as e:
            logger.error(f"Error invoking Groq: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((InternalServerError, RateLimitError, APITimeoutError))
    )
    def invoke_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Invokes the Groq model and returns a plain text string.
        """
        start_time = time.time()
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))
        
        try:
            logger.info(f"Invoking Groq text output (model={self.model_name})")
            result = self.llm.invoke(messages)
            latency = time.time() - start_time
            logger.info(f"Groq API call completed in {latency:.2f} seconds")
            return result.content
            
        except Exception as e:
            logger.error(f"Error invoking Groq: {str(e)}")
            raise

# Singleton instances
primary_llm_service = GroqService()
critic_llm_service = GroqService(model_name=os.getenv("GROQ_MODEL_CRITIC", "llama3-8b-8192"))
