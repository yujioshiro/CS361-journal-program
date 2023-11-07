import json
import os
import sys
from datetime import datetime
import subprocess

# Default configuration settings
DEFAULT_CONFIG = {
    "journal_directory": "journal_entries",
    "filename_format": "%Y-%m-%d_%H-%M-%S",
    "filename_extension": ".json",
    "first_time": True  
}

def load_config():
    global CONFIG
    if not os.path.isfile('config.json'):
        # If config.json does not exist, create it with default settings
        with open('config.json', 'w') as config_file:
            json.dump(DEFAULT_CONFIG, config_file, indent=4)
        CONFIG = DEFAULT_CONFIG
        # Since we just created the config file, it's the user's first time
        first_time_setup()
    else:
        with open('config.json', 'r') as config_file:
            CONFIG = json.load(config_file)
            if CONFIG.get('first_time', False):  # Check if it's the first run
                first_time_setup()

def first_time_setup():
    # This function will be called on the first run
    # You can place any first-time initialization or welcome messages here
    print("Welcome to the Journal App! It looks like this is your first time.")
    print("When you open this app, you can begin writing immediately.")
    print("When you are finished writing, press CTRL+D to save the journal entry.")
    print("There are several commands you can use, such as EDIT, DELETE, or SETTINGS.")
    print("Type EDIT and press ENTER to edit a previously written journal entry.")
    print("Type DELETE and press ENTER to delete a previously written journal entry.")
    print("Type SETTINGS and press ENTER to configure some settings. This will open up a vim instance in terminal, so make sure you know how to use vim!")
    input("Press ENTER to clear these instructions and begin writing. Don't worry, you can type HELP and press ENTER to bring up these commands again.")
    clear_screen()
    # After first time setup, set the flag to False and save the config
    CONFIG['first_time'] = False
    with open('config.json', 'w') as config_file:
        json.dump(CONFIG, config_file, indent=4)

def get_entry_filename(entry_id):
    filename = f"{entry_id}{CONFIG['filename_extension']}"
    return os.path.join(CONFIG['journal_directory'], filename)

def save_entry(entry_id, entry_content):
    if not os.path.exists(CONFIG['journal_directory']):
        os.makedirs(CONFIG['journal_directory'])
    with open(get_entry_filename(entry_id), 'w') as file:
        json.dump({"id": entry_id, "content": entry_content}, file, indent=4)

def write_entry(entry_content):
    if entry_content.strip().lower() == 'help':
        display_help()
        return
    
    entry_id = datetime.now().strftime(CONFIG['filename_format'])
    save_entry(entry_id, entry_content)
    print(f"\nEntry saved with ID: {entry_id}")

def edit_entry():
    entry_id = input("Enter the entry ID to edit: ")
    file_path = get_entry_filename(entry_id)
    if os.path.exists(file_path):
        with open(file_path, 'r+') as file:
            entry = json.load(file)
            print("\nCurrent entry content:")
            print(entry['content'])
            print("\nEdit your entry (press CTRL+D when finished):\n")
            new_content, _ = get_multiline_input("")
            if new_content:
                entry['content'] = new_content
                file.seek(0)
                json.dump(entry, file, indent=4)
                file.truncate()
                print("Entry updated.")
            else:
                print("No changes made.")
    else:
        print("Entry not found.")


def delete_entry():
    entry_id = input("Enter the entry ID to delete: ")
    file_path = get_entry_filename(entry_id)
    try:
        os.remove(file_path)
        print("Entry deleted.")
    except FileNotFoundError:
        print("Entry not found.")

def display_help():
    print("Welcome to the help menu. Here are the available commands:")
    print("Type your journal entry. When finished writing, press CTRL+D to save it.")
    print("Type 'EDIT' and ENTER to edit a previously written journal entry.")
    print("Type 'DELETE' and ENTER delete an existing entry.")
    print("Type 'SETTINGS' and ENTER to modify the configuration file in vim.")

def open_settings():
    # Open the config.json file with vim
    subprocess.run(['vim', 'config.json'])
    # Reload the configuration after editing
    load_config()

def clear_screen():
    # Clear the command line screen.
    os.system('cls' if os.name == 'nt' else 'clear')

def get_multiline_input(prompt_message):
    print(prompt_message)
    lines = []
    while True:
        try:
            line = input()
            if not lines:  # Check the command if it's the first line
                command = line.strip().lower()
                if command == 'edit':
                    edit_entry()
                    return None, True
                elif command == 'delete':
                    delete_entry()
                    return None, True
                elif command == 'settings':
                    open_settings()
                    return None, True
                elif command == 'help':
                    display_help()
                    return None, True
            lines.append(line)
        except EOFError:
            break  # CTRL+D or CTRL+Z was pressed
    return '\n'.join(lines), False

def main():
    clear_screen()
    load_config()  # Load the configuration at the start
    print("Welcome to your journal. Start writing your entry (CTRL+D to save) or type 'HELP' (and press ENTER to see available commands).")

    entry_content, command_issued = get_multiline_input("Begin writing your entry:")

    # If no command was issued and there is entry content, save the entry
    if entry_content and not command_issued:
        write_entry(entry_content)
        print("Entry saved. Exiting journal.")

if __name__ == '__main__':
    main()
