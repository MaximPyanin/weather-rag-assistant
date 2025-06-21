from flask_restx import Namespace, Resource
from src.api.validators.ask_validator import AskValidator


class WeatherRoutes:
    @staticmethod
    def init_routes(api, controller):
        ns = Namespace("weather", description="Weather operations")

        ask_model = api.models["AskModel"]
        answer_model = api.models["AnswerModel"]

        @ns.route("/ask")
        class Ask(Resource):
            @ns.expect(ask_model)
            @ns.marshal_with(answer_model)
            def post(self):
                data = AskValidator.validate()
                answer = controller.ask_weather(data["query"])
                return {"answer": answer}

        @ns.route("/refresh")
        class Refresh(Resource):
            def post(self):
                controller.refresh_weather_data()
                return {"status": "reindexed"}, 202

        api.add_namespace(ns, path="/api/v1")
