TARGET = data/campus_20.in
TARGET += data/campus_17.in
TARGET += data/campus_13.in
TARGET += data/campus_07.in

all: $(TARGET)
		@echo > /dev/null

data/campus_20.in: convert_real.py dataset1/sortedeventsseconds.txt dataset1/furnasupdated.txt dataset1/jarvisupdated.txt
	./$< dataset1/sortedeventsseconds.txt dataset1/furnasupdated.txt dataset1/jarvisupdated.txt > $@

data/campus_17.in: convert_real.py dataset2/sortedeventsseconds.txt dataset2/furnasupdated.txt dataset2/jarvisupdated.txt
	./$< dataset2/sortedeventsseconds.txt dataset2/furnasupdated.txt dataset2/jarvisupdated.txt > $@

data/campus_13.in: convert_real.py dataset3/sortedeventsseconds.txt dataset3/furnasupdated.txt dataset3/jarvisupdated.txt
	./$< dataset3/sortedeventsseconds.txt dataset3/furnasupdated.txt dataset3/jarvisupdated.txt > $@

data/campus_07.in: convert_real.py dataset4/sortedeventsseconds.txt dataset4/furnasupdated.txt dataset4/jarvisupdated.txt
	./$< dataset4/sortedeventsseconds.txt dataset4/furnasupdated.txt dataset4/jarvisupdated.txt > $@


clean:
	@rm -f data.dat
	@rm -f $(TARGET)

.PHONY: clean all
