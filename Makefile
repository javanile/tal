
init:
	@python3 -m venv .venv
	@source .venv/bin/activate

push:
	@git add .
	@git commit -am "New release!" || true
	@git push

test:
	python3 main.py lib/test.tal > out/test.yaml
