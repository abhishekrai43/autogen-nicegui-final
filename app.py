from datetime import datetime
from nicegui import ui, context
import autogen
from html_str import html_str
from swear_word_filter import check_swear_words, load_swear_words
from slash_commands import create_help_command,slash_commands,process_command
from ui_components import custom_render_message, dialog_box,format_message,data,completion_message
from positive_words import llm_resp,resp_llm,resp_only
import json
import asyncio


user_input_result = None
class CustomAssistantAgent(autogen.AssistantAgent):
    async def a_get_human_input(self, prompt: str) -> str:
        global user_input_result
        user_input_result = None

        def on_submit(input_value):
            global user_input_result
            user_input_result = input_value
            dialog.close()

        with ui.dialog() as dialog:
            ui.label(prompt)
            input_field = ui.text_input()
            ui.button('Submit', on_click=lambda: on_submit(input_field.value))

        while user_input_result is None:
            await asyncio.sleep(0.1)  # Async wait for the input to be submitted

        return user_input_result

load_swear_words()
last_processed_msg_index = -1
additional_input_field = None
# groupchat.messages()
@ui.page('/')
def main():
    global groupchat 
    global manager
    global messages
    global additional_input_field
    ui.add_head_html(html_str)
    messages = [("Task Manager", "Please click on Configure Agents button to start setting up your agents", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))]
    @ui.refreshable
    def chat_messages():
        for sender, text, stamp in messages:
            if sender == 'You':
                avatar_url = 'https://i.imgur.com/cdEg28i.png'  # User avatar
                custom_render_message(text, stamp, sender, avatar_url, sent=True)
                continue
            elif sender == 'Task Manager':
                avatar_url = 'https://i.imgur.com/4o5DyGB.png'  # User avatar
            else:
            # Find the agent with the matching name and use their avatar
             agent = next((agent for agent in data['agents'] if agent['name'] == sender), None)
             avatar_url = agent['avatar_url'] if agent else 'https://i.imgur.com/jRzh37d.jpg'

            # alternating messages on left or right for diffe
            custom_render_message(text, stamp, sender, avatar_url, sent=False)

            # custom_render_message(text, stamp, sender, avatar_url)
            if context.get_client().has_socket_connection:
                ui.run_javascript('''
                    const btn = document.getElementById("c35");
                    const scrollArea = document.querySelector('.q-scrollarea__container');
                    scrollArea.scrollTop = scrollArea.scrollHeight;
        
                ''')

    user_proxy = autogen.UserProxyAgent(
        name="Requestor",
        system_message='A human Admin',
        code_execution_config=False,
        human_input_mode=data['human_input_mode'],
    )

    # agents list
    agents = [user_proxy]

    async def show(dialog):
        result = await dialog
        if result == "Yes":
            create_agent()
        else:
            ui.notify(f'You chose {result}')
        print(json.dumps(data, indent=4, sort_keys=True))

    def create_agent():
        global groupchat, manager  # Declare global to modify the global instances

        # Clearing existing agents except user_proxy
        agents = [user_proxy]
        if data['agent_no'] < 2:
            with ui.dialog().classes('custom-dialog') as warn_dialog, ui.card():
                ui.label('"GroupChat is underpopulated with 1 agents. "'
                '"It is recommended to set Speaker Selection Method to round_robin or allow_repeat_speaker to False."'
                ).classes('custom-dialog-label')
                warn_dialog.open()

        # Adding new agents as per the data
        for agent_no in range(data['agent_no']):
            agents.append(CustomAssistantAgent(
                name=data['agents'][agent_no]['name'],
                system_message=data['agents'][agent_no]['system_message'],
            ))

        ui.notify('Chosen Settings Applied')
        groupchat = autogen.GroupChat(agents=agents, messages=[], max_round=data["max_count"],speaker_selection_method=data['speaker_selection_method'],allow_repeat_speaker=data['allow_repeat_speaker'])
        manager = autogen.GroupChatManager(groupchat=groupchat)
        chat_messages.refresh()


    async def process_chat_interaction(manager, user_message, messages, groupchat, last_processed_msg_index):
        await user_proxy.a_initiate_chat(manager, message=user_message)
        autogen_messages = groupchat.messages

        new_messages = autogen_messages[last_processed_msg_index + 1:]
        stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        for msg in new_messages:
            content = msg['content']
            sender_name = msg.get('name')  
            formatted_content = format_message(content)
            messages.append((sender_name, formatted_content, stamp))

        last_processed_msg_index += len(new_messages)
        chat_messages.refresh() 
        return last_processed_msg_index

    async def send():
        global last_processed_msg_index
        user_message = task_textarea.value
        stamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        task_textarea.value = '' 
        swear = check_swear_words(user_message)
        if swear:
            messages.append(('Task Manager', swear, stamp))
            chat_messages.refresh()
            return
        pos1 = resp_only(user_message)
        if pos1:
            messages.append(('You', user_message, stamp))
            messages.append(('Task Manager', pos1, stamp))
            chat_messages.refresh()
            return

        pos2 = resp_llm(user_message)  
        if pos2:
            messages.append(('You', user_message, stamp))
            messages.append(('Task Manager', pos2, stamp))
            chat_messages.refresh()
            # Call the process_chat_interaction function
            last_processed_msg_index = await process_chat_interaction(manager, user_message, messages, groupchat, last_processed_msg_index)
            # Append the completion message     
            messages.append(("Task Manager", completion_message, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
            chat_messages.refresh()
            return 
        pos3 = llm_resp(user_message)
        if pos3:
            messages.append(('You', user_message, stamp))
            chat_messages.refresh()
            # Call the process_chat_interaction function
            await user_proxy.a_initiate_chat(manager, message=user_message)
            autogen_messages = groupchat.messages
            new_messages = autogen_messages[last_processed_msg_index + 1:]
            for msg in new_messages:
                content = msg['content']
                sender_name = msg['name']
                formatted_content = format_message(content) + pos3  
                messages.append((sender_name, formatted_content, stamp))
                chat_messages.refresh()
            # Update the last processed message index
            last_processed_msg_index += len(new_messages)
            # Append a message indicating task completion
            messages.append(("Task Manager", completion_message, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
            chat_messages.refresh()
            return
        

        command, *additional_text = user_message.split(' ', 1)
        additional_text = additional_text[0] if additional_text else ""
            # Check for /help command
        if user_message.lower() == '/help':
            help_message = create_help_command(slash_commands)
            messages.append(('You', user_message, stamp))
            messages.append(('Task Manager', help_message, stamp))
            chat_messages.refresh()
            return
        response = process_command(command, additional_text)
        if response:
            messages.append(('You', user_message, stamp))
            chat_messages.refresh()
            await user_proxy.a_initiate_chat(manager, message=user_message)
            chat_messages.refresh()
            last_processed_msg_index = await process_chat_interaction(manager, user_message, messages, groupchat, last_processed_msg_index)
            messages.append(("Task Manager", completion_message, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
            chat_messages.refresh()
            return
        # Add the user's message to the chat
        messages.append(('You', user_message, stamp))
        chat_messages.refresh()
        last_processed_msg_index = await process_chat_interaction(manager, user_message, messages, groupchat, last_processed_msg_index)
        messages.append(("Task Manager", completion_message, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))
        chat_messages.refresh()

    def clear_chat():
        global messages
        messages.clear()  # Clear all messages
        chat_messages.refresh()  # Refresh the chat UI
        
    with ui.row().classes():
        with ui.column().classes('w-full h-full'):
            with ui.row().classes('d-flex justify-between bg-slate-700 w-full'):
                with ui.dialog().classes("w-full dialog-wrapper") as dialog, ui.card():
                    dialog_box(dialog)

                ui.button(text="Configure Agents", on_click=lambda e: show(dialog))
                ui.markdown('<span style="font-size: 20px; color: white; font-family: \'Orbitron\', sans-serif;">**Agent Assist**</span>')
                ui.button(text="Clear Conversation",on_click=clear_chat)

            with ui.row().classes('w-full'):
                with ui.scroll_area().classes('chat-area w-full p-3 bg-white'):
                    chat_messages()

    with ui.footer().classes('custom-footer'):
        task_textarea = ui.textarea().classes('auto-height-textarea')
        ui.button('Send', on_click=send).style('width: 90px; margin-top:7px;')
        ui.label('Type /help to show help commands').style('color: #04571e; margin-left: 250px; margin-top:15px; font-weight: bold; font-weight: bold; font-family: \'Orbitron\', sans-serif;').classes('text-sm')
        

ui.run(title='Agent Assist',host='0.0.0.0',port=443,ssl_certfile='/etc/letsencrypt/live/instaruth.com/fullchain.pem',ssl_keyfile='/etc/letsencrypt/live/instaruth.com/privkey.pem',reconnect_timeout=300)
