from localstack.utils.aws import aws_models
XSlxL=super
XSlxk=None
XSlxi=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  XSlxL(LambdaLayer,self).__init__(arn)
  self.cwd=XSlxk
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.XSlxi.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,XSlxi,env=XSlxk):
  XSlxL(RDSDatabase,self).__init__(XSlxi,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,XSlxi,env=XSlxk):
  XSlxL(RDSCluster,self).__init__(XSlxi,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,XSlxi,env=XSlxk):
  XSlxL(AppSyncAPI,self).__init__(XSlxi,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,XSlxi,env=XSlxk):
  XSlxL(AmplifyApp,self).__init__(XSlxi,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,XSlxi,env=XSlxk):
  XSlxL(ElastiCacheCluster,self).__init__(XSlxi,env=env)
class TransferServer(BaseComponent):
 def __init__(self,XSlxi,env=XSlxk):
  XSlxL(TransferServer,self).__init__(XSlxi,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,XSlxi,env=XSlxk):
  XSlxL(CloudFrontDistribution,self).__init__(XSlxi,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,XSlxi,env=XSlxk):
  XSlxL(CodeCommitRepository,self).__init__(XSlxi,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
