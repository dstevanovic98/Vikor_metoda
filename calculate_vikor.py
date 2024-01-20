import numpy
import pandas

from flask import Flask, render_template, request, redirect, url_for , session

def vikor(
    data: numpy.ndarray,
    alternative_names: list[str],
    criteria_benefitial: list[bool],
    weights: list[float],
    mi: float = 0.5
):
    def find_most_optimal(index: int):
        row_data = data.copy().transpose()
        is_benefitial = criteria_benefitial[index]
        return (
            numpy.max(row_data[index]) if is_benefitial else numpy.min(row_data[index])
        )

    def find_least_optimal(index: int):
        row_data = data.copy().transpose()
        is_benefitial = criteria_benefitial[index]
        return (
            numpy.min(row_data[index]) if is_benefitial else numpy.max(row_data[index])
        )

    fi_plus = [find_most_optimal(index) for index in range(len(criteria_benefitial))]
    fi_minus = [find_least_optimal(index) for index in range(len(criteria_benefitial))]

    normalized_data = data.copy()
    for row in range(data.shape[0]):
        for column in range(data.shape[1]):
            normalized_data[row, column] = (
                (fi_plus[column] - normalized_data[row, column])
                / (fi_plus[column] - fi_minus[column])
            ) * weights[column]

    sj = numpy.sum(normalized_data, 1)
    ri = numpy.max(normalized_data, 1)

    s_plus = numpy.min(sj)
    r_plus = numpy.min(ri)

    s_minus = numpy.max(sj)
    r_minus = numpy.max(ri)

    qj = (mi * ((sj - s_plus) / (s_minus - s_plus))) + (
        (1 - mi) * ((ri - r_plus) / (r_minus - r_plus))
    )

    j = data.shape[0]
    dq = 1 / (j - 1)

    return list(sorted(zip(qj, alternative_names), key=lambda x: x[0]))

data = numpy.array(
        [
            [43000, 4, 1000, 1.5],
            [45000, 6, 750, 1.7],
            [35000, 8, 1000, 2],
            [38000, 6, 750, 2.1],
            [39000, 8, 900, 1.8],
            [46000, 6, 750, 1.2],
            [50000, 6, 600, 1.1],
            [42000, 10, 800, 2.5],
        ]
    )
result = vikor(data,['Dell', 'HP',  'Lenovo', 'Asus', 'Acer', 'Sony', 'Apple', 'Toshiba'],[False, True, True, False],[0.25, 0.25, 0.25, 0.25])
print(result)
