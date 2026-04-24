from query import display_bleed_weapons
 
def main():
    choices = ["1","2","3","4"]
    print("\n=== ELDEN LORD BUILD OPTIMIZER ===")
    print("Your guide to optimizing builds in the Lands Between.\n")

    print("Select a damage type:")
    print("  1. Bleed")
    print("  2. Frost     (Coming Soon)")
    print("  3. Poison    (Coming Soon)")
    print("  4. Lightning (Coming Soon)")

    while True:
        choice = input("\nEnter choice (1-4): ").strip()
        if choice == "1":
            display_bleed_weapons()
            break
        elif choice not in choices:
            print("\nInvalid choice. Please try again and enter a number between 1 and 4.\n")
    
        print("\nThis build type is not yet implemented. Check back in a future update, Tarnished.")
 
if __name__ == "__main__":
    main()