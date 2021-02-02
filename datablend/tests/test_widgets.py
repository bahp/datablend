# Libraries
import pytest
import pandas as pd

# DataBlend libraries
from datablend.core.blend.template import BlenderTemplate
from datablend.core.widgets.base import BaseWidget
from datablend.core.widgets.format import RenameWidget
from datablend.core.widgets.format import ReplaceWidget
from datablend.core.widgets.format import DateTimeMergeWidget
from datablend.core.exceptions import WrongColumnType
from datablend.core.exceptions import MissingRequiredColumns
from datablend.core.exceptions import IncompatibleBlenderTemplateError
from datablend.core.exceptions import ReplaceWidgetMapWarning

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
# Widget tests
# ----------------------------
# Basic tests
# -----------
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


# ReplaceWidget tests
# -------------------
def test_widget_replace_raises_exception_on_missing_required_columns(bt_df):
    """"""
    bt_df = bt_df.drop(columns='to_replace')
    bt = BlenderTemplate().fit(bt_df)
    with pytest.raises(MissingRequiredColumns):
        ReplaceWidget().fit(bt)


def test_widget_replace_raises_warning(bt_df, data):
    """"""
    bt_df.at[3, 'to_replace'] = {'Male': 1}
    with pytest.warns(ReplaceWidgetMapWarning):
        ReplaceWidget().fit_transform(bt_df, data)


def test_widget_replace_from_dict(bt, data):
    """ReplaceWidget fit from dictionary"""
    transformed = ReplaceWidget().fit_transform(bt, data)
    unique = set(transformed.Sex.unique())
    assert unique.issubset(set(['Male', 'Female']))


def test_widget_replace_from_str(bt, data):
    """ReplaceWidget fit from str dictionary."""
    assert True


# EventWidget tests
# -----------------
def test_widget_event_raises_exception_on_missing_required_columns(bt_df):
    """"""
    assert True


# DateTimeMergeWidget tests
# -------------------------
def test_widget_dtmerge_raises_exception_on_missing_required_columns(bt_df):
    """"""
    assert True


# DateFromStudyDay tests
# ----------------------
def test_widget_dtfromstudyday_raises_exception_on_missing_required_columns(bt_df):
    """"""
    assert True


def test_widget_dtmerge(bt, data):
    """"""
    assert True


def test_widget_events(bt, data):
    """"""
    assert True


def test_widget_studyday(bt, data):
    """"""
    assert True


def test_widget_stack(bt, data):
    """"""
