from langchain.tools import tool

@tool
def get_available_discounts():
    """
    use this tool to find available discounts
    discount items are in list variable.each item in item is the discount object.
    object keys:
    discount_id: unique discount id
    items: milk,sugar,rice (items are in natural language and sometimes it may include category, based on the product, identift best suitable discount and apply)
    discount_type: amount or percentage, amount means we are providing some amount like x rupees, deduct discount_value key value from total order value and if discount type is percentage calculate discount amount based on total order value and discount_value key value example 5 means 5%

    """
    discounts=[
        {"discount_id":1, "items":"milk,sugar,rice","discount_type":"amount","discount_value":10},
        {"discount_id":2, "items":"daal,all skin care products","discount_type":"percentage","discount_value":5}

    ]

    return discounts