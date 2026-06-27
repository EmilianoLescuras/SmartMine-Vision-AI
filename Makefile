.PHONY: dev-setup generate-notebooks strip-notebooks help

help:
	@echo "Available targets:"
	@echo "  dev-setup           One-time setup for local dev (install git hooks)"
	@echo "  generate-notebooks  Regenerate all notebooks from scripts/generate_notebooks.py"
	@echo "  strip-notebooks     Manually strip outputs from all committed notebooks"

dev-setup:
	pip install nbstripout
	nbstripout --install
	git config pull.autostash true
	@echo ""
	@echo "Dev setup complete:"
	@echo "  - nbstripout: notebooks committed without outputs (no merge conflicts)"
	@echo "  - pull.autostash: git pull handles dirty notebooks automatically"

generate-notebooks:
	python scripts/generate_notebooks.py

strip-notebooks:
	find notebooks -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" \
	    -exec nbstripout {} \;
	@echo "All notebooks stripped."
