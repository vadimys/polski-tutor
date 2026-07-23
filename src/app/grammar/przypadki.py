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
                    "1. <code>Mianownik</code> — хто? що?\n2. <code>Dopełniacz</code> — кого? чого?\n"
                    "3. <code>Celownik</code> — кому? чому?\n4. <code>Biernik</code> — кого? що?\n"
                    "5. <code>Narzędnik</code> — ким? чим?\n6. <code>Miejscownik</code> — (о) кому? (о) чому?\n"
                    "7. <code>Wołacz</code> — звертання (гей, друже!)",
                ),
                Card(
                    "Гарна новина",
                    "Порядок і логіка майже такі, як в українській. Найчастіші — <code>Biernik</code> "
                    "(що бачу/маю) і <code>Dopełniacz</code> (нема чого). З них і почнемо після базового.",
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
                    "<code>Mianownik</code> — це та форма, що в словнику. Відповідає на <code>kto? co?</code> "
                    "і позначає <b>підмет</b> (того, хто діє).",
                    [("Kot śpi.", "Кіт спить."), ("Anna czyta.", "Анна читає.")],
                ),
                Card(
                    "Після «to jest»",
                    "Називаючи щось через <code>to jest…</code>, теж уживаємо Mianownik.",
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
                    "<code>Biernik</code> — це той, на кого <b>спрямована дія</b>. Питання <code>kogo? co?</code> "
                    "Це найчастіший відмінок після дій.",
                ),
                Card(
                    "Дієслова-тригери",
                    "Після <code>mieć</code> (мати), <code>lubić</code> (любити), <code>widzieć</code> (бачити), "
                    "<code>znać</code>, <code>jeść</code>, <code>pić</code>, <code>kupować</code> — іде Biernik.",
                    [("Mam kota.", "Маю кота."), ("Lubię kawę.", "Люблю каву."),
                     ("Widzę Annę.", "Бачу Анну.")],
                ),
                Card(
                    "Закінчення — просте",
                    "• жіночий -a → <code>-ę</code> (kawa→kawę, Anna→Annę)\n"
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
                    "<code>Dopełniacz</code> (kogo? czego?) — один із найважливіших. Три головні вживання: "
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
                    "Після слів кількості: <code>dużo</code>, <code>mało</code>, <code>trochę</code>, <code>ile</code>.",
                    [("dużo pracy", "багато роботи"), ("mało czasu", "мало часу"),
                     ("szklanka wody", "склянка води")],
                ),
                Card(
                    "Прийменники + Dopełniacz",
                    "Багато прийменників вимагають Dopełniacz: <code>do</code> (до), <code>od</code> (від), "
                    "<code>z</code> (з, звідки), <code>bez</code> (без), <code>dla</code> (для), <code>u</code> (у когось).",
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
                    "<code>Narzędnik</code> (kim? czym?) — три головні вживання: <b>ким я є</b>, "
                    "<b>з ким/чим</b>, <b>чим роблю</b> (інструмент).",
                ),
                Card(
                    "1) Бути кимось: być + Narzędnik",
                    "Професія/роль після <code>być</code> — у Narzędnik.",
                    [("Jestem studentem.", "Я студент."), ("Ona jest lekarką.", "Вона лікарка.")],
                    tip="Тому не «jestem student», а «jestem studentem». Дуже часта помилка початківців!",
                ),
                Card(
                    "2) З кимось: z + Narzędnik",
                    "Прийменник <code>z</code> у значенні «разом із» вимагає Narzędnik.",
                    [("z bratem", "з братом"), ("kawa z mlekiem", "кава з молоком")],
                ),
                Card(
                    "Закінчення",
                    "• чоловічий/середній → <code>-em</code> (student→studentem, okno→oknem)\n"
                    "• жіночий → <code>-ą</code> (kawa→kawą, Anna→Anną)\n"
                    "• множина → <code>-ami</code> (z przyjaciółmi — з друзями)",
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
                    "<code>Miejscownik</code> — єдиний відмінок, що <b>ніколи не буває без прийменника</b>. "
                    "Найчастіше — про <b>місце</b> (де?).",
                ),
                Card(
                    "Прийменники-тригери",
                    "<code>w</code> (у), <code>na</code> (на), <code>o</code> (про), <code>przy</code> (біля), <code>po</code> (після).",
                    [("w domu", "вдома"), ("na stole", "на столі"), ("myślę o tobie", "думаю про тебе")],
                ),
                Card(
                    "Закінчення (буває «мʼяким»)",
                    "Часто <code>-e</code> зі змʼякшенням приголосного, або <code>-u</code>:\n"
                    "• stół → na sto<code>le</code>, szkoła → w szko<code>le</code>\n"
                    "• dom → w do<code>mu</code>, pokój → w poko<code>ju</code>",
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
                    "<code>Celownik</code> (komu? czemu?) — той, <b>кому</b> щось даємо/робимо "
                    "(непрямий додаток).",
                ),
                Card(
                    "Дієслова-тригери",
                    "<code>dawać</code> (давати), <code>pomagać</code> (допомагати), <code>dziękować</code> (дякувати), "
                    "<code>mówić</code> (казати комусь).",
                    [("Daję mamie kwiaty.", "Даю мамі квіти."), ("Pomagam bratu.", "Допомагаю братові."),
                     ("Dziękuję ci.", "Дякую тобі.")],
                ),
                Card(
                    "Закінчення",
                    "• чоловічий → <code>-owi</code> (brat→bratowi, pan→panu — виняток)\n"
                    "• жіночий → <code>-e/-i</code> (mama→mamie, Anna→Annie)\n"
                    "• середній → <code>-u</code> (dziecko→dziecku)",
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
                    "<code>Wołacz</code> — форма для <b>звертання</b> (гей, Аню! пане!). В усному мовленні "
                    "часто заміняють на Mianownik, але у формальному й з іменами він живий.",
                ),
                Card(
                    "Закінчення",
                    "• жіночі імена → <code>-o</code> або <code>-u</code> (Anna→Anno, Ania→Aniu)\n"
                    "• чоловічі → <code>-e/-u</code> (Piotr→Piotrze, pan→panie)",
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
                    "• <code>mieć/lubić/widzieć</code> → Biernik\n• <code>nie ma / dużo / do, od, bez, dla</code> → Dopełniacz\n"
                    "• <code>być kim / z kim</code> → Narzędnik\n• <code>w, na, o</code> (місце) → Miejscownik\n"
                    "• <code>dawać, pomagać, dziękować</code> → Celownik",
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
