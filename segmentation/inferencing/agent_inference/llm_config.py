persona_prompt_prefix = """
  You are an expert in generating user personas using customer segment data.
  You are given stats of a customer segment that was achieved by implementing market segmentation on user behaviour data acquired from an online retail store.
  Using this data, generate a user persona. Example is given below:.

"""

orion_example = [
    {
        "input": """
        "avg_customer_age": 33.2,
        "avg_total_purchase_last_3_months": 3084.0,
        "avg_purchase_month_1": 3084.0,
        "avg_purchase_month_2": 0.0,
        "avg_purchase_month_3": 0.0,
        "avg_purchase_week_1": 3084.0,
        "avg_purchase_week_2": 0.0,
        "avg_purchase_week_3": 0.0,
        "avg_purchase_week_4": 0.0,
        "total_Books_purchased": 19.0,
        "total_Clothing_purchased": 23.0,
        "total_Electronics_purchased": 64.0,
        "total_Home_appliances_purchased": 1.0,
        "total_Female_users": 5,
        "total_Male_users": 0,
        "total_Cash_purchases": 0,
        "total_Credit_Card_purchases": 5,
        "total_Crypto_purchases": 0,
        "total_PayPal_purchases": 0,
        "age_range": "23-45",
        "median_age": 32.0,
        "age_25th_percentile": 23.0,
        "age_75th_percentile": 43.0
        """,
        "output": """'persona_name': 'Tech-Savvy Power Shopper','Name': 'Emily Harper','Age': 33,'Gender': 'Female',
        'Occupation': 'Mid-level Professional','Income': '$100k - $150k',
        'Purchase Habits': 'Spends large amounts in short bursts, prefers credit card payments.',
        'Category Insights': 'High interest in Electronics, Clothing, and Books.',
        'Additional Adoption Notes': 'Likely an early adopter of technology.',
        'Lifestyle': 'Values convenience and practicality.',
        'Motivations': 'Stays updated with the latest tech.',
        'Pain Points': 'Frustrated with delays in accessing cutting-edge tech.',
        'Target Channels': 'Email campaigns, tech review blogs, social media.',
        'Messaging': 'Focus on innovation, reliability, and value for money.',
        'Product Recommendations': 'Smart devices, premium clothing, e-books.',
        'Engagement': 'Personalized recommendations, credit card reward offers.',
        'taglines': 'Elevate Your Lifestyle with the Latest Tech and Timeless Fashion.'
        """,
    }
]

prompt_example_mapping = {"orion": orion_example}
