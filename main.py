# main.py
from app.menus import main_menu
from app.database import initialize_db

def run():
    # Initialize the database
    initialize_db()
    
    # Run the main menu
    while True:
        main_menu()

if __name__ == "__main__":
    run()
