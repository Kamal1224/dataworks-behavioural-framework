import os
from behave import fixture
from helpers import (
    aws_helper,
    console_printer,
)


@fixture
def clean_up_role_and_s3_objects(context, timeout=30, **kwargs):
    console_printer.print_info("Executing 'clean_up_role_and_s3_objects' fixture")

    aws_helper.remove_role(
        context.analytical_test_e2e_role, context.analytical_test_e2e_policies
    )

    aws_helper.clear_session()
    aws_helper.set_details_for_role_assumption(
        context.aws_role, context.aws_session_timeout_seconds
    )

    if context.analytical_test_data_s3_location.get("path"):
        aws_helper.remove_file_from_s3_and_wait_for_consistency(
            context.published_bucket,
            os.path.join(
                context.analytical_test_data_s3_location["path"],
                context.analytical_test_data_s3_location["file_name"],
            ),
        )

    if context.analytical_test_data_s3_location.get("paths"):
        for path in context.analytical_test_data_s3_location["paths"]:
            aws_helper.remove_file_from_s3_and_wait_for_consistency(
                context.published_bucket,
                os.path.join(
                    path, context.analytical_test_data_s3_location["file_name"]
                ),
            )


@fixture
def terminate_adg_cluster(context, timeout=30, **kwargs):
    console_printer.print_info("Executing 'terminate_adg_cluster' fixture")

    if "adg_cluster_id" in context and context.adg_cluster_id is not None:
        aws_helper.terminate_emr_cluster(context.adg_cluster_id)
    else:
        console_printer.print_info(
            f"No cluster id found for ADG so not terminating any cluster"
        )


@fixture
def terminate_pdm_cluster(context, timeout=30, **kwargs):
    console_printer.print_info("Executing 'terminate_pdm_cluster' fixture")

    if "pdm_cluster_id" in context and context.pdm_cluster_id is not None:
        aws_helper.terminate_emr_cluster(context.pdm_cluster_id)
    else:
        console_printer.print_info(
            f"No cluster id found for PDM so not terminating any cluster"
        )