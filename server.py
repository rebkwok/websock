#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect
from urllib.parse import urlencode

import sockgen


app = Flask(__name__)


def form_input(request):
    # result dict with each parameter as a tuple of (value, error)
    # units is a choice field, so no error option
    result = {
        'units': request.args.get('units', 'inches'),
        'stitches': request.args.get('stitches', 24),
        'rows': request.args.get('rows', 30),
        'circum': request.args.get('circum', 7),
        'foot_length': request.args.get('foot_length', 8),
        'ease': request.args.get('ease', -8),
        'divisible_by': request.args.get('divisible_by', 1),
    }

    errors = []

    for param in ['stitches', 'rows', 'circum', 'foot_length', 'ease']:
        try:
            result.update({param: float(result[param])})
        except ValueError:
            errors.append(param)

    try:
        result.update({'divisible_by': int(result['divisible_by'])})
    except ValueError:
        errors.append('divisible_by')

    return result, errors


@app.route('/')
def form():
    input_fields, error_list = form_input(request)
    return render_template(
        'form.html', data=input_fields, error_list=error_list
    )


@app.route('/links')
def links():
    return render_template('links.html')


@app.route('/pattern')
def pattern():
    data, error_list = form_input(request)

    if error_list:
        url_values = {
            'units': data['units'],
            'stitches': data['stitches'],
            'rows': data['rows'],
            'circum': data['circum'],
            'foot_length': data['foot_length']['value'],
            'ease': data['ease']['value'],
            'divisible_by': data['divisible_by']
        }

        url = '/?' + urlencode(url_values)

        return redirect(url)

    sock_info = sockgen.Pattern_info(
        data['units'], data['stitches'], data['rows']
    )
    cast_on, heel_end, toe_end, heel_length = sockgen.pattern(
        sock_info, data['circum'], data['divisible_by']
    )

    data.update({
        'sock_info': sock_info,
        'cast_on': cast_on,
        'heel_end': heel_end,
        'toe_end': toe_end,
        'heel_length': heel_length,
    })
    return render_template('pattern.html', data=data)


if __name__ == '__main__':
    app.run('0.0.0.0', 8000, debug=True)
