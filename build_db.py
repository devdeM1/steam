import os
from config import db
from models import Game, User, UserGame, Genre, Community, CommunityUser, CommunityGame
from datetime import datetime
from werkzeug.security import generate_password_hash


# Data to initialize database with
GAMES = [
    {"name": "Dota 2", "price": 0, "genre": "Strategy", "point": 5},
    {"name": "Hearthstone", "text": "Hearthstone: Heroes of Warcraft представляет собой коллекционную карточную онлайн-игру, основанную на пошаговой системе передаче ходов между оппонентами в течение матча с использованием предварительно подготовленных колод карт[22]. В игре доступны несколько игровых режимов, отличающихся правилами проведения матчей или использования колод. Как и в других играх этого жанра, в Hearthstone имеется стратегическая составляющая, проявляющаяся в тактике предматчевого сбора колод и рационального использования карт в течение матча, с элементом случайности, состоящем в порядке вытягивания карт из колоды и эффектах отдельных карт[8]. Каждый новый игрок после режима «Обучения» получает возможность бесплатно собрать базовый набор карт. В дальнейшем можно получить дополнительные наборы карт путём приобретения за игровую валюту или за реальные деньги по системе микротранзакций (при этом приобретаются комплекты случайных карт выбранного игроком дополнения)[8].Hearthstone не имеет общей сюжетной составляющей, и весь игровой процесс представлен матчами между двумя игроками в различных игровых режимах. Перед началом матча игрок собирает колоду из 30 карт и приступает к поиску противника в определённом режиме игры. После нахождения оппонента системой матчмейкинга между игроками случайным образом определяется право первого хода, и каждый из игроков вытягивает, в зависимости от очерёдности, по 3 или 4 карты из своей колоды. Предложенные карты игрок может в течение отведённого времени сменить на произвольные другие, содержащиеся в его колоде[9]. Каждая карта в игре обладает стоимостью, измеряемой в затрачиваемых на её использование «кристаллах маны» (англ. Mana crystals). Игроку, ходящему вторым, предоставляется карта «Монетка», дающая на один ход дополнительный кристалл маны[9].Игра начинается с одним кристаллом маны у каждого из игроков, количество которых увеличивается на один кристалл на следующий ход вплоть до 10 кристаллов (то есть на второй ход у игрока имеется 2 кристалла маны, на четвёртый — 4 и т. д.), причём использованные в предыдущий ход кристаллы полностью восполняются[9]. Число карт, которые можно сыграть за один игровой ход, ограничено только суммарной стоимостью по кристаллам маны и максимальным временем хода (90 секунд). Оба игрока представлены на игровом поле героями выбранных игровых классов, имеющими изначально по 30 единиц здоровья и обладающими уникальными для каждого из классов «силами героя» (англ. Hero power), использование которых стоит два кристалла маны (например, класс «Охотник» обладает способностью «Верный выстрел», наносящей две единицы урона герою противника). Каждый ход игрок вытягивает из колоды по одной карте. Единовременно в руке игрока не может находиться более десяти карт — каждая следующая вытянутая карта при полной руке уничтожается[8]. Игрок может разыгрывать карты только в свой ход, но эффекты отдельных карт воспроизводятся вне зависимости от очерёдности ходов оппонентов. При исчерпании всех карт игрок начинает вытягивать «карты усталости» (англ. Fatigue cards), наносящие урон здоровью его героя, увеличивающийся при вытягивании новой карты в арифметической прогрессии. Цель игры состоит в уничтожении при помощи собственных карт героя противника (то есть доведении его очков здоровья до нуля)[9]. Среднее время одного матча составляет от 10 до 15 минут[23]. ", "platforms": "Windows, OS X, iOS, Android", "date": "11.03.2013", "developer": "Blizzard Entertainment", "price": 7, "genre": "Strategy", "point": 9},
    {"name": "ELDEN RING", "price": 35, "genre": "RPG", "point": 9},
    {"name": "Rogue Legacy 2", "price": 10, "genre": "Indie", "point": 8},
    {"name": "NARAKA: BLADEPOINT", "price": 10, "genre": "PvP", "point": 7},
    {"name": "Hollow Knight", "price": 4, "genre": "Indie", "point": 9},
    {"name": "iRacing", "price": 7, "genre": "Simulation", "point": 8},
    {"name": "Deep Rock Galactic", "text": "Deep Rock Galactic — первый научно-фантастический шутер с видом от первого лица для совместной игры, в котором вас ждут крутые космические гномы, полностью разрушаемое окружение, процедурно генерируемые системы пещер и бесконечные волны инопланетных чудовищ.", "platform": "PlayStation 4, Xbox One, PlayStation 5, Microsoft Windows, Windows 10", "developer": "Ghost Ship Games", "date": "13.05.2020", "price": 7, "genre": "PvE", "point": 9},
    {"name": "The Stanley Parable: Ultra Deluxe", "price": 12, "genre": "Walking Simulator", "point": 9},
    {"name": "Slay the Spire", "price": 5, "genre": "Card Game", "point": 10},
    {"name": "Peglin", "price": 10, "genre": "Pinball", "point": 8},
    {"name": "Dread Hunger", "price": 15, "genre": "Survival", "point": 6},
    {"name": "Valheim", "price": 8, "genre": "Survival", "point": 9},
    {"name": "Nioh 2 – The Complete Edition", "price": 33, "genre": "JRPG", "point": 8},
    {"name": "Dune: Spice Wars", "price": 15, "genre": "Building", "point": 8},
    {"name": "Dorfromantik", "price": 6, "genre": "Puzzle", "point": 9},
    {"name": "Wallpaper Engine", "price": 3, "genre": "Indie", "point": 10},
    {"name": "STAR WARS™ Complete Collection", "price": 45, "genre": "RPG", "point": 9},
    {"name": "Phasmophobia", "price": 8, "genre": "Horror", "point": 9},
    {"name": "Underdog Detective Complete Season", "price": 14, "genre": "RPG", "point": 7},
    {"name": "Northgard", "price": 4, "genre": "RTS", "point": 9},
    {"name": "Rust", "price": 20, "genre": "Survival", "point": 9},
    {"name": "Raft", "price": 13, "genre": "Crafting", "point": 9},
    {"name": "Northgard: The Viking Age Edition", "price": 17, "genre": "RTS", "point": 8},
    {"name": "Dinosaur Fossil Hunter", "text": "Dinosaur Fossil Hunter — приключенческий симулятор с видом от первого лица, где вам предстоит стать охотником за окаменелостями динозавров. Во время прохождения вы отправитесь исследовать обширные локации и пустынные земли, бережно выкапывать скелеты и изучать их, чтобы в итоги отрыть свой собственный музей.", "date": "04.05.2022", "developer": "Pyramid Games", "platform": "Microsoft Windows", "price": 10, "genre": "Building", "point": 7},
    {"name": "Noita", "price": 9, "genre": "Roguelike", "point": 9},
    {"name": "Gunfire Reborn", "price": 8, "genre": "Action", "point": 7},
    {"name": "Dead Cells", "text": "Жанр Dead Cells описывается как «roguevania» — сочетание жанров roguelike с их процедурно генерируемыми уровнями и метроидваний с их action-геймплеем и связными мирами, требующими постепенного исследования[2]. Существо, которым управляет игрок, представляет собой разумный сгусток клеток, в каждом новом прохождении завладевающий трупом одного из казненных заключенных в огромной тюрьме. В ходе игры персонаж обследует различные подземелья, побеждает населяющих их врагов и собирает многочисленные предметы. Персонаж может носить с собой два оружия и два вспомогательных предмета и находить в подземельях новые — от мечей и метательных ножей до гранат, капканов и турельных установок. Оружие и предметы обладают разными случайно генерируемыми характеристиками и дополнительными эффектами, наподобие серии Diablo[3]. Так, оружие может наносить повышенный урон истекающим кровью врагам или заставлять трупы поверженных противников взрываться. Выпадающие из побежденных врагов предметы — «клетки» — позволяют в конце каждого уровня приобретать постоянные бонусы, как, например, возможность больше раз использовать склянку для восстановления здоровья или особо мощное оружие по найденным в подземельях чертежам[4]. Клетки можно потратить только в конце уровня; если игровой персонаж погибнет, не добравшись до выхода с уровня, он потеряет все собранные клетки.[5]Каждый уровень в каждом прохождении генерируется случайным образом — при этом игра собирает запутанные лабиринты из заранее определенных элементов, случайно разбрасывая по ним врагов и предметы. Подобно серии Souls, игра проводит игрока через сражения с врагами со сложным поведением и предполагает, что персонаж будет часто погибать, а игрок — учиться на своих ошибках. Хотя большинства сражений в игре можно избежать, в ходе прохождения.Dead Cells игрок должен победить нескольких особо сложных боссов.Dead Cells поддерживает интеграцию с видеостриминговым сервисом Twitch — это упрощает трансляцию игры через интернет и позволяет зрителям трансляции влиять на игровой процесс, например, голосуя в чате, каким путем должен двинуться игрок[6]. ", "platform": "Windows, macOS, Linux, PlayStation 4, Xbox One, Nintendo Switch, iOS, iPadOS, Android", "date": "07.08.2018", "developer": "Playdigious", "price": 8, "genre": "Indie", "point": 10},
    {"name": "Stardew Valley", "price": 10, "genre": "RPG", "point": 10},
    {"name": "Project Hospital Collection", "price": 13, "genre": "Strategy", "point": 8},
    {"name": "Ready or Not", "price": 25, "genre": "Tactical", "point": 9},
    {"name": "Escape Simulator", "price": 7, "genre": "Puzzle", "point": 9},
    {"name": "God of War", "price": 40, "genre": "Combat", "point": 10},
    {"name": "Project Zomboid", "price": 11, "genre": "Zombies", "point": 9},
    {"name": "Vampire Survivors", "price": 2, "genre": "RPG", "point": 10},
    {"name": "Squad", "price": 23, "genre": "War", "point": 9},
    {"name": "Dead Cells: Road to the Sea Bundle", "text": "Жанр Dead Cells описывается как «roguevania» — сочетание жанров roguelike с их процедурно генерируемыми уровнями и метроидваний с их action-геймплеем и связными мирами, требующими постепенного исследования[2]. Существо, которым управляет игрок, представляет собой разумный сгусток клеток, в каждом новом прохождении завладевающий трупом одного из казненных заключенных в огромной тюрьме. В ходе игры персонаж обследует различные подземелья, побеждает населяющих их врагов и собирает многочисленные предметы. Персонаж может носить с собой два оружия и два вспомогательных предмета и находить в подземельях новые — от мечей и метательных ножей до гранат, капканов и турельных установок. Оружие и предметы обладают разными случайно генерируемыми характеристиками и дополнительными эффектами, наподобие серии Diablo[3]. Так, оружие может наносить повышенный урон истекающим кровью врагам или заставлять трупы поверженных противников взрываться. Выпадающие из побежденных врагов предметы — «клетки» — позволяют в конце каждого уровня приобретать постоянные бонусы, как, например, возможность больше раз использовать склянку для восстановления здоровья или особо мощное оружие по найденным в подземельях чертежам[4]. Клетки можно потратить только в конце уровня; если игровой персонаж погибнет, не добравшись до выхода с уровня, он потеряет все собранные клетки.[5]Каждый уровень в каждом прохождении генерируется случайным образом — при этом игра собирает запутанные лабиринты из заранее определенных элементов, случайно разбрасывая по ним врагов и предметы. Подобно серии Souls, игра проводит игрока через сражения с врагами со сложным поведением и предполагает, что персонаж будет часто погибать, а игрок — учиться на своих ошибках. Хотя большинства сражений в игре можно избежать, в ходе прохождения Dead Cells игрок должен победить нескольких особо сложных боссов.Dead Cells поддерживает интеграцию с видеостриминговым сервисом Twitch — это упрощает трансляцию игры через интернет и позволяет зрителям трансляции влиять на игровой процесс, например, голосуя в чате, каким путем должен двинуться игрок[6]. " , "platform": "Nintendo Switch, PlayStation 4, Xbox One, Microsoft Windows, Linux, Mac OS" , "developer": "Motion Twin","date": "06.01.2022", "price": 12, "genre": "Roguelite", "point": 8},
    {"name": "Terraria", "price": 7, "genre": "2D", "point": 9.6},
    {"name": "King Arthur: Knight's Tale", "price": 21, "genre": "Strategy", "point": 8.3},
    {"name": "Project Hospital", "price": 5, "genre": "Building", "point": 9.1},
    {"name": "The Forest", "price": 11, "genre": "Horror", "point": 9.6},
    {"name": "The Planet Crafter", "price": 11.49, "genre": "Simulation", "point": 9.6},
    {"name": "Euro Truck Simulator 2", "price": 2.74, "genre": "Simulation", "point": 9.7},
    {"name": "WARNO", "price": 30, "genre": "PvP", "point": 8},
    {"name": "No Man's Sky", "price": 35, "genre": "Space", "point": 8},
    {"name": "JUNKPUNK", "price": 6, "genre": "Building", "point": 7},
    {"name": "Wildermyth", "price": 9, "genre": "Choices Matter", "point": 9},
    {"name": "Core Keeper", "text": "Core Keeper — аркадная песочницу на выживание с видом сверху, в которую вы сможете сыграть с друзьями в кооперативе до восьми человек. Вы выступите в роли исследователя, проснувшегося в древнем подземелье, наполненном враждебных существ, ловушек и сокровищ. Чтобы выжить в этом опасном месте, герою предстоит найти мощное снаряжение, прокачать способности и построить собственную базу в качестве убежища. Локации в игре генерируются случайным образом, что делает геймплей значительно реиграбельным. Основную опасность для персонажа будут представлять огромные монстры, в числе которых есть боссы.", "date": "01.01.2021", "developer": "Pugstorm", "platform": "Linux, Microsoft Windows", "price": 8, "genre": "2D", "point": 9, "pic_path": "Core Keeper"},
    #{"name": "Cultivation Tales", "price": 11, "genre": "Sandbox", "point": 3, "pic_path":"Cultivation Tales"},
    {"name": "Pummel Party", "price": 8, "genre": "Co-op", "point": 9},
    {"name": "Atelier Ryza: Ever Darkness & the Secret Hideout", "date": "26.10.2019", "platform": " Nintendo Switch, PC, PS4	","devoloper": "Koei Tecmo", "text":"Основанная на новом мире Atelier последняя игра в серии представляет концепцию «Самые обычные подростки вместе становятся взрослее... даже если совсем чуточку». Это история девочки и ее друзей, вставших на путь, ведущий к взрослению, и осознающих, что для них важнее всего на самом деле. Чтобы как можно красочнее рассказать историю о том, как главные персонажи открывают для себя нечто невиданное раньше, мы реализовали натуральные тени, которые позволят вам почувствовать дыхание этого мира. Игровая графика была еще сильнее улучшена, что позволяет совершенно по-новому показать этот мир повседневной жизни и невероятных приключений. Главные особенности ■Продвинутая система Synthesis и Location Points. Система Synthesis, позволяющая игрокам соединять материалы для создания новых предметов, претерпела значительные изменения. Теперь, помимо того, что вы сможете оценить эффект синтеза визуально, система позволит вам еще больше наслаждаться созданием новых рецептов. Кроме того, мы добавили Location Points, которые игроки могут создавать с помощью синтеза! ■Используйте различные инструменты для сбора новых материалов! Используя Gathering для сбора нужных для синтеза материалов, в зависимости от используемых инструментов вы получаете различные материалы, так что теперь вам будет проще получить желаемое. ■Динамичные битвы Сочетание походовой боевой системы с элементами реального времени позволит вам насладиться динамичными битвами, исход которых зависит от каждого вашего выбора! Эта система позволит еще сильнее прочувствовать укрепление неразрывной связи между вами и вашими друзьями. Сюжет Главный персонаж этой истории — Риза, самая обычная девочка. Устав от скучной деревенской жизни, она сбегает из своего дома и вместе со своими друзьями отправляется в тайное место, чтобы поговорить там о своих мечтах и спланировать захватывающие приключение. В один прекрасный день решительная Риза с друзьями решают отправиться в первое в их жизни приключение и исследовать запретный «остров по ту сторону». Теперь в компании алхимика и других новых друзей Ризу ждут такие летние приключения, которые они вовек не забудут.","price": 14, "genre": "Anime", "point": 7, },
    {"name": "Farming Simulator 22", "price": 35, "genre": "Co-op", "point": 9},
    {"name": "Enter the Gungeon", "price": 4, "genre": "Roguelike", "point": 9},
    {"name": "Danganronpa", "text": "Danganronpa: Trigger Happy Havoc (яп. ダンガンロンパ 希望の学園と絶望の高校生 данганромпа кибо: но гакуэн то дзэцубо: но ко:ко:сэй, Данганромпа: школа надежды и старшеклассники отчаяния) — игра в жанре визуальный роман, разработанная и опубликованная компанией Spike Chunsoft, позже была адаптирована в аниме и мангу.Игра была выпущена 25 ноября 2010 года исключительно в Японии для портативной приставки PlayStation Portable[3]. Аниме-адаптация игры аниме выполнена студией Lerche, премьера состоялась 4 июля 2013 года.Продолжение под названием Danganronpa 2: Goodbye Despair было выпущено для PlayStation Portable 26 июля 2012 года. Компиляция обеих игр с названием Danganronpa 1・2 Reload была выпущена для PlayStation Vita в Японии 10 октября 2013 года.12 января 2017 года вышла финальная часть игры New Danganronpa V3: Killing Harmony, повествующая абсолютно новую историю, никак не связанную с сюжетом предыдущих частей.Название Danganronpa происходит от слов «пуля» (яп. 弾丸 (ダンガン) данган) и «опровержение, доказательство» (яп. 論破 (ロンパ) ромпа), но так как слово написано катаканой, оно остаётся непереводимым. Во время расследования убийства, когда участники академии опровергают факты и предположения других учащихся, изображается пуля, которая «разбивает» неверные предположения. ", "platform": "PlayStation Portable iOS Android PlayStation VitaPC","date": "25.11.2010", "developer": "Spike Chunsoft", "price": 13, "genre": "Adventure", "point": 7, "pic_path": "Danganronpa"},
    {"name": "Satisfactory", "price": 15, "genre": "Crafting", "point": 9},
    {"name": "World War 3", "price": 8, "genre": "Modern", "point": 7},
    {"name": "Death's Door",  "text": "Death’s Door очень четко разделяет прогресс по сюжету на несколько стадий. После краткого вступления, призванного познакомить игрока с основными геймплейными элементами и структурой игры, мы получаем задание от большой и старой вороны: нам нужно посетить три локации и сразить местных боссов. Никакой свободы нам не дают - наш путь к цели строго линеен, без каких-либо срезок и обходных путей. Каждая из локаций поделена на 4 подлокации: подступы к крепости, сама крепость, погоня за боссом и арена с боссом. Каждая из подлокаций предлагает свой стиль геймплея, которому разработчики следуют на протяжении всей игры. Первая часть - подступы к крепости - вдохновлены классической метроидванией и серией Dark Souls в частности. Активируем дверь (местный костер) и отправляемся продвигаться по локации, открывая многочисленные шорткаты. Здесь мы играемся на большой карте, разделенной на зоны, которые представляют разного рода испытания. Где-то небольшую задачку решить, где-то пару мобов убить, а где-то - пережить несколько волн врагов. ", "date": "20.07.2021", "platform": "Microsoft Windows, Nintendo Switch, PlayStation 4, PlayStation 5, Xbox One, Xbox Series X/S", "developer": "Acid Nerve", "price": 8, "genre": "RPG", "point": 9},
    {"name": "Factorio", "price": 12, "genre": "Crafting", "point": 9},
    {"name": "Barotrauma", "text": "Это приключенческий экшен, события которого разворачиваются на Европе - планете-спутнике Юпитера. На промерзшей базе игроки сталкиваются с инопланетными формами жизни и должны постараться сделать все возможное, чтобы выжить и не стать чьим-то обедом.","developer": "Undertow Games FakeFish", "date": "05.06.2019", "platform": " Linux, Mac, PC	","price": 3, "genre": "Submarine", "point": 9, "pic_path":"Barotrauma"},
    {"name": "Risk of Rain 2: Survivors of the Void", "price": 8, "genre": "Co-op", "point": 8},
    {"name": "Nioh: Complete Edition", "price": 6, "genre": "Ninja", "point": 7},
    {"name": "Fall Guys: Ultimate Knockout", "price": 11, "genre": "PvP", "point": 7},
    {"name": "BeamNG.drive", "text":"BeamNG.drive — невероятно реалистичный автосимулятор с практически безграничными возможностями. В основе игры лежит система физики мягких объектов, способная правдоподобно моделировать компоненты автомобиля в реальном времени. Благодаря годам кропотливой разработки, исследований и испытаний, BeamNG.drive способен передать весь восторг вождения в реальном мире. ","date": "29.05.2015", "developer": "BeamNG", "platform": "Windows","price": 13, "genre": "Driving", "point": 9, "pic_path":"BeamNG.drive"},
    {"name": "Hades", "price": 13, "genre": "Mythology", "point": 9},
    {"name": "Don't Starve Together", "price": 8, "genre": "Crafting", "point": 9},
    #{"name": "Car Mechanic Simulator 2021", "price": 10, "genre": "Driving", "point": 9, "pic_path": "Car Mechanic Simulator 2021"},
    {"name": "Skul: The Hero Slayer", "price": 7, "genre": "2D", "point": 9},
    {"name": "7 Days to Die", "price": 15, "genre": "Open World", "point": 8,"platform":"Microsoft Windows, OS X, Linux, PlayStation 4, Xbox One", "developer": "The Fun Pimps ", "date": "13.12.2013", "text": "Это воксельная игра про выживание среди зомби-апокалипсиса, в которой игроки могут сообща строить свои общины, отбиваться от толп зомби и стараться выжить. Зомби в этой игре становятся агрессивнее с каждой ночью, поэтому игроки должны озаботиться защитой от зараженных в темное время суток."},
    {"name": "WARRIORS OROCHI 4 Ultimate Deluxe Edition", "price": 20, "genre": "Action", "point": 7},
    {"name": "WorldBox - God Simulator", "price": 10, "genre": "Sandbox", "point": 9},
    {"name": "Mount & Blade II: Bannerlord", "price": 30, "genre": "Action", "point": 9},
    {"name": "Beat Saber", "date": "21.05.2019", "developer": "Beat Games", "platform": "PlayStation 4, Windows", "price": 15, "genre": "Moddable", "point": 9,'pic_path':"Beat Saber", "text":"В первом квартале 2018 года вышла игра, которая без сомнений всколыхнула сообщества любителей VR пространств. Чешские разработчики представили «на суд» своё детище, а именно игру виртуальной реальности Beat Saber, которая практически мгновенно заслужило множество положительных отзывов. Причём лестно о Beat Saber высказываются не только рядовые пользователи, но и критики.Особенности игры:Создателем Beat Saber выступила маленькая студия Hyperbolic Magnetism. Достаточно простая концепция в совокупности с яркой графикой и динамичной музыкой, неожиданно произвели фурор в мире VR игр.Суть игры предельно проста, возможно поэтому гениальна, в ней нужно «разрезать» световыми мечами блоки, летящие на игрока. Каждый из кубов соответствует ноте воспроизводимой музыки. Чем точнее будут взмахи саблями, тем красивее и ритмичнее получится мелодия, и тем больше очков наберет игрок. Казалось бы, ничего сложного? Однако Beat Saber заво смогла увлечь даже закоренелых скептиков и противников VR."},
    {"name": "Kingdom Two Crowns", "price": 2, "genre": "Indie", "point": 9},
    {"name": "Euro Truck Simulator 2 - Iberia", "price": 10, "genre": "Indie", "point": 7},
    {"name": "Sable", "price": 8, "genre": "Indie", "point": 9},
    {"name": "TEKKEN 7", "price": 10, "genre": "Arcade", "point": 7},
    #{"name": "Bounty game", "price": 8, "genre": "Action", "point": 8, "pic_path": "Bounty game"},
    {"name": "Inscryption", "price": 13, "genre": "Adventure", "point": 10},
    {"name": "SCUM", "price": 16, "genre": "Zombies", "point": 8},
    {"name": "DayZ", "text": "Перед игроком в DayZ ставится цель выжить во враждебном мире, охваченном зомби-апокалипсисом. Созданный персонаж появляется в игровом мире с пустыми руками, имея при себе только самую простую одежду, химсвет и бинт. Открытый мир игры представляет собой обширную территорию площадью 225 квадратных километров, со множеством городов, деревень, полей и лесов, без каких-либо внутренних барьеров и загрузок; в отличие от одноимённой модификации, практически в любое здание в игре можно зайти[4]. Чтобы остаться в живых, персонаж должен разыскивать в заброшенных зданиях пищу, воду и лекарства[5][6]. Помимо собственно необходимых для выживания припасов, в игре также может найти разнообразные предметы одежды — одежда не только облегчает выживание, защищая персонажа от врагов и непогоды и позволяя носить с собой больше предметов, но и позволяет подчеркнуть его индивидуальность, сделав непохожим на других персонажей[7]. Предоставляя игроку возможность защищать себя от враждебных зомби и других игроков, DayZ содержит множество видов всевозможного оружия, от кухонных ножей до современных автоматов (хотя с версии 1.0 их количество изрядно подсократилось), а также разнообразные боеприпасы, прицелы и прочие принадлежности (среди них: цевья, приклады, сошки, прицелы, а само оружие возможно покрасить (убрано с официальных серверов с версии 1.0). В игру введены возможности выращивания овощей, рыбалки и разнообразной охоты, начиная от силков для поимки зайцев, и заканчивая банальной стрельбой по оленям. ", "platform": " 	ПК (Windows),PlayStation 4 и Xbox One", "developer": "Bohemia Interactive", "date": "07.08.2012", "price": 45, "genre": "Zombies", "point": 9, "pic_path": "DayZ"},
    {"name": "Teardown", "price": 11, "genre": "Voxel", "point": 9},
    {"name": "Stacklands", "price": 3, "genre": "Card Battler", "point": 9},
    {"name": "Garry's Mod", "price": 7, "genre": "Co-op", "point": 10},
    {"name": "UBOAT", "price": 15, "genre": "War", "point": 8},
    {"name": "Witch It", "price": 3, "genre": "Indie", "point": 8},
    {"name": "Underdog Detective-Episode 6 to 17", "price": 11, "genre": "RPG", "point": 5},
    {"name": "Frostpunk", "price": 4, "genre": "Survival", "point": 9},
    {"name": "Prehistoric Kingdom", "price": 15, "genre": "Sandbox", "point": 8},
    {"name": "Mirror 2: Project X Bundle", "price": 5, "genre": "RPG", "point": 7},
    {"name": "Streets of Rogue", "price": 4, "genre": "Action", "point": 10},
    {"name": "Unrailed!", "price": 3, "genre": "Co-op", "point": 9},
    {"name": "Bloons TD 6", "date": "13.06.2018",  "developer": "Ninja Kiwi", "platform": "Android, iOS, Microsoft Windows, macOS", "price": 6, "genre": "Co-op", "point": 10, "pic_path": "Bloons TD 6", "text": "Bloons TD 6 - это продолжение знаменитой Bloons TD, которая увидела свет в далеком 2007 году. Затем была целая серия новинок, которые полюбились игрокам разного возраста. Игра выполнена в стиле защита башен. Но вместо башен на поле ставятся забавные обезьянки.Главная задача игрока - не дать воздушным шарикам пересечь карту и достичь финальной точки. Для этого необходимо на поле расставить мартышек или специальные предметы. Каждая башня имеет свои особенности, при этом наносит урон шарикам. Но шарики не так просты, как может показаться на первый взгляд. В игре большое количество башен, которые улучшаются в сражениях. И очень много разного рода шариков. Самые мощные из них - это дирижабли, которые тоже делятся на несколько видов.На старте игры геймера знакомят с игровым процессом, дают почувствовать атмосферу битвы. Вы бесплатно получите обезьянку с дротиками, и вам дадут на растерзание цепочку красных шариков."},
    {"name": "DARK SOULS™: REMASTERED", "text": "Dark Souls Remastered - это переиздание самой первой части культовой ролевой серии, которое предлагает игрокам подтянутую графику, увеличенное количество кадров в секунду, различные балансные правки, а также выход на портативной Nintendo Switch. Также игра получила несколько небольших балансных изменений, обновленное расположение костров (например, добавился новый костер у кузнеца-скелета Вамоса), а также различные визуальные обновления. Dark Souls Remastered может похвастаться поддержкой разрешений до 4K, стабильным фреймрейтом в 60 кадров в секунду даже в Блайттауне, а также другими техническими улучшениями. " ,"developer": "From Software", "date": "24.05.2018", "platform": "PC, PS4, Xbox One и Nintendo Switch", "price": 40, "genre": "RPG", "point": 8, "pic_path":"DARK SOULS : REMASTERED"},
    {"name": "Subnautica", "price": 1, "genre": "Survival", "point": 10},
    {"name": "Metal Mind", "price": 8, "genre": "Roguelite", "point": 8},
]

USERS = [
    {"name": "Maks",
     "balance": 100,
     "country": "Belarus",
     "sex": "men",
     "login": "maks",
     "password": "1111",
     "email": "kyky@qq.com"},
    {"name": "Dima",
     "balance": 777,
     "country": "Belarus",
     "sex": "men",
     "login": "dima",
     "password": "1234",
     "email": "kyky@qq.com"
     },
    {"name": "Nikita",
     "balance": 0,
     "country": "Belarus",
     "sex": "men",
     "login": "nikita0812",
     "password": "1111",
     "email": "kykyq@qq.com"},
    {"name": "Andrei",
     "date": "18.02.1999",
     "balance": 100,
     "country": "Germany",
     "sex": "men",
     "login": "andreya",
     "password": "1111",
     "email": "kykyw@qq.com"},
    {"name": "Alex",
     "date": "08.07.1989",
     "balance": 100,
     "country": "USA",
     "sex": "men",
     "login": "alexqwe",
     "password": "1111",
     "email": "kykye@qq.com"},
    {"name": "Polina",
     "date": "02.12.2002",
     "balance": 100,
     "country": "Belarus",
     "sex": "women",
     "login": "impolina",
     "password": "1111",
     "email": "kykyr@qq.com"},
    {"name": "Tania",
     "date": "30.10.2012",
     "balance": 100,
     "country": "Russia",
     "sex": "women",
     "login": "tania322",
     "password": "1111",
     "email": "kykyy@qq.com"},
    {"name": "Vika",
     "date": "02.02.2002",
     "balance": 100,
     "country": "Belarus",
     "sex": "women",
     "login": "4ikavika",
     "password": "1111",
     "email": "kykyi@qq.com"},
    {"name": "Kristina",
     "date": "02.03.2002",
     "balance": 100,
     "country": "Belarus",
     "sex": "women",
     "login": "kristinka",
     "password": "1111",
     "email": "kykyasd@qq.com"},
    {"name": "Fillip",
     "date": "02.10.2002",
     "balance": 100,
     "country": "Belarus",
     "sex": "man",
     "login": "fillipgod",
     "password": "1111",
     "email": "kyky8@qq.com"},
    {"name": "Ksenia",
     "date": "02.02.2002",
     "balance": 100,
     "country": "Ukraine",
     "sex": "women",
     "login": "ksushatop",
     "password": "1111",
     "email": "kykqwer@qq.com"},
    {"name": "Felix",
     "date": "02.02.2002",
     "balance": 100,
     "country": "Belarus",
     "sex": "man",
     "login": "ymnuikotfelixnaidet",
     "password": "1111",
     "email": "kyky123@qq.com"},

]

USERS_GAMES = [
    {"game_name": "Hearthstone", "user_name": "Maks"},
    {"game_name": "Dota 2", "user_name": "Dima"},
    {"game_name": "Hearthstone", "user_name": "Dima"},
    {"game_name": "Peglin", "user_name": "Dima"},
    {"game_name": "SCUM", "user_name": "Dima"},
    {"game_name": "Witch It", "user_name": "Dima"},
]
'''{"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "Witch It", "user_name": "Maks"},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "SCUM", "user_name": "Dima"},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "Witch It", "user_name": "Dima"},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
    {"game_name": "", "user_name": ""},
'''

GENRES = [
    {"name": "Strategy"},
    {"name": "Shooter"},
    {"name": "RPG"},
    {"name": "Indie"},
    {"name": "PvP"},
    {"name": "Simulation"},
    {"name": "PvE"},
    {"name": "Walking Simulator"},
    {"name": "Card Game"},
    {"name": "Pinball"},
    {"name": "Survival"},
    {"name": "JRPG"},
    {"name": "Building"},
    {"name": "Puzzle"},
    {"name": "Horror"},
    {"name": "RTS"},
    {"name": "Crafting"},
    {"name": "Roguelike"},
    {"name": "Tactical"},
    {"name": "Combat"},
    {"name": "Zombies"},
    {"name": "War"},
    {"name": "Roguelite"},
    {"name": "2D"},
    {"name": "Space"},
    {"name": "Choices Matter"},
    {"name": "Sandbox"},
    {"name": "Co-op"},
    {"name": "Anime"},
    {"name": "Adventure"},
    {"name": "Modern"},
    {"name": "Action"},
    {"name": "Submarine"},
    {"name": "Ninja"},
    {"name": "Driving"},
    {"name": "Mythology"},
    {"name": "Open World"},
    {"name": "Moddable"},
    {"name": "Arcade"},
    {"name": "Voxel"},
    {"name": "Card Battler"},
]

COMMUNITY = [
    {"name": "Party 12 vs 12 Doka 2"},
    {"name": "easy-peasy, lemon squeezy"}
]

COMMUNITY_USER = [
    {"community_name": "Party 12 vs 12 Doka 2", "user_name": "Dima"},
    {"community_name": "Party 12 vs 12 Doka 2", "user_name": "Maks"},
    {"community_name": "easy-peasy, lemon squeezy", "user_name": "Dima"},
]

COMMUNITY_GAME = [
    {"community_name": "Party 12 vs 12 Doka 2", "game_name": "Dota 2"},
    {"community_name": "easy-peasy, lemon squeezy", "game_name": "Hearthstone"},
]

db.drop_all()
# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for genre in GENRES:
    g = Genre(
        name=genre.get("name")
    )
    db.session.add(g)

for game in GAMES:
    genre = Genre.query.filter(Genre.name == game.get("genre")).one_or_none()
    date = game.get("date")
    if date is not None:
        date = datetime.strptime(game.get("date"), '%d.%m.%Y'),
    else:
        date = datetime.now()
    p = Game(
        name=game.get("name"),
        price=game.get("price"),
        genre_id=genre.id,
        point=game.get("point"),
        pic_path=game.get("name"),
        text=game.get("text"),
        developer=game.get("developer"),
        date=date,
        platform=game.get("platform"),
    )
    db.session.add(p)

for user in USERS:
    u = User(
        name=user.get("name"),
        date=user.get("date"),
        balance=user.get("balance"),
        country=user.get("country"),
        sex=user.get("sex"),
        email=user.get("email")
    )
    db.session.add(u)

for connect in USERS_GAMES:
    game = Game.query.filter(Game.name == connect.get("game_name")).one_or_none()
    user = User.query.filter(User.name == connect.get("user_name")).one_or_none()
    c = UserGame(
        game_id=game.id,
        user_id=user.user_id
    )
    db.session.add(c)

for community in COMMUNITY:
    com = Community(
        name=community.get("name")
    )
    db.session.add(com)

for community_user in COMMUNITY_USER:
    community = Community.query.filter(Community.name == community_user.get("community_name")).one_or_none()
    user = User.query.filter(User.name == community_user.get("user_name")).one_or_none()
    c_u = CommunityUser(
        community_id=community.id,
        user_id=user.user_id
    )
    db.session.add(c_u)

for community_game in COMMUNITY_GAME:
    community = Community.query.filter(Community.name == community_game.get("community_name")).one_or_none()
    game = Game.query.filter(Game.name == community_game.get("game_name")).one_or_none()
    c_g = CommunityGame(
        community_id=community.id,
        game_id=game.id
    )
    db.session.add(c_g)

db.session.commit()
