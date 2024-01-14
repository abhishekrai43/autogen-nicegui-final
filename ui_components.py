from nicegui import ui
import re
import html
import os

completion_message = 'Previous Task completed. Please type in your new task.'
data = {
    'max_count': 0,
    'agent_no': 1,
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
            ui.label('Add agent')
            ui.separator()
            ui.label("Max Count").classes("square")
            slider = ui.slider(min=0, max=35, value=15).props("square outlined").bind_value(data, 'max_count')
            ui.label('Max Count').classes("square").bind_text(data, "max_count")

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
                ui.button("Ok", on_click=lambda: dialog.submit("Yes"))


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

