#Töhfə

Töhfələr çox xoşdur! Burada layihənin necə tərtib olunduğuna dair bəzi təlimatlar verilmişdir.

### CodeStyle

- PEP8-ə mümkün qədər riayət edin.

- Sətir uzunluqları 120 simvoldan az olmalıdır, xəritə/filtr üzərində siyahı anlayışlarından istifadə edin, arxada boşluq buraxmayın.

- Gələcək istinad üçün daha mürəkkəb kod parçaları şərh edilməlidir.

### Struktur

Layihəni mümkün qədər səliqəli saxlamaq üçün layihə strukturunda bir neçə öz-özünə qoyulan qaydalar var.
- Bütün modullar `modules/` kataloquna daxil olmalıdır.
- İstənilən verilənlər bazasına giriş `modullar/sql/` proqramında aparılmalıdır - SESSION-un heç bir nümunəsi başqa yerə idxal edilməməlidir.
- Verilənlər bazası seanslarınızın düzgün əhatə olunduğundan əmin olun! Həmişə onları düzgün şəkildə bağlayın.
- Yeni modul yaratarkən, onu daxil etmək üçün digər fayllara mümkün qədər az dəyişiklik edilməlidir.
Modul faylının silinməsi hələ də mükəmməl işlək vəziyyətdə olan bir botla nəticələnməlidir.
- Əgər modul bir neçə başqa fayldan asılıdırsa, onlar yüklənməyə bilər, onda modulun siyahısını yaradın.
atributlara baxaraq, `__main__` daxilində yükləmə vaxtı. Miqrasiya, /help, /stats, /info və bir çox başqa şeylər belədir
əsasında qurulur. O, botun LOAD və NO_LOAD konfiqurasiyaları ilə yaxşı işləməsinə imkan verir.
- Nəzərə alın ki, bəzi şeylər toqquşa bilər; məsələn, bir regex işləyicisi komanda işləyicisi ilə toqquşa bilər - bu halda, siz
onları müxtəlif dispetçer qruplarına yerləşdirməlidir.

Mürəkkəb görünə bilər, amma içəri girəndə mənalı olacaq. Məndən əl/məsləhət istəməkdən çekinmeyin!
