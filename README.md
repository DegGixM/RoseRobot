### DegGixM 
DegGixM Desdeki'ile RoseRobot GitHub.com -da Klonlanib Sunulur!
DegGixM Resmi Kanal'i Etrafli Melumat Ucun Resmi Kanali Bax.[DegGixM](https://t.me/DegGixM)
DegGixM Owner. [MUCVE](https;//t.me/MUCVE_M) 

<img src="https://te.legra.ph/file/50771de1bcd2e67af5ae4.jpg" width="550" height="450">
</p>


# tgbot
Sqlalchemy verilənlər bazası ilə python3-də işləyən modul teleqram Python botu.

Əvvəlcə çoxlu admin xüsusiyyətlərinə malik sadə qrup idarəetmə botu, o, modullar üçün əsasa çevrildi.
sadə sürükləmə və buraxma vasitəsilə sadə plagin genişlənməsini təmin etməyi hədəfləyən botlar.

Teleqramda [DegGixM](https://t.me/DegGixM) kimi tapıla bilər.

Öz botunuzu yaratmaqla bağlı suallarınız üçün [MUCVE](https://t.me/MUCVE_M) müraciət edin.
kömək etmək üçün könüllülər qrupu. Biz, həmçinin verilənlər bazası sxemi dəyişdikdə və bəzi cədvəl sütunları dəyişdirildikdə kömək edəcəyik
dəyişdirilmiş/əlavə edilmişdir (bu məlumat həmçinin öhdəçilik mesajlarında tapıla bilər)


Yeni funksiyalar və ya xəbərlər haqqında xəbərdar olmaq istəyirsinizsə, [DegGixM](https://t.me/DegGixM) qoşulun.
elanlar.

DegGixM və mən həm də kömək göstərmək məqsədi daşıyan [DegGixM](https://t.me/DegGixm) moderatorluq edə bilərik.
söhbətlərinizdə Marie qurmaq (*bot klonları üçün deyil).
Baqları bildirmək üçün qoşulmaqdan çekinmeyin və bot inkişafının statusundan xəbərdar olun.

Tədqiqatçılara qeyd edin ki, bütün sxem dəyişiklikləri öhdəçilik mesajlarında tapılacaq və onların hər hansı yeni öhdəlikləri oxumaq məsuliyyəti var.


## VACİB QEYD:

Bu layihə artıq aktiv baxım altında deyil. Bəzən səhv düzəlişləri buraxıla bilər, lakin heç bir yeni funksiyanın əlavə edilməsi planlaşdırılmır.
[DegGiXM](https://t.me/DegGixM) istifadəçiləri [DegGixM](https://t.me/DegGixM) saytına köçməyə təşviq olunurlar.
miqyaslılığı nəzərə alaraq qolanq dilində yazılmış bu layihənin təkmilləşdirilmiş versiyasıdır.

## Botun işə salınması.

Verilənlər bazanızı qurduqdan və konfiqurasiyanız tamamlandıqdan sonra (aşağıya baxın) sadəcə olaraq işə salın:

`python3 -m tg_bot`


## Botun qurulması (İstifadə etməzdən əvvəl bunu oxuyun!):
Zəhmət olmasa python3.6-dan istifadə etdiyinizə əmin olun, çünki köhnə python versiyalarında hər şeyin gözlənildiyi kimi işləyəcəyinə zəmanət verə bilmərəm!
Bunun səbəbi, markdown təhlilinin 3.6-da defolt olaraq sıralanan dict vasitəsilə təkrarlanması ilə həyata keçirilməsidir.

### Konfiqurasiya

Botunuzu konfiqurasiya etməyin iki mümkün yolu var: config.py faylı və ya ENV dəyişənləri.

Üstünlük verilən versiya `config.py` faylından istifadə etməkdir, çünki bu, bütün parametrlərinizi birlikdə qruplaşdıraraq görməyi asanlaşdırır.
Bu fayl `__main__.py` faylı ilə yanaşı, `tg_bot` qovluğunda yerləşdirilməlidir.
Bu, bot nişanınızın, həmçinin verilənlər bazası URI-nizin (verilənlər bazasından istifadə edirsinizsə) və ən çox yüklənəcəyi yerdir.
digər parametrləriniz.

sample_config-i idxal etmək və Konfiqurasiya sinfini genişləndirmək tövsiyə olunur, çünki bu, konfiqurasiyanızda bütün məlumatları ehtiva edəcəyinə əmin olacaq.
defolt parametrlər sample_config-də təyin olunur, beləliklə təkmilləşdirməyi asanlaşdırır.

Məsələn `config.py` faylı ola bilər:
```
tg_bot.sample_config idxal Konfiqurasiyasından


sinif İnkişafı (Konfiqurasiya):
    SAHİBİ_ID = 254318997 # teleqram ID-si
    OWNER_USERNAME = "SonOfLars" # mənim teleqram istifadəçi adım
    API_KEY = "sizin bot api açarınız" # mənim api açarım, botfather tərəfindən təmin edilir
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/database' # nümunə db etimadnaməsi
    MESSAGE_DUMP = '-1234567890' # botunuzun üzvü olduğu bəzi qrup çatı
    USE_MESSAGE_DUMP = Doğrudur
    SUDO_USERS = [18673980, 83489514] # Bota sudo girişi olan istifadəçilər üçün id-lərin siyahısı.
    YÜKLƏ = []
    NO_LOAD = ['tərcümə']
```

Əgər sizdə config.py faylı (heroku-da EG) yoxdursa, mühit dəyişənlərindən də istifadə etmək mümkündür.
Aşağıdakı env dəyişənləri dəstəklənir:
 - `ENV`: Bunu HƏR ŞEY olaraq təyin etmək env dəyişənlərini aktivləşdirəcək

 - `TOKEN`: Sətir kimi bot nişanınız.
 - `OWNER_ID`: Sahib ID-nizdən ibarət tam ədəd
 - `OWNER_USERNAME`: İstifadəçi adınız

 - `DATABASE_URL`: Verilənlər bazanız URL
 - `MESSAGE_DUMP`: isteğe bağlı: insanların köhnə mesajlarını silməsini dayandırmaq üçün cavablandırdığınız yadda saxladığınız mesajların saxlandığı söhbət
 - `YÜKLƏ`: Yükləmək istədiyiniz modulların boşluqla ayrılmış siyahısı
 - `NO_LOAD`: YÜKLƏMƏK İSTƏMƏYİNİZ modulların boşluqla ayrılmış siyahısı
 - `WEBHOOK`: Bunu HƏR ŞEY olaraq təyin etmək, env rejimində olarkən veb-qancaları işə salacaq.
 mesajlar
 - `URL`: Veb-qancanızın qoşulmalı olduğu URL (yalnız webhook rejimi üçün lazımdır)

 - `SUDO_USERS`: Sudo istifadəçiləri hesab edilməli olan user_id-lərinin boşluqla ayrılmış siyahısı
 - `SUPPORT_USERS`: Dəstək istifadəçiləri hesab edilməli olan istifadəçi id-lərinin boşluqla ayrılmış siyahısı (gban/ungban,
 başqa heçnə)
 - `WHITELIST_USERS`: Ağ siyahıya salınmış hesab edilməli olan istifadəçi id-lərinin boşluqla ayrılmış siyahısı - onları qadağan etmək olmaz.
 - `DONATION_LINK`: Könüllü: ianə almaq istədiyiniz link.
 - `CERT_PATH`: Webhook sertifikatınıza gedən yol
 - `PORT`: Veb-qancalarınız üçün istifadə ediləcək port
 - `DEL_CMDS`: Bu əmrdən istifadə etmək hüququ olmayan istifadəçilərdən əmrlərin silinib-silinməyəcəyi
 - `STRICT_GBAN`: Köhnə qruplar kimi yeni qruplarda da gbans tətbiq edin. Qadağan edilmiş istifadəçi danışanda ona qadağa qoyulacaq.
 - `İŞLƏR`: İstifadə ediləcək mövzuların sayı. 8 tövsiyə olunan (və defolt) məbləğdir, lakin təcrübəniz fərqli ola bilər.
 __Qeyd edək ki, daha çox mövzu ilə çılğınlıq botunuzu sürətləndirməyəcək.

## 🚀 Heroku Deployment

<h4>RoseRobot-ni Heroku-da yerləşdirmək üçün aşağıdakı düyməni basın!</h4>    
<a href="https://heroku.com/deploy/"><img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=https://github.com/DegGixM/RoseRobot=heroku" width="200""/></a>
