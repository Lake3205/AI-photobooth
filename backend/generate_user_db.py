import bcrypt

def generate_hashed_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

if __name__ == "__main__":
    print("=== User Generator ===\n")
    
    password = input("Enter the password: ")
    
    if not password:
        print("Please enter something!")
        exit(1)
    
    hashed = generate_hashed_password(password)
    
    print("\n=== Generated Hash ===")
    print(hashed)

    username = input("\nEnter the username (default: user): ").strip() or "user"

    print("\n=== SQL Insert Statement ===")
    print("SQL script for DB:\n")
    print(f"\nINSERT INTO users (username, hashed_password, role) VALUES ('{username}', '{hashed}', 'user');")
    print("\n=== Done ===")
