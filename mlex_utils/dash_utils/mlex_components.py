from mlex_utils.dash_utils.dbc_utils.job_manager import DbcJobManagerAIO
from mlex_utils.dash_utils.dbc_utils.parameter_items import DbcParameterItems
from mlex_utils.dash_utils.dmc_utils.job_manager import DmcJobManagerAIO
from mlex_utils.dash_utils.dmc_utils.parameter_items import DmcParameterItems


class MLExComponents:
    def __init__(self, ui_style):
        if ui_style != "dbc" and ui_style != "dmc":
            raise ValueError(f"ui_style must be one of ['dbc', 'dmc'], got {ui_style}")
        self.ui_style = ui_style

    def get_job_manager(self, **kwargs):
        if self.ui_style == "dbc":
            job_manager = DbcJobManagerAIO(**kwargs)
        else:
            job_manager = DmcJobManagerAIO(**kwargs)
        return job_manager

    def get_parameter_items(self, **kwargs):
        if self.ui_style == "dbc":
            parameter_items = DbcParameterItems(**kwargs)
        else:
            parameter_items = DmcParameterItems(**kwargs)
        return parameter_items
