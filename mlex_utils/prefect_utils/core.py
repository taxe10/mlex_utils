import asyncio
from typing import Optional

from prefect import get_client
from prefect.client.schemas.filters import (
    FlowRunFilter,
    FlowRunFilterName,
    FlowRunFilterParentFlowRunId,
    FlowRunFilterTags,
    LogFilter,
    LogFilterFlowRunId,
)
from prefect.client.schemas.objects import State, StateType
from prefect.client.schemas.sorting import LogSort


async def _schedule(
    deployment_name: str,
    flow_run_name: str,
    parameters: Optional[dict] = None,
    tags: Optional[list] = [],
):
    async with get_client() as client:
        deployment = await client.read_deployment_by_name(deployment_name)
        assert (
            deployment
        ), f"No deployment found in config for deployment_name {deployment_name}"
        flow_run = await client.create_flow_run_from_deployment(
            deployment.id,
            parameters=parameters,
            name=flow_run_name,
            tags=tags,
        )
    return flow_run.id


def schedule_prefect_flow(
    deployment_name: str,
    parameters: Optional[dict] = None,
    flow_run_name: Optional[str] = None,
    tags: Optional[list] = [],
):
    if not flow_run_name:
        model_name = parameters["model_name"]
        flow_run_name = f"{deployment_name}: {model_name}"
    flow_run_id = asyncio.run(
        _schedule(deployment_name, flow_run_name, parameters, tags)
    )
    return flow_run_id


async def _delete(
    flow_run_id: str,
):
    async with get_client() as client:
        await client.delete_flow_run(flow_run_id)


def delete_flow_run(flow_run_id: str):
    asyncio.run(_delete(flow_run_id))


async def _set_state(
    flow_run_id: str,
    state: StateType,
    force: bool = False,
):
    async with get_client() as client:
        await client.set_flow_run_state(flow_run_id, state, force=force)


async def _get_flow_run_state(flow_run_id):
    async with get_client() as client:
        flow_run = await client.read_flow_run(flow_run_id)
        return flow_run.state


def get_flow_run_state(flow_run_id):
    flow_run_state = asyncio.run(_get_flow_run_state(flow_run_id))
    return flow_run_state.type


def cancel_flow_run(flow_run_id: str):
    flow_run_state = asyncio.run(_get_flow_run_state(flow_run_id))
    if not flow_run_state.is_final():
        asyncio.run(_set_state(flow_run_id, State(type=StateType.CANCELLED)))
    pass


async def _get_name(flow_run_id, is_completed):
    async with get_client() as client:
        flow_run = await client.read_flow_run(flow_run_id)
        if flow_run and not is_completed:
            return flow_run.name
        elif flow_run and flow_run.state.is_final():
            if flow_run.state.is_completed():
                return flow_run.name
        return None


def get_flow_run_name(flow_run_id, is_completed=False):
    """
    Retrieves the name of the flow with the given id.
    If is_completed is True, it will return the name of the flow only if it is completed.
    """
    return asyncio.run(_get_name(flow_run_id, is_completed))


async def _flow_run_query(
    tags=None, flow_run_name=None, parent_flow_run_id=None, sort="START_TIME_DESC"
):
    flow_run_filter_parent_flow_run_id = (
        FlowRunFilterParentFlowRunId(any_=[parent_flow_run_id])
        if parent_flow_run_id
        else None
    )
    async with get_client() as client:
        flow_runs = await client.read_flow_runs(
            flow_run_filter=FlowRunFilter(
                name=FlowRunFilterName(like_=flow_run_name),
                parent_flow_run_id=flow_run_filter_parent_flow_run_id,
                tags=FlowRunFilterTags(all_=tags),
            ),
            sort=sort,
        )
        return flow_runs


async def _read_flow_run_logs(flow_run_id, limit=200, offset=0):
    async with get_client() as client:
        flow_run_logs = await client.read_logs(
            log_filter=LogFilter(
                flow_run_id=LogFilterFlowRunId(
                    any_=[flow_run_id],
                ),
            ),
            limit=limit,
            offset=offset,
            sort=LogSort.TIMESTAMP_ASC,
        )
        return flow_run_logs


def query_flow_runs(flow_run_name=None, tags=None):
    flow_runs_by_name = []
    flow_runs = asyncio.run(_flow_run_query(tags, flow_run_name=flow_run_name))
    for flow_run in flow_runs:
        if flow_run.state_name in {"Failed", "Crashed"}:
            flow_name = f"❌ {flow_run.name}"
        elif flow_run.state_name == "Completed":
            flow_name = f"✅ {flow_run.name}"
        elif flow_run.state_name == "Cancelled":
            flow_name = f"🚫 {flow_run.name}"
        else:
            flow_name = f"🕑 {flow_run.name}"
        flow_runs_by_name.append({"label": flow_name, "value": str(flow_run.id)})
    return flow_runs_by_name


def get_children_flow_run_ids(parent_flow_run_id, sort="START_TIME_ASC"):
    children_flow_runs = asyncio.run(
        _flow_run_query(parent_flow_run_id=parent_flow_run_id, sort=sort)
    )
    children_flow_run_ids = [
        str(children_flow_run.id) for children_flow_run in children_flow_runs
    ]
    return children_flow_run_ids


def get_flow_run_logs(flow_run_id):
    flow_run_logs = asyncio.run(_read_flow_run_logs(flow_run_id))
    return [log.message for log in flow_run_logs]
