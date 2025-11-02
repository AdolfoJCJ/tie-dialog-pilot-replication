
.PHONY: all setup clean figures metrics report

all: setup metrics figures report

setup:
	@mkdir -p reports/figures reports/artifacts data/interim data/processed

metrics:
	python scripts/run_pipeline.py --stage metrics --config configs/config.sample.yml

figures:
	python scripts/run_pipeline.py --stage figures --config configs/config.sample.yml

report:
	python scripts/run_pipeline.py --stage report --config configs/config.sample.yml

clean:
	rm -rf reports/figures/* reports/artifacts/* data/interim/* data/processed/*
