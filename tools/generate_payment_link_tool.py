from langchain.tools import tool

@tool 
def generate_payment_link(order_total,mobile,email):
    """
    use this tool to generate payment link
    """
    return "http://rzp.pay.com/links/wjhedcdwj"