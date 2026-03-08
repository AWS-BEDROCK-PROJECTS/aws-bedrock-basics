from aws_cdk import (
    Duration,
    Stack,
    aws_apigateway,
    aws_lambda,
    aws_iam
)
from constructs import Construct

class IaacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        summary_lambda = aws_lambda.Function(
            self,
            "SummaryTextLambda",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            code=aws_lambda.Code.from_asset("services"),
            handler="summary_lambda.handler",
            timeout=Duration.seconds(60)
        )

        summary_lambda.add_to_role_policy(aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            resources=["*"],
            actions=["bedrock:InvokeModel"]            
        ))

        api = aws_apigateway.RestApi(self, "SummaryTextApi")

        text_resource = api.root.add_resource("text")
        summary_integration = aws_apigateway.LambdaIntegration(summary_lambda)
        text_resource.add_method("POST", summary_integration)
