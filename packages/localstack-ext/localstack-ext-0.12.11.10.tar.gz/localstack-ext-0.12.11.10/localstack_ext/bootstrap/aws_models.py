from localstack.utils.aws import aws_models
EwmiR=super
EwmiP=None
EwmiY=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EwmiR(LambdaLayer,self).__init__(arn)
  self.cwd=EwmiP
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.EwmiY.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,EwmiY,env=EwmiP):
  EwmiR(RDSDatabase,self).__init__(EwmiY,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,EwmiY,env=EwmiP):
  EwmiR(RDSCluster,self).__init__(EwmiY,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,EwmiY,env=EwmiP):
  EwmiR(AppSyncAPI,self).__init__(EwmiY,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,EwmiY,env=EwmiP):
  EwmiR(AmplifyApp,self).__init__(EwmiY,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,EwmiY,env=EwmiP):
  EwmiR(ElastiCacheCluster,self).__init__(EwmiY,env=env)
class TransferServer(BaseComponent):
 def __init__(self,EwmiY,env=EwmiP):
  EwmiR(TransferServer,self).__init__(EwmiY,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,EwmiY,env=EwmiP):
  EwmiR(CloudFrontDistribution,self).__init__(EwmiY,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,EwmiY,env=EwmiP):
  EwmiR(CodeCommitRepository,self).__init__(EwmiY,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
