'''
1D Multichannel Streamdata Data
'''
import os
import errno
import math
import numpy as np


MAX_SIZE = 2**16
MAX_DATA_WIDTH = 32
DEFAULT_DATA_WIDTH = 16
MAX_CHANNELS = 256


class StreamData():
    '''
    classdocs
    '''

    # Define valid ranges for the several StreamData parameters
    PARAMS_RANGE = {
        "size":       (1, 2**32),
        "data_width": (1, MAX_DATA_WIDTH),
        "channels":   (1, MAX_CHANNELS)
    }

    def __init__(self, params=None):
        '''
        Constructor
        '''
        self.params = {
            "size":       1024,
            "data_width": DEFAULT_DATA_WIDTH,
            "channels":   1
        }
        self.stream_data = None
        self.set_params(params)

    def __getitem__(self, key):
        return self.get_stream_data()[key]

    def __setitem__(self, key, value):
        self.get_stream_data()[key] = value

    def __eq__(self, other):

        objs = (
            {"obj": self, "data": None, "stream": False},
            {"obj": other, "data": None, "stream": False}
        )

        for obj in objs:

            if isinstance(obj["obj"], StreamData):
                obj["data"] = obj["obj"].get_stream_data()
                obj["stream"] = True
            elif isinstance(obj["obj"], np.ndarray):
                obj["data"] = obj["obj"]
            else:
                return NotImplemented

        if not np.array_equal(objs[0]["data"], objs[1]["data"]):
            return False

        if (objs[0]["stream"] and objs[1]["stream"]) is True:
            if self.params != other.params:
                return False

        return True

    def get_np_shape(self):
        return (
            self.params['size'],
            self.params['channels']
        )

    def get_stream_data(self):
        return self.stream_data

    def check_params(self, params, use_assertions=False):

        params_keys = params.keys()
        range_keys = self.PARAMS_RANGE.keys()

        keys_are_equal = set(params_keys) == set(range_keys)

        if use_assertions:
            assert keys_are_equal, \
                "Parameter keys are invalid!\n" + \
                str(params_keys) + "\n" + str(range_keys)

        if not keys_are_equal:
            return False

        if use_assertions:
            for key, value in params.items():
                assert self.PARAMS_RANGE[key][0] <= value <= self.PARAMS_RANGE[key][1], \
                    'Parameter "' + key + '" is out of range!'

        for key, value in params.items():
            if not self.PARAMS_RANGE[key][0] <= value <= self.PARAMS_RANGE[key][1]:
                return False

        return True

    def set_params(self, params):

        if params is None:
            self.params = None
        elif self.check_params(params, True):
            self.params = params

    @classmethod
    def extract_params(cls, data, use_data_width=None):

        assert len(data.shape) in range(1, 3), \
            "Data has unsupported array dimensions! " + str(data.shape)

        max_value = np.amax(data)
        data_width = DEFAULT_DATA_WIDTH
        if use_data_width is None:
            data_width = DEFAULT_DATA_WIDTH
        elif use_data_width == "Real":
            if max_value == 0:
                max_value = 2**DEFAULT_DATA_WIDTH-1
            data_width = math.ceil(math.log2(max_value))
        else:
            data_width = use_data_width

        assert cls.PARAMS_RANGE["data_width"][0] <= data_width \
            <= cls.PARAMS_RANGE["data_width"][1], "Given data_width is out of allowed range!"

        assert max_value < 2**data_width, \
            "Given data_width missmatches the maximum stream_data value"

        num_channels = 1

        if len(data.shape) == 1:
            num_channels = 1
        else:

            assert cls.PARAMS_RANGE["channels"][0] <= data.shape[1] \
                <= cls.PARAMS_RANGE["channels"][1], "Data has unsupported array dimensions!"

            num_channels = data.shape[1]

        return {
            "size":       data.shape[0],
            "data_width": data_width,
            "channels":   num_channels
        }

    def check_data(self, data, use_data_width=None):

        assert data.dtype == np.int32, \
            "Data is not np.int32"

        extracted_params = self.extract_params(data, use_data_width)

        if extracted_params != self.params:
            print("*************************************************")
            print("Data Check Error")
            print("*************************************************")
            print("- Extracted Parameters:")
            print(extracted_params)
            print("- Set Parameters:")
            print(self.params)
            print("*************************************************")
            return False

        return True

    def init_with_data(self, data, extract_params=True, use_data_width=None):

        if extract_params:
            self.params = self.extract_params(data, use_data_width)
        else:
            assert self.check_data(data, use_data_width), \
                "Check Data failed!"

        assert self.params is not None, \
            "Stream parameters needs to be set first!"

        self.stream_data = data.reshape((self.params['size'], self.params['channels']))

    def init_with_random(self, seed=None, lower_limit=None, upper_limit=None):

        default_lower_limit = -2**(self.params['data_width']-1)
        default_upper_limit = 2**(self.params['data_width']-1)-1

        assert self.params is not None, \
            "Stream parameters needs to be set first!"

        if lower_limit is None:
            lower_limit = default_lower_limit

        if upper_limit is None:
            upper_limit = default_upper_limit

        assert lower_limit >= default_lower_limit, \
            "Lower limit out of data width"

        assert lower_limit <= default_upper_limit, \
            "Lower limit out of data width"

        if seed is not None:
            np.random.seed(seed)

        dim = self.get_np_shape()

        rnd_data = ((upper_limit-lower_limit)*np.random.rand(*dim) + lower_limit).astype(np.int32)

        self.init_with_data(rnd_data, False, self.params['data_width'])

    def save(self, path, allow_overwrite=False):
        '''
        Stores stream data (numpy array) as text file.

        Parameters:
        path (str): Path of txt file
        allow_overwrite (bool): When true and path already exists, file will
                                be overwritten.
        '''

        if not allow_overwrite and os.path.isfile(path):
            raise FileExistsError(
                errno.EEXIST, os.strerror(errno.EEXIST), path)

        # Prepare Header
        header = "{}\n{}\n{}\n".format(
            self.params["size"], self.params["data_width"], self.params["channels"]
        )

        max_value = 2**self.params['data_width'] - 1
        ascii_size = math.floor(math.log(max_value, 10)) + 1

        with open(path, "w") as txt_file:
            txt_file.write(header)

            # Write Stream Data
            for i in range(self.params['size']):
                line = ""
                for channel in range(self.params['channels']):
                    data_str = str(self.stream_data[i, channel])
                    line += data_str.rjust(ascii_size, " ") + " "
                txt_file.write(line + "\n")
            txt_file.close()

    def load(self, path):
        '''
        Loads stream data (numpy array) from text file.

        Parameters:
        path (str): Path of txt file
        '''

        if not os.path.isfile(path):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), path)

        with open(path, "r") as txt_file:

            states = [
                "HEADER_SIZE",
                "HEADER_DATA_WIDTH",
                "HEADER_CHANNELS",
                "DATA"
            ]

            stream_params = {"size": 0, "data_width": 8, "channels": 3}
            stream_data = None
            data_coord = [0, 0, 0]
            num_values = 0
            i = 0

            for raw_line in txt_file:

                line = raw_line.strip()

                # skip line if empty
                if line == "":
                    continue

                if states[0] == "HEADER_SIZE":
                    stream_params["size"] = int(line)
                    states.remove("HEADER_SIZE")
                elif states[0] == "HEADER_DATA_WIDTH":
                    stream_params["data_width"] = int(line)
                    states.remove("HEADER_DATA_WIDTH")
                elif states[0] == "HEADER_CHANNELS":
                    stream_params["channels"] = int(line)
                    stream_data = np.zeros(
                        (stream_params["size"], stream_params["channels"]), np.int32)
                    num_values = stream_params["size"] * stream_params["channels"]
                    states.remove("HEADER_CHANNELS")
                else:
                    data = [int(str_data) for str_data in line.split()]
                    for value in data:

                        i += 1

                        # pylint: disable=E1137
                        stream_data[
                            data_coord[0],
                            data_coord[1]
                        ] = value

                        data_coord[1] += 1
                        if data_coord[1] == stream_params["channels"]:
                            data_coord[1] = 0
                            data_coord[0] += 1

            txt_file.close()

        assert i == num_values, \
            "Read Error: Number of pixel does not match header"

        self.set_params(stream_params)
        self.init_with_data(
            stream_data[::, 0:stream_params["channels"]],
            False,
            stream_params["data_width"]
        )


def compare_stream(stream_a, stream_b):

    result = {
        "num_errors": 0,
        "first_error": None
    }

    if stream_a.params != stream_b.params:
        result['num_errors'] = -1
        return result

    num_errors = 0

    for i in range(stream_a.params['size']):
        for channel in range(0, stream_a.params['channels']):

            a_value = stream_a.get_stream_data()[i, channel]
            b_value = stream_b.get_stream_data()[i, channel]

            if a_value != b_value:
                num_errors += 1

                if result['first_error'] is None:
                    result['first_error'] = (i, channel)

    result['num_errors'] = num_errors
    return result


def assert_stream_equal(stream_a, stream_b, msg=""):

    result = compare_stream(stream_a, stream_b)

    if result["num_errors"] < 0:
        total_msg = "Image Parameter Missmatch!\n"
        total_msg += msg
        assert result["num_errors"] == 0, total_msg
    elif result["num_errors"] > 0:
        total_msg = "Image Data Missmatch!\n"
        total_msg += msg
        assert result["num_errors"] == 0, total_msg
