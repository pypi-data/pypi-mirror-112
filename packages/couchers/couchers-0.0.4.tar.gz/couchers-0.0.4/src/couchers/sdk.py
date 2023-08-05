import http.cookies

import grpc

from couchers.proto import auth_pb2, auth_pb2_grpc

DEFAULT_SERVER_ADDRESS = "api.couchers.org:8443"


class _CookieCreds:
    def __init__(self, cookie_name, cookie_value):
        self.cookie_name = cookie_name
        self.cookie_value = cookie_value

    def __call__(self, context, callback):
        callback((("cookie", f"{self.cookie_name}={self.cookie_value}"),), None)


class _MetadataKeeperInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self):
        self.latest_headers = {}

    def intercept_unary_unary(self, continuation, client_call_details, request):
        call = continuation(client_call_details, request)
        self.latest_headers = dict(call.initial_metadata())
        return call


def get_api_key(username, password, server_address=DEFAULT_SERVER_ADDRESS):
    with create_open_channel(server_address) as channel:
        metadata_interceptor = _MetadataKeeperInterceptor()
        channel = grpc.intercept_channel(channel, metadata_interceptor)
        auth = auth_pb2_grpc.AuthStub(channel)
        auth.Authenticate(auth_pb2.AuthReq(user=username, password=password))
        return http.cookies.SimpleCookie(metadata_interceptor.latest_headers["set-cookie"])["couchers-sesh"].value


def create_open_channel(server_address=DEFAULT_SERVER_ADDRESS):
    channel_creds = grpc.ssl_channel_credentials()
    return grpc.secure_channel(server_address, channel_creds)


def create_channel(api_key, server_address=DEFAULT_SERVER_ADDRESS):
    channel_creds = grpc.ssl_channel_credentials()
    cookie_creds = grpc.metadata_call_credentials(_CookieCreds("couchers-sesh", api_key))
    creds = grpc.composite_channel_credentials(channel_creds, cookie_creds)
    return grpc.secure_channel(server_address, creds)
