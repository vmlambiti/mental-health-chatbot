from setuptools import setup, find_packages

setup(
    name="mental_health_chatbot",
    version="1.0.0",
    author="Jwalith Kristam",
    author_email="jwalithkristam@gmail.com",
    description="A mental health support chatbot built with Streamlit, FAISS, and Google Generative AI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jwalith/mental_health_chatbot",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.25.0",
        "pandas",
        "numpy",
        "sentence-transformers",
        "faiss-cpu",
        "python-dotenv",
        "cryptography",
        "google-generativeai"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "run_chatbot=main:main",
        ],
    },
)
