"""Модуль 4 — Відмінки (przypadki). Ядро польської граматики: 7 відмінків по одному.

Педагогіка: для кожного відмінка — на яке ПИТАННЯ відповідає, КОЛИ вживається (дієслова-
й прийменники-тригери), базові закінчення та приклади. Без важких таблиць — правила,
що одразу працюють.
"""

from __future__ import annotations

from app.grammar.schema import Card, Lesson, Module, Quiz

MODULE = Module(
    id="przypadki",
    icon="🔑",
    title="Відмінки (7 відмінків)",
    subtitle="Серце польської: як і навіщо слова змінюють закінчення. По одному, просто.",
    lessons=[
        # ── Урок 0: вступ ──
        Lesson(
            id="pr_wstep",
            title="Що таке відмінки і навіщо",
            cards=[
                Card(
                    "Слово міняє «хвіст»",
                    "Відмінок — це форма іменника залежно від його ролі в реченні. Ти вже це знаєш "
                    "з української: <i>кіт → кота → котові</i>. У польській так само — 7 відмінків.",
                ),
                Card(
                    "7 відмінків і їхні питання",
                    "1. <b>Mianownik</b> — хто? що?\n2. <b>Dopełniacz</b> — кого? чого?\n"
                    "3. <b>Celownik</b> — кому? чому?\n4. <b>Biernik</b> — кого? що?\n"
                    "5. <b>Narzędnik</b> — ким? чим?\n6. <b>Miejscownik</b> — (о) кому? (о) чому?\n"
                    "7. <b>Wołacz</b> — звертання (гей, друже!)",
                ),
                Card(
                    "Гарна новина",
                    "Порядок і логіка майже такі, як в українській. Найчастіші — <b>Biernik</b> "
                    "(що бачу/маю) і <b>Dopełniacz</b> (нема чого). З них і почнемо після базового.",
                    tip="Не вчи всі таблиці одразу. Бери по відмінку, роби приклади — і воно вкладеться.",
                ),
            ],
        ),
        # ── Mianownik ──
        Lesson(
            id="pr_mianownik",
            title="1. Mianownik — базова форма",
            cards=[
                Card(
                    "Хто? Що?",
                    "<b>Mianownik</b> — це та форма, що в словнику. Відповідає на <b>kto? co?</b> "
                    "і позначає <b>підмет</b> (того, хто діє).",
                    [("Kot śpi.", "Кіт спить."), ("Anna czyta.", "Анна читає.")],
                ),
                Card(
                    "Після «to jest»",
                    "Називаючи щось через <b>to jest…</b>, теж уживаємо Mianownik.",
                    [("To jest dom.", "Це дім."), ("To są koty.", "Це коти.")],
                    tip="Це «нульова» форма-опора. Решта 6 відмінків — це зміни саме від неї.",
                ),
            ],
            quiz=[
                Quiz("На яке питання відповідає Mianownik?", ["kogo? czego?", "kto? co?", "kim? czym?"], 1,
                     "Mianownik — хто? що? (базова форма)."),
            ],
        ),
        # ── Biernik ──
        Lesson(
            id="pr_biernik",
            title="2. Biernik — прямий додаток (маю, бачу, люблю)",
            cards=[
                Card(
                    "Кого? Що?",
                    "<b>Biernik</b> — це той, на кого <b>спрямована дія</b>. Питання <b>kogo? co?</b> "
                    "Це найчастіший відмінок після дій.",
                ),
                Card(
                    "Дієслова-тригери",
                    "Після <b>mieć</b> (мати), <b>lubić</b> (любити), <b>widzieć</b> (бачити), "
                    "<b>znać</b>, <b>jeść</b>, <b>pić</b>, <b>kupować</b> — іде Biernik.",
                    [("Mam kota.", "Маю кота."), ("Lubię kawę.", "Люблю каву."),
                     ("Widzę Annę.", "Бачу Анну.")],
                ),
                Card(
                    "Закінчення — просте",
                    "• жіночий -a → <b>-ę</b> (kawa→kawę, Anna→Annę)\n"
                    "• чоловічий <b>живий</b> → як Dopełniacz (-a): kot→kota, pies→psa\n"
                    "• чоловічий <b>неживий</b> та середній → <b>без змін</b> (mam dom, mam okno)",
                    [("Piję kawę.", "Пʼю каву."), ("Mam psa.", "Маю пса."), ("Mam długopis.", "Маю ручку.")],
                    tip="Найпростіше правило: жіночий -a завжди стає -ę. Це працює скрізь.",
                ),
            ],
            quiz=[
                Quiz("«Люблю каву»: kawa змінюється на…", ["kawy", "kawę", "kawą"], 1,
                     "Жіночий -a → -ę: Lubię kawę."),
                Quiz("«Маю кота»: kot →", ["kot", "kota", "kotem"], 1,
                     "Чоловічий живий у Biernik = як Dopełniacz: kota."),
            ],
        ),
        # ── Dopełniacz ──
        Lesson(
            id="pr_dopelniacz",
            title="3. Dopełniacz — нема чого, чиє, багато",
            cards=[
                Card(
                    "Кого? Чого?",
                    "<b>Dopełniacz</b> (kogo? czego?) — один із найважливіших. Три головні вживання: "
                    "<b>заперечення</b>, <b>приналежність</b>, <b>кількість</b>.",
                ),
                Card(
                    "1) Заперечення: nie ma + Dopełniacz",
                    "Коли чогось <b>немає</b> або ти <b>не маєш</b> — іменник іде в Dopełniacz.",
                    [("Nie ma czasu.", "Немає часу."), ("Nie mam kota.", "Не маю кота."),
                     ("Nie ma Anny.", "Немає Анни.")],
                    tip="Порівняй: Mam kota (Biernik) → Nie mam kota (Dopełniacz). Заперечення «тягне» Dopełniacz.",
                ),
                Card(
                    "2) Чиє? (приналежність)",
                    "«Книжка кого?» — власник іде в Dopełniacz (як «книжка Анни»).",
                    [("książka Anny", "книжка Анни"), ("dom brata", "дім брата")],
                ),
                Card(
                    "3) Кількість: dużo, mało + Dopełniacz",
                    "Після слів кількості: <b>dużo</b>, <b>mało</b>, <b>trochę</b>, <b>ile</b>.",
                    [("dużo pracy", "багато роботи"), ("mało czasu", "мало часу"),
                     ("szklanka wody", "склянка води")],
                ),
                Card(
                    "Прийменники + Dopełniacz",
                    "Багато прийменників вимагають Dopełniacz: <b>do</b> (до), <b>od</b> (від), "
                    "<b>z</b> (з, звідки), <b>bez</b> (без), <b>dla</b> (для), <b>u</b> (у когось).",
                    [("do domu", "додому"), ("bez cukru", "без цукру"), ("dla mamy", "для мами")],
                ),
            ],
            quiz=[
                Quiz("«Не маю часу»: czas →", ["czas", "czasu", "czasem"], 1,
                     "Заперечення → Dopełniacz: nie mam czasu."),
                Quiz("Який відмінок після «dużo»?", ["Biernik", "Dopełniacz", "Narzędnik"], 1,
                     "dużo pracy — Dopełniacz."),
            ],
        ),
        # ── Narzędnik ──
        Lesson(
            id="pr_narzednik",
            title="4. Narzędnik — ким/чим, з ким, чим роблю",
            cards=[
                Card(
                    "Ким? Чим?",
                    "<b>Narzędnik</b> (kim? czym?) — три головні вживання: <b>ким я є</b>, "
                    "<b>з ким/чим</b>, <b>чим роблю</b> (інструмент).",
                ),
                Card(
                    "1) Бути кимось: być + Narzędnik",
                    "Професія/роль після <b>być</b> — у Narzędnik.",
                    [("Jestem studentem.", "Я студент."), ("Ona jest lekarką.", "Вона лікарка.")],
                    tip="Тому не «jestem student», а «jestem studentem». Дуже часта помилка початківців!",
                ),
                Card(
                    "2) З кимось: z + Narzędnik",
                    "Прийменник <b>z</b> у значенні «разом із» вимагає Narzędnik.",
                    [("z bratem", "з братом"), ("kawa z mlekiem", "кава з молоком")],
                ),
                Card(
                    "Закінчення",
                    "• чоловічий/середній → <b>-em</b> (student→studentem, okno→oknem)\n"
                    "• жіночий → <b>-ą</b> (kawa→kawą, Anna→Anną)\n"
                    "• множина → <b>-ami</b> (z przyjaciółmi — з друзями)",
                    [("Piszę długopisem.", "Пишу ручкою."), ("Jadę autobusem.", "Їду автобусом.")],
                ),
            ],
            quiz=[
                Quiz("«Я студент»: правильно —", ["Jestem student.", "Jestem studentem.", "Jestem studenta."], 1,
                     "być + Narzędnik: jestem studentem."),
                Quiz("«з братом» — brat →", ["brata", "bratem", "bratu"], 1, "z + Narzędnik -em: bratem."),
            ],
        ),
        # ── Miejscownik ──
        Lesson(
            id="pr_miejscownik",
            title="5. Miejscownik — де? (тільки з прийменником)",
            cards=[
                Card(
                    "(О) кому? (о) чому? Де?",
                    "<b>Miejscownik</b> — єдиний відмінок, що <b>ніколи не буває без прийменника</b>. "
                    "Найчастіше — про <b>місце</b> (де?).",
                ),
                Card(
                    "Прийменники-тригери",
                    "<b>w</b> (у), <b>na</b> (на), <b>o</b> (про), <b>przy</b> (біля), <b>po</b> (після).",
                    [("w domu", "вдома"), ("na stole", "на столі"), ("myślę o tobie", "думаю про тебе")],
                ),
                Card(
                    "Закінчення (буває «мʼяким»)",
                    "Часто <b>-e</b> зі змʼякшенням приголосного, або <b>-u</b>:\n"
                    "• stół → na sto<b>le</b>, szkoła → w szko<b>le</b>\n"
                    "• dom → w do<b>mu</b>, pokój → w poko<b>ju</b>",
                    [("w Warszawie", "у Варшаві (Warszawa→Warszawie)"), ("w Polsce", "у Польщі")],
                    tip="Miejscownik має найбільше варіантів. Не зубри таблицю — запамʼятовуй у фразах: «w domu», «na stole».",
                ),
            ],
            quiz=[
                Quiz("«вдома» польською —", ["w dom", "w domu", "w domem"], 1,
                     "Miejscownik: w domu."),
                Quiz("Miejscownik уживається…", ["завжди з прийменником", "без прийменника", "лише в множині"], 0,
                     "Тільки з прийменником (w, na, o, przy…)."),
            ],
        ),
        # ── Celownik ──
        Lesson(
            id="pr_celownik",
            title="6. Celownik — кому? (даю, допомагаю)",
            cards=[
                Card(
                    "Кому? Чому?",
                    "<b>Celownik</b> (komu? czemu?) — той, <b>кому</b> щось даємо/робимо "
                    "(непрямий додаток).",
                ),
                Card(
                    "Дієслова-тригери",
                    "<b>dawać</b> (давати), <b>pomagać</b> (допомагати), <b>dziękować</b> (дякувати), "
                    "<b>mówić</b> (казати комусь).",
                    [("Daję mamie kwiaty.", "Даю мамі квіти."), ("Pomagam bratu.", "Допомагаю братові."),
                     ("Dziękuję ci.", "Дякую тобі.")],
                ),
                Card(
                    "Закінчення",
                    "• чоловічий → <b>-owi</b> (brat→bratowi, pan→panu — виняток)\n"
                    "• жіночий → <b>-e/-i</b> (mama→mamie, Anna→Annie)\n"
                    "• середній → <b>-u</b> (dziecko→dziecku)",
                ),
            ],
            quiz=[
                Quiz("«Допомагаю братові»: brat →", ["brata", "bratem", "bratu/bratowi"], 2,
                     "Celownik чол.: bratu/bratowi."),
            ],
        ),
        # ── Wołacz ──
        Lesson(
            id="pr_wolacz",
            title="7. Wołacz — звертання",
            cards=[
                Card(
                    "Коли когось кличеш",
                    "<b>Wołacz</b> — форма для <b>звертання</b> (гей, Аню! пане!). В усному мовленні "
                    "часто заміняють на Mianownik, але у формальному й з іменами він живий.",
                ),
                Card(
                    "Закінчення",
                    "• жіночі імена → <b>-o</b> або <b>-u</b> (Anna→Anno, Ania→Aniu)\n"
                    "• чоловічі → <b>-e/-u</b> (Piotr→Piotrze, pan→panie)",
                    [("Aniu, chodź!", "Аню, ходи!"), ("Szanowny Panie!", "Шановний пане!"),
                     ("Mamo!", "Мамо!")],
                    tip="У листах/офіційно Wołacz обовʼязковий: «Drogi Piotrze», «Szanowni Państwo».",
                ),
            ],
            quiz=[
                Quiz("Звертання до Ani —", ["Ania!", "Aniu!", "Anią!"], 1, "Wołacz: Aniu!"),
            ],
        ),
        # ── Підсумок ──
        Lesson(
            id="pr_podsumowanie",
            title="Підсумок: як не заплутатись",
            cards=[
                Card(
                    "Швидка шпаргалка за питаннями",
                    "M: kto? co? · D: kogo? czego? · C: komu? czemu? · B: kogo? co? · "
                    "N: kim? czym? · Msc: o kim? o czym? · W: звертання",
                ),
                Card(
                    "Головні тригери-підказки",
                    "• <b>mieć/lubić/widzieć</b> → Biernik\n• <b>nie ma / dużo / do, od, bez, dla</b> → Dopełniacz\n"
                    "• <b>być kim / z kim</b> → Narzędnik\n• <b>w, na, o</b> (місце) → Miejscownik\n"
                    "• <b>dawać, pomagać, dziękować</b> → Celownik",
                ),
                Card(
                    "Стратегія навчання",
                    "Не вчи 7 таблиць. Запамʼятовуй <b>тригери</b> й <b>готові фрази</b> "
                    "(«w domu», «nie mam czasu», «jestem studentem»). Мозок сам виведе правило. "
                    "Ти вже знаєш каркас усієї польської граматики 💪",
                ),
            ],
            quiz=[
                Quiz("Після «nie ma» який відмінок?", ["Biernik", "Dopełniacz", "Celownik"], 1,
                     "Заперечення → Dopełniacz: nie ma czasu."),
                Quiz("«być + професія» — який відмінок?", ["Mianownik", "Narzędnik", "Biernik"], 1,
                     "być studentem — Narzędnik."),
            ],
        ),
    ],
)
