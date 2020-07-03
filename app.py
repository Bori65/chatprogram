from flask import render_template, Flask, escape, request
from flask_bootstrap import Bootstrap

messages = []
limit = 5
def concatMessages():
    ret = ""
    for i in messages:
        ret = ret+i
    return ret
