from flask_restx import fields


class WeatherModels:
    @staticmethod
    def init_models(api):
        ask_model = api.model(
            "AskModel",
            {"query": fields.String(required=True, description="Weather question")},
        )

        answer_model = api.model(
            "AnswerModel",
            {"answer": fields.String(description="Assistant response")},
        )

        api.models = {"AskModel": ask_model, "AnswerModel": answer_model}
