import tkinter as tk
from tkinter import filedialog, messagebox
from telethon import TelegramClient, errors
import asyncio
import pickle

# File name to store session information
SESSION_FILE = "session_info.pkl"

# Function to save session information
def save_session_info(api_id, api_hash, phone_number):
    session_info = {
        'api_id': api_id,
        'api_hash': api_hash,
        'phone_number': phone_number
    }
    with open(SESSION_FILE, 'wb') as f:
        pickle.dump(session_info, f)
    messagebox.showinfo("Saved", "Session information saved successfully.")

# Function to load session information
def load_session_info():
    try:
        with open(SESSION_FILE, 'rb') as f:
            session_info = pickle.load(f)
            return session_info['api_id'], session_info['api_hash'], session_info['phone_number']
    except FileNotFoundError:
        messagebox.showerror("Error", "No session information found.")
        return None, None, None
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load session information: {e}")
        return None, None, None

# Function to send messages
async def send_messages(api_id, api_hash, phone_number, message, attachment, numbers, delay):
    client = TelegramClient('session_name', api_id, api_hash)

    try:
        await client.start(phone_number)
    except errors.ApiIdInvalidError:
        messagebox.showerror("Error", "Invalid API ID or hash.")
        return
    except errors.PhoneNumberInvalidError:
        messagebox.showerror("Error", "Invalid phone number.")
        return
    except errors.FloodWaitError as e:
        messagebox.showerror("Error", f"Telegram API limit exceeded. Try again in {e.seconds} seconds.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect: {e}")
        return

    if not await client.is_user_authorized():
        try:
            await client.sign_in(phone_number)
            # Check if 2FA is enabled
            if not await client.is_user_authorized():
                password = input("Enter your 2FA password: ")
                await client.sign_in(password=password)
        except errors.SessionPasswordNeededError:
            password = input("Enter your 2FA password: ")
            await client.sign_in(password=password)
        except Exception as e:
            messagebox.showerror("Error", f"Authorization failed: {e}")
            return

    total_messages = len(numbers)

    for i, phone in enumerate(numbers, start=1):
        try:
            user = await client.get_entity(phone)
            await client.send_message(user, message, file=attachment if attachment else None)
            print(f'({i}/{total_messages}) Message sent to {phone}')
        except Exception as e:
            print(f'({i}/{total_messages}) Failed to send message to {phone}: {e}')

        await asyncio.sleep(delay)  # Delay between messages

    await client.disconnect()

# Function to handle send button click
def on_send_click():
    api_id = api_id_entry.get()
    api_hash = api_hash_entry.get()
    phone_number = phone_number_entry.get()
    message = message_text.get("1.0", tk.END).strip()
    attachment_path = attachment_entry.get()
    numbers = numbers_text.get("1.0", tk.END).strip().split('\n')
    delay = int(delay_entry.get())

    if not api_id or not api_hash or not phone_number or not message or not numbers or delay < 0:
        messagebox.showerror("Error", "All fields are required and delay must be non-negative!")
        return

    # Save session information
    save_session_info(api_id, api_hash, phone_number)

    # Run send_messages in asyncio event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_messages(api_id, api_hash, phone_number, message, attachment_path, numbers, delay))
    loop.close()

# Function to handle file dialog
def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

# Function to load session information into GUI
def load_session_to_gui():
    api_id, api_hash, phone_number = load_session_info()
    if api_id and api_hash and phone_number:
        api_id_entry.insert(0, api_id)
        api_hash_entry.insert(0, api_hash)
        phone_number_entry.insert(0, phone_number)

# GUI setup
root = tk.Tk()
root.title("Telegram Bulk Message Sender")

# Session Information Frame
session_frame = tk.LabelFrame(root, text="Session Information", padx=10, pady=10)
session_frame.pack(padx=10, pady=5, fill="x")

tk.Label(session_frame, text="API ID:").grid(row=0, column=0, sticky="e")
api_id_entry = tk.Entry(session_frame, width=40)
api_id_entry.grid(row=0, column=1, pady=5)

tk.Label(session_frame, text="API Hash:").grid(row=1, column=0, sticky="e")
api_hash_entry = tk.Entry(session_frame, width=40)
api_hash_entry.grid(row=1, column=1, pady=5)

tk.Label(session_frame, text="Phone Number:").grid(row=2, column=0, sticky="e")
phone_number_entry = tk.Entry(session_frame, width=40)
phone_number_entry.grid(row=2, column=1, pady=5)

# Load session information if available
load_session_to_gui()

# Bulk Message Frame
message_frame = tk.LabelFrame(root, text="Bulk Message", padx=10, pady=10)
message_frame.pack(padx=10, pady=5, fill="x")

tk.Label(message_frame, text="Message:").grid(row=0, column=0, sticky="nw")
message_text = tk.Text(message_frame, height=5, width=40)
message_text.grid(row=0, column=1, pady=5)

tk.Label(message_frame, text="Attachment:").grid(row=1, column=0, sticky="e")
attachment_entry = tk.Entry(message_frame, width=30)
attachment_entry.grid(row=1, column=1, pady=5, sticky="w")
attachment_button = tk.Button(message_frame, text="Browse", command=lambda: select_file(attachment_entry))
attachment_button.grid(row=1, column=2, padx=5)

tk.Label(message_frame, text="Delay (seconds):").grid(row=2, column=0, sticky="e")
delay_entry = tk.Entry(message_frame, width=5)
delay_entry.grid(row=2, column=1, pady=5, sticky="w")

# Numbers Frame
numbers_frame = tk.LabelFrame(root, text="Numbers", padx=10, pady=10)
numbers_frame.pack(padx=10, pady=5, fill="x")

tk.Label(numbers_frame, text="Phone Numbers:").grid(row=0, column=0, sticky="nw")
numbers_text = tk.Text(numbers_frame, height=10, width=40)
numbers_text.grid(row=0, column=1, pady=5)

# Send Button
send_button = tk.Button(root, text="Send Messages", command=on_send_click)
send_button.pack(pady=10)

root.mainloop()
