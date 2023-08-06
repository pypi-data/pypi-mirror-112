import click
from fastapi import FastAPI  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore

import c3loc.api2.alarms as alarms
import c3loc.api2.groups as groups
import c3loc.api2.listeners as listeners
import c3loc.api2.proximity as proximity
import c3loc.api2.sensors as sensors
import c3loc.api2.tags as tags
import c3loc.api2.zones as zones

app = FastAPI()
app.include_router(alarms.router)
app.include_router(groups.router)
app.include_router(listeners.router)
app.include_router(proximity.router)
app.include_router(sensors.router)
app.include_router(tags.router)
app.include_router(zones.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@click.command()
@click.option('--port', '-p', default=8000)
def main(port: int) -> None:
    import uvicorn  # type: ignore  # nocov
    uvicorn.run(app, host="0.0.0.0", port=port)  # nosec  # nocov


if __name__ == '__main__':  # nocov
    main()
