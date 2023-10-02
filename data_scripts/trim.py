import argparse

# Function to read input file and remove empty line breaks
# and take the first of each pair of strings
def clean_file(input_file, output_file):
    # Open the input file for reading
    with open(input_file, "r") as infile:
        # Initialize a variable to keep track of line pairs
        line_pair = 0
        # Initialize a list to store cleaned lines
        cleaned_lines = []

        # Read the file line by line
        for line in infile:
            # Remove trailing and leading whitespace
            line = line.strip()
            # Only process non-empty lines
            if line:
                # Increment the line_pair counter
                line_pair += 1
                # If it's the first line in the pair, add it to the list
                if line_pair % 2 != 0:
                    cleaned_lines.append(line)

    # Write the cleaned lines to the output file
    with open(output_file, "w") as outfile:
        for line in cleaned_lines:
            outfile.write(f"{line}\n")


if __name__ == "__main__":
    # Initialize argparse
    parser = argparse.ArgumentParser(
        description="Clean up text file by removing empty lines and taking only the first of each pair of lines."
    )
    # Add command-line arguments for input and output files
    parser.add_argument(
        "--input_file", type=str, required=True, help="Path to the input file."
    )
    parser.add_argument(
        "--output_file", type=str, required=True, help="Path to the output file."
    )
    args = parser.parse_args()

    # Call the clean_file function to process the input file
    clean_file(args.input_file, args.output_file)
