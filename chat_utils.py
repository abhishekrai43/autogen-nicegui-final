from openrouter_nicegui import groupchat, messages,chat_messages
from ui_components import format_message
from datetime import datetime

last_processed_msg_index = -1
def ui_response():
    global last_processed_msg_index
    autogen_messages = groupchat.messages
    new_messages = autogen_messages[last_processed_msg_index + 1:]
    for msg in new_messages:
        content = msg['content']
        sender_name = msg['name']

        # Format the content and sender based on the role
        formatted_content = format_message(content)  # Add any necessary formatting
        stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        # Append the message to the messages list for NiceGUI
        messages.append((sender_name, formatted_content, stamp))
        chat_messages.refresh()

    # Update the last processed message index
    last_processed_msg_index += len(new_messages)

    # Append a message indicating task completion
    completion_message = 'Previous Task completed. Please type in your new task.'
    messages.append(("System", completion_message, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
    return messages
    chat_messages.refresh()