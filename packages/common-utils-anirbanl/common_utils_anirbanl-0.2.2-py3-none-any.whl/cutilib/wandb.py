import wandb
from ..cutipy.designpatterns import singleton

@singleton
class Wandb:

    def __init__(self, key, entity, **kwargs):
        self.api_key = key
        wandb.login(key=self.api_key)

        self.job_type = None  # The type of job running
        self.dir = kwargs.get('dir')  # An absolute path to a directory where metadata will be stored
        # abspath to logdir
        self.config = kwargs.get('config') or dict()  # The hyper parameters to store with the run
        self.project = kwargs.get('project')  # The project to push metrics to
        self.entity = entity  # The entity to push metrics to
        self.tags = None  # A list of tags to apply to the run
        self.group = None  # A unique string shared by all runs in a given group
        self.resume = None  # True, the run auto resumes
        self.force = True  # Force authentication with wandb
        self.name = kwargs.get('name')  # A display name which does not have to be unique
        self.notes = None,  # A multiline string associated with the run
        self.id = None,  # A globally unique (per project) identifier for the run
        self.anonymous = None  # Controls whether anonymous logging is allowed.
        self.save_code = False # Save main script to wandb
        self.tensorboard = None
        self.sync_tensorboard = None
        self.monitor_gym = None

        wandb.init(job_type=self.job_type,
                   dir=self.dir,
                   config=self.config,
                   project=self.project,
                   entity=self.entity,
                   tags=self.tags,
                   group=self.group,
                   resume=self.resume,
                   force=self.force,
                   name=self.name,
                   notes=self.notes,
                   id=self.id,
                   anonymous=self.anonymous,
                   tensorboard=self.tensorboard,
                   sync_tensorboard=self.sync_tensorboard,
                   monitor_gym=self.monitor_gym
        )

    def log(self, kwargs, step=None):
        wandb.log(kwargs, step=step)



