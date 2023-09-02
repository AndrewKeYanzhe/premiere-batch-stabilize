#!/bin/bash



# Change to the script's directory
cd "$(dirname "$0")"

# activate virtual environment
source /Users/andrewke/Documents/Pymiere/pymiere/bin/activate


# Check if Adobe Premiere Pro is already running
if ! pgrep "Adobe Premiere Pro" >/dev/null; then
    echo "Launching Adobe Premiere Pro..."
    open -a "/Applications/Adobe Premiere Pro 2022/Adobe Premiere Pro 2022.app"
    
    start_time=$(date +%s)
    
    #premiere takes 6.2 seconds to load
    echo "Waiting for 10 seconds. Enter input folder (no need for quotes, use <backslash space> for space. can drag and drop folder into terminal): "
    # sleep 10

    read input_folder

    current_time=$(date +%s)

    elapsed_time=$((current_time - start_time))

    # while [$elapsed_time -le 10]; do
    #     current_time=$(date +%s)

    #     elapsed_time=$((current_time - start_time))
    #     sleep 1
    # done

    while true; do
        current_time=$(date +%s)
        elapsed_time=$((current_time - start_time))
        
        if [ "$elapsed_time" -ge 10 ]; then
        echo "Finished loading Premiere"
            break
        fi

        sleep 1
    done

    


    
else
    echo "Adobe Premiere Pro is already running."

    echo "Enter input folder (no need for quotes, use <backslash space> for space. can drag and drop folder into terminal): "

    read input_folder
fi





while true; do
    # Your script logic goes here

    # Run the Python script and capture its output
    output=$(python stabilize.py "$input_folder" 2>&1)

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