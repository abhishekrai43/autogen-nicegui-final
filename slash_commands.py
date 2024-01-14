slash_commands = {
    "<strong>/help</strong>": "Provide a summary of available commands and their functions.",
    "<strong>/python</strong>": "List 10 helpful Python commands or snippets.",
    "<strong>/debug</strong>": "Offer debugging tips or help identify issues in a provided code snippet.",
    "<strong>/algorithm</strong>": "Explain a specific algorithm or compare different algorithms for a given problem.",
    "<strong>/latest_tech</strong>": "Share the latest updates or news in technology and IT.",
    "<strong>/optimize</strong>": "Suggestions for optimizing a given piece of code or system.",
    "<strong>/AI_trends</strong>": "Discuss current trends and advancements in AI and machine learning.",
    "<strong>/web_dev</strong>": "Provide tips, tricks, or insights related to web development.",
    "<strong>/security</strong>": "Share best practices and tips for IT security and cybersecurity.",
    "<strong>/data_analysis</strong>": "Offer guidance or methods for effective data analysis."
}

def create_help_command(slash_commands):
    help_string = "Available Commands:\n"
    for command, description in slash_commands.items():
        help_string += f"<p>{command}: {description}</p>"
    return help_string

def process_command(command, additional_text):
    if command.lower() == '/help':
        return create_help_command(slash_commands)
    elif command.lower() == '/debug' and additional_text:
        return f"Please help me debug this code:\n\n{additional_text}"
    elif command.lower() == '/optimize' and additional_text:
        return f"Please provide optimization suggestions for this code:\n\n{additional_text}"
    elif command.lower() == '/algorithm' and additional_text:
        return f"Can you explain or compare the following algorithm(s): {additional_text}"
    elif command in slash_commands:
        return slash_commands[command]
    elif command.startswith('/'):
        return "Command not recognized. Please try again or use /help for a list of commands."
    return None