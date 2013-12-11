TARGETS = figures/capacity.pdf figures/lots.pdf figures/capacity_experiment.pdf figures/tracking_fastfill.pdf figures/accuracy_table.tex figures/accuracy_graph.pdf

TARGETS += runs/fastfill_10_10.data runs/fastfill_10_20.data runs/fastfill_10_50.data runs/fastfill_10_100.data runs/fastfill_01_10.data runs/fastfill_05_10.data runs/fastfill_20_10.data runs/fastfill_50_10.data
TARGETS += runs/slowfill_10_10.data runs/slowfill_10_20.data runs/slowfill_10_50.data runs/slowfill_10_100.data runs/slowfill_01_10.data runs/slowfill_05_10.data runs/slowfill_20_10.data runs/slowfill_50_10.data
TARGETS += runs/multifill_10_10.data runs/multifill_10_20.data runs/multifill_10_50.data runs/multifill_10_100.data runs/multifill_01_10.data runs/multifill_05_10.data runs/multifill_20_10.data runs/multifill_50_10.data
TARGETS += runs/highchurn_10_10.data runs/highchurn_10_20.data runs/highchurn_10_50.data runs/highchurn_10_100.data runs/highchurn_01_10.data runs/highchurn_05_10.data runs/highchurn_20_10.data runs/highchurn_50_10.data
TARGETS += runs/lowchurn_10_10.data runs/lowchurn_10_20.data runs/lowchurn_10_50.data runs/lowchurn_10_100.data runs/lowchurn_01_10.data runs/lowchurn_05_10.data runs/lowchurn_20_10.data runs/lowchurn_50_10.data
TARGETS += runs/campus_07_00.data runs/campus_13_00.data runs/campus_17_00.data runs/campus_20_00.data

all: $(TARGETS)

figures/capacity.pdf: simulator.py capacity.py lib.py lots/fastfill.xml
	./$< lots/fastfill.xml 0.1 0.2 0.9 0.9 --repeat=14 --seed=10 | ./capacity.py --output $@ 1>/dev/null

figures/lots.pdf: lots.py lib.py lots/fastfill.xml lots/slowfill.xml lots/multifill.xml lots/highchurn.xml lots/lowchurn.xml
	./$< $@ lots/fastfill.xml lots/slowfill.xml lots/multifill.xml lots/highchurn.xml lots/lowchurn.xml

figures/capacity_experiment.pdf: capacity_experiment.py simulator.py capacity.py lib.py lots/fastfill.xml lots/slowfill.xml lots/multifill.xml lots/highchurn.xml lots/lowchurn.xml
	./$< $@ lots/fastfill.xml lots/slowfill.xml lots/multifill.xml lots/highchurn.xml lots/lowchurn.xml

figures/tracking_fastfill.pdf: tracking.py runs/fastfill_10_10.data
	./$< $@ runs/fastfill_10_10.data

figures/accuracy_table.tex: accuracy.py 
	./$< runs/* > $@

figures/accuracy_graph.pdf: accuracy_graph.py 
	./$< runs/* > $@

#################

runs/campus_07_00.data: estimator.py lib.py data/campus_07.in
	cat data/campus_07.in | ./estimator.py 0.0 1.0 > $@

runs/campus_13_00.data: estimator.py lib.py data/campus_13.in
	cat data/campus_13.in | ./estimator.py 0.0 1.0 > $@

runs/campus_17_00.data: estimator.py lib.py data/campus_17.in
	cat data/campus_17.in | ./estimator.py 0.0 1.0 > $@

runs/campus_20_00.data: estimator.py lib.py data/campus_20.in
	cat data/campus_20.in | ./estimator.py 0.0 1.0 > $@

#################

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

#################

runs/slowfill_10_10.data: simulator.py estimator.py lib.py lots/slowfill.xml
	./$< lots/slowfill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=1 | ./estimator.py 0.1 1.0 > $@

runs/slowfill_10_20.data: simulator.py estimator.py lib.py lots/slowfill.xml
	./$< lots/slowfill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=2 | ./estimator.py 0.2 1.0 > $@

runs/slowfill_10_50.data: simulator.py estimator.py lib.py lots/slowfill.xml
	./$< lots/slowfill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=3 | ./estimator.py 0.5 1.0 > $@

runs/slowfill_10_100.data: simulator.py estimator.py lib.py lots/slowfill.xml
	./$< lots/slowfill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=4 | ./estimator.py 1.0 1.0 > $@

runs/slowfill_01_10.data: simulator.py estimator.py lib.py lots/slowfill.xml
	./$< lots/slowfill.xml 0.01 0.0 0.9 0.9 --repeat=1 --seed=5 | ./estimator.py 0.1 1.0 > $@

runs/slowfill_05_10.data: simulator.py estimator.py lib.py lots/slowfill.xml
	./$< lots/slowfill.xml 0.05 0.0 0.9 0.9 --repeat=1 --seed=6 | ./estimator.py 0.1 1.0 > $@

runs/slowfill_20_10.data: simulator.py estimator.py lib.py lots/slowfill.xml
	./$< lots/slowfill.xml 0.2 0.0 0.9 0.9 --repeat=1 --seed=7 | ./estimator.py 0.1 1.0 > $@

runs/slowfill_50_10.data: simulator.py estimator.py lib.py lots/slowfill.xml
	./$< lots/slowfill.xml 0.5 0.0 0.9 0.9 --repeat=1 --seed=8 | ./estimator.py 0.1 1.0 > $@

#################

runs/multifill_10_10.data: simulator.py estimator.py lib.py lots/multifill.xml
	./$< lots/multifill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=1 | ./estimator.py 0.1 1.0 > $@

runs/multifill_10_20.data: simulator.py estimator.py lib.py lots/multifill.xml
	./$< lots/multifill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=2 | ./estimator.py 0.2 1.0 > $@

runs/multifill_10_50.data: simulator.py estimator.py lib.py lots/multifill.xml
	./$< lots/multifill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=3 | ./estimator.py 0.5 1.0 > $@

runs/multifill_10_100.data: simulator.py estimator.py lib.py lots/multifill.xml
	./$< lots/multifill.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=4 | ./estimator.py 1.0 1.0 > $@

runs/multifill_01_10.data: simulator.py estimator.py lib.py lots/multifill.xml
	./$< lots/multifill.xml 0.01 0.0 0.9 0.9 --repeat=1 --seed=5 | ./estimator.py 0.1 1.0 > $@

runs/multifill_05_10.data: simulator.py estimator.py lib.py lots/multifill.xml
	./$< lots/multifill.xml 0.05 0.0 0.9 0.9 --repeat=1 --seed=6 | ./estimator.py 0.1 1.0 > $@

runs/multifill_20_10.data: simulator.py estimator.py lib.py lots/multifill.xml
	./$< lots/multifill.xml 0.2 0.0 0.9 0.9 --repeat=1 --seed=7 | ./estimator.py 0.1 1.0 > $@

runs/multifill_50_10.data: simulator.py estimator.py lib.py lots/multifill.xml
	./$< lots/multifill.xml 0.5 0.0 0.9 0.9 --repeat=1 --seed=8 | ./estimator.py 0.1 1.0 > $@

#################

runs/highchurn_10_10.data: simulator.py estimator.py lib.py lots/highchurn.xml
	./$< lots/highchurn.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=1 | ./estimator.py 0.1 1.0 > $@

runs/highchurn_10_20.data: simulator.py estimator.py lib.py lots/highchurn.xml
	./$< lots/highchurn.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=2 | ./estimator.py 0.2 1.0 > $@

runs/highchurn_10_50.data: simulator.py estimator.py lib.py lots/highchurn.xml
	./$< lots/highchurn.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=3 | ./estimator.py 0.5 1.0 > $@

runs/highchurn_10_100.data: simulator.py estimator.py lib.py lots/highchurn.xml
	./$< lots/highchurn.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=4 | ./estimator.py 1.0 1.0 > $@

runs/highchurn_01_10.data: simulator.py estimator.py lib.py lots/highchurn.xml
	./$< lots/highchurn.xml 0.01 0.0 0.9 0.9 --repeat=1 --seed=5 | ./estimator.py 0.1 1.0 > $@

runs/highchurn_05_10.data: simulator.py estimator.py lib.py lots/highchurn.xml
	./$< lots/highchurn.xml 0.05 0.0 0.9 0.9 --repeat=1 --seed=6 | ./estimator.py 0.1 1.0 > $@

runs/highchurn_20_10.data: simulator.py estimator.py lib.py lots/highchurn.xml
	./$< lots/highchurn.xml 0.2 0.0 0.9 0.9 --repeat=1 --seed=7 | ./estimator.py 0.1 1.0 > $@

runs/highchurn_50_10.data: simulator.py estimator.py lib.py lots/highchurn.xml
	./$< lots/highchurn.xml 0.5 0.0 0.9 0.9 --repeat=1 --seed=8 | ./estimator.py 0.1 1.0 > $@

#################

runs/lowchurn_10_10.data: simulator.py estimator.py lib.py lots/lowchurn.xml
	./$< lots/lowchurn.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=1 | ./estimator.py 0.1 1.0 > $@

runs/lowchurn_10_20.data: simulator.py estimator.py lib.py lots/lowchurn.xml
	./$< lots/lowchurn.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=2 | ./estimator.py 0.2 1.0 > $@

runs/lowchurn_10_50.data: simulator.py estimator.py lib.py lots/lowchurn.xml
	./$< lots/lowchurn.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=3 | ./estimator.py 0.5 1.0 > $@

runs/lowchurn_10_100.data: simulator.py estimator.py lib.py lots/lowchurn.xml
	./$< lots/lowchurn.xml 0.1 0.0 0.9 0.9 --repeat=1 --seed=4 | ./estimator.py 1.0 1.0 > $@

runs/lowchurn_01_10.data: simulator.py estimator.py lib.py lots/lowchurn.xml
	./$< lots/lowchurn.xml 0.01 0.0 0.9 0.9 --repeat=1 --seed=5 | ./estimator.py 0.1 1.0 > $@

runs/lowchurn_05_10.data: simulator.py estimator.py lib.py lots/lowchurn.xml
	./$< lots/lowchurn.xml 0.05 0.0 0.9 0.9 --repeat=1 --seed=6 | ./estimator.py 0.1 1.0 > $@

runs/lowchurn_20_10.data: simulator.py estimator.py lib.py lots/lowchurn.xml
	./$< lots/lowchurn.xml 0.2 0.0 0.9 0.9 --repeat=1 --seed=7 | ./estimator.py 0.1 1.0 > $@

runs/lowchurn_50_10.data: simulator.py estimator.py lib.py lots/lowchurn.xml
	./$< lots/lowchurn.xml 0.5 0.0 0.9 0.9 --repeat=1 --seed=8 | ./estimator.py 0.1 1.0 > $@

#################

clean:
	@rm -f $(TARGETS)

.PHONY: all
