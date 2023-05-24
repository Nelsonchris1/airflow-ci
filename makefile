dir: 
	sudo mkdir -p ./dags ./logs ./plugins ./config ./test && sudo chmod -R u=rwx,g=rwx,o=rwx logs plugins config dags test
up_doc:
	docker compose up airflow-init && docker compose up  --build -d

up: dir up_doc

down:
	docker compose down

install:
	docker exec webserver sh -c "pip install pytest black flake8 mypy isort apache-airflow"

pytest:
	docker exec webserver pytest /opt/airflow/test

formatter:
	docker exec webserver black /opt/airflow/dags/forex_data_pipeline.py

isort:
	docker exec webserver isort /opt/airflow/dags/forex_data_pipeline.py

lint:
	docker exec webserver flake8 /opt/airflow/dags/forex_data_pipeline.py

type:
	docker exec webserver mypy /opt/airflow/dags/forex_data_pipeline.py

check: formatter isort lint type


