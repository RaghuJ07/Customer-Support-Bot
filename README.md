# 🤖 Customer Support Chatbot

An intelligent **AI-powered Customer Support Chatbot** built using **LangChain**, **LangGraph**, and **Google Gemini** to automate customer interactions, answer queries, and provide smart conversational support.

This project is designed to simulate a modern customer service assistant that can handle user questions efficiently using advanced LLM orchestration.

---

## 🚀 Features

- 💬 Natural conversational customer support
- 🧠 Powered by Google Gemini LLM
- 🔗 Built with LangChain for prompt workflows
- 🌐 LangGraph for structured conversation flow
- ⚡ Fast and scalable architecture
- 🔒 Secure API key management using `.env`
- 🛠 Easy local setup and execution

---

## 🏗 Tech Stack

- **Python**
- **LangChain**
- **LangGraph**
- **Google Gemini API**
- **dotenv**

---

## 📂 Project Structure

```bash
customer-support-chatbot/
│── main.py
│── requirements.txt
│── .env
│── README.md


git clone https://github.com/RaghuJ07/Customer-Support-Bot
cd your-repo-name

#To install the libreries use this command
py -m pip install -r requirements.txt

#Assign the gemini api key to make this project connect to the llm
GOOGLE_API_KEY=your_google_api_key_here

#To run the project use this command
py -m main
