TARGETS = rates.pdf arrival.pdf departure.pdf search.pdf

rates.pdf: rates.py
	./$< $@ 2 10 20 100

arrival.pdf departure.pdf search.pdf: examples.py
	./$<

clean:
	@rm -f $(TARGETS)

all: $(TARGETS)

.PHONY: all
