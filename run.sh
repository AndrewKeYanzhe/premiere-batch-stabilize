#!/bin/bash



# Change to the script's directory
cd "$(dirname "$0")"

# activate virtual environment
source /Users/andrewke/Documents/Pymiere/pymiere/bin/activate


# Check if Adobe Premiere Pro is already running
if ! pgrep "Adobe Premiere Pro" >/dev/null; then
    echo "Launching Adobe Premiere Pro..."
    open -a "/Applications/Adobe Premiere Pro 2022/Adobe Premiere Pro 2022.app"
    
    
    #premiere takes 6.2 seconds to load
    echo "Waiting for 10 seconds..."
    sleep 10
    echo "Done waiting!"
else
    echo "Adobe Premiere Pro is already running."
fi





while true; do
    # Your script logic goes here

    # Run the Python script and capture its output
    output=$(python stabilize.py 2>&1)

    # # Print the captured output
    echo "$output"

    echo " "
    echo "This is your script. Press Enter to restart or type 'exit' to quit."
    
    read -r input

    if [[ "$input" == "exit" ]]; then
        echo "Exiting the script."
        break
    fi
done