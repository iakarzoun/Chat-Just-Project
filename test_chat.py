import requests

# 1. The question the student is asking
student_payload = {
<<<<<<< HEAD
    "question": "متى رح تبدأ حفلة التخريج لدفعة سنة 2026؟" 
=======
    "question": "متى تبدأ فترة الإنسحاب والإضافة للطلبة؟" 
>>>>>>> c2417573ac2d1d33e31f35032eebe3b63effae68
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