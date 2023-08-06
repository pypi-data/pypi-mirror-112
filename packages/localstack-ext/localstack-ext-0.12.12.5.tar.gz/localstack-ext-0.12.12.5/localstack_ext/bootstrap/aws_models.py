from localstack.utils.aws import aws_models
AtHaI=super
AtHaJ=None
AtHav=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  AtHaI(LambdaLayer,self).__init__(arn)
  self.cwd=AtHaJ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.AtHav.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,AtHav,env=AtHaJ):
  AtHaI(RDSDatabase,self).__init__(AtHav,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,AtHav,env=AtHaJ):
  AtHaI(RDSCluster,self).__init__(AtHav,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,AtHav,env=AtHaJ):
  AtHaI(AppSyncAPI,self).__init__(AtHav,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,AtHav,env=AtHaJ):
  AtHaI(AmplifyApp,self).__init__(AtHav,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,AtHav,env=AtHaJ):
  AtHaI(ElastiCacheCluster,self).__init__(AtHav,env=env)
class TransferServer(BaseComponent):
 def __init__(self,AtHav,env=AtHaJ):
  AtHaI(TransferServer,self).__init__(AtHav,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,AtHav,env=AtHaJ):
  AtHaI(CloudFrontDistribution,self).__init__(AtHav,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,AtHav,env=AtHaJ):
  AtHaI(CodeCommitRepository,self).__init__(AtHav,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
