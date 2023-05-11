# scribber-dwloader
This is a python script that connects to your email, searches for an [amazon kindle scribe] <https://www.amazon.com/Introducing-Kindle-Scribe-the-first-Kindle-for-reading-and-writing/dp/B09BS26B8B?th=1> notebook shared between the most recent mails and downloads it.

## Files
*main.py* : the one and only script file written on python.

## How 2 use it?
Very simple, really.
1. Make sure you have installed the included packages. *(requests, email, ...)*
2. Modify the **download route** in the `download_pdf` function.
3. Modify the **username** and **password** variable values with your actual email credentials.
4. Modify the `imap_server` variable value according to your email provider server.
5. [OPTIONAL] Modify the number of most recent emails to search between.
6. Run the script with the `python` interpreter.
