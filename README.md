# Mental Health Chatbot

## Overview

The **Mental Health Chatbot** is an AI-powered support tool designed to provide empathetic, personalized, and evidence-based guidance for mental health concerns. Built using cutting-edge technologies like Streamlit, FAISS, and Google's Generative AI, this chatbot delivers a secure and tailored experience for users seeking mental well-being support.

## Features

- **Personalized Support**: Tailored responses based on user age group and specific concerns (e.g., work stress, anxiety, sleep).
- **Secure Data Handling**: Uses encryption to securely store user concerns and maintains HIPAA-level privacy compliance.
- **Context-Aware Responses**: Integrates previous user interactions and "Your Previous Concerns" to provide consistent, context-driven replies.
- **Few-Shot Learning**: Leverages examples to improve chatbot accuracy and understand nuanced questions.
- **FAQ Integration**: Includes a dynamic FAQ section for quick answers to common mental health queries.
- **User Data Management**: Users can save their concerns and delete their data at any time, ensuring complete control over personal information.

## Project Structure

```plaintext
mental_health_chatbot/
│
├── app/                   # Application code
│   ├── chatbot_logic.py   # Core chatbot logic and processing
│   ├── config.py          # Configuration and prompt definitions
│   ├── data_loader.py     # Resource loading and setup
│   └── main.py            # Streamlit interface
│
├── data/                  # Data files and resources
│   ├── counselchat_with_embeddings.pkl
│   ├── faiss_index.bin
│   ├── faqs.csv
│   ├── encryption_key.key
│   └── user_memory.json
│
├── setup.py               # Setup script for easy installation
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md              # Project documentation
└── .gitignore             # Ignored files
```

## Technologies Used

* **Streamlit**: User-friendly web interface for real-time chatbot interactions.
* **FAISS**: Fast and efficient retrieval of contextually similar responses.
* **Sentence Transformers**: For generating embeddings from user input.
* **Google Generative AI (Gemini)**: To generate empathetic and helpful responses.
* **Encryption (Fernet)**: Ensures secure storage of sensitive user data.
* **Few-Shot Learning**: Enhances the chatbot's performance with example-based learning.

## How It Works

### User Interaction
* Users provide their name, age group, and specific concerns.
* Previous interactions are retrieved for context.

### Query Processing
* User input is processed and embedded using Sentence Transformers.
* FAISS retrieves relevant responses from a dataset of mental health exchanges.

### Response Generation
* A tailored prompt is constructed using user details, retrieved responses, and few-shot examples.
* Google Generative AI generates a context-aware, empathetic response.

### Secure Data Handling
* **Encrypted Data**: User concerns are encrypted before storage.
* **Data Access**: Data is easily accessible and deletable by the user.

## Getting Started

### Prerequisites
* Python 3.9 or later
* Required Python libraries (in `requirements.txt`)
* Docker (optional for containerization)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/mental_health_chatbot.git
cd mental_health_chatbot
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your environment variables** in a `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
DATA_PATH=data/
```

4. **Run the chatbot**:
```bash
streamlit run app/main.py
```

## Security and Privacy

* **Encrypted Data**: User concerns are encrypted using the Fernet symmetric encryption mechanism.
* **Data Deletion**: Users can delete their data via the chatbot interface.
* **Compliance**: Designed to follow privacy best practices and HIPAA-level compliance.

## Contributing

Feel free to fork this repository, create issues, or submit pull requests to improve the chatbot. Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


