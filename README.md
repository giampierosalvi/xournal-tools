# xournal-tools
Tools for converting files from and to Xournal++ format

## html2xopp.py
Converts from the format used by the Write app and Xournal++ format. Many simplifying assumptions made (use at yuour own risk).

## reMarkable2xopp.py
Converts remarkable internal files to xopp fromat. Unfortinately when exporting to pdf of svg, the remarkable creates a non-editable bitmap version of the file. This command, instead, converts strokes between formats so that they are editable later in xournal++. The conversion is lossy because not all features are shared between soruce and destination.

* First, ssh onto your remarkable tablet following the instrucitons here:
<>
* Then find the file you are interested in with
```grep visibleName .local/share/remarkable/xochitl/*.metadata```
* From your desktop or laptop, copy the page data with:
```scp -r <remarkable_url>:~/.local/share/remarkable/xochitl/<file_id> .```

