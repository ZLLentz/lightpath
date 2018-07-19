from unittest.mock import Mock
from distutils.spawn import find_executable

from lightpath.ui import LightApp
from lightpath.controller import LightController


def test_app_buttons(lcls_client):
    lightapp = LightApp(LightController(lcls_client))
    # Check we initialized correctly
    assert lightapp.upstream()
    # Create widgets
    assert len(lightapp.select_devices('MEC')) == 10
    # Setup new display
    mec_idx = lightapp.destination_combo.findText('MEC')
    lightapp.destination_combo.setCurrentIndex(mec_idx)
    lightapp.change_path_display()
    assert len(lightapp.rows) == 10


def test_lightpath_launch_script():
    # Check that the executable was installed
    assert find_executable('lightpath')


def test_focus_on_device(lcls_client, monkeypatch):
    lightapp = LightApp(LightController(lcls_client))
    row = lightapp.rows[8]
    monkeypatch.setattr(row, 'setFocus', Mock())
    # Grab the focus
    lightapp.focus_on_device(row.device.name)
    assert row.setFocus.called
    # Smoke test a bad device string
    lightapp.focus_on_device('blah')
