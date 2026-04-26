import subprocess

def check_disk_usage(threshold=90):
    # Запускаем команду 'df -h /' (проверяем корневой раздел)
    # capture_output=True — чтобы перехватить вывод в переменную
    # text=True — чтобы вывод был строкой, а не байтами
    result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Ошибка df: {result.stderr.strip()}")
        return

    # Вывод выглядит примерно так:
    # Filesystem      Size  Used Avail Use% Mounted on
    # /dev/sda1       50G   25G   25G  50% /
    lines = result.stdout.strip().split('\n')

    # Берем строку с / (смотрим по последней колонке, а не по позиции)
    # Это защищает от случая когда длинное имя устройства переносит строку
    data_line = next((l for l in lines[1:] if l.split()[-1] == '/'), None)
    if not data_line:
        print("Не удалось найти корневой раздел в выводе df.")
        return

    # Предпоследняя колонка — процент использования ("50%")
    usage_str = data_line.split()[-2]
    usage_percent = int(usage_str.replace('%', ''))

    print(f"Текущая загрузка диска: {usage_percent}%")

    if usage_percent > threshold:
        print(f"🔴 ALARM: Диск заполнен более чем на {threshold}%!")
    else:
        print("🟢 OK: Места достаточно.")

if __name__ == "__main__":
    check_disk_usage()
