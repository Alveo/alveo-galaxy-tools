GALAXY_DIST=/Users/steve/projects/third-party/galaxy
PLANEMO = planemo
TOOLSHED = testtoolshed

upload-apitools:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) tools/apitools

upload-nltk:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) tools/nltk

upload-parse_eval:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) tools/parse_eval

upload-textgrid:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) tools/textgrid

upload-vowel-plot:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) tools/vowel-plot

upload-wrassp:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) tools/wrassp

upload-maus:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) tools/maus

upload-ziptools:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) tools/ziptools

upload: upload-apitools upload-nltk upload-parse_eval upload-textgrid upload-vowel-plot upload-wrassp upload-maus upload-ziptools

lint:
	$(PLANEMO) shed_lint --tools --ensure_metadata --urls --report_level warn --fail_level error --recursive tools

flake8:
	flake8 --ignore=E501 tools
