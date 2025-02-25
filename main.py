from ui.main_window import create_main_window
from ui.loading_window import show_loading_screen, check_holiday_files

if __name__ == "__main__":
    check_holiday_files()
    show_loading_screen()
    create_main_window()
