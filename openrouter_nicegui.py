from datetime import datetime
from nicegui import ui, context
import autogen
from uuid import uuid4
import asyncio
import re
import html
from pathlib import Path

# Path to swear.txt relative to the current script
swear_file_path = Path(__file__).parent / 'swear.txt'
swear_words_set = set()

def load_swear_words():
    global swear_words_set
    if swear_file_path.exists():
        with open(swear_file_path, 'r') as file:
            swear_words_set = {line.strip().lower() for line in file}
load_swear_words()
last_processed_msg_index = -1
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config=False,
    human_input_mode="ALWAYS",
)

groupchat = autogen.GroupChat(agents=[user_proxy], messages=[], max_round=5)
manager = autogen.GroupChatManager(groupchat=groupchat)
slash_commands = {
    "/help": "Provide a summary of available commands and their functions.",
    "/python": "List 10 helpful Python commands or snippets.",
    "/debug": "Offer debugging tips or help identify issues in a provided code snippet.",
    "/algorithm": "Explain a specific algorithm or compare different algorithms for a given problem.",
    "/latest_tech": "Share the latest updates or news in technology and IT.",
    "/optimize": "Suggestions for optimizing a given piece of code or system.",
    "/AI_trends": "Discuss current trends and advancements in AI and machine learning.",
    "/web_dev": "Provide tips, tricks, or insights related to web development.",
    "/security": "Share best practices and tips for IT security and cybersecurity.",
    "/data_analysis": "Offer guidance or methods for effective data analysis."
}

# groupchat.messages()
@ui.page('/')
def main():
    ui.add_head_html('''
        <style>
        :root {
            font-family: 'Inter', sans-serif;
            --nicegui-default-padding: 0;
            --nicegui-default-gap: 0;
        }
        #c6 {
            margin-left: auto;
            margin-right: auto;
            width: 60%; 
            font-family: 'Roboto', sans-serif; /* Stylish font */
 
            }
        #c4, .custom-footer {
            margin-left: auto;
            margin-right: auto;
            width: 60%; 
         
        #c4 {
            margin-top: 10px; 
            height: 60vh; 
            width: 60%; 
            margin-left: auto;
            margin-right: auto;
            border: 1px solid #e2e8f0; 
            background-color: #f8fafc; 
            border-radius: 8px; 
            overflow: auto; 
        }
           
        }
        .chat-area {
            margin-left: auto !important;
            margin-right: auto !important;
            width: 60% !important; 
            height: calc(100vh - 175px) !important; 
            border: 1px solid #e2e8f0 !important; 
            background-color: #f8fafc !important; 
            border-radius: 8px !important; 
        }
        .custom-footer {
            position: fixed;
            left: 5px;
            bottom: 0;
            padding: 10px;
           
        }
        .q-message-container {align-items: start!important; }

        .q-message-text, .q-message-text--received {
            font-family: 'Roboto', sans-serif; 
            background-color: transparent; 
            border: none; 
            color: #FFFFFF; 
            word-wrap: break-word; 
        }

        .q-message-text--received {
            overflow: hidden; 
            white-space: normal; 
            letter-spacing: .15em; 
        }
        pre {
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-left: 3px solid #f36d33;
            color: #666;
            page-break-inside: avoid;
            font-family: monospace;
            font-size: 15px;
            line-height: 1.6;
            max-width: 100%;
            overflow: auto;
            display: block;
            padding: 1em;
            margin: 0.5em 0;
            word-wrap: break-word;
        }

        code {
            font-family: monospace;
            line-height: 1.6;
        }
        .message-left {
            display: flex;
            align-items: center;
            justify-content: start;
        }

        .message-right {
            display: flex;
            align-items: center;
            justify-content: end;
        }

        .message-box {
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            background-color: lightgray;
        }
        </style>
    ''')
    messages = []
    user_id = str(uuid4())  # Unique ID for each user session

    @ui.refreshable
    def chat_messages():
        for sender, text, stamp in messages:
            if sender == 'You':
                avatar_url = 'https://i.imgur.com/cdEg28i.png'  # User avatar
            else:
                avatar_url = 'https://i.imgur.com/ndKiywr.png'  # Bot avatar

            custom_render_message(text, stamp, sender, avatar_url)
        if context.get_client().has_socket_connection:
            ui.run_javascript('setTimeout(() => window.scrollTo(0, document.body.scrollHeight), 0)')
    
    def custom_render_message(text, stamp, sender, avatar_url):
        rendered = False
        # Split the message into parts (text and code)
        parts = re.split(r"(<codeblock>.*?</codeblock>)", text, flags=re.DOTALL)
        for part in parts:
            if "<codeblock>" in part:
                # Handling code block
                code_content = re.search(r"<codeblock>(.*?)</codeblock>", part, re.DOTALL)
                if code_content:
                    code_text = html.unescape(code_content.group(1))
                    ui.code(code_text).classes('w-full bg-transparent')
            elif part.strip():
                # Handling regular text
                if not rendered:
                    ui.chat_message(text=part, stamp=stamp, name=sender, avatar=avatar_url, sent=sender == 'You').classes(
                    'w-full bg-transparent')
                    rendered = True
                else:
                    ui.chat_message(text=part, stamp=stamp, sent=sender == 'You').classes(
                    'w-full bg-transparent')
    def create_help_command(slash_commands):
        help_string = "Available Commands:\n"
        for command, description in slash_commands.items():
            help_string += f"{command}: {description}\n"
        return help_string
    
    async def send():
        global last_processed_msg_index
        user_message = task_input.value
        stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        task_input.value = '' 
            # Read swear words from the file
        words_in_message = set(word.lower() for word in user_message.split())
        found_swear_words = words_in_message.intersection(swear_words_set)
        if found_swear_words:
            warning_message = f"Please avoid using inappropriate language. Found: {', '.join(found_swear_words)}"
            messages.append(('System', warning_message, stamp))
            chat_messages.refresh()
            return
        # Split the command and the accompanying text
        command, *additional_text = user_message.split(' ', 1)
        additional_text = additional_text[0] if additional_text else ""
            # Check for /help command
        if user_message.lower() == '/help':
            help_message = create_help_command(slash_commands)
            messages.append(('You', user_message, stamp))
            messages.append(('System', help_message, stamp))
            chat_messages.refresh()
            return
        # Handle /debug command
        if command.lower() == '/debug' and additional_text:
            user_message = f"Please help me debug this code:\n\n{additional_text}"
        # Handle /optimize command
        elif command.lower() == '/optimize' and additional_text:
            user_message = f"Please provide optimization suggestions for this code:\n\n{additional_text}"
        # Handle /algorithm command
        elif command.lower() == '/algorithm' and additional_text:
            user_message = f"Can you explain or compare the following algorithm(s): {additional_text}"
        # Other commands are processed as usual
        else:
            if command in slash_commands:
                user_message = slash_commands[command]
            elif command.startswith('/'):
                error_message = "Command not recognized. Please try again or use /help for a list of commands."
                messages.append(('You', user_message, stamp))
                messages.append(('System', error_message, stamp))
                chat_messages.refresh()
                return

        # Add the user's message to the chat
        messages.append(('You', user_message, stamp))
        chat_messages.refresh()
 
        await user_proxy.a_initiate_chat(manager, message=user_message)

        autogen_messages = groupchat.messages
        new_messages = autogen_messages[last_processed_msg_index + 1:]
        for msg in new_messages:
            content = msg['content']
            sender_name = msg['name']

            # Format the content and sender based on the role
            formatted_content = format_message(content)  # Add any necessary formatting

            # Append the message to the messages list for NiceGUI
            messages.append((sender_name, formatted_content, stamp))
            chat_messages.refresh()

        # Update the last processed message index
        last_processed_msg_index += len(new_messages)

        # Append a message indicating task completion
        completion_message = 'Previous Task completed. Please type in your new task.'
        messages.append(("System", completion_message, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
        chat_messages.refresh()

    def format_message(message):
        # Replace code blocks with a special marker
        formatted_message = re.sub(
            r"```(.*?)```", 
            lambda match: "<codeblock>" + html.escape(match.group(1)) + "</codeblock>", 
            message, 
            flags=re.DOTALL
        )
        return formatted_message
       
    with ui.scroll_area().classes('chat-area w-full p-3 bg-white'):
        chat_messages()
    with ui.footer().classes('custom-footer'):
        task_input = ui.input().style('width: calc(100% - 100px);')
        ui.button('Send', on_click=send).style('width: 90px;')

@ui.page('/ConfigureAgents')
def configure_agents():
    with ui.card().classes('q-pa-md q-ma-md flex flex-center border-2 rounded-lg shadow-2xl'):
        ui.label('Agent Configuration').classes('text-h6 q-mb-md')
        num_agents = ui.select([1, 2, 3], value=1, label='Number of Agents',on_change=lambda e: ui.notify(e.value)).classes('w-40')
        agent_name_1 = ui.input(label='Agent 1 Name', placeholder='Name').classes('q-mb-md')
        agent_system_message_1 = ui.textarea('Agent 1 System Message', placeholder='System Message').classes('q-mb-md')
        agent_name_2 = ui.input(label='Agent 2 Name', placeholder='Name').set_visibility(False)
        agent_system_message_2 = ui.textarea('Agent 2 System Message', placeholder='System Message').set_visibility(False)
        agent_name_3 = ui.input(label='Agent 3 Name', placeholder='Name').set_visibility(False)
        agent_system_message_3 = ui.textarea('Agent 3 System Message', placeholder='System Message').set_visibility(False)
        ui.label('Max Rounds').classes('q-mb-md')
        max_round_slider = ui.slider(min=1, max=10, step=1, value=5).classes('q-mb-md').on('update:model-value', lambda e: ui.notify(e.args),
        throttle=1.0)

        def apply_configuration():
            # Logic to create agents and update groupchat
            agents = []
            if num_agents.value >= 1:
                agents.append(autogen.AssistantAgent(name=agent_name_1.value, system_message=agent_system_message_1.value))
            if num_agents.value >= 2:
                agents.append(autogen.AssistantAgent(name=agent_name_2.value, system_message=agent_system_message_2.value))
            if num_agents.value == 3:
                agents.append(autogen.AssistantAgent(name=agent_name_3.value, system_message=agent_system_message_3.value))

            # Update groupchat with new agents and max_round
            groupchat.agents = [user_proxy] + agents
            groupchat.max_round = max_round_slider.value
            ui.notify('Configuration Applied')

        ui.button('Apply', on_click=apply_configuration)

        def update_visibility():
            agent_name_2.set_visibility(num_agents.value >= 2)
            agent_system_message_2.set_visibility(num_agents.value >= 2)
            agent_name_3.set_visibility(num_agents.value == 3)
            agent_system_message_3.set_visibility(num_agents.value == 3)
    # Add CSS for overall page styling
    ui.add_head_html('''
    <style>
        body {
            background-color: #f5f5f5; /* Light grey background */
        }
        .flex-center {
            justify-content: center; /* Center card horizontally */
            align-items: center; /* Center card vertically */
            height: 100vh; /* Full viewport height */
        }
        .q-card {
            width: 50%; /* Adjust card width */
            background-color: #ffffff; /* White card background */
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* Card shadow */
        }
        .q-input, .q-select, .q-slider {
            width: 100%; /* Full width inputs */
        }
    </style>
    ''')

    def apply_configuration():
        # Logic to create agents and update groupchat
        agents = []
        if num_agents.value >= 1:
            agents.append(autogen.AssistantAgent(name=agent_name_1.value, system_message=agent_system_message_1.value))
        if num_agents.value >= 2:
            agents.append(autogen.AssistantAgent(name=agent_name_2.value, system_message=agent_system_message_2.value))
        if num_agents.value == 3:
            agents.append(autogen.AssistantAgent(name=agent_name_3.value, system_message=agent_system_message_3.value))

        # Update groupchat with new agents and max_round
        groupchat.agents = [user_proxy] + agents
        groupchat.max_round = max_round_slider.value
        ui.notify('Configuration Applied')

    ui.button('Apply', on_click=apply_configuration)
main()
configure_agents()
ui.run(title='Chat with Autogen Assistant',host='localhost',reload=False)
