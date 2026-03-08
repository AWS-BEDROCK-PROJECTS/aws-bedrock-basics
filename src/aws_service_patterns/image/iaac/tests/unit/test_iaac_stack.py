import aws_cdk as core
import aws_cdk.assertions as assertions

from iaac.iaac_stack import IaacStack

# example tests. To run these tests, uncomment this file along with the example
# resource in iaac/iaac_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = IaacStack(app, "iaac")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
