import datetime
import importlib
import re
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop, Dispatcher
from telegram.utils.helpers import escape_markdown

from tg_bot import dispatcher, updater, TOKEN, WEBHOOK, OWNER_ID, DONATION_LINK, CERT_PATH, PORT, URL, LOGGER, \
    ALLOW_EXCL
#modulları dinamik yükləmək üçün lazımdır
# QEYD: Modul sırasına zəmanət verilmir, bunu konfiqurasiya faylında qeyd edin!
from tg_bot.modules import ALL_MODULES
from tg_bot.modules.helper_funcs.chat_status import is_user_admin
from tg_bot.modules.helper_funcs.misc import paginate_modules

PM_START_TEXT = """
Salam mənim adım {}! Məndən necə istifadə edəcəyinizlə bağlı hər hansı sualınız varsa, /help - oxuyun və sonra @MarieSupport səhifəsinə keçin.

Mən python-telegram-bot kitabxanasından istifadə edərək python3-də qurulmuş qrup meneceri botuyam və tam açıq mənbəyəm; \
məni işarələyən şeyləri tapa bilərsiniz [burada](https://github.com/DegGixM/RoseRobot)!

Hər hansı bir səhv, sualınız ilə github-da sorğu göndərməkdən və ya dəstək qrupum @DegGixM ilə əlaqə saxlamaqdan çekinmeyin \
və ya xüsusiyyət sorğularınız ola bilər :)
Yeni funksiyalar, dayanmalar və s. haqqında elanlar üçün @MarieNews adlı xəbər kanalım da var.

Mövcud əmrlərin siyahısını /help ilə tapa bilərsiniz.

Əgər məndən istifadə etməkdən həzz alırsansa və/yaxud mənə vəhşi təbiətdə sağ qalmağıma kömək etmək istəyirsənsə, VPS-i maliyyələşdirməyə/təkmilləşdirməyə kömək etmək üçün / bağış et!
"""
HELP_STRINGS = """
Salam! Mənim adım *{}*.
Mən bir neçə əyləncəli əlavələri olan modul qrup idarəetmə botuyam! Bəziləri haqqında fikir əldə etmək üçün aşağıdakılara nəzər salın.
sizə kömək edə biləcəyim şeylər.

*Əsas* əmrlər mövcuddur:
  - /start: botu işə salın
  - / help: PM sizə bu mesajdır.
  - /help <modul adı>: PM sizə həmin modul haqqında məlumatdır.
  - /donate: ianə vermək haqqında məlumat!
  - /parametrlər:
    - PM-də: bütün dəstəklənən modullar üçün parametrlərinizi sizə göndərəcək.
    - qrupda: bütün söhbət parametrləri ilə sizi pm-ə yönləndirəcək.

{}
Və aşağıdakılar:
""".format(dispatcher.bot.first_name, "" if not ALLOW_EXCL else "\nBütün əmrlər ya ilə istifadə edilə bilər / or !.\n")

DONATE_STRING = """Hey, ianə vermək istədiyinizi eşitdiyimə şadam!
Məni indi olduğum yerə çatdırmaq üçün yaradıcım çox zəhmət çəkdi və hər bir ianə kömək edir \
məni daha da yaxşılaşdırmaq üçün onu motivasiya et. Bütün ianə pulları məni qəbul etmək üçün daha yaxşı VPS-ə və/yaxud pivəyə gedəcək.
(onun tərcümeyi-halına baxın!). O, sadəcə kasıb tələbədir, ona görə də hər kiçik kömək edir!
Ona ödəməyin iki yolu var; [DegGixM GitHub](https://github.com/DegGixM/RoseRobot) və ya [DegGixM](https://t.me/DegGixM)."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

GDPR = []

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("tg_bot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Eyni ada malik iki modul ola bilməz! Zəhmət olmasa birini dəyişdirin")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # chat_migrated hadisələrdə köçmək üçün söhbətlər
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(chat_id=chat_id,
                                text=text,
                                parse_mode=ParseMode.MARKDOWN,
                                reply_markup=keyboard)


@run_async
def test(bot: Bot, update: Update):
    # pprint(qiymətləndirmə(str(yeniləmə)))
     # update.effective_message.reply_text("Yaxşı tester! _Məndə* `markdown` var", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("Bu şəxs mesajı redaktə etdi")
    print(update.effective_message)

@run_async
def start(bot: Bot, update: Update, args: List[str]):
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_text(
                PM_START_TEXT.format(escape_markdown(first_name), escape_markdown(bot.first_name), OWNER_ID),
                parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text("Hə, necəsən?")


# test məqsədləri üçün
def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # update.message.chat_id-i söhbət siyahısından silin
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # qüsurlu sorğuları idarə edin - aşağıda daha ətraflı oxuyun!
    except TimedOut:
        print("no nono3")
        # yavaş əlaqə problemlərini həll edin
    except NetworkError:
        print("no nono4")
        # digər əlaqə problemlərini həll edin
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # qrupun chat_id-i dəyişdi, əvəzinə e.new_chat_id istifadə edin
    except TelegramError:
        print(error)
        # bütün digər teleqramla əlaqəli səhvləri idarə edin

@run_async
def help_button(bot: Bot, update: Update):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            text = "Budur *{}* modulu üçün yardım:\n".format(HELPABLE[module].__mod_name__) \
                   + HELPABLE[module].__help__
            query.message.reply_text(text=text,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton(text="Back", callback_data="help_back")]]))

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.reply_text(HELP_STRINGS,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(curr_page - 1, HELPABLE, "help")))

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.reply_text(HELP_STRINGS,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(next_page + 1, HELPABLE, "help")))

        elif back_match:
            query.message.reply_text(text=HELP_STRINGS,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help")))

        # fırlanan ağ dairənin olmamasına əmin olun
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message == "Mesaj dəyişdirilməyib":
            pass
        elif excp.message == "Sorğunun id-si etibarsızdır":
            pass
        elif excp.message == "Mesaj silinə bilməz":
            pass
        else:
            LOGGER.exception("Kömək düymələrində istisna":. %s", str(query.data))


@run_async
def get_help(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:

        update.effective_message.reply_text("Mümkün əmrlərin siyahısını əldə etmək üçün mənimlə PM-də əlaqə saxlayın.",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="Help",
                                                                       url="t.me/{}?start=help".format(
                                                                           bot.username))]]))
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = "üçün mövcud yardım budur *{}* module:\n".format(HELPABLE[module].__mod_name__) \
               + HELPABLE[module].__help__
        send_help(chat.id, text, InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="help_back")]]))

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id)) for mod in USER_SETTINGS.values())
            dispatcher.bot.send_message(user_id, "Bunlar cari parametrlərinizdir:" + "\n\n" + settings,
                                        parse_mode=ParseMode.MARKDOWN)

        else:
            dispatcher.bot.send_message(user_id, "Görünür, hər hansı bir istifadəçi üçün xüsusi parametrlər mövcud deyil :'(",
                                        parse_mode=ParseMode.MARKDOWN)

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(user_id,
                                        text="Hansı modulu yoxlamaq istərdiniz {}'s settings for?".format(
                                            chat_name),
                                        reply_markup=InlineKeyboardMarkup(
                                            paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)))
        else:
            dispatcher.bot.send_message(user_id, "Deyəsən, heç bir söhbət parametri mövcud deyil :'(\nBunu göndər"
                                                  "qrup söhbətində onun cari parametrlərini tapmaq üçün adminsiniz!",
                                        parse_mode=ParseMode.MARKDOWN)


@run_async
def settings_button(bot: Bot, update: Update):
    query = update.callback_query
    user = update.effective_user
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* üçün aşağıdakı parametrlərə malikdir *{}* module:\n\n".format(escape_markdown(chat.title),
                                                                                     CHAT_SETTINGS[
                                                                                         module].__mod_name__) + \
                   CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(text=text,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton(text="Back",
                                                                callback_data="stngs_back({})".format(chat_id))]]))

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text("salam! üçün kifayət qədər bir neçə parametr var {} - gedin və nəyi seçin "
                                     "maraqlanırsınız.".format(chat.title),
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(curr_page - 1, CHAT_SETTINGS, "stngs",
                                                          chat=chat_id)))

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
                   query.message.reply_text("salam! üçün kifayət qədər bir neçə parametr var {} - gedin və nəyi seçin "
                                     "maraqlanırsınız.".format(chat.title),
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(next_page + 1, CHAT_SETTINGS, "stngs",
                                                          chat=chat_id)))

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(text="salam! üçün kifayət qədər bir neçə parametr var {} - gedin və nəyi seçin "
                                          "maraqlanırsınız.".format(escape_markdown(chat.title)),
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(paginate_modules(0, CHAT_SETTINGS, "stngs",
                                                                                        chat=chat_id)))

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message == "Mesaj dəyişdirilməyib":
            pass
        elif excp.message == "Sorğu id-si etibarsızdır":
            pass
        elif excp.message == "Mesaj silinə bilməz":
            pass
        else:
            LOGGER.exception("Parametrlər düymələrində istisna. %s", str(query.data))


@run_async
def get_settings(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]
    args = msg.text.split(None, 1)

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Bu söhbətin, eləcə də sizin ayarlarınızı əldə etmək üçün bura klikləyin."
            msg.reply_text(text,
                           reply_markup=InlineKeyboardMarkup(
                               [[InlineKeyboardButton(text="Settings",
                                                      url="t.me/{}?start=stngs_{}".format(
                                                          bot.username, chat.id))]]))
        else:
            text = "Parametrlərinizi yoxlamaq üçün bura klikləyin."

    else:
        send_settings(chat.id, user.id, True)


@run_async
def donate(bot: Bot, update: Update):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]

    if chat.type == "private":
        update.effective_message.reply_text(DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

        if OWNER_ID != 254318997 and DONATION_LINK:
            update.effective_message.reply_text("Hazırda məni idarə edən şəxsə də ianə verə bilərsiniz "
                                                "[here]({})".format(DONATION_LINK),
                                                parse_mode=ParseMode.MARKDOWN)

    else:
        try:
            bot.send_message(user.id, DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

            update.effective_message.reply_text("Yaradanıma ianə verməklə bağlı sizə PM göndərdim!")
        except Unauthorized:
            update.effective_message.reply_text("İanə haqqında məlumat almaq üçün əvvəlcə mənimlə əlaqə saxlayın.")


def migrate_chats(bot: Bot, update: Update):
    msg = update.effective_message  # Növ: Könüllü[Mesaj]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("dən köçür %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Uğurla köçdü!")
    raise DispatcherHandlerStop


def main():
    test_handler = CommandHandler("test", test)
    start_handler = CommandHandler("start", start, pass_args=True)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    # dispatcher.add işləyicisi (test işləyicisi)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)
                             
# dispatcher.add səhv idarəedicisi (xəta geri çağırış)

     # daşqın əleyhinə prosessor əlavə edin
                             
    Dispatcher.process_update = process_update

    if WEBHOOK:
        LOGGER.info("Veb kancalardan istifadə.")
        updater.start_webhook(listen="127.0.0.1",
                              port=PORT,
                              url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN,
                                    certificate=open(CERT_PATH, 'rb'))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Uzun sorğudan istifadə.")
        updater.start_polling(timeout=15, read_latency=4)

    updater.idle()


CHATS_CNT = {}
CHATS_TIME = {}


def process_update(self, update):
    # Səsvermə zamanı xəta baş verdi
    if isinstance(update, TelegramError):
        try:
            self.dispatch_error(None, update)
        except Exception:
            self.logger.exception('Səhv işlənərkən tutulmamış xəta yarandı')
        return

    now = datetime.datetime.utcnow()
    cnt = CHATS_CNT.get(update.effective_chat.id, 0)

    t = CHATS_TIME.get(update.effective_chat.id, datetime.datetime(1970, 1, 1))
    if t and now > t + datetime.timedelta(0, 1):
        CHATS_TIME[update.effective_chat.id] = now
        cnt = 0
    else:
        cnt += 1

    if cnt > 10:
        return

    CHATS_CNT[update.effective_chat.id] = cnt
    for group in self.groups:
        try:
            for handler in (x for x in self.handlers[group] if x.check_update(update)):
                handler.handle_update(update, self)
                break

        # Hər hansı digər işləyici ilə işləməyi dayandırın.
        except DispatcherHandlerStop:
            self.logger.debug('Dispetçer İşləyicisinin Dayanmasına görə əlavə işləyicilərin dayandırılması')
            break

       # Hər hansı bir səhv göndərin.
        except TelegramError as te:
            self.logger.warning('Yeniləmə işlənərkən Telegram xətası yarandı')

            try:
                self.dispatch_error(update, te)
            except DispatcherHandlerStop:
                self.logger.debug('Xəta idarəedicisi əlavə işləyiciləri dayandırdı')
                break
            except Exception:
                self.logger.exception('Səhv işlənərkən tutulmamış xəta qaldırıldı')

        # Səhvlər mövzunu dayandırmamalıdır.
        except Exception:
            self.logger.exception('Yeniləmə işlənərkən tutulmamış xəta yarandı')


if __name__ == '__main__':
    LOGGER.info("Modullar uğurla yükləndi: " + str(ALL_MODULES))
    main()
