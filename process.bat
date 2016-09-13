REM Usage: process train_input train_score test_input test_score model_output result_output

python calculate_svr.py %1 %2 %3 %4 %5

python evaluate_model.py %4 %3 %6

perl correlation-noconfidence.pl %6 %4

@echo off
REM process train\12STS.input.MSRpar.txt train\12STS.gs.MSRpar.txt test\12STS.input.MSRpar.txt test\12STS.gs.MSRpar.txt model.txt output.txt

REM process train\12STS.input.MSRvid.txt train\12STS.gs.MSRvid.txt test\12STS.input.MSRvid.txt test\12STS.gs.MSRvid.txt model.txt output.txt

REM process train\12STS.input.SMTeuroparl.txt train\12STS.gs.SMTeuroparl.txt test\12STS.input.SMTeuroparl.txt test\12STS.gs.SMTeuroparl.txt model.txt output.txt

REM process train\13STS.input.FNWN.txt train\13STS.gs.FNWN.txt test\13STS.input.FNWN.txt test\13STS.gs.FNWN.txt model.txt output.txt

REM process train\13STS.input.headlines.txt train\13STS.gs.headlines.txt test\13STS.input.headlines.txt test\13STS.gs.headlines.txt model.txt output.txt

REM process train\13STS.input.OnWN.txt train\13STS.gs.OnWN.txt test\13STS.input.OnWN.txt test\13STS.gs.OnWN.txt model.txt output.txt

REM process train\joint.input.txt train\joint.gs.txt test\joint.input.txt test\joint.gs.txt model.txt output.txt

REM process train\joint_long.input.txt train\joint_long.gs.txt test\joint_long.input.txt test\joint_long.gs.txt model_long.txt output.txt
REM process train\joint_short.input.txt train\joint_short.gs.txt test\joint_short.input.txt test\joint_short.gs.txt model_short.txt output.txt
REM process train\joint_unbalanced.input.txt train\joint_unbalanced.gs.txt test\joint_unbalanced.input.txt test\joint_unbalanced.gs.txt model_unbalanced.txt output.txt
REM process train\joint_veryshort.input.txt train\joint_veryshort.gs.txt test\joint_veryshort.input.txt test\joint_veryshort.gs.txt model_veryshort.txt output.txt
