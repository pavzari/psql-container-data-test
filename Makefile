up:
	docker compose up -d

down:
	docker compose down 

run-tests:
	export PYTHONPATH=${PWD} && pytest test/

shell:
	docker exec -ti runner bash

run-main:
	docker exec runner python /code/src/main.py

run-test:
	docker exec runner pytest /code/test


