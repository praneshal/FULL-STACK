import bcrypt

# Generate a salt
salt = bcrypt.gensalt()

# Hash a password
password = "doamr@143"
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

# Verify the password
if bcrypt.checkpw(password.encode('utf-8'), hashed):
    print("Password is correct")
else:
    print("Password is incorrect")
