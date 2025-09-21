Project VerifyMe
This repository contains the prototype for Project VerifyMe, a submission for the Meesho DICE Challenge. This project proposes an AI-powered solution to combat seller-side return fraud within the e-commerce ecosystem.

Our Philosophy: Problem-First, Technology-Second
The core strength of this project lies in the identification of a high-impact, real-world problem: the significant financial and operational burden that fraudulent returns place on Meesho's sellers. Our primary focus was the strategic brainstorming and design of a feasible, scalable solution that protects sellers and builds trust.

The technology demonstrated here (Streamlit, Google Gemini) serves as a functional proof-of-concept. It validates that the proposed workflow is practical and effective. At a production scale, we envision Meesho leveraging its vast resources to build a custom, in-house model, and this project provides the strategic blueprint for that initiative.

How It Works
The solution is a two-phase system:

Seller Creates "Product Fingerprint": In the Supplier Hub, a seller uploads product images. Our system's AI engine analyzes them and generates a 3-point checklist of key, verifiable features. The seller must approve this checklist to make the product live.

Delivery Partner Verifies Return: At the point of pickup, the delivery partner uses a mobile app to take a photo of the returned item. The AI performs a real-time comparison against the approved checklist and provides an instant MATCH or NO MATCH verdict.

Running the Prototype
To run the Streamlit web application on your local machine, follow these steps:

Clone the Repository

git clone [https://github.com/tuhsin45/product-verification-mvp.git](https://github.com/tuhsin45/product-verification-mvp.git)
cd product-verification-mvp

Install Dependencies

pip install -r requirements.txt

Set Up API Key

Create a new folder in the root directory named .streamlit.

Inside the .streamlit folder, create a new file named secrets.toml.

Add your Google Gemini API key to this file in the following format:

GEMINI_API_KEY = "YOUR_API_KEY_HERE"

Run the Application

streamlit run app.py
