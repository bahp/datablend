# Libraries
import pytest
import pathlib
import runpy

"""
.. note: Executing the oucru examples might fail when using github 
         actions because they load data from .csv/.xls(x) files that 
         might not have been pushed to github. In addition, it 
         writes .xls(x) files.
"""

# Find the examples folder
examples = pathlib.Path(__file__, '../../../', 'examples').resolve()

# Find all the scripts
scripts_widgets = (examples / 'widgets').glob('**/*.py')
scripts_template = (examples / 'template').glob('**/*.py')
scripts_blender = (examples / 'blender').glob('**/*.py')


# scripts_oucru06dx = (examples / 'oucru/oucru-06dx').glob('**/*.py')

@pytest.mark.parametrize('script', scripts_widgets)
def test_script_execution_widgets(script):
    runpy.run_path(str(script))


@pytest.mark.parametrize('script', scripts_widgets)
def test_script_execution_template(script):
    runpy.run_path(str(script))


@pytest.mark.parametrize('script', scripts_widgets)
def test_script_execution_blender(script):
    runpy.run_path(str(script))

# @pytest.mark.parametrize('script', scripts_oucru06dx)
# def test_script_execution_blender(script):
#    runpy.run_path(str(script))
