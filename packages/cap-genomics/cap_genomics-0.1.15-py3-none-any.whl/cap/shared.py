from munch import Munch

Shared = Munch()

Shared.data = Munch()

Shared.logFile = 'NoLogFile'

Shared.fileSystem = None

Shared.vepCheckWaitTime = 5

Shared.CurrentStageForLogging = None
Shared.CurrentFunctionForLogging = list()

Shared.numPartitions = Munch()
Shared.numPartitions.default = 4
Shared.numPartitions.min = 1
Shared.numPartitions.max = 32  

Shared.numSgeJobs = Munch()
Shared.numSgeJobs.default = 4
Shared.numSgeJobs.min = 1
Shared.numSgeJobs.max = 32