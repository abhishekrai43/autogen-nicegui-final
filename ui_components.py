from nicegui import ui
import re
import html

completion_message = 'Previous Task completed. Please type in your new task.'
data = {
    'max_count': 5,
    'human_input_mode': 'NEVER',
    'speaker_selection_method': 'auto',
    'agent_no': 1,
    'allow_repeat_speaker':True,
    'user_system_message':'A human Admin',
    'agents': [
        {
            'name': '',
            'system_message': '',
            'avatar_url': 'https://i.imgur.com/sIpKKMZ.jpg'
            
        },
        {
            'name': '',
            'system_message': '',
            'avatar_url': 'https://i.imgur.com/JuHbFz6.jpg'
        },
                    {
            'name': '',
            'system_message': '',
            
        },


    ]
}
def agent_card(container):
    container.clear()
    with container:
        for i in range(data['agent_no']):
            with ui.card().classes("w-full mb-4"):  # Ensure the card takes the full width of the container
                ui.label("Agent").classes("square")
                ui.separator()
                ui.input(label="Name", placeholder="Enter your Name").props(
                    "square outlined dense clearable").bind_value(data['agents'][i], "name")
                ui.textarea(label="System message", placeholder="Enter your messages").props(
                    "square outlined dense").bind_value(data['agents'][i], "system_message").style('height: 100px; max-height: 150px; overflow-y: auto;')  
                ui.separator()



def dialog_box(dialog):
    with ui.column():
        with ui.card().classes("w-full dialog-card"):
            ui.label('Click the HELP button below to know more about these options')
            ui.separator()
            ui.label("Max Rounds").classes("square")
            slider = ui.slider(min=0, max=35, value=15).props("square outlined").bind_value(data, 'max_count')
            ui.label('Max Rounds').classes("square").bind_text(data, "max_count")
            human_input_mode_dropdown = ui.select(
                label='Human Input Mode', 
                options=['NEVER', 'TERMINATE', 'ALWAYS'], 
                value='NEVER'
            ).bind_value(data, 'human_input_mode')

            speaker_selection_method_dropdown = ui.select(
                label='Speaker Selection Method', 
                options=['auto', 'manual', 'random', 'round_robin'], 
                value='auto'
            ).bind_value(data, 'speaker_selection_method')
            allow_repeat_speaker = ui.select(
                label='Allow Repeat Speaker', 
                options=[True, False], 
                value=True
            ).bind_value(data, 'allow_repeat_speaker')
            container1 = ui.column().classes("gap-5 p-2")
            container2 = ui.column().classes("dialog-form-container gap-5").style("max-height: 600px; overflow-y: auto;")  # Set a maximum height and allow scrolling
            with container1:
                ui.label("No. of agents: ")
                ui.select([1, 2, 3], value=1, on_change=lambda e: agent_card(container2)).bind_value(data,
                                                                                                    "agent_no")
            with container2:
                agent_card(container2)
            with ui.row().classes('flex justify-between w-full'):
                ui.button("Cancel", on_click=lambda: dialog.submit("No"))
                ui.button('Help', on_click=show_help_dialog)
                ui.button("Ok", on_click=lambda: dialog.submit("Yes"))

def show_help_dialog():
        markdown_text = """
        **Max Rounds**
        The maximum number of rounds.

        **Human Input Mode**
        Specifies whether to ask for human inputs every time a message is received. Possible values are "ALWAYS", "TERMINATE", "NEVER".

        - **ALWAYS**: The agent prompts for human input every time a message is received. The conversation stops when the human input is "exit", or when `is_termination_msg` is True and there is no human input.
        - **TERMINATE**: The agent only prompts for human input when a termination message is received or the number of auto replies reaches `max_consecutive_auto_reply`.
        - **NEVER**: The agent will never prompt for human input. The conversation stops when the number of auto replies reaches `max_consecutive_auto_reply` or when `is_termination_msg` is True.

        **Speaker Selection Method**
        The method for selecting the next speaker. The default is "auto". Options include (case insensitive):

        - **auto**: The next speaker is selected automatically by the LLM.
        - **manual**: The next speaker is selected manually by user input.
        - **random**: The next speaker is selected randomly.
        - **round_robin**: The next speaker is selected in a round-robin fashion, i.e., iterating in the same order as provided in agents.

        **Allow Repeat Speaker**
        Determines whether to allow the same speaker to speak consecutively. The default is `True`, where all speakers are allowed to speak consecutively. If `allow_repeat_speaker` is a list of Agents, then only those listed agents are allowed to repeat. If set to `False`, no speakers are allowed to repeat.

        """
        ui.markdown(markdown_text).style('color: #0FA47F; background-color: white; margin-top: 10px;')
def custom_render_message(text, stamp, sender, avatar_url, sent):
    rendered = False
    parts = re.split(r"(<codeblock>.*?</codeblock>)", text, flags=re.DOTALL)

    for part in parts:
        if "<codeblock>" in part:
            # Handle code block
            code_content = re.search(r"<codeblock>(.*?)</codeblock>", part, re.DOTALL)
            if code_content:
                code_text = html.unescape(code_content.group(1))
                ui.code(code_text).classes('w-full bg-transparent')
        elif part.strip():
            # Handle regular text
            if not rendered:
                ui.chat_message(text=part, stamp=stamp, name=sender, avatar=avatar_url,text_html=True, sent=sent).classes(
                    f'w-full bg-transparent')
                rendered = True

def format_message(message):
    # Replace code blocks with a special marker
    formatted_message = re.sub(
        r"```(.*?)```",
        lambda match: "<codeblock>" + html.escape(match.group(1)) + "</codeblock>",
        message,
        flags=re.DOTALL
    )
    return formatted_message

