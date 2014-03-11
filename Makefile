START = xxxnote
END = missing
CLASS = $(PYTEX)/cls/sigchi.cls

export TEXINPUTS:=.:$(PYTEX)/cls:

all: paper ABSTRACT wc

figures:
	@cd figures ; make

ABSTRACT: $(PYTEX)/bin/clean $(PYTEX)/bin/lib.py abstract.tex
	@$(PYTEX)/bin/clean abstract.tex ABSTRACT

wc: abstract.tex
	@$(PYTEX)/bin/wc $< -

# 16 Nov 2010 : GWA : Add other cleaning rules here.

clean: rulesclean
	@rm -f ABSTRACT

include $(PYTEX)/make/Makerules
