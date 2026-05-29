from query import display_bleed_weapons, display_madness_build
 
def main():
    choices = ["1","2","3","4","5"]

    print("\n=== ELDEN LORD BUILD OPTIMIZER ===")
    print("Your guide to optimizing builds in the Lands Between.\n")

    print("Select a damage type:")
    print("  1. Bleed")
    print("  2. Madness")
    print("  3. Frost     (Coming Soon)")
    print("  4. Poison    (Coming Soon)")
    print("  5. Lightning (Coming Soon)")

    while True:
        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            display_bleed_weapons()
            break

        if choice == "2":
            display_madness_build()
            break

        if choice not in choices:
            print("\nInvalid choice. Please try again and enter a number between 1 and 4.\n")
            continue

        print("\nThis build type is not yet implemented. Check back in a future update, Tarnished.")
 
if __name__ == "__main__":
    main()