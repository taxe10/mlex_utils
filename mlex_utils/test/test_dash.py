from mlex_utils.dash_utils.job_manager import get_job_manager_aio


def test_get_job_manager():
    job_manager = get_job_manager_aio("dmc")
    assert job_manager is not None

    job_manager = get_job_manager_aio("dbc")
    assert job_manager is not None


def test_advanced_options_dmc():
    from mlex_utils.dash_utils.dmc_utils.job_manager import JobManagerAIO

    job_manager = JobManagerAIO()

    assert job_manager.toggle_modal(1, 0, False)
    assert not job_manager.toggle_modal(0, 1, True)


def test_advanced_options_dbc():
    from mlex_utils.dash_utils.dbc_utils.job_manager import JobManagerAIO

    job_manager = JobManagerAIO()

    assert job_manager.toggle_modal(1, 0, False)
    assert not job_manager.toggle_modal(0, 1, True)
