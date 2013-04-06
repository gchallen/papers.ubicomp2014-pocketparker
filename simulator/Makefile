TARGETS = figures/capacity.pdf figures/lots.pdf

all: $(TARGETS)

figures/capacity.pdf: simulator.py capacity.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.1 0.2 0.9 0.9 --repeat=14 --seed=10 | ./capacity.py --output $@ 1>/dev/null

figures/lots.pdf: lots.py lots/fastfill.xml lots/slowfill.xml lots/highchurn.xml lots/lowchurn.xml lots/multifill.xml
	./$< $@ lots/fastfill.xml lots/slowfill.xml lots/highchurn.xml lots/lowchurn.xml lots/multifill.xml

clean:
	@rm -f $(TARGETS)

.PHONY: all
