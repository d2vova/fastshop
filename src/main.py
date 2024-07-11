from fastapi import FastAPI
from sqladmin import Admin
from src.admin import register_admin_views
from src.authentication.views import router as auth_router
from src.base_settings import base_settings
from src.catalogue.views import product_router
from src.common.databases.postgres import postgres
from src.general.views import router as status_router
from src.routes import BaseRoutesPrefixes
from src.users.views import user_router
from src.users.views.user_address import user_address_router

def include_routes(application: FastAPI) -> None:
    application.include_router(
        router=status_router,
    )
    application.include_router(
        router=auth_router,
        prefix=BaseRoutesPrefixes.authentication,
        tags=['Authentication'],
    )
    application.include_router(
        router=product_router,
        prefix=BaseRoutesPrefixes.catalogue,
        tags=['Catalogue'],
    )
    application.include_router(
        router=user_router,
        prefix=BaseRoutesPrefixes.account,
        tags=['Account'],
    )
    application.include_router(
        router=user_address_router,
        prefix="/users",
        tags=['UserAddresses'],
    )

def get_application() -> FastAPI:
    application = FastAPI(
        debug=base_settings.debug,
        docs_url=BaseRoutesPrefixes.swagger if base_settings.debug else None,
        redoc_url=BaseRoutesPrefixes.redoc if base_settings.debug else None,
        openapi_url=BaseRoutesPrefixes.openapi if base_settings.debug else None,
    )

    @application.on_event('startup')
    def startup():
        postgres.connect(base_settings.postgres.url)
        engine = postgres.get_engine()
        admin = Admin(app=application, engine=engine)
        register_admin_views(admin)

    @application.on_event('shutdown')
    async def shutdown():
        await postgres.disconnect()

    include_routes(application)

    return application


app = get_application()
