import pytest
from click.testing import CliRunner
from metacli import metacli
import pathlib
import os
import shutil


def test_generate_empty_project(monkeypatch):
    runner = CliRunner()

    generator = metacli.metacli
    result = runner.invoke(generator, "--help")
    assert result.exit_code == 0

    # clean up
    template_base_path = "./templates/empty_project_test/"
    result_base_path = "./empty_project_test/"
    if os.path.exists(result_base_path):
        shutil.rmtree(result_base_path)

    # mock new project path and name
    monkeypatch.setattr(metacli, "get_project_path_and_name", lambda: ("./", "empty_project_test"))

    # mock input path
    result = runner.invoke(generator, ["create_project"])
    assert result.exit_code == 0

    # compare new generated file with templates
    for name in ["__init__.py", "setup.py", "plugin_commands.json", "empty_project_testcli.py"]:
        with open(template_base_path + name, "r") as f:
            template = f.read()

        with open(result_base_path + name, "r") as f:
            result = f.read()
        assert template.strip() == result.strip()

    # clean up
    if os.path.exists(result_base_path):
        shutil.rmtree(result_base_path)


def test_generate_project_from_json(monkeypatch):
    runner = CliRunner()

    generator = metacli.metacli
    result = runner.invoke(generator, "--help")
    assert result.exit_code == 0

    # clean up
    template_base_path = "./templates/json_project_test/"
    result_base_path = "./json_project_test/"
    if os.path.exists(result_base_path):
        shutil.rmtree(result_base_path)

    # mock new project path and name
    monkeypatch.setattr(metacli, "get_project_path_and_name", lambda: ("./", "json_project_test"))

    # mock input path
    result = runner.invoke(generator, ["create_project", "--fromjson", "templates/schema.json"])
    assert result.exit_code == 0

    # compare new generated file with templates
    for name in ["__init__.py", "setup.py", "plugin_commands.json", "json_project_testcli.py"]:
        with open(template_base_path + name, "r") as f:
            template = f.read()

        with open(result_base_path + name, "r") as f:
            result = f.read()
        assert template.strip() == result.strip()

    # clean up
    if os.path.exists(result_base_path):
        shutil.rmtree(result_base_path)


def test_generate_project_from_yaml(monkeypatch):
    runner = CliRunner()

    generator = metacli.metacli
    result = runner.invoke(generator, "--help")
    assert result.exit_code == 0

    # clean up
    template_base_path = "./templates/yaml_project_test/"
    result_base_path = "./yaml_project_test/"
    if os.path.exists(result_base_path):
        shutil.rmtree(result_base_path)

    # mock new project path and name
    monkeypatch.setattr(metacli, "get_project_path_and_name", lambda: ("./", "yaml_project_test"))

    # mock input path
    result = runner.invoke(generator, ["create_project", "--fromyaml", "templates/schema.yaml"])
    assert result.exit_code == 0

    # compare new generated file with templates
    for name in ["__init__.py", "setup.py", "plugin_commands.json", "yaml_project_testcli.py"]:
        with open(template_base_path + name, "r") as f:
            template = f.read()

        with open(result_base_path + name, "r") as f:
            result = f.read()
        assert template.strip() == result.strip()

    # clean up
    if os.path.exists(result_base_path):
        shutil.rmtree(result_base_path)


if __name__ == '__main__':
    pytest.main()
