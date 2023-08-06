from setuptools import setup

name = "types-oauthlib"
description = "Typing stubs for oauthlib"
long_description = '''
## Typing stubs for oauthlib

This is a PEP 561 type stub package for the `oauthlib` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `oauthlib`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/oauthlib. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `80f61d220965cdfc5018c8dd6f82585c2af1b89d`.
'''.lstrip()

setup(name=name,
      version="3.1.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['oauthlib-stubs'],
      package_data={'oauthlib-stubs': ['uri_validate.pyi', 'common.pyi', '__init__.pyi', 'signals.pyi', 'oauth2/__init__.pyi', 'oauth2/rfc6749/tokens.pyi', 'oauth2/rfc6749/utils.pyi', 'oauth2/rfc6749/errors.pyi', 'oauth2/rfc6749/request_validator.pyi', 'oauth2/rfc6749/parameters.pyi', 'oauth2/rfc6749/__init__.pyi', 'oauth2/rfc6749/clients/web_application.pyi', 'oauth2/rfc6749/clients/legacy_application.pyi', 'oauth2/rfc6749/clients/mobile_application.pyi', 'oauth2/rfc6749/clients/backend_application.pyi', 'oauth2/rfc6749/clients/service_application.pyi', 'oauth2/rfc6749/clients/base.pyi', 'oauth2/rfc6749/clients/__init__.pyi', 'oauth2/rfc6749/endpoints/introspect.pyi', 'oauth2/rfc6749/endpoints/authorization.pyi', 'oauth2/rfc6749/endpoints/pre_configured.pyi', 'oauth2/rfc6749/endpoints/revocation.pyi', 'oauth2/rfc6749/endpoints/base.pyi', 'oauth2/rfc6749/endpoints/resource.pyi', 'oauth2/rfc6749/endpoints/metadata.pyi', 'oauth2/rfc6749/endpoints/token.pyi', 'oauth2/rfc6749/endpoints/__init__.pyi', 'oauth2/rfc6749/grant_types/authorization_code.pyi', 'oauth2/rfc6749/grant_types/base.pyi', 'oauth2/rfc6749/grant_types/refresh_token.pyi', 'oauth2/rfc6749/grant_types/client_credentials.pyi', 'oauth2/rfc6749/grant_types/implicit.pyi', 'oauth2/rfc6749/grant_types/__init__.pyi', 'oauth2/rfc6749/grant_types/resource_owner_password_credentials.pyi', 'openid/__init__.pyi', 'openid/connect/__init__.pyi', 'openid/connect/core/tokens.pyi', 'openid/connect/core/exceptions.pyi', 'openid/connect/core/request_validator.pyi', 'openid/connect/core/__init__.pyi', 'openid/connect/core/endpoints/pre_configured.pyi', 'openid/connect/core/endpoints/userinfo.pyi', 'openid/connect/core/endpoints/__init__.pyi', 'openid/connect/core/grant_types/hybrid.pyi', 'openid/connect/core/grant_types/dispatchers.pyi', 'openid/connect/core/grant_types/authorization_code.pyi', 'openid/connect/core/grant_types/base.pyi', 'openid/connect/core/grant_types/implicit.pyi', 'openid/connect/core/grant_types/__init__.pyi', 'oauth1/__init__.pyi', 'oauth1/rfc5849/utils.pyi', 'oauth1/rfc5849/signature.pyi', 'oauth1/rfc5849/errors.pyi', 'oauth1/rfc5849/request_validator.pyi', 'oauth1/rfc5849/parameters.pyi', 'oauth1/rfc5849/__init__.pyi', 'oauth1/rfc5849/endpoints/signature_only.pyi', 'oauth1/rfc5849/endpoints/authorization.pyi', 'oauth1/rfc5849/endpoints/pre_configured.pyi', 'oauth1/rfc5849/endpoints/base.pyi', 'oauth1/rfc5849/endpoints/resource.pyi', 'oauth1/rfc5849/endpoints/access_token.pyi', 'oauth1/rfc5849/endpoints/__init__.pyi', 'oauth1/rfc5849/endpoints/request_token.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
