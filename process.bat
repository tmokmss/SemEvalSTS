REM Usage: process train_input train_score test_input test_score result

python calculate_svr.py %1 %2 %3 %4 %5

perl correlation-noconfidence.pl %5 %4

@echo off
REM process_new train\12STS.input.MSRpar.txt train\12STS.gs.MSRpar.txt test\12STS.input.MSRpar.txt test\12STS.gs.MSRpar.txt output.txt

REM process_new train\12STS.input.MSRvid.txt train\12STS.gs.MSRvid.txt test\12STS.input.MSRvid.txt test\12STS.gs.MSRvid.txt output.txt

REM process_new.bat train\13STS.input.FNWN.txt train\13STS.gs.FNWN.txt test\13STS.input.FNWN.txt test\13STS.gs.FNWN.txt output.txt
