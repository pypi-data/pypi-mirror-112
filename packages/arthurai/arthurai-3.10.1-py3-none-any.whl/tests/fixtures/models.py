import pytest

from arthurai import ArthurModel, ArthurAttribute
from arthurai.common.constants import InputType, OutputType, ValueType, Stage


TABULAR_MODEL_ID = "tabby-mc-tabface"
INT_INPUT = "int_input"
INT_INPUT_ATTR = ArthurAttribute(name=INT_INPUT, value_type=ValueType.Integer, stage=Stage.ModelPipelineInput,
                                 categorical=True)
FLOAT_INPUT = "float_input"
FLOAT_INPUT_ATTR = ArthurAttribute(name=FLOAT_INPUT, value_type=ValueType.Float, stage=Stage.ModelPipelineInput)
PRED = "pred"
PRED_ATTR = ArthurAttribute(name=PRED, value_type=ValueType.Float, stage=Stage.PredictedValue)
GROUND_TRUTH = "ground_truth"
GROUND_TRUTH_ATTR = ArthurAttribute(name=GROUND_TRUTH, value_type=ValueType.Float, stage=Stage.GroundTruth)


@pytest.fixture
def tabular_model(mock_client):
    model_data = {
        "partner_model_id": "",
        "input_type": InputType.Tabular,
        "output_type": OutputType.Regression,
        "display_name": "",
        "description": "",
        "attributes": [INT_INPUT_ATTR, FLOAT_INPUT_ATTR, PRED_ATTR, GROUND_TRUTH_ATTR],
    }
    model = ArthurModel(client=mock_client.client, **model_data)
    model.id = TABULAR_MODEL_ID
    return model
