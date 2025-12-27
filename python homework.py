import json
from datetime import datetime

""" json is for saving/ loading notes
 datetime for automatic"""

NOTES_FILE = "notes.json"


def load_notes():
    """
    Load notes from JSON file.
    If the file does not exist, return an empty list.
    """
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_notes(notes):
    """
    Save notes to JSON file.
    """
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4, ensure_ascii=False)


def print_header(title):
    """
    Display a clear header with specific design.
    """
    print("\n" + "=" * 20)
    print(f"{title:^20}")  # center the title
    print("=" * 20)


def print_note(i, note):
    """
    this function takes an index and a dictionary, and prints the note in a consistent form
    """
    print(f"\n[{i}] {note['title']}")
    print(f"Date: {note.get('date', '')}")
    """ gets the value of date, it it doesnt exist it return empty string"""
    tags = note.get("tags", [])
    if tags:
        print("Tags:", ", ".join(tags))
        """ joins the words in the tags. """
    print("-" * 30)
    print(note["content"])
    print("-" * 30)


def add_note(notes):
    """
    Adds a new note to the list according to the input.
    """
    print_header("Add a New Note")

    title = input("Title: ").strip()
    while title == "":
        print("Please enter a valid title.")
        title = input("Title: ").strip()

    content = input("Content: ").strip()

    tags_input = input("Tags (separated by commas, e.g. work,school,todo): ").strip()
    if tags_input:
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
    else:
        tags = []

    # Bonus: automatic timestamp
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    note = {
        "title": title,
        "content": content,
        "tags": tags,
        "date": date_str
    }

    notes.append(note)
    """ add to the end of the list"""
    save_notes(notes)
    print("Note added successfully!")


def list_notes(notes):
    """
    Print all notes.
    """
    print_header("All Notes")

    if not notes:
        print("No notes yet.")
        return

    for idx, note in enumerate(notes, start=1):
        print_note(idx, note)


def search_notes(notes):
    """
    Look for notes that contain a keyword in the title or content.
    lets the user edit or remove a found note.
    """
    print_header("Find Notes")

    search_text = input("Type a word to search for: ").strip().lower()
    if search_text == "":
        print("Search text cannot be empty.")
        return

    matches = []
    for number, item in enumerate(notes, start=1):
        title_text = item["title"].lower()
        content_text = item["content"].lower()

        if search_text in title_text or search_text in content_text:
            matches.append((number, item))

    if len(matches) == 0:
        print("No matching notes were found.")
        return

    print(f"\n{len(matches)} result(s) found:")
    for number, item in matches:
        print_note(number, item)

    choice = input(
        "\nWould you like to edit or delete a note? (edit, delete, Enter = cancel): "
    ).strip().lower()

    if choice not in ("edit", "delete"):
        return

    try:
        selected = int(input("Enter the note number: "))
    except ValueError:
        print("That is not a valid number.")
        return

    if selected < 1 or selected > len(notes):
        print("This number does not exist.")
        return

    if choice == "edit":
        edit_note(notes, selected - 1)
    else:
        delete_note_by_index(notes, selected - 1)


def edit_note(notes, i=None):
    """ this function takes a note and edits according to input"""
    print_header("Edit a Note")

    if not notes:
        print("No notes to edit.")
        return

    if i is None:
        # Show all notes and let the user choose
        list_notes(notes)
    try:
        num = int(input("Enter the note number to edit: "))
    except ValueError:
        print("This number does not exist.")
        return

    if num < 1 or num > len(notes):
        print("Note number is out of range.")
        return

    i = num - 1

    note = notes[i]
    print(f"\nEditing note [{i + 1}] - {note['title']}")

    new_title = input(f"New title (Enter to keep: '{note['title']}'): ").strip()
    if new_title:
        note["title"] = new_title

    new_content = input("New content (Enter to keep current): ").strip()
    if new_content:
        note["content"] = new_content

    tags_input = input(
        f"New tags (comma separated) (Enter to keep: {', '.join(note.get('tags', []))}): "
    ).strip()
    if tags_input:
        note["tags"] = [t.strip() for t in tags_input.split(",") if t.strip()]

    save_notes(notes)
    print("The note is updated!")


def filter_by_tag(notes):
    """
    this function takes a tag and displays notes that include it (ignores letter case).
    """
    print_header("Search Tag")

    user_tag = input("Type a tag to filter by: ").strip().lower()
    if user_tag == "":
        print("Please enter a tag to continue.")
        return

    matches = []
    for number, entry in enumerate(notes, start=1):
        tags_lowercase = [tag.lower() for tag in entry.get("tags", [])]
        if user_tag in tags_lowercase:
            matches.append((number, entry))

    if len(matches) == 0:
        print("No notes matched the selected tag.")
        return

    print(f"\n{len(matches)} note(s) found for tag '{user_tag}':")
    for number, entry in matches:
        print_note(number, entry)


def delete_note_by_index(notes, i):
    """
   This function takes a note and index and deletes it.
    """
    note = notes[i]
    confirm = input(f"Are you sure you want to delete '{note['title']}'? (y/n): ").strip().lower()
    if confirm == "y":
        notes.pop(i)
        save_notes(notes)
        print("Note deleted.")
    else:
        print("Delete cancelled.")


def delete_note(notes):
    """
    This function takes a list of notes and allows the user to delete one by specifying its number
    """
    print_header("Delete a Note")

    if not notes:
        print("No notes available.")
        return

    list_notes(notes)

    try:
        num = int(input("Enter the note number to delete: "))
    except ValueError:
        print("Invalid number.")
        return

    if num < 1 or num > len(notes):
        print("Note number out of range.")
        return

    delete_note_by_index(notes, num - 1)


def main():
    """
    This function takes no arguments, and it runs the main loop of the application.
    Based on the user’s choice, it calls the appropriate function,
    and when the user chooses to exit, it saves the notes and ends the program.
    """

    notes = load_notes()

    while True:
        print_header("Personal Notebook Manager")
        print("1. Add a new note")
        print("2. List all notes")
        print("3. Search notes")
        print("4. Filter notes by tag")
        print("5. Edit a note")
        print("6. Delete a note")
        print("7. Exit")

        choice = input("Type your choice: ").strip()

        if choice == "1":
            add_note(notes)
        elif choice == "2":
            list_notes(notes)
        elif choice == "3":
            search_notes(notes)
        elif choice == "4":
            filter_by_tag(notes)
        elif choice == "5":
            edit_note(notes)
        elif choice == "6":
            delete_note(notes)
        elif choice == "7":
            save_notes(notes)
            print("Thanks for using the notebook!")
            break
        else:
            print("Choose a valid number.")


if __name__ == "__main__":
    main()
