import json
import os
from typing import List, Union, Any

from loguru import logger

from .config import BASE_URL_PRODUCTION
from .exception import ApiException, SchemasException
from .requestor import Request
from .utils import list_to_query_param, list_dict_to_dict, object_list_to_dict_list
from .schemas import TrialStatus, Trial, Trials, Evaluation, TrialFailed, ObjectId, Experiment, Metric, Parameter, \
    FocusedParameter, Constraint, BaseInfo, ExperimentStatus, Experiments


class Optimus(object):
    def __init__(self, token: str = None, base_url: str = None):
        self._set_token(token)
        self.base_url = base_url or BASE_URL_PRODUCTION
        self.url = {}
        self.request = Request(headers=self.headers)

    def _set_token(self, token: str = None):
        if token:
            self.token = token
        else:
            self.token = os.getenv("OPTIMUS_API_TOKEN")
        if not self.token:
            raise SchemasException("token invalid")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-type": "application/json",
        }

    def experiments(self, id: str = None):
        if id:
            ObjectId(obj=id)
            self.url.update({"experiment_id": id})
        return self

    def trials(self, id: str = None):
        if id:
            ObjectId(obj=id)
            self.url.update({"trial_id": id})
        return self

    def _validate_experiment_id(self):
        if "experiment_id" not in self.url:
            raise SchemasException("experiment id is invalid")

    def _validate_ids(self):
        self._validate_experiment_id()
        if not self.url.get("trial_id", ""):
            raise SchemasException("trial id is invalid")

    def _update(self, param, kind: str = "parameter"):
        if not self.url.get('experiment_id'):
            raise SchemasException("please assign an experiment")

        if kind != "basic" and len(param) <= 0:
            raise SchemasException(f"must one {kind}")

        url = f"{self.base_url}/experiments/{self.url['experiment_id']}/{kind}"
        if kind != "basic":
            tmp = []
            for i in param:
                tmp.append(i.__dict__)
        else:
            tmp = param.__dict__
        response = self.request.put(url, data=json.dumps(tmp))
        if response:
            response = Experiment(**response)
            logger.info("experiment {} {} updated", response.id, kind)
        else:
            logger.info("experiment {} failed to update {}", response.id, kind)
        self.url = {}
        return response

    def create(self, name: str = None, description: str = None, parallel_count: int = 3, metrics: List[Metric] = None,
               parameters: List[Parameter] = None, constraints: List[Constraint] = None,
               focused_parameters: List[FocusedParameter] = None):
        if "trial_id" in self.url:
            raise logger.warning("please use add method to create trial")
        url = f"{self.base_url}/experiments"
        data = {
            "name": name,
            "description": description,
            "parallelCount": parallel_count,
            "metrics": object_list_to_dict_list(metrics),
            "parameters": object_list_to_dict_list(parameters),
            "constraints": object_list_to_dict_list(constraints),
            "focusedParameters": object_list_to_dict_list(focused_parameters)
        }
        response = self.request.post(url, data=json.dumps(data))

        if response:
            response = Experiment(**response)
            logger.info("create experiment {}", response)
        else:
            logger.error(f"create experiment error")
        return response

    def update_metrics(self,  metrics: List[Metric]):
        return self._update(metrics, kind="metrics")

    def update_parameters(self, parameters: List[Parameter]):
        return self._update(parameters, kind="parameters")

    def update_focused_parameters(self, focused: List[FocusedParameter]):
        return self._update(focused, kind="focused-parameters")

    def update_constraints(self, constraints: List[Constraint]):
        return self._update(constraints, kind="constraints")

    def update_base_info(self, base_info: BaseInfo):
        return self._update(base_info, kind="basic")

    def start(self):
        self._validate_experiment_id()
        if self.url.get("experiment_id", "") and self.url.get("trial_id"):
            url = f"{self.base_url}/experiments/{self.url['experiment_id']}/trials/{self.url['trial_id']}/start"
            response = self.request.post(url)
            if response:
                response = Trial(**response)
                logger.info("trial {} started", response.id)
            else:
                logger.warning("trial {} failed to start", response.id)
        else:
            url = f"{self.base_url}/experiments/{self.url['experiment_id']}/start"
            response = self.request.post(url)
            if response:
                response = Experiment(**response)
                logger.info("experiment {} started", response.id)
            else:
                logger.warning("experiment {} failed to start", self.url['experiment_id'])
        self.url = {}
        return response

    def pause(self):
        self._validate_experiment_id()
        if "trial_id" in self.url:
            raise logger.warning("trial has no pause method")
        url = f"{self.base_url}/experiments/{self.url['experiment_id']}/pause"
        response = self.request.post(url)
        if response:
            response = Experiment(**response)
            logger.info("pause experiment {}", response.id)
        else:
            pass
        self.url ={}
        return response

    def _fetch_all_trials(self, status):
        if status:
            query_str = list_to_query_param("status", [i.value for i in status])
            url = f"{self.base_url}/experiments/{self.url['experiment_id']}/trials?{query_str}"
        else:
            url = f"{self.base_url}/experiments/{self.url['experiment_id']}/trials"
        response = self.request.get(url=url)
        if response:
            response = Trials(trials=response).trials
            ids = [i.id for i in response]
            logger.info("fetched trials {}", len(response))
        else:
            logger.warning("found no trials that is status in {}", status)
        self.url = {}
        return response

    def _fetch_all_experiments(self, status):
        if status:
            query_str = list_to_query_param("status", [i.value for i in status])
            url = f"{self.base_url}/experiments?{query_str}"
        else:
            url = f"{self.base_url}/experiments"
        response = self.request.get(url=url)
        if response:
            response = Experiments(experiments=response).experiments
            logger.info("fetched experiments {}", len(response))
        else:
            logger.warning("found no experiments with status in {}", status)
        self.url = {}
        return response

    def fetch_all(self, status: List[Union[TrialStatus, ExperimentStatus]] = None) -> Union[bool, Trials]:
        if self.url.get("experiment_id", ""):
            return self._fetch_all_trials(status)
        else:
            return self._fetch_all_experiments(status)

    def fetch(self) -> Union[bool, Trial]:
        self._validate_experiment_id()
        if self.url.get("experiment_id", "") and self.url.get("trial_id"):
            url = f"{self.base_url}/experiments/{self.url['experiment_id']}/trials/{self.url['trial_id']}"
            response = self.request.get(url=url)
            if response:
                response = Trial(**response)
                logger.info("fetched trial {}", self.url['trial_id'])
            else:
                logger.warning("failed to fetch trial {}", self.url['trial_id'])
        else:
            url = f"{self.base_url}/experiments/{self.url['experiment_id']}"
            response = self.request.get(url=url)
            if response:
                response = Experiment(**response)
                logger.info("fetched experiment {}", self.url['experiment_id'])
            else:
                logger.warning("failed to fetch {}", self.url['experiment_id'])
        return response

    def fail(self, reason: str = None, detail: str = None, **kwargs) -> Union[bool, Trial]:
        self._validate_ids()
        url = f"{self.base_url}/experiments/{self.url['experiment_id']}/trials/{self.url['trial_id']}/fail"
        data = {"reason": reason, "detail": detail}
        TrialFailed(**data)
        response = self.request.post(url=url, data=json.dumps(data))
        if response:
            response = Trial(**response)
            logger.info("uploaded trial {} failure to server", self.url['trial_id'])
        else:
            logger.warning("failed to upload trial {} failure to server", self.url['trial_id'])
        self.url = {}
        return response

    def start_one(self) -> Union[bool, Trial]:
        logger.info("starting a new trial")
        self._validate_experiment_id()
        url = f"{self.base_url}/experiments/{self.url['experiment_id']}/trials/start-one"
        response = self.request.post(url=url)
        if response:
            response = Trial(**response)
            logger.info("trial {} started", response.id)
        else:
            logger.warning("trial {} failed to start", response.id)
        self.url = {}
        return response

    def evaluate(self, evaluations=None, **kwargs) -> Union[bool, Trial]:
        self._validate_ids()
        eval_dict = evaluations if evaluations else kwargs
        evaluations = self._format_evaluations(eval_dict)
        url = f"{self.base_url}/experiments/{self.url['experiment_id']}/trials/{self.url['trial_id']}/evaluate"
        response = self.request.post(url, data=json.dumps(evaluations))
        if response:
            response = Trial(**response)
            logger.info("trial {} evaluated", self.url['trial_id'])
        else:
            logger.warning("trial {} failed to evaluate", self.url['trial_id'])
        self.url = {}
        return response

    def solve(self, problem, max_trials_num: int = 1, experiment_id: str = None, target_min_num: int = 0,
              target_name: List[str] = None):
        trial = ""
        logger.info("starting to solve experiment {}", experiment_id)
        try:
            for _ in range(0, max_trials_num):
                trial = self.experiments(id=experiment_id).start_one()
                logger.info("trial #{} suggested assignments {}", trial.sequence, trial.assignment)
                res = problem(trial.assignment)
                logger.info("trial #{} evaluated with {}", trial.sequence, res)
                self.experiments(id=experiment_id).trials(id=trial.id).evaluate(evaluations=res)
                # metrics = list_dict_to_dict(trial.metrics)
                # if self._auto_stop(res, metrics, target_min_num, target_name):
                #     logger.info("target was reached")
                #     return "finish"
        except KeyboardInterrupt:
            logger.warning("keyboard interrupted")
            self.experiments(id=experiment_id).trials(id=trial.id).fail(reason="KeyboardInterrupt")
        except ApiException as e:
            logger.error(e)
        except Exception as e:
            logger.opt(exception=e).error("Unknown exception {}", e)
            self.experiments(id=experiment_id).trials(id=trial.id).fail(
                reason="UnknownException", detail=str(e)
            )

    @staticmethod
    def _format_evaluations(evaluations):
        if not evaluations:
            raise SchemasException("evaluations must not be empty")
        eva_list = []
        for k, v in evaluations.items():
            eva_dict = {"name": k, "value": v}
            Evaluation(**eva_dict)
            eva_list.append(eva_dict)
        return {"evaluations": eva_list}

    @staticmethod
    def _judge_single_target(res: dict, metrics: dict) -> bool:
        result = False
        for k, v in res.items():
            if metrics.get(k, ""):
                if metrics.get("objective", "") == "max":
                    result = True if v > metrics[k] else result
                else:
                    result = True if v < metrics[k] else result
            return result

    @staticmethod
    def _judge_multiple_target_with_min_num(res: dict, metrics: dict, min_num: int) -> bool:
        total = 0
        result = False
        for k, v in res.items():
            if metrics.get(k, ""):
                if metrics.get("objective", "") == "max":
                    total = total + 1 if v > metrics else total
                else:
                    total = total + 1 if v < metrics else total
        result = True if total >= min_num else result
        return result

    @staticmethod
    def _judge_multiple_target_with_target_name(res: dict, metrics: dict, target_names: list) -> bool:
        for i in target_names:
            if not metrics.get(i, "") or not res.get(i, ""):
                return False
            else:
                if metrics.get("objective", "") == "max":
                    if res[i] < metrics[i]:
                        return False
                else:
                    if res[i] > metrics[i]:
                        return False
        return True

    @staticmethod
    def _judge_multiple_target_with_all(res: dict, metrics: dict) -> bool:
        for k, v in res:
            if not metrics.get(k):
                return False
            else:
                if metrics.get("objective", "") == "max":
                    if res[k] < metrics[k]:
                        return False
                else:
                    if res[k] > metrics[k]:
                        return False
        return True

    def _auto_stop(self, res: dict, metrics: dict, target_min_num: int, target_name: List[str]) -> bool:
        if len(metrics) == 1:
            return self._judge_single_target(res, metrics)
        elif len(metrics) > 1:
            if target_min_num > 0:
                return self._judge_multiple_target_with_min_num(res, metrics, target_min_num)
            elif len(target_name) > 0:
                return self._judge_multiple_target_with_target_name(res, metrics, target_name)
            else:
                return self._judge_multiple_target_with_all(res, metrics)