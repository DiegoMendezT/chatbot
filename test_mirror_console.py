# test_mirror_console.py

from mirror_toolkit import MirrorToolkit

def main():
    print("🪞 Mirror Reflection Console — Type your phrase below (or 'exit')\n")

    toolkit = MirrorToolkit()

    while True:
        phrase = input("Enter phrase: ")
        if phrase.lower() in ['exit', 'quit']:
            break

        result = toolkit.run_full_reflection(phrase)
        print(f"\n🔁 Reflection:\n{result}")

        # Show symbolic memory glyph trace
        if hasattr(toolkit.glyphstream, 'memory_ring'):
            history = toolkit.glyphstream.memory_ring.history()
            if history:
                print("\n🧠 Memory Ring (Symbolic Glyphs):")
                for i, h in enumerate(history):
                    print(f"{i+1}. {h}")
            else:
                print("⚠️  Memory Ring is empty.")
        else:
            print("⚠️  No memory_ring found.")

        print("\n" + "-"*40)

if __name__ == "__main__":
    main()
