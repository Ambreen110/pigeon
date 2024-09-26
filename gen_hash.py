from werkzeug.security import generate_password_hash

password = 'mypass'
password_hash = generate_password_hash(password, method='pbkdf2:sha256')
print(password_hash)
