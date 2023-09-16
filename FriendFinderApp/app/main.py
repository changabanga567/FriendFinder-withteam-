import tkinter as tk
import hashlib
from tkinter import messagebox
from database import Database

class App:
    def __init__(self, root):
        self.current_user_id = None
        self.root = root
        self.root.title("Friend Finder")

        # frames design
        self.login_frame = tk.Frame(self.root)
        self.register_frame = tk.Frame(self.root)
        self.dashboard_frame = tk.Frame(self.root)  # Initialize the dashboard_frame here

        # go back to login frame
        self.show_login_frame()

    def show_login_frame(self):
        """Display the login frame."""
        # Clear the register frame
        for widget in self.register_frame.winfo_children():
         widget.destroy()

        self.register_frame.pack_forget()
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # Username
        tk.Label(self.login_frame, text="Username:").pack(pady=10)
        self.login_username_entry = tk.Entry(self.login_frame)
        self.login_username_entry.pack(pady=5)

        # Password
        tk.Label(self.login_frame, text="Password:").pack(pady=10)
        self.login_password_entry = tk.Entry(self.login_frame, show="*")
        self.login_password_entry.pack(pady=5)

        # Buttons
        tk.Button(self.login_frame, text="Login", command=self.login_user).pack(pady=20)
        tk.Button(self.login_frame, text="Go to Register", command=self.show_register_frame).pack(pady=10)

    def login_user(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()  # Retrieve password from the entry

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        self.cursor.execute(query, (username, hashed_password))
        result = self.cursor.fetchone()
        return result

    def logout(self):
        # Clear current user data
        self.current_user_id = None

        # Destroy dashboard widgets
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
    
        #  Hide dashboard frame and show login frame
        self.dashboard_frame.pack_forget()
        self.show_login_frame()

    def show_register_frame(self):
        """Display the register frame."""
    # Clear the login frame
        for widget in self.login_frame.winfo_children():
         widget.destroy()

        self.login_frame.pack_forget()
        self.register_frame.pack(fill=tk.BOTH, expand=True)

        # Username
        tk.Label(self.register_frame, text="Username:").pack(pady=10)
        self.register_username_entry = tk.Entry(self.register_frame)
        self.register_username_entry.pack(pady=5)

        # Password
        tk.Label(self.register_frame, text="Password:").pack(pady=10)
        self.register_password_entry = tk.Entry(self.register_frame, show="*")
        self.register_password_entry.pack(pady=5)

        # Name
        tk.Label(self.register_frame, text="Name:").pack(pady=10)
        self.register_name_entry = tk.Entry(self.register_frame)
        self.register_name_entry.pack(pady=5)

        # Email
        tk.Label(self.register_frame, text="Email:").pack(pady=10)
        self.register_email_entry = tk.Entry(self.register_frame)
        self.register_email_entry.pack(pady=5)

        # Buttons
        tk.Button(self.register_frame, text="Register", command=self.register_new_user).pack(pady=20)
        tk.Button(self.register_frame, text="Go to Login", command=self.show_login_frame).pack(pady=10)

    def register_new_user(self):
        db = Database()
        success = db.register_user(
            self.register_username_entry.get(),
            self.register_password_entry.get(),
            self.register_name_entry.get(),
            self.register_email_entry.get()
        )
        db.close()

        if success:
            messagebox.showinfo("Success", "Registered successfully!")
            self.show_login_frame()
        else:
            messagebox.showerror("Error", "Registration failed. Username or email might already be in use.")

    def show_dashboard(self):

    # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)

        print("Displaying dashboard...")

    # Display pending friend requests
        self.display_pending_requests()

    def display_pending_requests(self):
        """Display pending friend requests."""
        tk.Label(self.dashboard_frame, text="Pending Friend Requests:").pack(pady=20)
    
        db = Database()
        requests = db.get_pending_requests(self.current_user_id)
        db.close()

        if requests:
            for sender_id, username, name in requests:
                request_frame = tk.Frame(self.dashboard_frame)
                request_frame.pack(fill=tk.BOTH, pady=5)

                tk.Label(request_frame, text=f"Request from {username} ({name})").pack(side=tk.LEFT)
                tk.Button(request_frame, text="Accept", command=lambda sender_id=sender_id: self.accept_request(sender_id)).pack(side=tk.RIGHT, padx=5)
                tk.Button(request_frame, text="Reject", command=lambda sender_id=sender_id: self.reject_request(sender_id)).pack(side=tk.RIGHT)
            else:
                tk.Label(self.dashboard_frame, text="No pending friend requests.").pack(pady=20)

    # Display the 'See Friends List' button
        tk.Button(self.dashboard_frame, text="See Friends List", command=self.display_friends).pack(pady=10)

    # Search bar
        self.search_entry = tk.Entry(self.dashboard_frame)
        self.search_entry.pack(pady=20)
        tk.Button(self.dashboard_frame, text="Search Users", command=self.search_users).pack(pady=10)

    
    def display_friends(self):
        # Clear the dashboard of previous content
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        print("Displaying friends list...")


        db = Database()
        friends = db.get_friends(self.current_user_id)
        db.close()


        for friend in friends:
            print(friend)

    # Clear the login frame
        for widget in self.login_frame.winfo_children():
            widget.destroy()
        self.login_frame.pack_forget()

    # Create the dashboard frame
        self.dashboard_frame = tk.Frame(self.root)
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)


    # Display pending friend requests
        tk.Label(self.dashboard_frame, text="Pending Friend Requests:").pack(pady=20)
        db = Database()
        requests = db.get_pending_requests(self.current_user_id)
        db.close()

    # add button to view users profile
        tk.Button(self.dashboard_frame, text="View Profile", command=self.show_profile).pack(pady=20)

    #show friends list
        tk.Button(self.dashboard_frame, text="See Friends List", command=self.display_friends).pack(pady=10)


    #logout
        tk.Button(self.dashboard_frame, text="Logout", command=self.logout).pack(pady=20)


        if requests:
            for sender_id, username, name in requests:
                request_frame = tk.Frame(self.dashboard_frame)
                request_frame.pack(fill=tk.BOTH, pady=5)

            tk.Label(request_frame, text=f"Request from {username} ({name})").pack(side=tk.LEFT)
            tk.Button(request_frame, text="Accept", command=lambda sender_id=sender_id: self.accept_request(sender_id)).pack(side=tk.RIGHT, padx=5)
            tk.Button(request_frame, text="Reject", command=lambda sender_id=sender_id: self.reject_request(sender_id)).pack(side=tk.RIGHT)

        # Search bar
        self.search_entry = tk.Entry(self.dashboard_frame)  # Add this line
        self.search_entry.pack(pady=20)  # And this line

        self.search_button = tk.Button(self.dashboard_frame, text="Search Users", command=self.search_users)
        self.search_button.pack(pady=10)

    def search_users(self):
        query = self.search_entry.get()
        

        # Clear any previous search results, except for the search bar and button
        for widget in self.dashboard_frame.winfo_children():
         if widget not in (self.search_entry, self.search_button):
            widget.destroy()

        db = Database()
        results = db.search_users(query)
        db.close()

        # Display new search results
        for user_id, username, name in results:
            result_frame = tk.Frame(self.dashboard_frame)
            result_frame.pack(fill=tk.BOTH, pady=5)

            tk.Label(result_frame, text=f"Username: {username}, Name: {name}").pack(side=tk.LEFT)
            tk.Button(result_frame, text="Send Request", command=lambda user_id=user_id: self.send_request(user_id)).pack(side=tk.RIGHT)

    
    def show_profile(self):
    # Clear the current frame
        self.clear_frame(self.dashboard_frame)

        # Initialize the profile frame
        self.profile_frame = tk.Frame(self.root)
        self.profile_frame.pack(fill=tk.BOTH, expand=True)
        tk.Button(self.profile_frame, text="Back", command=self.return_to_dashboard).pack(pady=20)


        # Fetch user details
        db = Database()
        user_details = db.get_user_details(self.current_user_id)
        friends = db.get_friends(self.current_user_id)
        db.close()

        # Display user details
        tk.Label(self.dashboard_frame, text=f"Username: {user_details[0]}").pack(pady=10)
        tk.Label(self.dashboard_frame, text=f"Name: {user_details[1]}").pack(pady=10)
        tk.Label(self.dashboard_frame, text=f"Email: {user_details[2]}").pack(pady=10)

        # Display friend list
        tk.Label(self.dashboard_frame, text="Friends:").pack(pady=20)
        for friend_id, username, name in friends:
            friend_frame = tk.Frame(self.dashboard_frame)
            friend_frame.pack(fill=tk.BOTH, pady=5)
            tk.Label(friend_frame, text=f"{username} ({name})").pack(side=tk.LEFT)
            tk.Button(friend_frame, text="Remove", command=lambda friend_id=friend_id: self.remove_friend(friend_id)).pack(side=tk.RIGHT)



    def show_friends_list(self):
        # Clear the dashboard
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        db = Database()
        friends = db.get_friends(self.current_user_id)
        db.close()

        # Display each friend
        for friend_id, username, name in friends:
            friend_frame = tk.Frame(self.dashboard_frame)
            friend_frame.pack(fill=tk.BOTH, pady=5)
            tk.Label(friend_frame, text=f"Username: {username}, Name: {name}").pack(side=tk.LEFT)

        # Add a back button to return to the dashboard
        tk.Button(self.dashboard_frame, text="Back to Dashboard", command=self.show_dashboard).pack(pady=20)


        
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        frame.pack_forget()

    def return_to_dashboard(self):
        """Clear the profile frame and show the dashboard."""
        self.clear_frame(self.profile_frame)
        self.show_dashboard()
    
    
    
    def send_request(self, receiver_id):
        db = Database()
        success = db.send_friend_request(self.current_user_id, receiver_id)
        db.close()

        if success:
            messagebox.showinfo("Success", "Friend request sent!")
        else:
            messagebox.showerror("Error", "Failed to send friend request.")

    def accept_request(self, sender_id):
        print("Accepting friend request...")
        db = Database()
        db.accept_friend_request(sender_id, self.current_user_id)
        db.close()
        self.show_dashboard()  # Refresh dashboard

    def reject_request(self, sender_id):
        db = Database()
        db.reject_friend_request(sender_id, self.current_user_id)
        db.close()
        self.show_dashboard()  # Refresh dashboard

    def remove_friend(self, friend_id):
        db = Database()
        db.remove_friend(self.current_user_id, friend_id)
        db.close()
        self.show_profile()  # Refresh the profile view after removing a friend


    def open_chat(self, friend_id):
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title("Chat")

        self.message_display = tk.Text(self.chat_window, height=20, width=50)
        self.message_display.pack(pady=20)

        self.message_entry = tk.Entry(self.chat_window, width=40)
        self.message_entry.pack(pady=10, side=tk.LEFT)

        tk.Button(self.chat_window, text="Send", command=lambda: self.send_message(friend_id)).pack(side=tk.RIGHT)

    # Display recent messages
        self.display_recent_messages(friend_id)

    def send_message(self, receiver_id):
        message_text = self.message_entry.get()
        if message_text:
            db = Database()
            db.send_message(self.current_user_id, receiver_id, message_text)
            db.close()

            self.message_display.insert(tk.END, f"You: {message_text}\n")
            self.message_entry.delete(0, tk.END)

    def display_recent_messages(self, friend_id):
        db = Database()
        messages = db.get_messages(self.current_user_id, friend_id)
        for sender_id, message_text, _ in messages:
            sender = "You" if sender_id == self.current_user_id else "Friend"
            self.message_display.insert(tk.END, f"{sender}: {message_text}\n")
            db.close()

        # Fetch the list of friends from the database
        db = Database()
        friends = db.get_friends(self.current_user_id)
        db.close()

        # Create a label to indicate the friends list
        tk.Label(self.dashboard_frame, text="Friends List", font=("Arial", 16)).pack(pady=10)

        #  go over list of friends and display each one
        for friend_id, username, name in friends:
            friend_frame = tk.Frame(self.dashboard_frame, borderwidth=1, relief="solid")
            friend_frame.pack(fill=tk.BOTH, pady=5)
            tk.Label(friend_frame, text=f"Username: {username}, Name: {name}").pack(side=tk.LEFT, padx=10)
            # You can also add more features/buttons for each friend if needed

        # Add a back button to return to the main dashboard
        tk.Button(self.dashboard_frame, text="Back to Dashboard", command=self.show_dashboard).pack(pady=20)


        



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
