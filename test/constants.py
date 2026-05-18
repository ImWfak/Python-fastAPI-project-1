NONEXISTENT_ID = -1

PYDANTIC_BASE_URL = r"https://errors\.pydantic\.dev/2\.12\/v"

STRING_TYPE_PATTERN = (
        r"Input should be a valid string "
        r"\[type=string_type, input_value=.+, input_type=int\]\n"
        r"\s+For further information visit " + PYDANTIC_BASE_URL + r"\/string_type"
)
DECIMAL_TYPE_PATTERN = (
        r"Input should be a valid decimal "
        r"\[type=decimal_parsing, input_value='', input_type=str\]\n"
        r"\s+For further information visit " + PYDANTIC_BASE_URL + r"\/decimal_parsing"
)
ENUM_TYPE_PATTERN = (
        r"Input should be 'HIGH', 'MIDDLE' or 'LOW' "
        r"\[type=enum, input_value='', input_type=str]\n"
        r"\s+For further information visit " + PYDANTIC_BASE_URL + r"\/enum"
)