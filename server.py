import random

import numpy as np
from flask import Flask, request, jsonify

from optimization import Optimizer, Table


# -----------------------------------------
# funcs
# -----------------------------------------


def _check_table_can_solve(table: Table) -> bool:
    result_table = Optimizer.run(table=table)
    if result_table is not None:
        return True
    else:
        return False


def _solve_table(table: Table) -> Table:
    result_table = Optimizer.run(table=table)
    assert type(result_table) == Table
    return result_table


def _prepare_init_table(n_empty_cells: int) -> Table:
    seed = random.randint(1, 10000)
    empty_number_array = np.zeros(Table.table_size(), dtype=int)
    empty_table = Table(number_array=empty_number_array)
    result_table = Optimizer.run(table=empty_table, seed=seed)
    assert type(result_table) == Table
    result_table.convert_some_cells_to_zero(n_cells_to_zero=n_empty_cells, seed=seed)
    return result_table


# -----------------------------------------
# server
# -----------------------------------------


app = Flask(__name__)


@app.route("/api/check-table-can-solve", methods=["POST"])
def check_table_can_solve():
    try:
        number_dict = request.get_json()

        table = Table.from_number_dict(number_dict=number_dict)
        can_solve = _check_table_can_solve(table=table)

        return jsonify(
            {
                "can_solve": can_solve,
            }
        )
    except:
        return jsonify(
            {
                "error": "something error",
            }
        )


@app.route("/api/solve-table", methods=["POST"])
def solve_table():
    try:
        number_dict = request.get_json()

        init_table = Table.from_number_dict(number_dict=number_dict)
        solved_table = _solve_table(table=init_table)

        return jsonify(solved_table.number_dict)
    except:
        return jsonify(
            {
                "error": "something error",
            }
        )


@app.route("/api/prepare-init-table", methods=["POST"])
def prepare_init_table():
    try:
        n_empty_cells = request.get_json()["n_empty_cells"]
        init_table = _prepare_init_table(n_empty_cells=n_empty_cells)

        return jsonify(init_table.number_dict)
    except:
        return jsonify(
            {
                "error": "something error",
            }
        )


if __name__ == "__main__":
    app.run(debug=True)
