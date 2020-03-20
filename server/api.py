import responder

api = responder.API(
    cors=True,
    allowed_hosts=["*"],
    cors_params={"allow_origins": "*",
                 "allow_methods": "*",
                 "allow_headers": "*"
                 })


@api.route("/test")
class TestResource:
    def on_get(self, req, resp):
        resp.text = "OK!"


if __name__ == '__main__':
    api.run(address='0.0.0.0', debug=True)
