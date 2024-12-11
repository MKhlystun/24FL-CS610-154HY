def parse_simulation_statistics(file_path):
    # Dictionary to hold the parsed statistics
    statistics = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Start processing lines after the header
    for line in lines:
        line = line.strip()

        # Skip the header or any blank lines
        if line.startswith('----------') or not line:
            continue
        
        # Split the line into the metric name, value, and comment
        parts = line.split(maxsplit=2)

        if len(parts) == 3:
            key, value, comment = parts
            # Attempt to convert the value to a float, int, or leave as string
            try:
                if value.lower() == "nan":
                    parsed_value = float('nan')
                elif "." in value:
                    parsed_value = float(value)
                else:
                    parsed_value = int(value)
            except ValueError:
                parsed_value = value
            
            # Store in the dictionary
            statistics[key] = {
                "value": parsed_value,
                "comment": comment.strip()
            }

    return statistics


# Example usage
file_path = "simulation_statistics.txt"  # Replace with the actual file path
stats = parse_simulation_statistics(file_path)

# Print the parsed statistics
for key, info in stats.items():
    print(f"{key}: Value = {info['value']}, Comment = {info['comment']}")

