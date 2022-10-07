# xournal-tools
Tools for converting files from and to Xournal++ format

## html2xopp.py
Converts from the format used by the Write app and Xournal++ format. Many simplifying assumptions made (use at your own risk).

## xopp2longimg.py

Converts a .xopp file (Xournal++) to a "long image", meaning that all pages will be stacked below each other. 
The Python image manipulation package "Pillow" is required, you can install it with e. g. `pip install pillow`. Any image file format you can think of should be supported. 
Make sure that you have Xournal++ installed and it's in your PATH. You can check that with the command `xournalpp`.
