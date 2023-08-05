from localstack.utils.aws import aws_models
qgyfx=super
qgyfk=None
qgyfG=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  qgyfx(LambdaLayer,self).__init__(arn)
  self.cwd=qgyfk
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.qgyfG.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,qgyfG,env=qgyfk):
  qgyfx(RDSDatabase,self).__init__(qgyfG,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,qgyfG,env=qgyfk):
  qgyfx(RDSCluster,self).__init__(qgyfG,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,qgyfG,env=qgyfk):
  qgyfx(AppSyncAPI,self).__init__(qgyfG,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,qgyfG,env=qgyfk):
  qgyfx(AmplifyApp,self).__init__(qgyfG,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,qgyfG,env=qgyfk):
  qgyfx(ElastiCacheCluster,self).__init__(qgyfG,env=env)
class TransferServer(BaseComponent):
 def __init__(self,qgyfG,env=qgyfk):
  qgyfx(TransferServer,self).__init__(qgyfG,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,qgyfG,env=qgyfk):
  qgyfx(CloudFrontDistribution,self).__init__(qgyfG,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,qgyfG,env=qgyfk):
  qgyfx(CodeCommitRepository,self).__init__(qgyfG,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
