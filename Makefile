.PHONY: dev-setup generate-notebooks strip-notebooks help

help:
	@echo "Available targets:"
	@echo "  dev-setup           One-time setup for local dev (install git hooks)"
	@echo "  generate-notebooks  Regenerate all notebooks from scripts/generate_notebooks.py"
	@echo "  strip-notebooks     Manually strip outputs from all committed notebooks"

dev-setup:
	pip install nbstripout
	nbstripout --install
	@echo ""
	@echo "nbstripout installed. Notebooks will be committed without outputs or"
	@echo "execution counts — merge conflicts on notebook metadata are now impossible."

generate-notebooks:
	python scripts/generate_notebooks.py

strip-notebooks:
	find notebooks -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" \
	    -exec nbstripout {} \;
	@echo "All notebooks stripped."
