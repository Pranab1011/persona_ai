import streamlit as st

# Define persona data
personas = {
    "Tech-Savvy Power Shopper": {
        "image": "personas/data/images/Tech-Savvy-Power-Shopper.png",  # Path to the image
        "demographics": {
            "Name": "Emily Harper",
            "Age": 33,
            "Gender": "Female",
            "Occupation": "Mid-level Professional",
            "Income": "$100000",
        },
        "behavioral_traits": {
            "Purchase Habits": "Spends large amounts in short bursts, prefers credit card payments.",
            "Category Insights": "High interest in Electronics, Clothing, and Books.",
            "Additional Adoption Notes": "Likely an early adopter of technology.",
        },
        "psychographics": {
            "Lifestyle": "Values convenience and practicality.",
            "Motivations": "Stays updated with the latest tech.",
            "Pain Points": "Frustrated with delays in accessing cutting-edge tech.",
        },
        "marketing_strategy": {
            "Target Channels": "Email campaigns, tech review blogs, social media.",
            "Messaging": "Focus on innovation, reliability, and value for money.",
            "Product Recommendations": "Smart devices, premium clothing, e-books.",
            "Engagement": "Personalized recommendations, credit card reward offers.",
        },
        "taglines": [
            "Elevate Your Lifestyle with the Latest Tech and Timeless Fashion.",
            "Designed for Women Who Lead!",
        ],
    },
    # Add more customer segments as needed
}

# Streamlit app layout
st.title("CUSTOMER PERSONA VIEWER")

# Sidebar for persona selection and demographics
st.sidebar.header("Select Customer Segment")
selected_persona = st.sidebar.selectbox("Choose Persona", list(personas.keys()))

# Display persona image and demographics
persona_data = personas[selected_persona]
st.sidebar.image(persona_data["image"], caption=selected_persona, use_column_width=True)
st.sidebar.subheader("Demographics")
for key, value in persona_data["demographics"].items():
    st.sidebar.write(f"**{key}:** {value}")

# Custom CSS to apply borders, colors, and fonts
st.markdown(
    """
    <style>
    h1 {
        font-family: 'Georgia', serif; /* Change the font */
        font-size: 24px; /* Adjust font size */
        color: #9da48a; /* Set a custom color */
        text-align: center; /* Center-align the header */
        border-top: 3px solid #9da48a; /* Add an underline */
        padding-top: 10px; /* Add some space below the border */
        margin-top: 2px; /* Add spacing between header and next content */
    }
    
    h2 {
        font-family: 'Georgia', serif; /* Change the font */
        font-size: 32px; /* Adjust font size */
        color: #828e5d; /* Set a custom color */
        text-align: center; /* Center-align the header */
        border-bottom: 3px solid #4CAF50; /* Add an underline */
        padding-bottom: 10px; /* Add some space below the border */
        margin-bottom: 20px; /* Add spacing between header and next content */
    }
    
    /* Section styling */
    .section {
        border: 0px solid #a3ad83;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #292929;
        min-height: 400px; /* Ensures equal height for Behavioral Traits and Psychographics */
    }
    
    [data-testid="stSidebar"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    /* Heading styles */
    .section h3 {
        font-family: 'Arial', sans-serif;
        color: #bfd47d;
        font-size: 24px;
    }

    /* Subheading styles */
    .section h4 {
        font-family: 'Helvetica', sans-serif;
        color: #f9ffed;
        font-size: 20px;
    }

    /* Content text styles */
    .section p {
        font-family: 'Verdana', sans-serif;
        color: #f9ffed;
        font-size: 16px;
    }

    /* Tagline section */
    .tagline-section p {
        font-family: 'Courier New', Courier, monospace;
        font-size: 18px;
        color: #f9ffed;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Main body with 4 sections
st.header(f"Persona: {selected_persona}")


# Display sections
def display_section(title, content):
    section_html = f"""
    <div class="section">
        <h3>{title}</h3>
        {''.join([f'<p><strong>{key}:</strong> {value}</p>' for key, value in content.items()])}
    </div>
    """
    st.markdown(section_html, unsafe_allow_html=True)


# First row: Behavioral Traits and Psychographics side by side
col1, col2 = st.columns(2)
with col1:
    display_section("Behavioral Traits", persona_data["behavioral_traits"])
with col2:
    display_section("Psychographics", persona_data["psychographics"])

# Second row: Marketing Strategy (full width)
display_section("Marketing Strategy", persona_data["marketing_strategy"])

# Third row: Suggested Taglines (full width)
taglines_html = f"""
<div class="section">
    <h3>Suggested Taglines for Engagement</h3>
    {''.join([f'<p>- {tagline}</p>' for tagline in persona_data["taglines"]])}
</div>
"""
st.markdown(taglines_html, unsafe_allow_html=True)
