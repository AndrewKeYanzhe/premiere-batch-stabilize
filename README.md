# premiere-batch-stabilize-python

This script uses the [Pymiere](https://github.com/qmasingarbe/pymiere) library to automate video stabilization in Premiere Pro.

The script loops through all `.mov` and `.mp4` files in the `input folder` and does the following:

1. Move source file to the `Original files` folder
2. Import clip and add to sequence
3. Stabilize video
4. Export video to the root `input folder`

Tested on Premiere Pro 22.6.2, M1 Macbook Air, macOS Ventura



