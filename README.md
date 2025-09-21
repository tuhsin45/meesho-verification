# Project VerifyMe

This repository contains the prototype for Project VerifyMe, a submission for the Meesho DICE Challenge. This project proposes an AI-powered solution to combat seller-side return fraud within the e-commerce ecosystem.

## Our Philosophy: Problem-First, Technology-Second

The core strength of this project lies in the identification of a high-impact, real-world problem: the significant financial and operational burden that fraudulent returns place on Meesho's sellers. Our primary focus was the strategic brainstorming and design of a feasible, scalable solution that protects sellers and builds trust.

The technology demonstrated here (Streamlit, Google Gemini) serves as a functional proof-of-concept. It validates that the proposed workflow is practical and effective. At a production scale, we envision Meesho leveraging its vast resources to build a custom, in-house model, and this project provides the strategic blueprint for that initiative.

## How It Works

The solution is a two-phase system:

1.  **Seller Creates "Product Fingerprint"**: In the Supplier Hub, a seller uploads product images. Our system's AI engine analyzes them and generates a 3-point checklist of key, verifiable features. The seller must approve this checklist to make the product live.

2.  **Delivery Partner Verifies Return**: At the point of pickup, the delivery partner uses a mobile app to take a photo of the returned item. The AI performs a real-time comparison against the approved checklist and provides an instant **MATCH** or **NO MATCH** verdict.

## Running the Prototype

To run the Streamlit web application on your local machine, follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/tuhsin45/product-verification-mvp.git](https://github.com/tuhsin45/product-verification-mvp.git)
    cd product-verification-mvp
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up API Key**
    * Create a new folder in the root directory named `.streamlit`.
    * Inside the `.streamlit` folder, create a new file named `secrets.toml`.
    * Add your Google Gemini API key to this file in the following format:
        ```toml
        GEMINI_API_KEY = "YOUR_API_KEY_HERE"
        ```

4.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

## Future Vision & System Design

This prototype establishes the core concept. A production-level system would include further enhancements to create a more robust and fair ecosystem:

* **Human-in-the-Loop:** The delivery partner would retain the final authority to manually override the AI's decision in rare edge cases (e.g., obvious physical damage not captured by the AI), ensuring a balanced system of checks.
* **Fraud Penalties:** Data from verified fraudulent returns could be used to implement a penalty system for repeat offenders, such as the temporary suspension of the Cash on Delivery (COD) option, creating a strong disincentive for fraud.
* **Seller Accountability:** The seller-approved "Product Fingerprint" also acts as a binding agreement, protecting honest sellers while preventing dishonest sellers from falsely claiming a legitimate return is fake.

Ultimately, Project VerifyMe is designed to provide a more secure and hassle-free return experience for all stakeholders involved.
