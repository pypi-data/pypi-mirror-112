from localstack.utils.aws import aws_models
mhNDa=super
mhNDn=None
mhNDR=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  mhNDa(LambdaLayer,self).__init__(arn)
  self.cwd=mhNDn
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.mhNDR.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,mhNDR,env=mhNDn):
  mhNDa(RDSDatabase,self).__init__(mhNDR,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,mhNDR,env=mhNDn):
  mhNDa(RDSCluster,self).__init__(mhNDR,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,mhNDR,env=mhNDn):
  mhNDa(AppSyncAPI,self).__init__(mhNDR,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,mhNDR,env=mhNDn):
  mhNDa(AmplifyApp,self).__init__(mhNDR,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,mhNDR,env=mhNDn):
  mhNDa(ElastiCacheCluster,self).__init__(mhNDR,env=env)
class TransferServer(BaseComponent):
 def __init__(self,mhNDR,env=mhNDn):
  mhNDa(TransferServer,self).__init__(mhNDR,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,mhNDR,env=mhNDn):
  mhNDa(CloudFrontDistribution,self).__init__(mhNDR,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,mhNDR,env=mhNDn):
  mhNDa(CodeCommitRepository,self).__init__(mhNDR,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
