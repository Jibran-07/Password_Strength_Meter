import streamlit as st
import re
import random
import string

def check_password_strength(password):
    score = 0
    feedback = []
    common_passwords = ["password", "password123", "123456789", "qwerty", "admin123", "letmein", "secret"]
    if password.lower() in common_passwords:
        return 0, ["❌ Password is too common. Choose a unique password."], "Weak"
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long (12+ for best security).")
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    if re.search(r"[!@#$%^&*]", password):
        score += 2
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    if score >= 6:
        feedback.append("✅ Strong Password! Great job!")
        strength = "Strong"
    elif score >= 4:
        feedback.append("⚠️ Moderate Password - Consider adding more security features.")
        strength = "Moderate"
    else:
        feedback.append("❌ Weak Password - Improve it using the suggestions above.")
        strength = "Weak"
    return score, feedback, strength

def generate_strong_password(length=12):
    if length < 8:
        length = 8
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*")
    ]
    for _ in range(length - 4):
        password.append(random.choice(chars))
    random.shuffle(password)
    return ''.join(password)

def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔒")
    st.title("🔒 Password Strength Meter")
    st.write("Enter a password to evaluate its strength or generate a secure one.")
    password = st.text_input("Enter your password:", type="password")
    if password:
        score, feedback, strength = check_password_strength(password)
        st.subheader("Password Analysis")
        st.write(f"**Strength**: {strength} (Score: {score}/7)")
        for message in feedback:
            st.write(message)
        st.progress(min(score / 7, 1.0))
        if strength != "Strong":
            if st.button("Suggest a Strong Password"):
                suggested_password = generate_strong_password()
                st.write(f"**Suggested Strong Password**: `{suggested_password}`")
                score, feedback, strength = check_password_strength(suggested_password)
                st.write(f"**New Password Strength**: {strength} (Score: {score}/7)")
    st.subheader("Generate a Secure Password")
    pass_length = st.slider("Select password length:", 8, 20, 12)
    if st.button("Generate Password"):
        new_password = generate_strong_password(pass_length)
        st.write(f"**Generated Password**: `{new_password}`")
        score, feedback, strength = check_password_strength(new_password)
        st.write(f"**Strength**: {strength} (Score: {score}/7)")

if __name__ == "__main__":
    main()