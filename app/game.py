import random

MAGIC_NUMBER_MIN = 2
MAGIC_NUMBER_MAX = 10


def get_magic_number() -> int:
    return random.randint(2, 10)


def play_mash(categories: list, magic_number: int) -> dict:
    """
    Uses the magic number to iteratively remove options from the categories.
    - Flatten into a single list
    - Remove options based on the magic number
    - Reconsolidate the options after each removal
    - Modulo used to wrap around the list

    Need to remove elements and re-flatten to temp list as we go. Simply adding the chosen element each time won't
    because it'll mess up the modulo arithmetic.
    """

    # Check for valid magic number
    if not isinstance(magic_number, int) or magic_number < MAGIC_NUMBER_MIN or magic_number > MAGIC_NUMBER_MAX:
        raise ValueError(
            f"Magic number must be an integer between {MAGIC_NUMBER_MIN} and {MAGIC_NUMBER_MAX} (inclusive)."
        )

    # Add MASH as the primary category
    mash_category = {"name": "MASH", "options": ["Mansion", "Apartment", "Shack", "House"]}
    all_categories = [mash_category] + categories

    # Copy the options for elimination
    survivor_options = [list(category["options"]) for category in all_categories]

    # Flatten all options into a single list to iterate through for elimination
    flat_options = []
    for i, category_options in enumerate(survivor_options):
        for option in category_options:
            # Maintain category index with the option
            flat_options.append((i, option))

    # We're just intrested in the remainder after modulo to give us the index
    index_to_remove = (magic_number - 1) % len(flat_options)

    survivor_count = sum(len(cat) for cat in survivor_options)

    # Keep removing options until there's only one option left in each category
    while survivor_count > len(all_categories):
        item_to_remove = flat_options.pop(index_to_remove)
        category_idx, option_value = item_to_remove

        # Remove it from our main list of live_options
        if option_value in survivor_options[category_idx]:
            survivor_options[category_idx].remove(option_value)

        # Rebuild flat_options without removed item and any categories with only the one option left
        temp_flat_options = []
        for i, category_options in enumerate(survivor_options):
            if len(category_options) > 1:  # If only 1 option left, skip it
                for option in category_options:
                    temp_flat_options.append((i, option))

        flat_options = temp_flat_options

        if not flat_options:
            # We are done
            break

        # Removal index keeps increasing but wraps around due to modulo
        index_to_remove = (index_to_remove + magic_number - 1) % len(flat_options)

        # Update the live options length
        survivor_count = sum(len(cat) for cat in survivor_options)

    result = {}
    for i, category in enumerate(all_categories):
        if survivor_options[i]:
            result[category["name"]] = survivor_options[i][0]

    return result


if __name__ == "__main__":
    # Run as standalone script for debugging
    categories = [
        {"name": "Car", "options": ["Sedan", "SUV", "Truck"]},
        {"name": "Job", "options": ["Doctor", "Engineer", "Artist"]},
        {"name": "Pet", "options": ["Dog", "Cat", "Fish"]},
    ]

    # magic_number = get_magic_number()
    magic_number = 1  # Test magic number
    print(f"Magic number: {magic_number}")
    result = play_mash(categories, magic_number)
    print("Mash result:", result)
