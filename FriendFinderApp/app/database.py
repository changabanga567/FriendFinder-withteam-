import hashlib
import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Goukou400',
            database='friend'
        )
        self.cursor = self.conn.cursor()

    def register_user(self, username, password, name, email):

        """
        Register a new user.
        """
        try:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()  # Assuming you're using SHA-256 for hashing
            self.cursor.execute("INSERT INTO users (username, password, name, email) VALUES (%s, %s, %s, %s)",
                            (username, hashed_password, name, email))
            self.conn.commit()

            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.conn.rollback()

            return False

    def login_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()  # Hash the password before checking
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        self.cursor.execute(query, (username, hashed_password))
        result = self.cursor.fetchone()
        return result
        

    
    def username_exists(self, username):
        """
        Check if the given username already exists in the database.
        """
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
        result = self.cursor.fetchone()[0]
        return result > 0
    
    def search_users(self, query):
        search_query = f"%{query}%"
        self.cursor.execute("SELECT id, username, name FROM users WHERE username LIKE %s OR name LIKE %s", (search_query, search_query))
        return self.cursor.fetchall()
    
    def send_friend_request(self, sender_id, receiver_id):
        if sender_id == receiver_id:
            return False  # Users can't send requests to themselves
        # Check if request already exists
        self.cursor.execute("SELECT * FROM friend_requests WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s)", (sender_id, receiver_id, receiver_id, sender_id))
        if self.cursor.fetchone():
            return False  # Request already exists

        self.cursor.execute("INSERT INTO friend_requests (sender_id, receiver_id) VALUES (%s, %s)", (sender_id, receiver_id))
        self.conn.commit()
        return True
    
    def get_user_details(self, user_id):
        self.cursor.execute("SELECT username, name, email FROM users WHERE id = %s", (user_id,))
        return self.cursor.fetchone()

    def get_friends(self, user_id):
        self.cursor.execute("""
            SELECT id, username, name
            FROM users
            WHERE id IN (
                SELECT user_one_id FROM friendships WHERE user_two_id = %s AND status = 'ACCEPTED'
                UNION
                SELECT user_two_id FROM friendships WHERE user_one_id = %s AND status = 'ACCEPTED'
            )
        """, (user_id, user_id))
        return self.cursor.fetchall()
    
    def get_pending_requests(self, user_id):
        self.cursor.execute("SELECT sender_id, username, name FROM friend_requests JOIN users ON sender_id = users.id WHERE receiver_id = %s AND status = 'PENDING'", (user_id,))
        return self.cursor.fetchall()

    def accept_friend_request(self, sender_id, receiver_id):
        self.cursor.execute("UPDATE friend_requests SET status = 'ACCEPTED' WHERE sender_id = %s AND receiver_id = %s", (sender_id, receiver_id))
        self.conn.commit()

    def add_friend(self, user_id, friend_id):
        self.cursor.execute("INSERT INTO friends (user_id, friend_id) VALUES (%s, %s)", (user_id, friend_id))
        self.cursor.execute("INSERT INTO friends (user_id, friend_id) VALUES (%s, %s)", (friend_id, user_id))  # Friendship is mutual
        self.conn.commit()

    def remove_friend(self, user_id, friend_id):
        self.cursor.execute("DELETE FROM friends WHERE user_id = %s AND friend_id = %s", (user_id, friend_id))
        self.cursor.execute("DELETE FROM friends WHERE user_id = %s AND friend_id = %s", (friend_id, user_id))  # Remove mutual friendship
        self.conn.commit()

    def reject_friend_request(self, sender_id, receiver_id):
        self.cursor.execute("UPDATE friend_requests SET status = 'REJECTED' WHERE sender_id = %s AND receiver_id = %s", (sender_id, receiver_id))
        self.conn.commit()

    def send_message(self, sender_id, receiver_id, message_text):
        query = "INSERT INTO messages (sender_id, receiver_id, message_text) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (sender_id, receiver_id, message_text))
        self.conn.commit()

    def get_messages(self, user_id_1, user_id_2):
        query = ("SELECT sender_id, content FROM messages WHERE (sender_id = %s AND receiver_id = %s) OR "
             "(sender_id = %s AND receiver_id = %s) ORDER BY timestamp ASC")
        self.cursor.execute(query, (user_id_1, user_id_2, user_id_2, user_id_1))
        return self.cursor.fetchall()


    def close(self):
        self.cursor.close()
        self.conn.close()
