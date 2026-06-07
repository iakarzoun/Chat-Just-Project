import requests

student_payload = {
    # The new follow-up question
    "question": "can u find the contact for me?", 
    
    # The running transcript of everything said before
    "history": [
        {
            "user": "What is the graduation project?", 
            "ai": "It is a final project required for graduation."
        },
        {
            "user": "where should i do to pay the bills?", 
            "ai": "I apologize, but the provided information does not specify... I recommend you contact the university's Financial Department or Student Affairs Office directly."
        }
    ]
}
print("📱 Sending question and memory to the Waiter...")

# 2. Send the message to your local Flask server
url = "http://127.0.0.1:5000/ask"
response = requests.post(url, json=student_payload)

# 3. Print the AI's answer!
if response.status_code == 200:
    print("\n🤖 AI Answer:")
    print(response.json()["answer"])
else:
    print("\n❌ Error:", response.text)