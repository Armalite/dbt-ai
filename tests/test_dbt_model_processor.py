import os
import tempfile
import pytest
from dbt_ai.dbt import DbtModelProcessor  # 

# Sample data for testing
sample_yaml_content = """
models:
  - name: model1
    description: Example model 1
  - name: model2
    description: Example model 2
"""

sample_sql_content = "SELECT * FROM table1;"

@pytest.fixture
def dbt_project(tmp_path):
    models_path = tmp_path / "models"
    models_path.mkdir()

    yaml_file = tmp_path / "schema.yml"
    yaml_file.write_text(sample_yaml_content)

    sql_file = models_path / "model1.sql"
    sql_file.write_text(sample_sql_content)

    return tmp_path

def test_find_yaml_files(dbt_project):
    processor = DbtModelProcessor(dbt_project)
    yaml_files = processor.find_yaml_files()

    assert len(yaml_files) == 1
    assert os.path.basename(yaml_files[0]) == "schema.yml"

def test_model_has_metadata(dbt_project):
    processor = DbtModelProcessor(dbt_project)

    assert processor.model_has_metadata("model1")
    assert processor.model_has_metadata("model2")
    assert not processor.model_has_metadata("model3")

def test_suggest_dbt_model_improvements(dbt_project):
    processor = DbtModelProcessor(dbt_project)
    model_file = os.path.join(dbt_project, "models", "model1.sql")

    # You should replace 'None' with the actual expected output format of your suggestions
    assert processor.suggest_dbt_model_improvements(model_file, "model1") == None

def test_process_model(dbt_project):
    processor = DbtModelProcessor(dbt_project)
    model_file = os.path.join(dbt_project, "models", "model1.sql")

    result = processor.process_model(model_file)

    assert result["name"] == "model1"
    assert result["has_metadata"]
    # You should replace 'None' with the actual expected output format of your suggestions
    assert result["suggestions"] == None

def test_process_dbt_models(dbt_project):
    processor = DbtModelProcessor(dbt_project)
    models = processor.process_dbt_models()

    assert len(models) == 1

    model = models[0]
    assert model["name"] == "model1"
    assert model["has_metadata"]
    # You should replace 'None' with the actual expected output format of your suggestions
    assert model["suggestions"] == None
