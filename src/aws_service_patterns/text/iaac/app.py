#!/usr/bin/env python3
import os

import aws_cdk as cdk

from iaac.iaac_stack import IaacStack


app = cdk.App()
IaacStack(app, "IaacStackSummary")

app.synth()
