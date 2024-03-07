import httpx
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

TELEGRAM_TOKEN = ''
NEWS_API_KEY = ''
articles = []

def start(update, context):
    update.message.reply_text(
        "Merhaba! /haber komutunu kullanarak Türkiye'deki haberleri alabilirsiniz."
    )

def get_news(update, context):
    global articles 
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'tr',
        'apiKey': NEWS_API_KEY
    }
    response = httpx.get(url, params=params)
    news_data = response.json()
    if news_data['status'] == 'ok':
        articles = news_data['articles']
        buttons = []
        for article in articles:
            title = article['title']
            url = article['url']
            buttons.append([InlineKeyboardButton(title, url=url)])
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_photo(photo='https://pbs.twimg.com/profile_images/1609254835051700225/DsTAHc3S_400x400.jpg', caption='Haberleri yazarlara göre filtrelemek ister misiniz?')
        authors = [article['author'] for article in articles]
        author_buttons = [authors[i:i+2] for i in range(0, len(authors), 2)]
        buttons = []
        for i in range(len(author_buttons)):
            buttons.append([InlineKeyboardButton(author, callback_data=f'author_{author}') for author in author_buttons[i]])
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text('Yazarları görmek için butona basın:', reply_markup=reply_markup)
    else:
        update.message.reply_text('Haberleri alırken bir hata oluştu.')

def filter_by_author(update, context):
    global articles 
    author = update.callback_query.data.split('_')[1]
    filtered_articles = [article for article in articles if article['author'] == author]
    buttons = []
    for article in filtered_articles:
        title = article['title']
        url = article['url']
        buttons.append([InlineKeyboardButton(title, url=url)])


    reply_markup = InlineKeyboardMarkup(buttons)
    update.callback_query.answer()
    update.callback_query.edit_message_text(f'İşte {author} tarafından yazılan haberler:', reply_markup=reply_markup)
    

    update.callback_query.message.reply_text("Tekrarda Tüm yayınları göstermek için /haber komutunu kullanabilirsiniz.")

def show_authors(update, context):
    if update.callback_query.data == 'show_authors':
        reply_markup = InlineKeyboardMarkup(buttons)
        update.callback_query.answer()
        update.callback_query.edit_message_caption(caption='Lütfen bir yayın seçin:', reply_markup=reply_markup)

def show_all_news(update, context):
    if update.callback_query.data == 'show_all_news':
        get_news(update, context)

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("haber", get_news))
    dp.add_handler(CallbackQueryHandler(filter_by_author))
    dp.add_handler(CallbackQueryHandler(show_authors))
    dp.add_handler(CallbackQueryHandler(show_all_news))  
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
