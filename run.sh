#!/bin/bash



# Change to the script's directory
cd "$(dirname "$0")"


<<comment
cd /Users/andrewke/Desktop/premiere-batch-stabilize-python
comment

#important: bash define variable cannot have space before or after =
default_input_folder="/Users/andrewke/Desktop/MLV_export"

prompt_input_folder=1

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

    if [ $prompt_input_folder -eq 1 ]; then
        read input_folder
    fi

    # if [ $input_folder -eq ""]; then
    #     input_folder=$default_input_folder
    # fi
    

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

    if [ $prompt_input_folder -eq 1 ]; then
        read input_folder
    fi

    # if [ $input_folder -eq ""]; then
    #     input_folder=$default_input_folder
    # fi

fi





while true; do
    # Your script logic goes here


    if [[ -n "$input_folder" ]]; then
        echo "input_folder is a non-empty string. using input_folder as argument in stabilise.py"

        # Run the Python script and capture its output
        output=$(python stabilize.py "$input_folder" 2>&1)
    else
        echo "input_folder is either empty or not a string. using default input folder in stabilise.py"

        # Run the Python script and capture its output
        output=$(python stabilize.py 2>&1)
    fi

    

    # # Print the captured output
    echo "$output"




    echo " "
    echo "Press Enter to restart. Type 'f' to switch to a different input folder. Type 'exit' to quit."
    
    read -r input

    if [[ "$input" == "f" ]]; then
        echo "Enter input folder (no need for quotes, use <backslash space> for space. can drag and drop folder into terminal): "

        read input_folder
        
    fi

    if [[ "$input" == "exit" ]]; then
        echo "Exiting the script."
        break
    fi
done



# Todo : There might be a bug when switching from Internal disk to external hard disk. Folder of videos fails to change