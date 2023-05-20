fixRelativeLinkDocs:
	sed  's/\.\/docs/\./g'  README.md > docs/README.md
	#sed  's/\.\/docs/\./g'  README.cs.md > docs/README.cs.md

generateTeamPortfolio:
	@echo "Generating team portfolio..."
	python3 generateTeamPortfolio.py

# Docs
docs-build: fixRelativeLinkDocs generateTeamPortfolio
	@echo "Building docs..."
	mkdocs build

docs-serve: fixRelativeLinkDocs generateTeamPortfolio
	@echo "Serving docs..."
	mkdocs serve

docs-deploy: fixRelativeLinkDocs generateTeamPortfolio
	@echo "Deploying docs..."
	mkdocs gh-deploy --force