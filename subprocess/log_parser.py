# Функция для поиска ошибок в лог-файле
def scan_logs(log_path, keyword="ERROR"):
    print(f"--- Начинаю сканирование файла: {log_path} ---")
    
    found_errors = 0 # Счетчик найденных ошибок
    
    try:
        # 'with open' — это контекстный менеджер.
        # Он сам закроет файл, даже если внутри произойдет ошибка.
        # 'r' — режим чтения (read).
        # encoding='utf-8' — важно указывать кодировку, чтобы не словить кракозябры.
        with open(log_path, 'r', encoding='utf-8') as file:
            
            # enumerate позволяет нам получать не только строку, но и её номер (i)
            # start=1 — чтобы нумерация шла с 1, а не с 0 (удобнее для человека)
            for line_number, line in enumerate(file, start=1):
                
                # line.strip() убирает лишние пробелы и перенос строки (\n) в конце
                clean_line = line.strip()
                
                # Проверяем, есть ли ключевое слово (например, "ERROR") в этой строке
                if keyword in clean_line:
                    print(f"Найден {keyword} на строке {line_number}: {clean_line}")
                    found_errors += 1
                    
        print(f"--- Сканирование завершено. Найдено ошибок: {found_errors} ---")

    except FileNotFoundError:
        print("ОШИБКА: Файл логов не найден! Проверьте путь.")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")

# Создадим для теста фейковый лог, чтобы скрипту было что читать
def create_dummy_log():
    dummy_name = "server.log"
    with open(dummy_name, "w", encoding="utf-8") as f:
        f.write("INFO: Сервер запущен\n")
        f.write("INFO: Пользователь вошел\n")
        f.write("ERROR: Соединение разорвано (Timeout)\n") # Вот это мы ищем
        f.write("INFO: Повторная попытка\n")
        f.write("CRITICAL ERROR: Диск отвалился!\n") # И это тоже
    return dummy_name

if __name__ == "__main__":
    # 1. Создаем тестовый файл
    log_file = create_dummy_log()
    
    # 2. Запускаем наш сканер
    scan_logs(log_file, keyword="ERROR")
    
    # 3. Убираем за собой (можно закомментировать, если хочешь посмотреть файл)
    import os
    if os.path.exists(log_file):
        os.remove(log_file)