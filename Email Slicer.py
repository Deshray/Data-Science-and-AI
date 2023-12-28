email = str(input("Please enter your email address")).strip()
username = email[:email.index("@")]
domain = email[email.index("@") + 1:]
print ("Your username is:", username)
print("Your email address domain is:", domain)
