START = xxxnote
END = missing
CLASS = $(PYTEX)/cls/sensys.cls

all: paper ABSTRACT

ABSTRACT: abstract.tex
	@$(PYTEX)/bin/clean $< $@

# 16 Nov 2010 : GWA : Add other cleaning rules here.

clean: rulesclean
	@rm -f ABSTRACT

include $(PYTEX)/make/Makerules
