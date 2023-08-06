from localstack.utils.aws import aws_models
qQSPo=super
qQSPH=None
qQSPK=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  qQSPo(LambdaLayer,self).__init__(arn)
  self.cwd=qQSPH
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.qQSPK.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,qQSPK,env=qQSPH):
  qQSPo(RDSDatabase,self).__init__(qQSPK,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,qQSPK,env=qQSPH):
  qQSPo(RDSCluster,self).__init__(qQSPK,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,qQSPK,env=qQSPH):
  qQSPo(AppSyncAPI,self).__init__(qQSPK,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,qQSPK,env=qQSPH):
  qQSPo(AmplifyApp,self).__init__(qQSPK,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,qQSPK,env=qQSPH):
  qQSPo(ElastiCacheCluster,self).__init__(qQSPK,env=env)
class TransferServer(BaseComponent):
 def __init__(self,qQSPK,env=qQSPH):
  qQSPo(TransferServer,self).__init__(qQSPK,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,qQSPK,env=qQSPH):
  qQSPo(CloudFrontDistribution,self).__init__(qQSPK,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,qQSPK,env=qQSPH):
  qQSPo(CodeCommitRepository,self).__init__(qQSPK,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
