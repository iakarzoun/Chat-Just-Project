import requests

# 1. The question the student is asking
student_payload = {
    "question": "متى تبدأ فترة الإنسحاب والإضافة للطلبة؟" 
}

print("📱 Sending question to the Waiter...")

# 2. Send the message to your local Flask server
url = "http://127.0.0.1:5000/ask"
response = requests.post(url, json=student_payload)

# 3. Print the AI's answer!
if response.status_code == 200:
    print("\n🎓 AI Answer:")
    print(response.json()["answer"])
else:
    print("\n❌ Error:", response.text)