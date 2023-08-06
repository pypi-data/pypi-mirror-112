import pandas as pd
from climetlab import Source
import intake


class Intake(Source):
    def __init__(self):
        pass

    def load_data(self, data):
        if data.endswith('.csv'):
            return intake.open_csv(data)
        if data.endswith('.nc'):
            return intake.open_netcdf(data)
        if data.endswith('.zarr'):
            return intake.open_zarr(data)
        if data.endswith('.grib') or data.endswith('.grb'):
            return intake.open_grib(data)

        raise ValueError(f"Unsupported {data} type.")


source = Intake()