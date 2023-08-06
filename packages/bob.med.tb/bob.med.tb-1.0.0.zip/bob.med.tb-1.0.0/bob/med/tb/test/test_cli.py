#!/usr/bin/env python
# coding=utf-8

"""Tests for our CLI applications"""

import os
import re
import pandas as pd
import fnmatch
import tempfile
import contextlib
from bob.extension import rc
import pkg_resources

import nose.tools

from click.testing import CliRunner

from . import mock_dataset

# Download test data and get their location if needed
montgomery_datadir = mock_dataset()

_pasa_checkpoint_URL = (
    "http://www.idiap.ch/software/bob/data/bob/bob.med.tb/master/_test_fpasa_checkpoint.pth"
)
_signstotb_checkpoint_URL = (
    "http://www.idiap.ch/software/bob/data/bob/bob.med.tb/master/_test_signstotb_checkpoint.pth"
)
_logreg_checkpoint_URL = (
    "http://www.idiap.ch/software/bob/data/bob/bob.med.tb/master/_test_logreg_checkpoint.pth"
)
_densenetrs_checkpoint_URL = (
    "http://www.idiap.ch/software/bob/data/bob/bob.med.tb/master/_test_densenetrs_checkpoint.pth"
)

@contextlib.contextmanager
def rc_context(**new_config):
    old_rc = rc.copy()
    rc.update(new_config)
    try:
        yield
    finally:
        rc.clear()
        rc.update(old_rc)

@contextlib.contextmanager
def stdout_logging():

    ## copy logging messages to std out
    import sys
    import logging
    import io

    buf = io.StringIO()
    ch = logging.StreamHandler(buf)
    ch.setFormatter(logging.Formatter("%(message)s"))
    ch.setLevel(logging.INFO)
    logger = logging.getLogger("bob")
    logger.addHandler(ch)
    yield buf
    logger.removeHandler(ch)

def _assert_exit_0(result):

    assert (
        result.exit_code == 0
    ), f"Exit code {result.exit_code} != 0 -- Output:\n{result.output}"

def _data_file(f):
    return pkg_resources.resource_filename(__name__, os.path.join("data", f))

def _check_help(entry_point):

    runner = CliRunner()
    result = runner.invoke(entry_point, ["--help"])
    _assert_exit_0(result)
    assert result.output.startswith("Usage:")

def test_config_help():
    from ..scripts.config import config

    _check_help(config)


def test_config_list_help():
    from ..scripts.config import list

    _check_help(list)

def test_config_list():
    from ..scripts.config import list

    runner = CliRunner()
    result = runner.invoke(list)
    _assert_exit_0(result)
    assert "module: bob.med.tb.configs.datasets" in result.output
    assert "module: bob.med.tb.configs.models" in result.output

def test_config_list_v():
    from ..scripts.config import list

    result = CliRunner().invoke(list, ["--verbose"])
    _assert_exit_0(result)
    assert "module: bob.med.tb.configs.datasets" in result.output
    assert "module: bob.med.tb.configs.models" in result.output

def test_config_describe_help():
    from ..scripts.config import describe

    _check_help(describe)

def test_config_describe_montgomery():
    from ..scripts.config import describe

    runner = CliRunner()
    result = runner.invoke(describe, ["montgomery"])
    _assert_exit_0(result)
    assert "Montgomery dataset for TB detection" in result.output

def test_dataset_help():
    from ..scripts.dataset import dataset

    _check_help(dataset)

def test_dataset_list_help():
    from ..scripts.dataset import list

    _check_help(list)

def test_dataset_list():
    from ..scripts.dataset import list

    runner = CliRunner()
    result = runner.invoke(list)
    _assert_exit_0(result)
    assert result.output.startswith("Supported datasets:")

def test_dataset_check_help():
    from ..scripts.dataset import check

    _check_help(check)

def test_dataset_check():
    from ..scripts.dataset import check

    runner = CliRunner()
    result = runner.invoke(check, ["--verbose", "--limit=2"])
    _assert_exit_0(result)

def test_main_help():
    from ..scripts.tb import tb

    _check_help(tb)

def test_train_help():
    from ..scripts.train import train

    _check_help(train)

def _str_counter(substr, s):
    return sum(1 for _ in re.finditer(substr, s, re.MULTILINE))

def test_predict_help():
    from ..scripts.predict import predict

    _check_help(predict)

def test_predtojson_help():
    from ..scripts.predtojson import predtojson

    _check_help(predtojson)

def test_aggregpred_help():
    from ..scripts.aggregpred import aggregpred

    _check_help(aggregpred)

def test_evaluate_help():
    from ..scripts.evaluate import evaluate

    _check_help(evaluate)

def test_compare_help():
    from ..scripts.compare import compare

    _check_help(compare)

def test_train_pasa_montgomery():

    # Temporarily modify Montgomery datadir
    new_value = {"bob.med.tb.montgomery.datadir": montgomery_datadir}
    with rc_context(**new_value):

        from ..scripts.train import train

        runner = CliRunner()

        with stdout_logging() as buf:

            output_folder = "results"
            result = runner.invoke(
                train,
                [
                    "pasa",
                    "montgomery",
                    "-vv",
                    "--epochs=1",
                    "--batch-size=1",
                    "--normalization=current",
                    f"--output-folder={output_folder}",
                ],
            )
            _assert_exit_0(result)

            assert os.path.exists(os.path.join(output_folder, "model_final.pth"))
            assert os.path.exists(
                os.path.join(output_folder, "model_lowest_valid_loss.pth")
            )
            assert os.path.exists(os.path.join(output_folder, "last_checkpoint"))
            assert os.path.exists(os.path.join(output_folder, "constants.csv"))
            assert os.path.exists(os.path.join(output_folder, "trainlog.csv"))
            assert os.path.exists(os.path.join(output_folder, "model_summary.txt"))

            keywords = {
                r"^Found \(dedicated\) '__train__' set for training$": 1,
                r"^Found \(dedicated\) '__valid__' set for validation$": 1,
                r"^Continuing from epoch 0$": 1,
                r"^Saving model summary at.*$": 1,
                r"^Model has.*$": 1,
                r"^Saving checkpoint": 2,
                r"^Total training time:": 1,
                r"^Z-normalization with mean": 1,
            }
            buf.seek(0)
            logging_output = buf.read()

            for k, v in keywords.items():
                assert _str_counter(k, logging_output) == v, (
                    f"Count for string '{k}' appeared "
                    f"({_str_counter(k, logging_output)}) "
                    f"instead of the expected {v}:\nOutput:\n{logging_output}"
                )

def test_predict_pasa_montgomery():

    # Temporarily modify Montgomery datadir
    new_value = {"bob.med.tb.montgomery.datadir": montgomery_datadir}
    with rc_context(**new_value):

        from ..scripts.predict import predict

        runner = CliRunner()

        with stdout_logging() as buf:

            output_folder = "predictions"
            result = runner.invoke(
                predict,
                [
                    "pasa",
                    "montgomery",
                    "-vv",
                    "--batch-size=1",
                    "--relevance-analysis",
                    f"--weight={_pasa_checkpoint_URL}",
                    f"--output-folder={output_folder}",
                ],
            )
            _assert_exit_0(result)

            # check predictions are there
            predictions_file1 = os.path.join(output_folder, "train/predictions.csv")
            predictions_file2 = os.path.join(output_folder, "validation/predictions.csv")
            predictions_file3 = os.path.join(output_folder, "test/predictions.csv")
            assert os.path.exists(predictions_file1)
            assert os.path.exists(predictions_file2)
            assert os.path.exists(predictions_file3)

            keywords = {
                r"^Loading checkpoint from.*$": 1,
                r"^Total time:.*$": 3,
                r"^Relevance analysis.*$": 3,
            }
            buf.seek(0)
            logging_output = buf.read()

            for k, v in keywords.items():
                assert _str_counter(k, logging_output) == v, (
                    f"Count for string '{k}' appeared "
                    f"({_str_counter(k, logging_output)}) "
                    f"instead of the expected {v}:\nOutput:\n{logging_output}"
                )

def test_predtojson():

    # Temporarily modify Montgomery datadir
    new_value = {"bob.med.tb.montgomery.datadir": montgomery_datadir}
    with rc_context(**new_value):

        from ..scripts.predtojson import predtojson

        runner = CliRunner()

        with stdout_logging() as buf:

            predictions = _data_file("test_predictions.csv")
            output_folder = "pred_to_json"
            result = runner.invoke(
                predtojson,
                [
                    "-vv",
                    "train",
                    f"{predictions}",
                    "test",
                    f"{predictions}",
                    f"--output-folder={output_folder}"
                ],
            )
            _assert_exit_0(result)

            # check json file is there
            assert os.path.exists(os.path.join(output_folder, "dataset.json"))

            keywords = {
                r"Output folder: pred_to_json": 1,
                r"Saving JSON file...": 1,
                r"^Loading predictions from.*$": 2,
            }
            buf.seek(0)
            logging_output = buf.read()

            for k, v in keywords.items():
                assert _str_counter(k, logging_output) == v, (
                    f"Count for string '{k}' appeared "
                    f"({_str_counter(k, logging_output)}) "
                    f"instead of the expected {v}:\nOutput:\n{logging_output}"
                )

def test_evaluate_pasa_montgomery():

    # Temporarily modify Montgomery datadir
    new_value = {"bob.med.tb.montgomery.datadir": montgomery_datadir}
    with rc_context(**new_value):

        from ..scripts.evaluate import evaluate

        runner = CliRunner()

        with stdout_logging() as buf:

            prediction_folder = "predictions"
            output_folder = "evaluations"
            result = runner.invoke(
                evaluate,
                [
                    "-vv",
                    "montgomery",
                    f"--predictions-folder={prediction_folder}",
                    f"--output-folder={output_folder}",
                    "--threshold=train",
                    "--steps=2000"
                ],
            )
            _assert_exit_0(result)

            # check evaluations are there
            assert os.path.exists(os.path.join(output_folder, "test.csv"))
            assert os.path.exists(os.path.join(output_folder, "train.csv"))
            assert os.path.exists(os.path.join(output_folder, "test_score_table.pdf"))
            assert os.path.exists(os.path.join(output_folder, "train_score_table.pdf"))

            keywords = {
                r"^Skipping dataset '__train__'": 1,
                r"^Evaluating threshold on.*$": 1,
                r"^Maximum F1-score of.*$": 4,
                r"^Set --f1_threshold=.*$": 1,
                r"^Set --eer_threshold=.*$": 1,
            }
            buf.seek(0)
            logging_output = buf.read()

            for k, v in keywords.items():
                assert _str_counter(k, logging_output) == v, (
                    f"Count for string '{k}' appeared "
                    f"({_str_counter(k, logging_output)}) "
                    f"instead of the expected {v}:\nOutput:\n{logging_output}"
                )

def test_compare_pasa_montgomery():

    # Temporarily modify Montgomery datadir
    new_value = {"bob.med.tb.montgomery.datadir": montgomery_datadir}
    with rc_context(**new_value):

        from ..scripts.compare import compare

        runner = CliRunner()

        with stdout_logging() as buf:

            predictions_folder = "predictions"
            output_folder = "comparisons"
            result = runner.invoke(
                compare,
                [
                    "-vv",
                    "train",
                    f"{predictions_folder}/train/predictions.csv",
                    "test",
                    f"{predictions_folder}/test/predictions.csv",
                    f"--output-figure={output_folder}/compare.pdf",
                    f"--output-table={output_folder}/table.txt",
                    "--threshold=0.5"
                ],
            )
            _assert_exit_0(result)

            # check comparisons are there
            assert os.path.exists(os.path.join(output_folder, "compare.pdf"))
            assert os.path.exists(os.path.join(output_folder, "table.txt"))

            keywords = {
                r"^Dataset '\*': threshold =.*$": 1,
                r"^Loading predictions from.*$": 2,
                r"^Tabulating performance summary...": 1,
            }
            buf.seek(0)
            logging_output = buf.read()

            for k, v in keywords.items():
                assert _str_counter(k, logging_output) == v, (
                    f"Count for string '{k}' appeared "
                    f"({_str_counter(k, logging_output)}) "
                    f"instead of the expected {v}:\nOutput:\n{logging_output}"
                )

def test_train_signstotb_montgomery_rs():

    from ..scripts.train import train

    runner = CliRunner()

    with stdout_logging() as buf:

        output_folder = "results"
        result = runner.invoke(
            train,
            [
                "signs_to_tb",
                "montgomery_rs",
                "-vv",
                "--epochs=1",
                "--batch-size=1",
                f"--weight={_signstotb_checkpoint_URL}",
                f"--output-folder={output_folder}",
            ],
        )
        _assert_exit_0(result)

        assert os.path.exists(os.path.join(output_folder, "model_final.pth"))
        assert os.path.exists(
            os.path.join(output_folder, "model_lowest_valid_loss.pth")
        )
        assert os.path.exists(os.path.join(output_folder, "last_checkpoint"))
        assert os.path.exists(os.path.join(output_folder, "constants.csv"))
        assert os.path.exists(os.path.join(output_folder, "trainlog.csv"))
        assert os.path.exists(os.path.join(output_folder, "model_summary.txt"))

        keywords = {
            r"^Found \(dedicated\) '__train__' set for training$": 1,
            r"^Found \(dedicated\) '__valid__' set for validation$": 1,
            r"^Continuing from epoch 0$": 1,
            r"^Saving model summary at.*$": 1,
            r"^Model has.*$": 1,
            r"^Saving checkpoint": 2,
            r"^Total training time:": 1,
        }
        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )

def test_predict_signstotb_montgomery_rs():

    from ..scripts.predict import predict

    runner = CliRunner()

    with stdout_logging() as buf:

        output_folder = "predictions"
        result = runner.invoke(
            predict,
            [
                "signs_to_tb",
                "montgomery_rs",
                "-vv",
                "--batch-size=1",
                "--relevance-analysis",
                f"--weight={_signstotb_checkpoint_URL}",
                f"--output-folder={output_folder}",
            ],
        )
        _assert_exit_0(result)

        # check predictions are there
        predictions_file = os.path.join(output_folder, "train/predictions.csv")
        RA1 = os.path.join(output_folder, "train_RA.pdf")
        RA2 = os.path.join(output_folder, "validation_RA.pdf")
        RA3 = os.path.join(output_folder, "test_RA.pdf")
        assert os.path.exists(predictions_file)
        assert os.path.exists(RA1)
        assert os.path.exists(RA2)
        assert os.path.exists(RA3)

        keywords = {
            r"^Loading checkpoint from.*$": 1,
            r"^Total time:.*$": 3*15,
            r"^Starting relevance analysis for subset.*$": 3,
            r"^Creating and saving plot at.*$": 3,
        }
        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )

def test_train_logreg_montgomery_rs():

    from ..scripts.train import train

    runner = CliRunner()

    with stdout_logging() as buf:

        output_folder = "results"
        result = runner.invoke(
            train,
            [
                "logistic_regression",
                "montgomery_rs",
                "-vv",
                "--epochs=1",
                "--batch-size=1",
                f"--weight={_logreg_checkpoint_URL}",
                f"--output-folder={output_folder}",
            ],
        )
        _assert_exit_0(result)

        assert os.path.exists(os.path.join(output_folder, "model_final.pth"))
        assert os.path.exists(
            os.path.join(output_folder, "model_lowest_valid_loss.pth")
        )
        assert os.path.exists(os.path.join(output_folder, "last_checkpoint"))
        assert os.path.exists(os.path.join(output_folder, "constants.csv"))
        assert os.path.exists(os.path.join(output_folder, "trainlog.csv"))
        assert os.path.exists(os.path.join(output_folder, "model_summary.txt"))

        keywords = {
            r"^Found \(dedicated\) '__train__' set for training$": 1,
            r"^Found \(dedicated\) '__valid__' set for validation$": 1,
            r"^Continuing from epoch 0$": 1,
            r"^Saving model summary at.*$": 1,
            r"^Model has.*$": 1,
            r"^Saving checkpoint": 2,
            r"^Total training time:": 1,
        }
        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )

def test_predict_logreg_montgomery_rs():

    from ..scripts.predict import predict

    runner = CliRunner()

    with stdout_logging() as buf:

        output_folder = "predictions"
        result = runner.invoke(
            predict,
            [
                "logistic_regression",
                "montgomery_rs",
                "-vv",
                "--batch-size=1",
                f"--weight={_logreg_checkpoint_URL}",
                f"--output-folder={output_folder}",
            ],
        )
        _assert_exit_0(result)

        # check predictions are there
        predictions_file = os.path.join(output_folder, "train/predictions.csv")
        wfile = os.path.join(output_folder, "LogReg_Weights.pdf")
        assert os.path.exists(predictions_file)
        assert os.path.exists(wfile)

        keywords = {
            r"^Loading checkpoint from.*$": 1,
            r"^Total time:.*$": 3,
            r"^Logistic regression identified: saving model weights.*$": 1,
        }
        buf.seek(0)
        logging_output = buf.read()

        for k, v in keywords.items():
            assert _str_counter(k, logging_output) == v, (
                f"Count for string '{k}' appeared "
                f"({_str_counter(k, logging_output)}) "
                f"instead of the expected {v}:\nOutput:\n{logging_output}"
            )

def test_aggregpred():

    # Temporarily modify Montgomery datadir
    new_value = {"bob.med.tb.montgomery.datadir": montgomery_datadir}
    with rc_context(**new_value):

        from ..scripts.aggregpred import aggregpred

        runner = CliRunner()

        with stdout_logging() as buf:

            predictions = "predictions/train/predictions.csv"
            output_folder = "aggregpred"
            result = runner.invoke(
                aggregpred,
                [
                    "-vv",
                    f"{predictions}",
                    f"{predictions}",
                    f"--output-folder={output_folder}"
                ],
            )
            _assert_exit_0(result)

            # check csv file is there
            assert os.path.exists(os.path.join(output_folder, "aggregpred.csv"))

            keywords = {
                r"Output folder: aggregpred": 1,
                r"Saving aggregated CSV file...": 1,
                r"^Loading predictions from.*$": 2,
            }
            buf.seek(0)
            logging_output = buf.read()

            for k, v in keywords.items():
                assert _str_counter(k, logging_output) == v, (
                    f"Count for string '{k}' appeared "
                    f"({_str_counter(k, logging_output)}) "
                    f"instead of the expected {v}:\nOutput:\n{logging_output}"
                )

# Not enough RAM available to do this test
# def test_predict_densenetrs_montgomery():

#     # Temporarily modify Montgomery datadir
#     new_value = {"bob.med.tb.montgomery.datadir": montgomery_datadir}
#     with rc_context(**new_value):

#         from ..scripts.predict import predict

#         runner = CliRunner()

#         with stdout_logging() as buf:

#             output_folder = "predictions"
#             result = runner.invoke(
#                 predict,
#                 [
#                     "densenet_rs",
#                     "montgomery_f0_rgb",
#                     "-vv",
#                     "--batch-size=1",
#                     f"--weight={_densenetrs_checkpoint_URL}",
#                     f"--output-folder={output_folder}",
#                     "--grad-cams"
#                 ],
#             )
#             _assert_exit_0(result)

#             # check predictions are there
#             predictions_file1 = os.path.join(output_folder, "train/predictions.csv")
#             predictions_file2 = os.path.join(output_folder, "validation/predictions.csv")
#             predictions_file3 = os.path.join(output_folder, "test/predictions.csv")
#             assert os.path.exists(predictions_file1)
#             assert os.path.exists(predictions_file2)
#             assert os.path.exists(predictions_file3)
#             # check some grad cams are there
#             cam1 = os.path.join(output_folder, "train/cams/MCUCXR_0002_0_cam.png")
#             cam2 = os.path.join(output_folder, "train/cams/MCUCXR_0126_1_cam.png")
#             cam3 = os.path.join(output_folder, "train/cams/MCUCXR_0275_1_cam.png")
#             cam4 = os.path.join(output_folder, "validation/cams/MCUCXR_0399_1_cam.png")
#             cam5 = os.path.join(output_folder, "validation/cams/MCUCXR_0113_1_cam.png")
#             cam6 = os.path.join(output_folder, "validation/cams/MCUCXR_0013_0_cam.png")
#             cam7 = os.path.join(output_folder, "test/cams/MCUCXR_0027_0_cam.png")
#             cam8 = os.path.join(output_folder, "test/cams/MCUCXR_0094_0_cam.png")
#             cam9 = os.path.join(output_folder, "test/cams/MCUCXR_0375_1_cam.png")
#             assert os.path.exists(cam1)
#             assert os.path.exists(cam2)
#             assert os.path.exists(cam3)
#             assert os.path.exists(cam4)
#             assert os.path.exists(cam5)
#             assert os.path.exists(cam6)
#             assert os.path.exists(cam7)
#             assert os.path.exists(cam8)
#             assert os.path.exists(cam9)

#             keywords = {
#                 r"^Loading checkpoint from.*$": 1,
#                 r"^Total time:.*$": 3,
#                 r"^Grad cams folder:.*$": 3,
#             }
#             buf.seek(0)
#             logging_output = buf.read()

#             for k, v in keywords.items():
#                 assert _str_counter(k, logging_output) == v, (
#                     f"Count for string '{k}' appeared "
#                     f"({_str_counter(k, logging_output)}) "
#                     f"instead of the expected {v}:\nOutput:\n{logging_output}"
#                 )