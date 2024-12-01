# persona_ai

**persona_ai** is a Streamlit application designed to display AI-generated marketing personas based on user behavior data. This project integrates machine learning techniques with OpenAI's advanced language models to provide insightful and actionable marketing profiles.

## 🚀 Features

1. **Feature Engineering**  
   - Extracts key attributes from raw user behavior data.  
   - Customizable to suit diverse datasets.  

2. **Clustering**  
   - Groups users into meaningful segments for targeted marketing.  

3. **Post-Processing**  
   - Enhances segments by calculating additional metrics.  

4. **Persona Generator**  
   - Uses OpenAI API to generate detailed personas based on segment metrics.  
   - Implements Few-Shot Learning for prompt optimization.  

5. **Future Enhancements**  
   - Plans to incorporate **Chain of Thought (CoT)** reasoning for better persona generation.  

## ⚙️ Customization

The codebase is adaptable to various user behavior datasets:  
- Modify the **feature engineering pipeline** to process new data.  
- Update **configuration files** to match dataset attributes.  
- Supports integration with cloud storage and compute platforms (e.g., AWS, GCP).  

## 💻 Prerequisites

1. **Python 3.8 or higher**  
   Install the required version from [Python.org](https://www.python.org/downloads/).
   
2. **Install Dependencies**  
   Install the necessary Python packages using the following command:
   ```bash
   pip install -r requirements.txt
    ```

## 🚀 Running the App

1. **Clone the Repository**
     Clone the project repository to your local machine using:
    ```bash
    streamlit run app/main.py
   ```
   
## 🛠 Future Roadmap
- Chain of Thought Reasoning:
We plan to integrate Chain of Thought (CoT) reasoning to enhance persona generation by allowing better logical thinking and improved decision-making.

- Cloud Integration:
In the future, the app will be compatible with cloud storage and compute platforms like AWS, Google Cloud, or Azure to manage larger datasets and scaling.

- Advanced Metrics:
The app will evolve to include predictive analytics and marketing recommendations, allowing marketers to receive actionable insights from the personas.

##🌐 Contact
If you have any questions or suggestions, feel free to reach out!

- Author: Pranab Pathak
- Email: pranab.pathak44@gmail.com
