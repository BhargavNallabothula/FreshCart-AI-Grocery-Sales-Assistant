from config.settings import settings
#from langchain_anthropic import chatanthropic
from langchain_openai import ChatOpenAI
from tools.discounts_tool import get_available_discounts
from tools.email_tool import send_email
from tools.generate_payment_link_tool import generate_payment_link
from tools.product_search_tool import search_products


class LLMClient:


    @staticmethod
    def get_llm_client(provider:str| None=None):

        provider=provider or settings.DEFAULT_LLM

        if provider.lower()=="openai":
            llm_client = ChatOpenAI(model=settings.DEFAULT_OPENAI_MODEL,api_key=settings.OPENAI_API_KEY)
        

        #if provider.lower()=="anthropic":
            #llm_client= chatanthropic(model=settings.DEFAULT_ANTHROPIC_MODEL,api_key=settings.ANTHROPIC_API_KEY)
            #llm_client.bind_tools([search_products,send_email,generate_payment_link,get_available_discounts])
        return llm_client

    @staticmethod
    def get_tools():
        return [search_products,send_email,generate_payment_link,get_available_discounts]


