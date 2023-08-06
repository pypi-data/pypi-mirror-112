# PlantCV classes
import os
import json
from LivestockCV.core import fatal_error


class Params:
    def __init__(self, device=0, debug=None, debug_outdir=".", line_thickness=5, dpi=100, text_size=0.55,
                 text_thickness=2, marker_size=60, color_scale="gist_rainbow", color_sequence="sequential",
                 saved_color_scale=None, verbose=True):

        self.device = device
        self.debug = debug
        self.debug_outdir = debug_outdir
        self.line_thickness = line_thickness
        self.dpi = dpi
        self.text_size = text_size
        self.text_thickness = text_thickness
        self.marker_size = marker_size
        self.color_scale = color_scale
        self.color_sequence = color_sequence
        self.saved_color_scale = saved_color_scale
        self.verbose = verbose


class Outputs:


    def __init__(self):
        self.measurements = {}
        self.images = []
        self.observations = {}

        # Add a method to clear measurements
    def clear(self):
        self.measurements = {}
        self.images = []
        self.observations = {}

    # Method to add observation to outputs
    def add_observation(self, sample, variable, trait, method, scale, datatype, value, label):


        # Create an empty dictionary for the sample if it does not exist
        if sample not in self.observations:
            self.observations[sample] = {}

        # Supported data types
        supported_dtype = ["int", "float", "str", "list", "bool", "tuple", "dict", "NoneType", "numpy.float64"]
        # Supported class types
        class_list = [f"<class '{cls}'>" for cls in supported_dtype]

        # Send an error message if datatype is not supported by json
        if str(type(value)) not in class_list:
            # String list of supported types
            type_list = ', '.join(map(str, supported_dtype))
            fatal_error(f"The Data type {type(value)} is not compatible with JSON! Please use only these: {type_list}!")

        # Save the observation for the sample and variable
        self.observations[sample][variable] = {
            "trait": trait,
            "method": method,
            "scale": scale,
            "datatype": str(datatype),
            "value": value,
            "label": label
        }

    # Method to save observations to a file
    def save_results(self, filename, outformat="json"):

        if outformat.upper() == "JSON":
            if os.path.isfile(filename):
                with open(filename, 'r') as f:
                    hierarchical_data = json.load(f)
                    hierarchical_data["observations"] = self.observations
            else:
                hierarchical_data = {"metadata": {}, "observations": self.observations}

            with open(filename, mode='w') as f:
                json.dump(hierarchical_data, f)
        elif outformat.upper() == "CSV":
            # Open output CSV file
            csv_table = open(filename, "w")
            # Write the header
            csv_table.write(",".join(map(str, ["sample", "trait", "value", "label"])) + "\n")
            # Iterate over data samples
            for sample in self.observations:
                # Iterate over traits for each sample
                for var in self.observations[sample]:
                    val = self.observations[sample][var]["value"]
                    # If the data type is a list or tuple we need to unpack the data
                    if isinstance(val, list) or isinstance(val, tuple):
                        # Combine each value with its label
                        for value, label in zip(self.observations[sample][var]["value"],
                                                self.observations[sample][var]["label"]):
                            # Skip list of tuple data types
                            if not isinstance(value, tuple):
                                # Save one row per value-label
                                row = [sample, var, value, label]
                                csv_table.write(",".join(map(str, row)) + "\n")
                    # If the data type is Boolean, store as a numeric 1/0 instead of True/False
                    elif isinstance(val, bool):
                        row = [sample,
                               var,
                               int(self.observations[sample][var]["value"]),
                               self.observations[sample][var]["label"]]
                        csv_table.write(",".join(map(str, row)) + "\n")
                    # For all other supported data types, save one row per trait
                    # Assumes no unusual data types are present (possibly a bad assumption)
                    else:
                        row = [sample,
                               var,
                               self.observations[sample][var]["value"],
                               self.observations[sample][var]["label"]
                               ]
                        csv_table.write(",".join(map(str, row)) + "\n")


