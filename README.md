# My Local ChatGPT

Telegram-бот, который умеет:

* 💬 Общаться в чате с локальной LLM (через Ollama)
* 🖼 Генерировать изображения по промптам (через ComfyUI)
* 🖼️ Распознавать картинки, присланные пользователями
* 🚀 Работает полностью локально, ничего не отправляет в интернет
* 🔐 Безопасен: всё крутится на `localhost`

---

## Запуск бота

1. Клонируй репозиторий и перейди в папку проекта:

   git clone https://github.com/Inartful/MyLocalChatGPT.git
   cd MyLocalChatGPT

2. Создай и активируй виртуальное окружение:

   python -m venv venv
   source venv/bin/activate  # для Linux/macOS
   venv\Scripts\activate     # для Windows

3. Установи зависимости:

   pip install -r requirements.txt

4. Запусти бота:

   ./run.sh

---

## Требования

* Python 3.8+
* Локально установленные сервисы:

  * Ollama (LLM и распознавание изображений)
  * ComfyUI (Генерация изображений)

