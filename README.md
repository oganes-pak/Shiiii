# USB Encryptor

## Описание программы
USB Encryptor — это приложение на Python с графическим интерфейсом (Kivy), предназначенное для шифрования и расшифрования файлов на USB-накопителях. Программа использует простой метод шифрования на основе XOR и кодировки Base64, а также позволяет пользователю управлять шифрованием через удобный GUI.

Программа разработана исключительно в **научных и учебных целях** для демонстрации принципов работы с файловыми системами и алгоритмов шифрования. Она **не предназначена** для защиты конфиденциальных данных, поскольку используемый метод шифрования не является криптографически стойким.

---

## Функциональные возможности
- Автоматическое **обнаружение подключенных USB-устройств** и обновление списка дисков.
- **Шифрование файлов** с использованием пароля, введенного пользователем.
- **Расшифрование файлов**, если пароль введен правильно.
- **Резервное копирование** файлов перед шифрованием.
- **Прогресс-бар** и возможность отмены операции.
- Переключение между **светлой и темной темой** интерфейса.

---

## Алгоритм работы
### 1. Определение USB-устройств
- Программа получает список подключенных дисков, исключая системные.
- При обнаружении нового USB-накопителя выводится уведомление.
- Обновление списка происходит каждые 2 секунды.

### 2. Шифрование файлов
- Пользователь выбирает диск и вводит пароль.
- Создается папка `Backup`, куда копируются файлы перед шифрованием.
- Каждый файл читается побайтово, и к каждому байту применяется **XOR с паролем**.
- Результат кодируется в **Base64** и сохраняется обратно.
- В корневую папку диска записывается файл `control.txt`, содержащий зашифрованный маркер для проверки пароля.

### 3. Расшифрование файлов
- Пользователь вводит пароль.
- Программа читает `control.txt` и расшифровывает маркер.
- Если пароль неверен, расшифрованное слово не совпадает с оригиналом.
- При правильном пароле файлы декодируются и сохраняются в исходном виде.

### 4. Управление процессом
- Во время шифрования/дешифрования отображается **прогресс-бар**.
- При нажатии кнопки «Отмена» процесс прерывается.

---

## Возможные уязвимости и угрозы
### 1. **Ненадежное шифрование (XOR + Base64)**
- XOR легко взламывается, если известен хотя бы один фрагмент исходного текста.
- Base64 — это не защита, а лишь способ кодирования данных.
- Пароль не проходит хеширование, что делает возможным атаку перебором (brute force).

### 2. **Отсутствие защиты от подмены `control.txt`**
- Если злоумышленник заменит `control.txt` заранее подготовленным файлом, он сможет заставить программу принять неверный пароль.

### 3. **Отсутствие проверки резервной копии**
- Программа создает `Backup`, но не использует его при расшифровке.
- Если пользователь введет неверный пароль, он может перезаписать файлы поврежденной версией.

### 4. **Отсутствие подтверждения перед перезаписью**
- Нет диалогового окна с предупреждением перед изменением файлов.
- Пользователь может случайно потерять оригинальные данные.

---
## Заключение
Программа **USB Encryptor** разработана исключительно для **исследовательских и образовательных целей**. Она демонстрирует основные принципы работы с файловыми системами и шифрования данных, но **не должна использоваться для защиты конфиденциальной информации**.

Если вам нужна **реальная безопасность**, используйте современные криптографические библиотеки, такие как `cryptography` или `PyCryptodome`, и избегайте XOR-шифрования без дополнительной защиты.

---

## Разработчик
- grock
- **Имя:** [@narkomanchik228]
---
## Фото
- Интерфес программы
![image](https://github.com/user-attachments/assets/7a477b3e-b2cc-4999-ba24-410aadbc42f7)

- Задаем пароль 
![image](https://github.com/user-attachments/assets/8ede22cb-d079-424e-8b41-d481c2e14abc)

- Процесс шифрования
![image](https://github.com/user-attachments/assets/b43c5227-498b-4c79-8761-485427b0bb16)

- Демонстрация того что после шифрования фото не открывается
![image](https://github.com/user-attachments/assets/d2ad7660-b435-4cdc-89e1-0fbc991580e3)

- Изображение после расшифровки
![image](https://github.com/user-attachments/assets/404a97f2-f582-475d-b28f-cce0c91ca90b)

- Файлы на флешке после шифрования 
![image](https://github.com/user-attachments/assets/fce62a12-bcee-448b-83fc-9348cbad5591)

- Файлы на флешке до шифрования 
![image](https://github.com/user-attachments/assets/8911747e-d07d-4048-b188-9fe698a54dbc)

- Процесс
![image](https://github.com/user-attachments/assets/d48501b1-3a16-4198-bb29-8910ff8c571c)

https://youtu.be/JCQhOczMCQI

