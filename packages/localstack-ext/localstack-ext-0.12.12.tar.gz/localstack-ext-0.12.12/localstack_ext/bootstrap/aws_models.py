from localstack.utils.aws import aws_models
zGfRj=super
zGfRu=None
zGfRa=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  zGfRj(LambdaLayer,self).__init__(arn)
  self.cwd=zGfRu
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.zGfRa.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,zGfRa,env=zGfRu):
  zGfRj(RDSDatabase,self).__init__(zGfRa,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,zGfRa,env=zGfRu):
  zGfRj(RDSCluster,self).__init__(zGfRa,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,zGfRa,env=zGfRu):
  zGfRj(AppSyncAPI,self).__init__(zGfRa,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,zGfRa,env=zGfRu):
  zGfRj(AmplifyApp,self).__init__(zGfRa,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,zGfRa,env=zGfRu):
  zGfRj(ElastiCacheCluster,self).__init__(zGfRa,env=env)
class TransferServer(BaseComponent):
 def __init__(self,zGfRa,env=zGfRu):
  zGfRj(TransferServer,self).__init__(zGfRa,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,zGfRa,env=zGfRu):
  zGfRj(CloudFrontDistribution,self).__init__(zGfRa,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,zGfRa,env=zGfRu):
  zGfRj(CodeCommitRepository,self).__init__(zGfRa,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
