if not __name__.endswith("sample_config"):
    import sys
    print("README oxumaq üçün oradadır. Bu nümunə konfiqurasiyanı konfiqurasiya faylına genişləndirin, sadəcə adını dəyişməyin və dəyişdirin "
           "burada dəyərlər var. Bunu etmək sizə əks nəticə verəcəkdir.\nBot tərk edir.", file=sys.stderr)
    quit(1)


# Eyni dir və idxalda yeni config.py faylı yaradın, sonra bu sinfi genişləndirin.
class Config(object):
    LOGGER = True

    # TƏLƏB OLUNUR
    API_KEY = "YOUR KEY HERE"
    OWNER_ID = "YOUR ID HERE"  # Əgər bilmirsinizsə, botu işə salın və onunla şəxsi söhbətinizdə /id edin
    OWNER_USERNAME = "YOUR USERNAME HERE"

    # RECOMMENDED
    SQLALCHEMY_DATABASE_URI = 'sqldbtype://username:pw@hostname:port/db_name'  # istənilən verilənlər bazası modulları üçün lazımdır
    MESSAGE_DUMP = None  # "saxla" mesajlarının davam etdiyinə əmin olmaq lazımdır
    LOAD = []
    #Bəzi uzun müddət işləyən sed əmrlərinin cpu istifadəsini maksimuma çatdırdığı aşkar edildikdən sonra sed aradan qaldırıldı
     # və botu öldürdü. Onu yenidən aktivləşdirərkən diqqətli olun!
    NO_LOAD = ['translation', 'rss', 'sed']
    WEBHOOK = False
    URL = None

    # OPTIONAL
    SUDO_USERS = []  # Bota sudo girişi olan istifadəçilər üçün id-lərin (istifadəçi adlarının deyil) siyahısı.
     SUPPORT_USERS = [] # Gban-a icazə verilən, lakin qadağan edilə bilən istifadəçilər üçün id-lərin (istifadəçi adlarının deyil) siyahısı.
     WHITELIST_USERS = [] # Bot tərəfindən qadağan edilməyən/qovulmayan istifadəçilər üçün id-lərin (istifadəçi adlarının deyil) siyahısı.
     DONATION_LINK = None # EG, paypal
     CERT_PATH = None
    PORT = 5000
    DEL_CMDS = False  # "Mavi mətn klikləməlidir" əmrlərini silməyiniz lazım olub-olmaması
    STRICT_GBAN = False
    WORKERS = 8  # İstifadə ediləcək alt başlıqların sayı. Bu tövsiyə olunan məbləğdir - özünüz üçün ən yaxşı olanı görün!
    BAN_STICKER = 'CAADAgADOwADPPEcAXkko5EB3YGYAg'  # banhammer marie stikeri
    ALLOW_EXCL = False  #İcazə verin! əmrləri, eləcə də /


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
