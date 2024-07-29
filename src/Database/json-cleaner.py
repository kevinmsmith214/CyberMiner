def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Finding the positions of the first '[' and last ']'
    first_bracket_index = content.find('[')
    last_bracket_index = content.rfind(']')

    # Isolate and retain only the first '[' and last ']'
    part_before_first_bracket = content[:first_bracket_index + 1]
    part_between_brackets = content[first_bracket_index + 1:last_bracket_index]
    part_after_last_bracket = content[last_bracket_index:]

    # Remove all other '[' and ']' in the middle part
    part_between_brackets = part_between_brackets.replace('[', '').replace(']', '')

    # Combine the parts back together
    content = part_before_first_bracket + part_between_brackets + part_after_last_bracket

    # Initialize variables to build the final content
    final_content = ""
    parts = content.split('}')
    num_parts = len(parts)

    # Process all parts except the very last chunk after the last '}'
    for i in range(num_parts - 1):
        # Strip spaces to check if we should add a comma
        part_clean = parts[i].rstrip()
        # Append corrected part with '}', adding a comma only if it's not the last part
        final_content += part_clean + '},' if i < num_parts - 2 else part_clean + '}'

    # Add the last part (there's no '}' at the end of this part)
    final_content += parts[-1]

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(final_content)

# Example usage
file_path = 'scraped_dataXX'
process_file(file_path)
