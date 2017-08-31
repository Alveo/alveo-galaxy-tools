GALAXY_DIST=/Users/steve/projects/third-party/galaxy
PLANEMO = planemo
TOOLSHED = testtoolshed

upload-apitools:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) apitools

upload-nltk:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) nltk

upload-parse_eval:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) parse_eval

upload-textgrid:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) textgrid

upload-vowel-plot:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) vowel-plot

upload-wrassp:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) wrassp

upload-maus:
	$(PLANEMO) shed_update --force_repository_creation --check_diff -t $(TOOLSHED) maus


upload: upload-apitools upload-nltk upload-parse_eval upload-textgrid upload-vowel-plot upload-wrassp upload-maus


datatypes:
	ln -s datatypes/alveo.py $(GALAXY_DIST)/lib/galaxy/datatypes/
	ln -s datatypes/datatypes_conf.xml $(GALAXY_DIST)/lib/galaxy/config/
