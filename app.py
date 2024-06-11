from flask import Flask, render_template, request
from cryptography.fernet import Fernet

app = Flask(__name__)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        action = request.form['action']

        if action == 'encrypt':
            card_number = request.form['card_number']
            card_holder = request.form['card_holder']
            expiry_date = request.form['expiry_date']
            cvv = request.form['cvv']

            if not card_number or not card_holder or not expiry_date or not cvv:
                result = "Please fill out all fields to encrypt."
            else:
                credit_card_details = f"{card_number}|{card_holder}|{expiry_date}|{cvv}"
                encrypted_text = cipher_suite.encrypt(credit_card_details.encode()).decode()
                result = f"Encrypted: {encrypted_text}"

        elif action == 'decrypt':
            encrypted_text = request.form['encrypted_text']

            try:
                decrypted_text = cipher_suite.decrypt(encrypted_text.encode()).decode()
                card_number, card_holder, expiry_date, cvv = decrypted_text.split('|')
                result = f"Decrypted:\nCard Number: {card_number}\nCard Holder: {card_holder}\nExpiry Date: {expiry_date}\nCVV: {cvv}"
            except Exception as e:
                result = f"An error occurred during decryption: {str(e)}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
