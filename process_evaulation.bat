REM process_evaluation test_input.txt test_score.txt output.txt

python evaluate_model.py %1 %3

perl correlation-noconfidence.pl %3 %2

@echo off
REM process_evaulation.bat test\12STS.input.MSRvid.txt test\12STS.gs.MSRvid.txt output.txt
REM process_evaulation.bat test\12STS.input.MSRpar.txt test\12STS.gs.MSRpar.txt output.txt
REM process_evaulation.bat test\12STS.input.SMTeuroparl.txt test\12STS.gs.SMTeuroparl.txt output.txt
REM process_evaulation.bat test\13STS.input.OnWN.txt test\13STS.gs.OnWN.txt output.txt
REM process_evaulation.bat test\13STS.input.headlines.txt test\13STS.gs.headlines.txt output.txt
REM process_evaulation.bat test\13STS.input.FNWN.txt test\13STS.gs.FNWN.txt output.txt
REM process_evaulation.bat test\joint.input.txt test\joint.gs.txt output.txt
REM process_evaulation.bat test\joint_veryshort.input.txt test\joint_veryshort.gs.txt output.txt
REM process_evaulation.bat test\joint_short.input.txt test\joint_short.gs.txt output.txt
REM process_evaulation.bat test\joint_unbalanced.input.txt test\joint_unbalanced.gs.txt output.txt
REM process_evaulation.bat test\joint_long.input.txt test\joint_long.gs.txt output.txt
