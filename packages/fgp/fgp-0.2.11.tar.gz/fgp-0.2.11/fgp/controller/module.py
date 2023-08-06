from fgp.controller import ApiClient
from fgp.model.module import Module
from fgp.model.device import Device
from loguru import logger
from fgp.model.module_state import ModuleState
from fgp.model.module_event import ModuleEvent
from fgp.utils.datetime_to_ms import datetime_to_ms
import datetime
import json


def module_exists(client: ApiClient, module: Module):
    try:
        client.device.get(device_type='module', lookup_key=f'module.{module.name}')
        return True
    except Exception as e:
        if 'Not Found' in str(e):
            return False
        raise e


def get_module(client: ApiClient, module: Module) -> Device:
    # check if module exists
    r = client.device.get(
        device_type='module',
        lookup_key=f'module.{module.name}'
    )
    return Device.from_api_response(r)


def create_module(client: ApiClient, module: Module) -> Device:
    ret = client.device.create(
        device_type='module',
        device_name=f'module.{module.name}',
        device_description=module.description
    )
    return Device.from_api_response(ret)


def register(client: ApiClient, module: Module):
    if not module_exists(client, module):
        logger.info(f'Module {module.name} not found, creating a new device for it')
        create_module(client, module)
    return get_module(client, module)


def get_run(client: ApiClient, device_name: str, run_id: int) -> ModuleState:
    date_from = datetime.datetime.utcfromtimestamp(run_id/1000-1)
    date_to = datetime.datetime.utcfromtimestamp(run_id/1000+1)
    ret = client.store.get_data(
        device_type='module',
        date_from=date_from,
        date_to=date_to,
        store_name='module_run',
        devices=[device_name]
    )
    if len(ret["doc"]) == 0:
        raise ValueError(f'Run with run_id={run_id} not found, used date_from={date_from}, date_to={date_to}')
    data_str = ret["doc"][0]
    if not data_str:
        raise ValueError(f'Invalid run, no data found in "doc" field {ret}')
    data = json.loads(data_str)
    return ModuleState.from_dict(data)


def call_lambda(client: ApiClient, device_name, lambda_name: str, payload: dict) -> dict:
    return client.lambdas.call(
        device_type='module',
        lookup_name='name',
        lookup_key=device_name,
        lambda_name=lambda_name,
        payload=payload
    )


class ModuleController:
    module: Module = None
    client: ApiClient = None
    device: Device = None
    run: ModuleState = None

    def __init__(self, module: Module, client: ApiClient):
        self.module = module
        self.client = client
        self.device = register(client=client, module=module)

    def call_lambda(self, lambda_name: str, payload: dict) -> dict:
        return call_lambda(
            client=self.client,
            device_name=self.device.name,
            lambda_name=lambda_name,
            payload=payload
        )

    def set_state(self, state: dict):
        return self.call_lambda(
            lambda_name='update_module_state',
            payload=state
        )

    def get_state(self) -> ModuleState:
        result = self.client.device.get_many('module', [self.device.name], extension_names=['module_state'])
        if len(result) != 1:
            raise Exception('Module not found')
        module_dict = result[0]
        state = ModuleState.from_api_response(module_dict.get('module_state')) if module_dict.get('module_state') else None
        return state

    def get_run(self) -> ModuleState:
        self.run = get_run(client=self.client, run_id=self.run.runId, device_name=self.device.name)
        return self.run

    def create_run(self) -> ModuleState:
        ret = self.call_lambda(lambda_name='create_module_run', payload={
            'version': self.module.version
        })
        self.run = ModuleState.from_dict(ret.get('data'))
        return self.run

    def update_run(self, data: dict) -> ModuleState:
        return self.call_lambda(
            lambda_name='update_module_run',
            payload={**data, 'runId': self.run.runId}
        )

    def start_run(self, status='RUNNING', data: dict = None) -> ModuleState:
        data = data if data is not None else {}
        data['dateStarted'] = datetime_to_ms(datetime.datetime.utcnow())
        self.create_event(event_type='PRODUCER', event_name='JOB_START')
        return self.call_lambda(
            lambda_name='update_module_run',
            payload={**data, 'runId': self.run.runId, 'status': status}
        )

    def end_run(self, status='COMPLETE', data: dict = None) -> ModuleState:
        data = data if data is not None else {}
        data['dateEnd'] = datetime_to_ms(datetime.datetime.utcnow())
        self.create_event(event_type='PRODUCER', event_name='JOB_END', data={'status': status})
        return self.call_lambda(
            lambda_name='update_module_run',
            payload={**data, 'runId': self.run.runId, 'status': status}
        )

    def create_event(self, event_type: str, event_name: str, data: dict = None) -> ModuleEvent:
        if self.run is None:
            raise RuntimeError('A run must be started before an event can be created')
        data = data if data is not None else {}
        payload = {
            **data,
            "eventType": event_type,
            "eventName": event_name,
            "runId": self.run.runId,
            "version": self.run.version
        }
        ret = self.call_lambda(
            lambda_name='create_module_event',
            payload=payload
        )

        if ret.get('error'):
            raise Exception(ret.get('error'))

        return ModuleEvent.from_dict(ret.get('data'))
