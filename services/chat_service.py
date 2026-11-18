from models.chat_request import ChatRequestModel
from config.llm_config import LLMClient
from prompts.sales_ai_prompt import ai_prompt 
import json
import pymysql
from langchain.agents import create_agent


from tools.product_search_tool import search_products
def get_db_connection():
    connection=pymysql.connect(host="localhost",user="root",password="bhargav1740",port=3306,database="genai_pro3_db",cursorclass=pymysql.cursors.DictCursor)
    return connection

class ChatService:


    def ai_chat(self,req:ChatRequestModel):

        query="select * from conv_messages where conv_id=%s"
        conn= get_db_connection()
        cursor=conn.cursor()
        cursor.execute(query,(req.conv_id,))

        db_messages=cursor.fetchall()

        conv_history=""
        messages=[]

        for msg in db_messages:
            conv_history=conv_history+ f"user_type:{msg['message_from']} and user_message:{msg['message']}\n"
            message={"role":msg["message_from"],"content":msg["message"]}
            messages.append(message)

        conv_history=conv_history+f"user input:{req.user_message}\n"  
        messages.append({"role":"user","content":req.user_message})


        llm_client=LLMClient.get_llm_client()

        prompt=ai_prompt

        prompt=f"{prompt} \n {conv_history}"

        sales_agent=create_agent(model=llm_client,system_prompt=prompt,tools=LLMClient.get_tools())

        response=sales_agent.invoke({"messages":messages})
        ai_response=response["messages"][-1].content

        json_response=json.loads(ai_response)

        insert_query="insert into conv_messages(conv_id,message,message_from) VALUES (%s,%s,%s)"
        cursor.execute(insert_query,(req.conv_id,req.user_message,"user"))

        insert_query="insert into conv_messages(conv_id,message,message_from) VALUES (%s,%s,%s)"
        cursor.execute(insert_query,(req.conv_id,json_response["message"],"assistant"))

        conn.commit()
        conn.close()

        return json_response