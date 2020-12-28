# Libraries
import pytest
import pandas as pd

# DataBlend libraries
from datablend.core.blend import BlenderTemplate
from datablend.core.widgets import BaseWidget
from datablend.core.widgets import RenameWidget
from datablend.core.exceptions import WrongColumnType
from datablend.core.exceptions import MissingRequiredColumns
from datablend.core.exceptions import IncompatibleBlenderTemplateError


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
        {'from_name': 'Sex', 'to_name': 'gender'}
    ]
    # Return
    return template


@pytest.fixture
def bt_df(bt_json):
    return pd.DataFrame(bt_json)


@pytest.fixture
def blender_template(bt_df):
    return BlenderTemplate().fit(bt_df)

# ----------------------------
# RenameWidget tests
# ----------------------------
"""
    .. note: bt refers to blender_template
    .. note: df refers to dataframe
"""


# ----------------------------
# BlenderTemplate tests
# ----------------------------
def test_bt_raises_exception_on_None():
    """Widget none template."""
    with pytest.raises(TypeError):
        BlenderTemplate().fit(None)


def test_bt_from_df(bt_df):
    """Widget none template."""
    bt = BlenderTemplate().fit(bt_df)
    assert isinstance(bt, BlenderTemplate)


def test_bt_from_json(bt_json):
    """"""
    bt = BlenderTemplate().fit(bt_json)
    assert isinstance(bt, BlenderTemplate)


# ----------------------------
# RenameWidget tests
# ----------------------------
def test_widget_raises_exception_on_None():
    """"""
    with pytest.raises(TypeError):
        RenameWidget().fit(None)


def test_widget_fit_from_df(bt_df):
    """"""
    widget = RenameWidget().fit(bt_df)
    assert isinstance(widget, BaseWidget)


def test_widget_fit_from_json(bt_json):
    """"""
    widget = RenameWidget().fit(bt_json)
    assert isinstance(widget, BaseWidget)


def test_widget_raises_exception_on_missing_required_columns(bt_df):
    """"""
    bt_df = bt_df.drop(columns='to_name')
    bt = BlenderTemplate().fit(bt_df)
    with pytest.raises(MissingRequiredColumns):
        RenameWidget().fit(bt)