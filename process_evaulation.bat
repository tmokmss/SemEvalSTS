REM process_evaluation model.txt test_input.txt test_score.txt output.txt

python evaluate_model.py %1 %2 %4

perl correlation-noconfidence.pl %4 %3

@echo off
REM process_evaulation.bat model.txt test\12STS.input.MSRvid.txt test\12STS.gs.MSRvid.txt output.txt
