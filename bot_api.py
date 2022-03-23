# %%

# importar librerias

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from pdf_to_txt import save_pdf_as_text
import glob
import os

# Funcionalidad básica del bot

help_text = '''Para obtener el pdf con el texto buscable, basta enviar el pdf como archivo.'''

unknown_text = '''Lo sentimos, no reconocemos lo ingresado. 
        Entre "/ayuda" para obtener información.'''

# Resolución de la imagen en ppi, mayor resolución da mejores resultados pero 
# consume más memoria.
resolution = 300 

# Token único para comunicarse con el bot
bot_token = "¡¡¡Inserte aquí el token!!!!"
updater = Updater(bot_token, use_context=True)
  
# Mensaje que se despliega la primera vez que se chatea con el bot  
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "¡Hola! Este bot toma un pdf escaneado y te lo regresa con el texto.")
    update.message.reply_text(help_text)

# Contiene el mensaje de ayuda del bot
def help(update: Update, context: CallbackContext):
    update.message.reply_text(help_text)

def download_file(update: Update, context: CallbackContext):

    # Descargar el archivo

    # Obtener el  enlace para descargar el archivo
    document_id = update.message.document.file_id
    file = updater.bot.get_file(document_id)
    file.download()
    file_name = file.file_path.split('/')[-1]
    update.message.reply_text("Archivo descargado con éxito.")

    # Procesar el archivo
    save_pdf_as_text(file_name, resolution, "./")
    update.message.reply_text("Archivo procesado con éxito.")

    # Entregar el resultado
    with open(file_name[:-4] + '_anotado.pdf', 'rb') as result:
        update.message.reply_document(result)

    # Limpiar
    if '.py' not in file_name[:-4]:
        for f in glob.glob(file_name[:-4] + '*'):
            os.remove(f)

# Mensaje desplegado ante un comando desconocido
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(unknown_text%update.message.text)

# Mensaje desplegado ante un texto desconocido
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(unknown_text%update.message.text)

# Agregamos handlers

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('ayuda', help))
updater.dispatcher.add_handler(MessageHandler(
    Filters.document.pdf, download_file))
updater.dispatcher.add_handler(MessageHandler(
    # Filtra comandos desconocidos
    Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(
    # Filtra documentos desconocidos
    (Filters.document&(~Filters.document.pdf)), unknown))
# Filtra mensajes desconocidos.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

# Lanzamos el bot
updater.start_polling()
# %%
