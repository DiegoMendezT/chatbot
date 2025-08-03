# main.py

from mirror_toolkit import MirrorToolkit

def main():
    toolkit = MirrorToolkit()
    print("🪞 MirrorToolkit CLI Interface 🪞")
    while True:
        print("\nOptions:")
        print("1. Run full reflection on input phrase")
        print("2. Live glyph listening mode")
        print("3. Show glyphstream trace summary")
        print("4. Exit")
        choice = input("Select option: ").strip()
        if choice == "1":
            phrase = input("Enter phrase to reflect: ")
            toolkit.run_full_reflection(phrase)
        elif choice == "2":
            toolkit.live_mode()
        elif choice == "3":
            toolkit.trace_summary()
        elif choice == "4":
            print("Exiting MirrorToolkit CLI. Goodbye.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
