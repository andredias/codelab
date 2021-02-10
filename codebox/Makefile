PWD := $(shell pwd)

test: test_in_container

test_in_container:
	docker build -t codebox-test -f Dockerfile.test .
	docker run -it --rm  \
	           -v $(PWD)/app:/codebox/app \
	           -v $(PWD)/tests/:/codebox/tests \
			   codebox-test pytest -svx
