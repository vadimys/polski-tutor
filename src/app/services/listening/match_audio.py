"""Аудіо-зіставлення (MATCH_AUDIO) — multi-select; ключ звірено з офіц. klucz."""

from __future__ import annotations

from app.services.listening.schema import MatchAudio

MATCH_AUDIO: list[MatchAudio] = [
    MatchAudio(
        id="am2020_4",
        title="Іспит 2020 — Zad IV (życie w wielkich miastach)",
        intro=(
            "Прослухай <b>4 мовців</b> про життя у великих містах і зістав кожен опис "
            "A–E з тим, кого він стосується. <b>Один опис може стосуватися кількох осіб</b> "
            "(тисни всі номери, тоді «Готово»). На іспиті лунає двічі."
        ),
        speakers=[
            "Dla mnie miasto to koszmar – wszędzie korki, dużo ludzi, szaro. Tylu ludzi "
            "dookoła, a nie ma czasu, żeby się z kimś zaprzyjaźnić. Jest więcej możliwości – "
            "praca, siłownie, kina, teatry, ale to nie znaczy, że życie jest lepsze.",
            "Dzieciństwo spędziłam w małym mieście, ale nie chcę tam wrócić. Denerwuje mnie, "
            "gdy ludzie za bardzo interesują się sprawami innych, a to niestety jest typowe "
            "dla takich miejsc. Wszyscy komentują życie sąsiadów. Zdecydowanie wolę duże "
            "miasta, chociaż ceny są tam wyższe niż w mniejszych miejscowościach.",
            "Przeprowadzka do bloku była moim błędem. Staram się żyć w zgodzie z sąsiadami, "
            "ale inni niekoniecznie – sąsiadka nocami ogląda seriale i cały blok też je słyszy, "
            "studenci z góry słuchają muzyki techno na cały regulator.",
            "Plusem życia w miastach jest łatwy dostęp do rozrywki – kina, kluby, kawiarnie "
            "i bliskość różnych luksusowych centrów handlowych. Jednak towary w markowych "
            "sklepach i przyjemności dużo kosztują, a ja jestem osobą oszczędną. Nie "
            "chciałabym mieszkać w dużym mieście – nie lubię hałasu, brudnych ulic i spalin.",
        ],
        prompts=[
            "A. narzeka na hałaśliwych sąsiadów.",
            "B. wymienia miejsca, gdzie można spędzić wolny czas.",
            "C. mówi, że życie w mieście jest drogie.",
            "D. zwraca uwagę na zanieczyszczenie.",
            "E. nie lubi osób za bardzo ciekawych tego, jak żyją inni.",
        ],
        key=[[2], [0, 3], [1, 3], [3], [1]],  # офіц.: A=3, B=1&4, C=2&4, D=4, E=2
        explain=[
            "Особа 3: гучні сусіди — серіали вночі, техно на повну → A.",
            "Особи 1 і 4 перелічують місця дозвілля (праця/кіно/театри · кіно/клуби/кав'ярні) → B.",
            "Особи 2 і 4: ціни вищі · речі й розваги дорого коштують → C.",
            "Особа 4: не любить брудних вулиць і вихлопів (spaliny) → D.",
            "Особа 2: дратують ті, хто надто цікавиться життям інших → E.",
        ],
    ),
    MatchAudio(
        id="am2402_5",
        title="Реальний іспит лютий-2024 — Zad V (wydarzenia kulturalne)",
        intro=(
            "Прослухай <b>5 мовців</b> про участь у культурних подіях і зістав кожен опис "
            "A–D з тим, кого він стосується. <b>Один опис може стосуватися кількох осіб</b>. "
            "На іспиті лунає двічі."
        ),
        speakers=[
            "Raz w tygodniu w konkretny dzień mogę odwiedzić wybrane muzeum lub galerię i nie "
            "płacić za bilet. A raz w roku podczas nocy muzeów niemal wszystkie instytucje "
            "kultury w Polsce otwierają swoje drzwi dla zwiedzających. Wtedy razem z moją "
            "rodziną oglądam ciekawe wystawy.",
            "Lubię oglądać filmy, ale nie w multipleksach. Wolę małe sale kinowe, dlatego "
            "wybieram kameralne festiwale, podczas których prezentowane są filmy z określonego "
            "gatunku lub z określonego kraju. Jeżdżę też na festiwale filmowe za granicę, "
            "między innymi do Cannes i do Berlina, skąd przywożę niezapomniane wrażenia!",
            "Uwielbiam kino. Jestem na bieżąco z każdym nowym tytułem, ponieważ często chodzę "
            "na pokazy premierowe. Jeśli dowiem się, że coś nowego wchodzi na ekrany, to od "
            "razu kupuję bilety dla siebie i przyjaciółki.",
            "Lubię muzykę klasyczną i często jej słucham. Chciałabym chodzić do filharmonii "
            "lub opery, ale ceny biletów są za wysokie. Na szczęście w parku, gdzie spaceruję, "
            "mogę latem bezpłatnie słuchać muzyki Chopina na żywo.",
            "Często uczestniczę w spotkaniach autorskich, które są organizowane przez "
            "biblioteki lub domy kultury w moim mieście. Ponadto szukam imprez dla fanów "
            "literatury. Targi książki w dużych miastach w Polsce przyciągają wielu "
            "miłośników książek, którzy mogą spotkać tam ulubionych autorów.",
        ],
        prompts=[
            "A. korzysta z darmowych ofert.",
            "B. chodzi na spotkania z pisarzami.",
            "C. dzieli swoją pasję z bliskimi.",
            "D. uczestniczy w zagranicznych wydarzeniach kulturalnych.",
        ],
        key=[[0, 3], [4], [0, 2], [1]],  # офіц.: A=1&4, B=5, C=1&3, D=2
        explain=[
            "Особи 1 і 4: безкоштовний музей/ніч музеїв · безкоштовний Шопен у парку → A.",
            "Особа 5: spotkania autorskie, targi książki → B.",
            "Особи 1 і 3: з родиною · для себе й подруги → C (ділиться пристрастю з близькими).",
            "Особа 2: фестивалі за кордоном (Cannes, Berlin) → D.",
        ],
    ),
    MatchAudio(
        id="am2404_5",
        title="Реальний іспит квітень-2024 — Zad V (śniadania)",
        intro=(
            "Прослухай <b>4 мовців</b> про сніданкові звички і зістав кожен опис A–E з тим, "
            "кого він стосується. <b>Один опис може стосуватися кількох осіб</b>. "
            "На іспиті лунає двічі."
        ),
        speakers=[
            "Śniadanie to dla mnie najważniejszy posiłek. Jem je każdego dnia bez wyjątku. "
            "Staram się komponować zdrowe, pełne witamin dania. Na moim stole często pojawiają "
            "się warzywa, musli, a czasem jajecznica z boczkiem. Jeśli mam ochotę, to "
            "przygotowuję śniadania kontynentalne, np. rogaliki z dżemem i owocami.",
            "Całkowicie zrezygnowałem ze śniadań, nie mam na to czasu. Lubię dłużej pospać, "
            "a potem szybko szykuję się do wyjścia. Pierwszy posiłek jem w pracy koło "
            "południa. Idę wtedy na lunch z kolegami albo kupuję coś w pobliskim sklepie.",
            "Nie bardzo lubię gotować, a rano przygotowuję jedzenie w prosty i szybki sposób, "
            "tak, żeby nie zajęło mi to więcej niż 10 minut. Zwykle są to kanapki lub tosty, "
            "bo nie wyobrażam sobie śniadań bez chleba lub bułek.",
            "Jestem na diecie i zrezygnowałam całkowicie z mięsa. Zamówiłam catering, który "
            "przywozi mi gotowe posiłki do pracy i w związku z tym nie przygotowuję śniadań "
            "w domu. To jest bardzo wygodne, bo nie muszę się martwić zakupami i gotowaniem.",
        ],
        prompts=[
            "A. nie je śniadań w domu.",
            "B. bardzo lubi jeść na śniadanie pieczywo.",
            "C. ma różnorodne menu.",
            "D. je wegetariańskie śniadania.",
            "E. zwykle śniadanie robi w kilka minut.",
        ],
        key=[[1, 3], [2], [0], [3], [2]],  # офіц.: A=2&4, B=3, C=1, D=4, E=3
        explain=[
            "Особи 2 і 4: не снідає / відмовився · catering у роботу, вдома не готує → A.",
            "Особа 3: канапки/тости, без хліба не уявляє сніданку → B.",
            "Особа 1: овочі, музлі, яєчня, рогалики — різноманітне меню → C.",
            "Особа 4: на дієті, відмовилася від м'яса → D.",
            "Особа 3: не більше 10 хвилин → E.",
        ],
    ),
    MatchAudio(
        id="am2406_5",
        title="Реальний іспит червень-2024 — Zad V (zakupy)",
        intro=(
            "Прослухай <b>5 мовців</b> про підхід до покупок і зістав кожен опис A–D з тим, "
            "кого він стосується. <b>Один опис може стосуватися кількох осіб</b>. "
            "На іспиті лунає двічі."
        ),
        speakers=[
            "Uwielbiam kupować ubrania z nowych kolekcji. Szukam zawsze czegoś nietypowego, "
            "co będzie inne, niż mają wszyscy. Zakupy robię nie tylko dlatego, że muszę. "
            "To, co kupuję, daje mi możliwość pokazania tego, kim jestem.",
            "Dla mnie liczy się przede wszystkim to, co praktyczne. Najczęściej wybieram "
            "stacjonarne sklepy, gdzie mogę dokładnie obejrzeć produkt, sprawdzić, ile "
            "kosztuje i kupić tańszy.",
            "Elektronika i nowoczesne rozwiązania to moja pasja i nie wyobrażam sobie życia "
            "bez gadżetów. Dla mnie zakupy online to nie tylko wygoda, ale również szansa na "
            "kupienie sprzętów, które niedawno pojawiły się na rynku.",
            "Szukanie dobrych okazji to dla mnie prawdziwa przyjemność! Najpierw porównuję "
            "ceny produktów w różnych sklepach i staram się znaleźć najlepsze oferty. Bardzo "
            "cieszy mnie, że oszczędzam, a jednocześnie kupuję rzeczy wysokiej jakości.",
            "Zdrowy styl życia jest dla mnie najważniejszy. Regularnie korzystam z dostawy "
            "do domu świeżych owoców i warzyw od rolnika. Wybieram produkty ekologiczne, "
            "które są przyjazne dla środowiska. Dla mnie to ważny aspekt każdego zakupu.",
        ],
        prompts=[
            "A. kupuje naturalne produkty.",
            "B. zwraca uwagę na ceny produktów.",
            "C. zwykle wybiera najnowsze modele.",
            "D. poszukuje oryginalnych i wyjątkowych rzeczy.",
        ],
        key=[[4], [1, 3], [0, 2], [0]],  # офіц.: A=5, B=2&4, C=1&3, D=1
        explain=[
            "Особа 5: екопродукти, овочі/фрукти від фермера → A.",
            "Особи 2 і 4: практичність/дешевше · порівнює ціни, шукає нагоди → B.",
            "Особи 1 і 3: нові колекції · щойно випущені ґаджети → C (найновіші моделі).",
            "Особа 1: щось нетипове, інше ніж у всіх → D (оригінальні речі).",
        ],
    ),
    MatchAudio(
        id="am2302_5",
        title="Реальний іспит лютий-2023 — Zad V (poznawanie znajomych)",
        intro=(
            "Прослухай <b>4 поради</b>, як заводити нових знайомих, і зістав кожен опис A–D "
            "з тим, кого він стосується. <b>Один опис може стосуватися кількох осіб</b>. "
            "На іспиті лунає двічі."
        ),
        speakers=[
            "Jeżeli szukasz sposobu, żeby poznać nowych znajomych, powinieneś zdecydować się "
            "na aktywność fizyczną. Nie musisz od razu uprawiać wspinaczki wysokogórskiej czy "
            "innych sportów ekstremalnych. Na początku zapisz się na trening na siłowni. "
            "Poznasz aktywnych ludzi, z którymi po ćwiczeniach usiądziecie w barze i zjecie "
            "coś smacznego.",
            "Możesz zapisać się do klubu dyskusyjnego lub literackiego, żeby brać udział "
            "w interesujących wydarzeniach. Dzięki temu twoje życie nie będzie szare "
            "i monotonne. Znajdziesz się wśród ciekawych ludzi, z którymi podyskutujesz na "
            "różne tematy.",
            "Obecnie ludzie nie mają czasu na dbanie o stare przyjaźnie. Warto zadzwonić do "
            "kolegów ze szkoły i razem wyjść na obiad czy drinka. Świetnym pomysłem będzie "
            "wycieczka z przyjaciółmi w jakieś piękne miejsce. Z całą pewnością będziecie "
            "mogli porozmawiać i powspominać stare dobre czasy.",
            "Jeśli chcesz poznać znajomych, to powinieneś zapisać się na jakiś kurs. Może to "
            "być kurs językowy, programowania albo szycia. Łatwiej jest nawiązać nowe "
            "znajomości z ludźmi, którzy mają podobne zainteresowania. Przy okazji możesz "
            "nauczyć się czegoś praktycznego.",
        ],
        prompts=[
            "A. Uważa, że wyjazdy grupowe zbliżają ludzi.",
            "B. Sugeruje, że wspólne jedzenie pomaga w kontaktach międzyludzkich.",
            "C. Zwraca uwagę, że szukanie znajomych można łączyć z uczeniem się.",
            "D. W spotkaniach towarzyskich widzi szansę na zmianę rutyny.",
        ],
        key=[[2], [0, 2], [3], [1]],  # офіц.: A=3, B=1&3, C=4, D=2
        explain=[
            "Особа 3: wycieczka z przyjaciółmi → A (групові виїзди зближують).",
            "Особи 1 і 3: bar i coś smacznego · obiad czy drinka → B (спільна їжа).",
            "Особа 4: kurs językowy/programowania → C (поєднати з навчанням).",
            "Особа 2: życie nie będzie szare i monotonne → D (зміна рутини).",
        ],
    ),
    MatchAudio(
        id="am2304_5",
        title="Реальний іспит квітень-2023 — Zad V (nauczyciele)",
        intro=(
            "Прослухай <b>4 спогади</b> про вчителів і зістав кожен опис A–D з тим, кого він "
            "стосується. <b>Один опис може стосуватися кількох осіб</b>. На іспиті лунає двічі."
        ),
        speakers=[
            "Do dziś wspominam matematyczki z liceum. Obie panie były łagodne, cierpliwe "
            "i w prosty sposób umiały wytłumaczyć lekcję. Mówiły do uczniów po imieniu. "
            "Nauczycielki miały wpływ na moją karierę zawodową, ponieważ pracowałam jako "
            "księgowa.",
            "Nauczycielka języka polskiego była z Krakowa i podczas lekcji dużo nam o tym "
            "mieście opowiadała, na przykład dlaczego ulice w centrum mają takie, a nie inne "
            "nazwy. Najbardziej podobało mi się to, że polonistka nigdy nas nie krytykowała, "
            "w każdym znalazła coś pozytywnego. Pozwalała nam też decydować, o których "
            "książkach chcemy rozmawiać na lekcjach.",
            "Miałam ogromne szczęście do nauczycieli, ale najbardziej lubiłam panią od "
            "biologii. Uczyła świetnie, dzięki niej poszłam na studia przyrodnicze i zostałam "
            "zoologiem. Pani Magdalena mówiła też, że trzeba studiować całe życie, więc teraz "
            "– już jako emerytka – zapisałam się na zajęcia uniwersytetu dla seniorów.",
            "Ze szkoły zapamiętałem nauczyciela historii, ponieważ lubiłem ten przedmiot. "
            "Nasz historyk znał odpowiedź na każde nasze pytanie, a ponadto był bardzo "
            "kulturalnym człowiekiem – szanował nas i swoją pracę. Do dziś jest moim "
            "autorytetem.",
        ],
        prompts=[
            "A. Wspomina, że nauczyciel szukał lub nauczycielka szukała mocnych stron uczniów.",
            "B. Dzięki nauczycielowi lub nauczycielce wybrał zawód.",
            "C. Chwali nauczyciela lub nauczycielkę za dużą wiedzę i traktuje go/ją jako wzór.",
            "D. Już nie pracuje zawodowo, ale wciąż się uczy.",
        ],
        key=[[1], [0, 2], [3], [2]],  # офіц.: A=2, B=1&3, C=4, D=3
        explain=[
            "Особа 2: w każdym znalazła coś pozytywnego → A (шукала сильні сторони).",
            "Особи 1 і 3: księgowa завдяки вчителькам · zoolog завдяки біологині → B.",
            "Особа 4: znał odpowiedź na każde pytanie, autorytet → C.",
            "Особа 3: emerytka, uniwersytet dla seniorów → D (вже не працює, але вчиться).",
        ],
    ),
    MatchAudio(
        id="am2306_5",
        title="Реальний іспит червень-2023 — Zad V (szukanie pracy)",
        intro=(
            "Прослухай <b>4 поради</b>, як шукати роботу, і зістав кожен опис A–D з тим, кого "
            "він стосується. <b>Один опис може стосуватися кількох осіб</b>. На іспиті лунає двічі."
        ),
        speakers=[
            "Jeśli zastanawiasz się, jak znaleźć nową pracę, zacznij od sprawdzenia sytuacji "
            "na rynku pracy w twoim mieście. Będziesz wiedział, czy masz dużą konkurencję "
            "i jakie są szanse na zatrudnienie. Kluczem do sukcesu jest również poznanie "
            "swoich mocnych i słabych stron, warto wiedzieć, w czym jesteśmy dobrzy, a co nam "
            "nie wychodzi.",
            "Przed spotkaniem z rekruterem przeczytaj ofertę pracy, spróbuj odpowiedzieć na "
            "najczęściej zadawane podczas tego typu rozmowy pytania. Dowiedz się więcej "
            "o firmie, do której aplikujesz. Dzień wcześniej przygotuj sobie ubranie, sprawdź "
            "prognozę pogody i trasę dojazdu, żeby być na miejscu 15 minut przed czasem.",
            "Rozwijaj się! Czytaj książki specjalistyczne, chodź na szkolenia, rób to, co "
            "pomoże ci być specjalistą i zdobyć potrzebne kompetencje zawodowe, napisz o tym "
            "w swoim CV. Przyszły pracodawca to zauważy i doceni. Rozwój osobisty jest "
            "zresztą ważny zawsze, nie tylko wtedy, gdy szukasz pracy.",
            "Dbaj o swój profil w sieci. Załóż i prowadź konto na Facebooku czy Instagramie. "
            "Dodawaj informacje o swoich umiejętnościach, obowiązkach i ukończonych szkołach. "
            "Publikuj wartościowe i edukacyjne treści na konkretne tematy. Niech twoi "
            "obserwatorzy widzą, że jesteś profesjonalistą.",
        ],
        prompts=[
            "A. proponuje, żeby dbać o swoją edukację.",
            "B. radzi, żeby być aktywnym w mediach społecznościowych.",
            "C. poleca dobrze przygotować się do rozmowy kwalifikacyjnej.",
            "D. radzi przeanalizować swoje wady i zalety.",
        ],
        key=[[2, 3], [3], [1], [0]],  # офіц.: A=3&4, B=4, C=2, D=1
        explain=[
            "Особи 3 і 4: szkolenia/rozwój · wartościowe i edukacyjne treści → A (дбати про освіту).",
            "Особа 4: konto na Facebooku/Instagramie → B (соцмережі).",
            "Особа 2: przed spotkaniem z rekruterem, przygotuj się → C (до співбесіди).",
            "Особа 1: poznanie mocnych i słabych stron → D (проаналізувати вади й переваги).",
        ],
    ),
    MatchAudio(
        id="am2311_5",
        title="Реальний іспит листопад-2023 — Zad V (zarządzanie czasem)",
        intro=(
            "Прослухай <b>4 поради</b> про керування часом і зістав кожен опис A–E з тим, кого "
            "він стосується. <b>Один опис може стосуватися кількох осіб</b>. На іспиті лунає двічі."
        ),
        speakers=[
            "Aby lepiej organizować swój czas, zwykle mam przy sobie planer lub notatnik, "
            "tworzę listę wszystkich rzeczy do zrobienia i ustalam, o której godzinie to "
            "robię. Czasem korzystam z różnych aplikacji lub z funkcji notatek w telefonie "
            "i ustawiam alarm, aby o niczym nie zapomnieć.",
            "Robię pauzę między obowiązkami w pracy co dwie godziny. Zwykle planuję ten czas "
            "w ciągu dnia. To pomaga mi być bardziej zorganizowanym i zrelaksowanym. Kiedy "
            "mam więcej czasu, przeznaczam go na krótką drzemkę lub spacer.",
            "Budzę się rano i zaczynam swój dzień około 5:30. Mam wtedy więcej czasu, żeby "
            "pomyśleć o wielu rzeczach i przygotować się do pracy. Kilka dodatkowych godzin "
            "pozwala mi bez stresu wykonać zaplanowane zadania lub zjeść spokojnie śniadanie.",
            "Codziennie przygotowuję listę terminów i rzeczy do zrobienia, dzięki temu jakość "
            "mojej pracy jest bardzo dobra. Najpierw realizuję jedno zadanie z listy, potem "
            "kolejne, ale nigdy nie robię wielu rzeczy naraz. Czasem jestem zaskoczony, jak "
            "dużo rzeczy udało mi się zrobić.",
        ],
        prompts=[
            "A. wolny czas w ciągu dnia poświęca na odpoczynek lub sport.",
            "B. tworzy plan zadań na każdy dzień.",
            "C. zaczyna wcześnie swój dzień.",
            "D. robi regularne przerwy.",
            "E. dzięki technologii lepiej pamięta o swoich zadaniach.",
        ],
        key=[[1], [0, 3], [2], [1], [0]],  # офіц.: A=2, B=1&4, C=3, D=2, E=1
        explain=[
            "Особа 2: drzemka lub spacer → A (відпочинок у вільний час).",
            "Особи 1 і 4: lista rzeczy do zrobienia · codziennie lista terminów → B (план на день).",
            "Особа 3: budzę się około 5:30 → C (рано починає день).",
            "Особа 2: pauza co dwie godziny → D (регулярні перерви).",
            "Особа 1: aplikacje, alarm → E (технологія допомагає пам'ятати).",
        ],
    ),
    MatchAudio(
        id="am2211_5",
        title="Реальний іспит листопад-2022 — Zad V (komunikacja miejska)",
        intro=(
            "Прослухай <b>4 мовців</b> про переваги громадського транспорту і зістав кожен "
            "опис A–D з тим, кого він стосується. <b>Один опис може стосуватися кількох осіб</b>. "
            "На іспиті лунає двічі."
        ),
        speakers=[
            "Kiedy przesiadam się z samochodu na autobus bądź tramwaj, nie tylko wydaję mniej "
            "pieniędzy na paliwo, ale również dbam o środowisko. Mniej spalin to zdecydowanie "
            "czystsze powietrze i ograniczenie smogu w mieście.",
            "Kiedy jadę tramwajem lub metrem, nie tracę cennych minut na stanie w korkach "
            "i szukanie miejsca parkingowego. Dzięki temu jestem wcześniej w biurze, "
            "a przystanek mam bardzo blisko.",
            "Jazda komunikacją miejską jest krótsza niż samochodem, szczególnie o 8.00 rano, "
            "kiedy muszę dostać się na uniwersytet. To również czas na jakąś książkę, rozmowę "
            "ze znajomymi czy po prostu chwilę relaksu w trakcie pracowitego dnia.",
            "Nie muszę mieć prawa jazdy, by dostać się tam, gdzie chcę. Z łatwością można "
            "zmieniać tramwaje, autobusy i metro. A dzięki różnym programom w telefonie "
            "w każdej chwili mogę sprawdzić, o której godzinie będzie mój autobus i gdzie "
            "muszę się przesiąść. W internecie mogę nawet kupić bilet.",
        ],
        prompts=[
            "A. korzysta z aplikacji mobilnych, kiedy porusza się po mieście.",
            "B. może zaoszczędzić czas i szybciej dotrzeć do celu.",
            "C. dzięki zmianie transportu oszczędza pieniądze.",
            "D. przejazd komunikacją miejską wykorzystuje na czytanie lub odpoczynek.",
        ],
        key=[[3], [1, 2], [0], [2]],  # офіц.: A=4, B=2&3, C=1, D=3
        explain=[
            "Особа 4: programy w telefonie, kupić bilet → A (мобільні застосунки).",
            "Особи 2 і 3: wcześniej w biurze · jazda krótsza niż samochodem → B (економія часу).",
            "Особа 1: wydaję mniej na paliwo → C (економія грошей).",
            "Особа 3: czas na książkę, relaks → D (читання/відпочинок).",
        ],
    ),
]
