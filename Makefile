up:
	docker compose up -d

down:
	docker compose down 

run-tests:
	export PYTHONPATH=${PWD} && pytest test/

runner-shell:
	docker exec -it runner bash

runner-main:
	docker exec runner python /code/src/main.py

runner-test:
	docker exec runner pytest /code/test


