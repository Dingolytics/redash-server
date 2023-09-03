from json import loads as json_loads
from flask import request
from redash import models
from redash.handlers.base import routes
from redash.utils import collect_parameters_from_request


@routes.route("/ext/widgets/<int:query_id>/<template>", methods=["GET"])
def render_widget(query_id: int, template: str):
    query = models.Query.get_by_id(query_id)
    query_runner = query.data_source.query_runner

    parameterized = query.parameterized
    parameterized.apply(
        collect_parameters_from_request(request.args)
    )

    result_str, error = query_runner.run_query(
        # query_runner.annotate_query(parameterized.text, {})
        parameterized.text,
        user=None
    )

    if not error:
        data = json_loads(result_str)
    else:
        data = None

    # TODO: Render result to template

    return {
        "data": data,
        "error": error,
    }
