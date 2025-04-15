#!/usr/bin/env python3
from aws_cdk import App
from infrastructure.database import DatabaseStack

app = App()
DatabaseStack(app, "SongDatabaseStack")
app.synth() 