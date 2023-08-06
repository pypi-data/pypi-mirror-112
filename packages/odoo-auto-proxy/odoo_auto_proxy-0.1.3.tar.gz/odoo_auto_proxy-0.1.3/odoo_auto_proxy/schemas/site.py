from schema import Schema, And, Or, Use, Optional, Literal
from .tools import HasKey, Nullable, Url, List

SiteConfigSchemaObject = {
    "server_name": Use(str),
    Optional("web_upstream", default="localhost:8069"): str,
    Optional("poll_upstream", default="localhost:8072"): str,
    Optional("proxy_pass"): Use(str),  # Or default=None ?
    Optional("disable_longpolling", default=False): bool,
    Optional("httpaccess", default=True): bool,
    Optional("httpsaccess"): bool,
    Optional("posbox", default=False): bool,
    Optional("proxy_http_11"): bool,
    Optional("cache_statics"): bool,
    Optional("disable_cache_zone"): bool,
    Optional("header_upgrade"): bool,
    Optional("header_connection"): bool,
    Optional("header_host"): bool,
    Optional("masquerade"): str,
    Optional("redirect"): str,
    Optional("allow_tls_v1"): Nullable(bool),
    Optional("enable_hsts"): bool,
    Optional("certificate_folder"): str,
    Optional("ssl_certificate"): str,
    Optional("ssl_certificate_key"): str,
    Optional("ssl_trusted_certificate"): bool,
    Optional("disable_stapling"): bool,
    Optional("ip_allow", default=[]): List(str),
    Optional("ip_deny", default=[]): List(str),
}

SiteConfigSchema = Schema(
    And(
        Schema(SiteConfigSchemaObject, ignore_extra_keys=True),
        # Or(
        #     HasKey("certificat_folder"),
        #     And(
        #         HasKey("ssl_certificate"),
        #         HasKey("ssl_certificate_key"),
        #     )
        # )
    ),
    ignore_extra_keys=True,
)