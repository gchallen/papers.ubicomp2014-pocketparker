TARGETS = figures/capacity.pdf figures/lots.pdf figures/capacity_experiment.pdf
TARGETS += runs/fastfill_10_10.data runs/slowfill_10_10.data runs/multifill_10_10.data runs/highchurn_10_10.data runs/lowchurn_10_10.data
TARGETS += runs/fastfill_10_20.data runs/fastfill_10_50.data runs/fastfill_10_100.data
TARGETS += runs/fastfill_01_10.data runs/fastfill_05_10.data runs/fastfill_20_10.data runs/fastfill_50_10.data
TARGETS += figures/tracking_fastfill.pdf figures/accuracy_table.tex

all: $(TARGETS)

figures/capacity.pdf: simulator.py capacity.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.1 0.2 0.9 0.9 --repeat=14 --seed=10 | ./capacity.py --output $@ 1>/dev/null

figures/lots.pdf: lots.py lib.py lots/fastfill.xml lots/slowfill.xml lots/highchurn.xml lots/lowchurn.xml lots/multifill.xml
	./$< $@ lots/fastfill.xml lots/slowfill.xml lots/highchurn.xml lots/lowchurn.xml lots/multifill.xml

figures/capacity_experiment.pdf: capacity_experiment.py simulator.py capacity.py lib.py lots/fastfill.xml lots/slowfill.xml lots/highchurn.xml lots/lowchurn.xml lots/multifill.xml
	./$< $@ lots/fastfill.xml lots/slowfill.xml lots/highchurn.xml lots/lowchurn.xml lots/multifill.xml

runs/slowfill_10_10.data: simulator.py estimator.py lib.py lots/slowfill.xml
	./$< lots/slowfill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=1 | ./estimator.py 0.1 1.0 > $@

runs/multifill_10_10.data: simulator.py estimator.py lib.py lots/multifill.xml
	./$< lots/multifill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=1 | ./estimator.py 0.1 1.0 > $@

runs/highchurn_10_10.data: simulator.py estimator.py lib.py lots/highchurn.xml
	./$< lots/highchurn.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=1 | ./estimator.py 0.1 1.0 > $@

runs/lowchurn_10_10.data: simulator.py estimator.py lib.py lots/lowchurn.xml
	./$< lots/lowchurn.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=1 | ./estimator.py 0.1 1.0 > $@

runs/fastfill_10_10.data: simulator.py estimator.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=1 | ./estimator.py 0.1 1.0 > $@

runs/fastfill_10_20.data: simulator.py estimator.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=2 | ./estimator.py 0.2 1.0 > $@

runs/fastfill_10_50.data: simulator.py estimator.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=3 | ./estimator.py 0.5 1.0 > $@

runs/fastfill_10_100.data: simulator.py estimator.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=4 | ./estimator.py 1.0 1.0 > $@

runs/fastfill_01_10.data: simulator.py estimator.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.01 0.0 0.9 0.9 --repeat=1 --seed=5 | ./estimator.py 0.1 1.0 > $@

runs/fastfill_05_10.data: simulator.py estimator.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.05 0.0 0.9 0.9 --repeat=1 --seed=6 | ./estimator.py 0.1 1.0 > $@

runs/fastfill_20_10.data: simulator.py estimator.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.2 0.0 0.9 0.9 --repeat=1 --seed=7 | ./estimator.py 0.1 1.0 > $@

runs/fastfill_50_10.data: simulator.py estimator.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.5 0.0 0.9 0.9 --repeat=1 --seed=8 | ./estimator.py 0.1 1.0 > $@

figures/tracking_fastfill.pdf: tracking.py runs/fastfill_10_10.data
	./$< $@ runs/fastfill_10_10.data

figures/accuracy_table.tex: accuracy.py 
	./$< runs/* > $@

clean:
	@rm -f $(TARGETS)

.PHONY: all
