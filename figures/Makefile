TARGETS = rates.pdf

rates.pdf: rates.py
	./$< $@ 2 10 20 100

clean:
	@rm -f $(TARGETS)

all: $(TARGETS)

.PHONY: all
