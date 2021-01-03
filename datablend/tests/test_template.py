# Libraries
import pytest
import pandas as pd

# DataBlend libraries
from datablend.core.blend import BlenderTemplate
from datablend.core.exceptions import BTNullValueError
from datablend.core.exceptions import BTDuplicateError
from datablend.core.exceptions import BTMissingRequiredColumnsError

"""
.. note: bt is the acronym for BlenderTemplate
         df is the acronym for DataFrame
"""

@pytest.fixture
def data():
    """Returns a basic data DataFrame."""
    data = [
        {'StudyNo': '32dx-001', 'Temp': 37.2, 'Shock': False, 'Sex': 1},
        {'StudyNo': '32dx-002', 'Temp': 36.5, 'Shock': False, 'Sex': 1},
        {'StudyNo': '32dx-003', 'Temp': 39.8, 'Shock': True, 'Sex': 2},
        {'StudyNo': '32dx-004', 'Temp': 37.4, 'Shock': False, 'Sex': 1}
    ]
    # Return
    return pd.DataFrame(data)


@pytest.fixture
def bt_json():
    # Template
    template = [
        # Example rename widget
        {'from_name': 'StudyNo', 'to_name': 'study_number'},
        {'from_name': 'Temp', 'to_name': 'body_temperature'},
        {'from_name': 'Shock', 'to_name': 'shock'},
        {'from_name': 'Sex', 'to_name': 'gender',
         'to_replace': {'Male': 1, 'Female': 2}}
    ]
    # Return
    return template


@pytest.fixture
def bt_df(bt_json):
    return pd.DataFrame(bt_json)


@pytest.fixture
def bt(bt_df):
    return BlenderTemplate().fit(bt_df)


# ----------------------------
# BlenderTemplate tests
# ----------------------------
def test_bt_fit_raises_exception_on_None():
    """BlenderTemplate error: None template."""
    with pytest.raises(TypeError):
        BlenderTemplate().fit(None)


def test_bt_fit_raises_exception_missing_required_column_error_from_name(bt_df):
    """BlenderTemplate error: The required column 'from_name' is missing."""
    bt_df = bt_df.drop(columns='from_name')
    with pytest.raises(BTMissingRequiredColumnsError):
        BlenderTemplate().fit(bt_df)


def test_bt_fit_raises_exception_missing_required_column_error_to_name(bt_df):
    """BlenderTemplate error: The required column 'to_name' is missing."""
    bt_df = bt_df.drop(columns='to_name')
    with pytest.raises(BTMissingRequiredColumnsError):
        BlenderTemplate().fit(bt_df)


def test_bt_fit_raises_exception_null_value_error(bt_df):
    """BlenderTemplate error: The column has null values."""
    # Remove the last to_name value
    bt_df.iloc[-1, bt_df.columns.get_loc('to_name')] = None
    with pytest.raises(BTNullValueError):
        BlenderTemplate().fit(bt_df)


def test_bt_fit_raises_exception_duplicate_error(bt_df):
    """BlenderTemplate error: The column has duplicated values."""
    # Set equal first and last from_name values
    first = bt_df.iloc[0, bt_df.columns.get_loc('from_name')]
    bt_df.iloc[-1, bt_df.columns.get_loc('from_name')] = first
    with pytest.raises(BTDuplicateError):
        BlenderTemplate().fit(bt_df)


def test_bt_fit_from_df(bt_df):
    """BlenderTemplate fit from dataframe."""
    bt = BlenderTemplate().fit(bt_df)
    assert isinstance(bt, BlenderTemplate)


def test_bt_fit_from_json(bt_json):
    """BlenderTemplate fit from json."""
    bt = BlenderTemplate().fit(bt_json)
    assert isinstance(bt, BlenderTemplate)


def test_bt_fit_from_data(data):
    """BlenderTemplate fit from data."""
    bt = BlenderTemplate().fit_from_data(data)
    assert isinstance(bt, BlenderTemplate)
