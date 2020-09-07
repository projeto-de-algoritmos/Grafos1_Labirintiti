BIN=env/bin/
help:
		@echo "Makefile para a Execução do Projeto"
		@echo ""
		@echo " - A utilização da virtualenv é recomendada"
		@echo "   -> Para saber mais, acesse: https://encurtador.com.br/suKN5"
		@echo ""
		@echo "Commandos:"
		@echo "install     Instala os requisitos do projeto"
		@echo "run         Executa o projeto"
		@echo ""

install:
		pip3 install -r requirements.txt
run:
		python3 main.py