TARGETS = figures/capacity.pdf


figures/capacity.pdf: simulator.py capacity.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.1 0.2 0.9 0.9 --repeat=14 --seed=10 | ./capacity.py --output $@ 1>/dev/null

clean:
	@rm -f $(TARGETS)

all: $(TARGETS)

.PHONY: all
