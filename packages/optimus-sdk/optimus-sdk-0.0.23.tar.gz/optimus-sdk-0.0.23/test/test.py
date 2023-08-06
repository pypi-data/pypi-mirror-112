import json
import unittest
from unittest.mock import MagicMock

from optimus.optimus import Optimus
from optimus.schemas import TrialStatus, Metric, BaseInfo, Parameter, Constraint, FocusedParameter

TEST_EXPERIMENT_ID = "60a1d3acc70a061f09de2c23"


class OptimusTest(unittest.TestCase):
    """Simple unittest"""

    def setUp(self) -> None:
        self.optimus = Optimus(token="TEST_TOKEN", base_url="https://example.com")
        json_experiment = '''{
                    "id": "60e262903e33018eeced6742",
                    "name": "string",
                    "description": "string",
                    "parallelCount": 4,
                    "status": "Running",
                    "createdAt": "2021-07-05T01:38:24.987Z",
                    "updatedAt": "2021-07-05T02:10:31.644795Z",
                    "metrics": null,
                    "parameters": null,
                    "constraints": null,
                    "completed": false,
                    "completedAt": "0001-01-01T00:00:00Z",
                    "initialized": true,
                    "focusedParameters": null
                }'''
        self.experiment = json.loads(json_experiment)

    def test_fetch_all(self):
        trial_dict = [
            {
                "id": "60a1d3acc70a061f09de2c25",
                "sequence": 1,
                "experimentId": TEST_EXPERIMENT_ID,
                "assignments": None,
                "status": "Pending",
                "createdAt": "2021-05-17T02:23:40.395Z",
                "updatedAt": "2021-05-17T02:23:40.395Z",
                "startedAt": "0001-01-01T00:00:00Z",
            }
        ]
        self.optimus.request.get = MagicMock(return_value=trial_dict)
        trial = (
            self.optimus.experiments(id=TEST_EXPERIMENT_ID)
            .trials()
            .fetch_all(status=[TrialStatus.PENDING])
        )
        self.assertEqual(trial[0].experimentId, TEST_EXPERIMENT_ID)
        self.assertEqual(trial[0].status, TrialStatus.PENDING)

    def test_fetch(self):
        trial_dict = {
            "id": "60a1d3acc70a061f09de2c25",
            "sequence": 1,
            "experimentId": TEST_EXPERIMENT_ID,
            "assignments": None,
            "status": "Pending",
            "createdAt": "2021-05-17T02:23:40.395Z",
            "updatedAt": "2021-05-17T02:23:40.395Z",
            "startedAt": "0001-01-01T00:00:00Z",
        }
        self.optimus.request.get = MagicMock(return_value=trial_dict)
        trial = (
            self.optimus.experiments(id=TEST_EXPERIMENT_ID)
            .trials("60a1d3acc70a061f09de2c25")
            .fetch()
        )
        self.assertEqual(trial.id, "60a1d3acc70a061f09de2c25")
        self.assertEqual(trial.experimentId, TEST_EXPERIMENT_ID)

    def test_start(self):
        trial_dict = {
            "id": "60a1d3acc70a061f09de2c25",
            "sequence": 1,
            "experimentId": TEST_EXPERIMENT_ID,
            "assignments": None,
            "status": "Started",
            "createdAt": "2021-05-17T02:23:40.395Z",
            "updatedAt": "2021-05-17T02:23:40.395Z",
            "startedAt": "0001-01-01T00:00:00Z",
        }
        self.optimus.request.post = MagicMock(return_value=trial_dict)
        trial = (
            self.optimus.experiments(id=TEST_EXPERIMENT_ID)
            .trials("60a1d3acc70a061f09de2c25")
            .start()
        )
        self.assertEqual(trial.id, "60a1d3acc70a061f09de2c25")
        self.assertEqual(trial.experimentId, TEST_EXPERIMENT_ID)
        self.assertEqual(trial.status, TrialStatus.STARTED)

    def test_evaluate(self):
        trial_dict = {
            "id": "60a1d3acc70a061f09de2c25",
            "sequence": 1,
            "experimentId": TEST_EXPERIMENT_ID,
            "assignments": None,
            "status": "Started",
            "createdAt": "2021-05-17T02:23:40.395Z",
            "updatedAt": "2021-05-17T02:23:40.395Z",
            "startedAt": "0001-01-01T00:00:00Z",
            "failedDetail": None,
        }
        self.optimus.request.post = MagicMock(return_value=trial_dict)
        trial = (
            self.optimus.experiments(id=TEST_EXPERIMENT_ID)
            .trials("60a1d3acc70a061f09de2c25")
            .evaluate(name=1)
        )
        self.assertEqual(trial.id, "60a1d3acc70a061f09de2c25")
        self.assertEqual(trial.experimentId, TEST_EXPERIMENT_ID)
        self.assertEqual(trial.status, TrialStatus.STARTED)

    def test_fail(self):
        trial_dict = {
            "id": "60a1d3acc70a061f09de2c25",
            "sequence": 1,
            "experimentId": TEST_EXPERIMENT_ID,
            "assignments": None,
            "status": "Started",
            "createdAt": "2021-05-17T02:23:40.395Z",
            "updatedAt": "2021-05-17T02:23:40.395Z",
            "startedAt": "0001-01-01T00:00:00Z",
        }
        self.optimus.request.post = MagicMock(return_value=trial_dict)
        trial = (
            self.optimus.experiments(id=TEST_EXPERIMENT_ID)
            .trials("60a1d3acc70a061f09de2c25")
            .fail(reason="NoEvaluation", detail="test")
        )
        self.assertEqual(trial.id, "60a1d3acc70a061f09de2c25")
        self.assertEqual(trial.experimentId, TEST_EXPERIMENT_ID)
        self.assertEqual(trial.status, TrialStatus.STARTED)

    def test_auto_stop(self):
        res = {"v1": 4.00, "v2": 5.00}
        metrics = {"v1": 3.00, "v2": 6.00}
        target_min_num = 0
        target_name = ["v2"]
        res = self.optimus._auto_stop(res, metrics, target_min_num, target_name)
        self.assertEqual(res, True)

    def test_fetch_experiment(self):
        res = self.experiment

        self.optimus.request.get = MagicMock(return_value=res)
        experiment = (
            self.optimus.experiments('60e262903e33018eeced6742').fetch()
        )
        self.assertEqual(experiment.id, "60e262903e33018eeced6742")

    def test_fetch_all_experiment(self):
        res = self.experiment
        tmp = [res]
        self.optimus.request.get = MagicMock(return_value=tmp)
        experiments = (
            self.optimus.experiments().fetch_all()
        )

        self.assertEqual(len(experiments), 1)
        self.assertEqual(experiments[0].id, "60e262903e33018eeced6742")

    def test_create_experiment(self):
        res = self.experiment
        self.optimus.request.post = MagicMock(return_value=res)
        experiment = (
            self.optimus.create(name="string", description="string", parallel_count=4)
        )

        self.assertEqual(experiment.id, "60e262903e33018eeced6742")
        self.assertEqual(experiment.name, "string")

    def test_update_base_info(self):
        res = self.experiment
        res['name'] = "test1"
        base_info = BaseInfo(name="test1", )
        self.optimus.request.put = MagicMock(return_value=res)
        experiment = (
            self.optimus.experiments(res["id"]).update_base_info(base_info)
        )

        self.assertEqual(experiment.name, "test1")

    def test_update_metrics(self):
        res = self.experiment
        metric = Metric(name="test", objective="min", strategy="optimize", target=0.98, range=None)
        metrics = [metric]
        res['metrics'] = [metric.__dict__]
        self.optimus.request.put = MagicMock(return_value=res)
        experiment = (
            self.optimus.experiments(res["id"]).update_metrics(metrics)
        )

        self.assertEqual(experiment.metrics[0].name, "test")

    def test_update_parameter(self):
        res = self.experiment
        momentum = Parameter(name="momentum", type="r", range=[0, 1], scale="linear", precision=8, step=0)
        parameters = [momentum]
        res['parameters'] = [momentum.__dict__]
        self.optimus.request.put = MagicMock(return_value=res)
        experiment = (
            self.optimus.experiments(res["id"]).update_parameters(parameters)
        )

        self.assertEqual(experiment.parameters[0].precision, 8)

    def test_update_constraints(self):
        res = self.experiment
        constraint = Constraint(expr="momentum * 2", operator="<=", value=1)
        constraints = [constraint]
        res['constraints'] = [constraint.__dict__]

        self.optimus.request.put = MagicMock(return_value=res)
        experiment = (
            self.optimus.experiments(res["id"]).update_constraints(constraints)
        )

        self.assertEqual(experiment.constraints[0].value, 1)

    def test_update_focused_parameters(self):
        res = self.experiment
        focused_parameter = FocusedParameter(name="hidden_size", value="128")
        focused_parameters = [focused_parameter]

        res['focusedParameters'] = [focused_parameter.__dict__]

        self.optimus.request.put =  MagicMock(return_value=res)
        experiment = (
            self.optimus.experiments(res["id"]).update_focused_parameters(focused_parameters)
        )

        self.assertEqual(experiment.focusedParameters[0].name, "hidden_size")


if __name__ == "__main__":
    unittest.main()
