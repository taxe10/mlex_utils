def get_job_manager_aio(ui_style="dbc"):
    if ui_style == "dbc":
        from mlex_utils.dash_utils.dbc_utils.job_manager import JobManagerAIO

        return JobManagerAIO()
    elif ui_style == "dmc":
        from mlex_utils.dash_utils.dmc_utils.job_manager import JobManagerAIO

        return JobManagerAIO()
    else:
        raise ValueError(f"ui_style must be one of ['dbc', 'dmc'], got {ui_style}")
