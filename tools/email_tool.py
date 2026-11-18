from langchain.tools import tool 

@tool
def send_email(email:str):

    """
    use this tool to send bill and payment link to the user email id
    """
    return "email sent to " +email

