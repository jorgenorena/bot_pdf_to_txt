# bot_pdf_to_txt

A telegram bot that annotates a pdf file with its text using tesseract.

Uses tesseract (tested on version 4.1.1), python 3, python telegram bot (tested on version 13.11).

Requires: pytesseract, pdf2image, python-telegram-bot, PyPDF2.

To configure, change the bot token in bot_api.py, and the path to the tesseract executable in pdf_to_txt.py.

To use simply run bot_api.py.
