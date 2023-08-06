from localstack.utils.aws import aws_models
TaSjC=super
TaSjV=None
TaSjw=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  TaSjC(LambdaLayer,self).__init__(arn)
  self.cwd=TaSjV
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.TaSjw.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,TaSjw,env=TaSjV):
  TaSjC(RDSDatabase,self).__init__(TaSjw,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,TaSjw,env=TaSjV):
  TaSjC(RDSCluster,self).__init__(TaSjw,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,TaSjw,env=TaSjV):
  TaSjC(AppSyncAPI,self).__init__(TaSjw,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,TaSjw,env=TaSjV):
  TaSjC(AmplifyApp,self).__init__(TaSjw,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,TaSjw,env=TaSjV):
  TaSjC(ElastiCacheCluster,self).__init__(TaSjw,env=env)
class TransferServer(BaseComponent):
 def __init__(self,TaSjw,env=TaSjV):
  TaSjC(TransferServer,self).__init__(TaSjw,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,TaSjw,env=TaSjV):
  TaSjC(CloudFrontDistribution,self).__init__(TaSjw,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,TaSjw,env=TaSjV):
  TaSjC(CodeCommitRepository,self).__init__(TaSjw,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
