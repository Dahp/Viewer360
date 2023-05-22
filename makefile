# Определение переменных
PYTHON = python3
SRC_DIR = .
MAIN_FILE = EquiView360.py
VENV_DIR = .venv

# Правило по умолчанию
default: run

# # Установка виртуального окружения
# venv:
# 	$(PYTHON) -m venv $(VENV_DIR)

# # Активация виртуального окружения
# activate:
# 	source $(VENV_DIR)/bin/activate

# # Установка зависимостей
# install:
# 	pip install -r requirements.txt

# Запуск программы
run:
	sudo $(PYTHON) $(SRC_DIR)/$(MAIN_FILE)

# Очистка
# clean:
# 	rm -rf $(VENV_DIR)

.PHONY: run
# .PHONY: default venv activate install run clean
