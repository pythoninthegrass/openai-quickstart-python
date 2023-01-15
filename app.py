#!/usr/bin/env python3

import openai
import os
from decouple import config
from flask import Flask, redirect, render_template, request, url_for


# custom app name based on tld w/host, port, debug options
app = Flask("openai-quickstart-python")                     # default (__name__)

if config("OPENAI_API_KEY") is not None:
    openai.api_key = config("OPENAI_API_KEY")
else:
    openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest ten names for an animal that is a superhero.

    Animal: Cat
    Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
    Animal: Dog
    Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
    Animal: {}
    Names:""".format(
            animal.capitalize()
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
