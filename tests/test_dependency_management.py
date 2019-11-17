from metacli.dependency_management import DependencyManagement
import pathlib
import os


def test_dependency_management(monkeypatch):
    dm = DependencyManagement()

    # get example/dog path
    base = pathlib.Path(__file__).resolve().parent
    dog_path = str((base / pathlib.Path("../example/dog")).resolve())

    # mock input path
    monkeypatch.setattr(dm, "get_base_plugin_path", lambda: dog_path)

    # run dependency management
    dm.gather_packages_for_plugins_and_check_conflicts()

    # check package result
    requirement_path = dog_path + '/requirements.txt'
    with open(requirement_path, "r") as f:
        ans = f.read()

    assert """click\npandas\npytest\n""" == ans

    # cleanup
    os.remove(requirement_path)
