

# Всё вместе

Здесь вкратце расписаны всевозможные тернистые пути от начала разработки игры на QSP (с использованием различных средств и инструментов) до ее реализации и запуска игры у конечного игрока.

## Написание игры

```mermaid
graph TD
  GameDev[Разработчик игры] --> |пишет игру в| Редактор

  Редактор --> |бывает| QGen[QGen]
  QGen --> |компилирует| БинарныйФайл[Бинарный файл игры .qsp]

  Редактор --> |бывает| VSCode[VS Code]
  VSCode --> |редактирует и проверяет код| Qsp.FSharp.VsCode[Qsp.FSharp.VsCode]

  VSCode --> |генерирует| ГолыеИсходники

  Редактор --> |бывает| ЛюбойТекстовыйРедактор[Любой текстовый редактор]
  ЛюбойТекстовыйРедактор --> |генерирует| ГолыеИсходники[Голые исходники .qsps .qsrc]

  Редактор --> |бывает| Sublime[Sublime Text]
  Sublime --> |генерирует| ГолыеИсходники
  Sublime --> |редактирует и проверяет код| JAD_for_QSP[JAD_for_QSP]

  ГолыеИсходники --> QSP_CLI[qsp-cli]
  QSP_CLI --> |компилирует| БинарныйФайл
  ГолыеИсходники --> TXT2GAM[TXT2GAM]
  TXT2GAM --> |компилирует| БинарныйФайл

  ГолыеИсходники --> ИграНаQsp[Игра на QSP]
  БинарныйФайл --> ИграНаQsp
```

Разработчик игры на QSP пишет игру в:

* QGen
* редакторе

  * Sublime Text
  * VS Code
  * любой текстовый редактор

Если в Sublime Text, то при проверке кода используется расширение JAD_for_QSP

Если в VS Code, то при написании кода используется расширение Qsp.FSharp.VsCode

QGen преобразовывает исходник в бинарный файл игры

Голые исходники, написанные в редакторах, либо оставляются так, либо преобразовываются в бинарник с помощью одной из утилит:

* QSP CLI
* TXT2GAM

Некоторые утилиты позволяют преобразовать бинарные файлы игр обратно в текстовый формат.

## Воспроизведение игры

```mermaid
flowchart TD
  ИграНаQsp --> ГолыеИсходники
  ГолыеИсходники --> |воспроизводятся в| Плеер
  ИграНаQsp --> БинарныйФайл
  БинарныйФайл --> |воспроизводятся в| Плеер

  Плеер --> |бывает| Classic[Classic]
  Classic --> |интерпретирует игровой код в| QSPLib[QSPLib]

  Плеер --> |бывает| Navigator[Navigator]
  Navigator --> |интерпретирует игровой код в| QSPLib

  Плеер --> |бывает| QSpider[QSpider]
  QSpider --> |использует| qsp-wasm-engine
  qsp-wasm-engine --> |интерпретирует игровой код в| QSPLib
```

Голые исходники или бинарники воспроизводятся в плеерах:

* Classic
* Navigator
* QSpider

Classic и Navigator используют интерпретатор QSPLib.

QSpider использует qsp-wasm-engine, который является обёрткой над интерпретатором QSPLib.

## Распространение игры

```mermaid
flowchart TD
  ИграНаQsp --> КаталогQSP[Каталог на https://qsp.org/]
  ИграНаQsp --> |оборачивается в| QSpiderStandalone[QSpider Standalone]
  QSpiderStandalone --> |выкладывается на| GitHubPages
  QSpiderStandalone --> |выкладывается на| ItchIo[itch.io]
```

В дальнейшем разработчик игры выкладывает ресурсы игры в:

* каталог QSP
* на GitHub Pages с помощью QSpider Standalone

Теперь игрок может:

* Скачать игру с [каталога на QSP](https://qsp.org/index.php?option=com_sobi2&Itemid=55) и воспроизвести ее в плеерах
* Запустить игру с [QSpider](https://dev.qsp.org/qspider)

  Там можно либо:

  * открыть со своего устройства .qsp файл
  * добавить игру с библиотеки и запустить
  * запустить игру по прямой ссылке

    * Игру с каталога

      Если знать ID игры (к примеру, 285 — "Баллада о Герое"), то можно ее запустить так:

      ```text
      https://qspfoundation.github.io/qspider/?catalogId=285
      ```

    * С отдельного источника

      К примеру, есть игра "Баллада о Герое", которая лежит по следующей ссылке:

      ```text
      https://aleksversus.github.io/QSP-storage/game/heroballad/heroballad.qsp
      ```

      Эту ссылку можно загнать в QSpider:

      ```text
      https://qspfoundation.github.io/qspider/?config=https://aleksversus.github.io/QSP-storage/game/heroballad/heroballad.qsp
      ```

      И [пройти по ней](https://qspfoundation.github.io/qspider/?config=https://aleksversus.github.io/QSP-storage/game/heroballad/heroballad.qsp)

* Зайти по ссылке на GitHub, itch.io и т.п. и просто начать играть

Самый лучший вариант, как облегчить жизнь разработчику игры и игроку, — залить игру на сайт и дать игроку прямую ссылку на игру. Так можно избежать +100500 проблем.
