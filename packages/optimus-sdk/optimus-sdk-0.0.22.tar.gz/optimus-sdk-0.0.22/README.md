# Optimus Python API
 This is the Optimus Python API client. Use this to natively call Optimus API endpoints to operate trials and report data.

 For more help getting start with Optimus and Python, check out the [docs](https://stg.aiexcelsior.art/docs)

 Take a look in `examples` for example usage.
  
## Getting Started
Install the optimus python modules with `pip install optimus-sdk`.

Sign up for an account at <https://stg.aiexcelsior.art>.  In order to use the API, you'll need your API token from the [API tokens page]().

To call the API, instantiate a connection with your token.

### Authentication
Authenticate each connection with your API token directly(will override any token set via environment variable):

```python
from optimus import Optimus
optimus = Optimus(token=OPTIMUS_API_TOKEN)
```

### Authentication with Environment Variable

Insert your API token into the environment variable OPTIMUS_API_TOKEN, and instantiate a connection:
```python
from optimus import Optimus
optimus = Optimus()
```

### Start Trial

Then, you can use connection to start API trial. An example getting a trial and starting the trial.

```python
from optimus import Optimus
optimus = Optimus(token=OPTIMUS_API_TOKEN)

# get all the trials those status are Pending.
trials = optimus.experiments(id=experiment_id).trials().fetch_all(status=["Pending"])

# use first trial of the trials to starting
trial = optimus.experiments(id=experiment_id).trials(id=trials[0].id).stat()

# evaluate the trial result to server
evaluation = optimus.experiments(id=experiment_id).trials(trials[0].id).evaluate(name=value)
```


> **__NOTE:__**  the experiment_id in the above, you can find it in your UI page.


### API Token

Your API token does not have permission to view or modify information about individual user accounts, so it is safe to include when running Optimus in production.

### Endpoints

> **__NOTE:__** At now, we already provided trials' API. Others API we will provide in the near future. Please wait some time.

Endpoints are grouped by objects on the connection. For example, endpoints that interact with experiments are under `optimus.experiments`.`ENDPOINT_GROUP(ID)` operates on a single object, while `ENDPOINT_GROUP()` will operate on multiple objects.

`POST`, `GET`, `PUT` and `DELETE` translate to the method calls `create`, `fetch`, `update` and `delete`. To retrieve an experiment, call `optimus.experiment(ID).fetch`. To create an experiment call `optimus.experiments(ID).create()`. Parameters are passed to the API as named arguments.

Just like in the resource urls, `trials` are  under `experiments`. Access these objects with `optimus.experiments(ID).trials`. The REST endpoint `POST /v1/experiments/1/trials` then translates to `optimus.experiments(ID).trials().create()`.

## Change Log

### [0.0.14] 2021-07-07
[Added] add unit test of experiment

### [0.0.12]  2021-06-02
[Added] change log
[Added] Added completion condition exit function
[Added] Added create experiment method


