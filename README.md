# premiere-batch-stabilize-python

This script uses the [Pymiere](https://github.com/qmasingarbe/pymiere) library to automate video stabilization in Premiere Pro.

The script loops through all `.mov` files in the `input folder` and does the following:

1. Import clip and add to sequence
2. Stabilize video
3. Export video to the `output folder`
4. Move source file to the `completed folder`

Tested on Premiere Pro 22.6.2, M1 Macbook Air, macOS Ventura



