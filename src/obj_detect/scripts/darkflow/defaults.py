class argHandler(dict):
    
    # A class to check if all the input parameters are ok..if not then show error message or set to defaults
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    _descriptions = {'help, --h, -h': 'show this super helpful message and exit'}
    
    # Setting the default values
    def setDefaults(self):
        self.define('labels', 'labels.txt', 'path to labels file')
        self.define('binary', './bin/', 'path to .weights directory')
        self.define('backup', './ckpt/', 'path to backup folder')
        self.define('summary', '', 'path to TensorBoard summaries directory')
        self.define('threshold', 0.1, 'detection threshold')
        self.define('model', '', 'configuration of choice')
        self.define('load', '', 'how to initialize the net? Either from .weights or a checkpoint, or even from scratch')
        self.define('gpu', 0.0, 'how much gpu (from 0.0 to 1.0)')
        self.define('gpuName', '/gpu:0', 'GPU device name')
        self.define('demo', '', 'demo on webcam')
        self.define('queue', 1, 'process demo in batch')
        self.define('saveVideo', False, 'Records video from input video or camera')

    # Defining the arguments and their description
    def define(self, argName, default, description):
        self[argName] = default
        self._descriptions[argName] = description
    
    # Running the help
    def help(self):
        print('Example usage: flow --imgdir sample_img/ --model cfg/yolo.cfg --load bin/yolo.weights')
        print('')
        print('Arguments:')
        spacing = max([len(i) for i in self._descriptions.keys()]) + 2
        for item in self._descriptions:
            currentSpacing = spacing - len(item)
            print('  --' + item + (' ' * currentSpacing) + self._descriptions[item])
        print('')
        exit()

    # Checking if all the input parameters are ok! 
    def parseArgs(self, args):
        print('')
        i = 1
        while i < len(args):
            if args[i] == '-h' or args[i] == '--h' or args[i] == '--help':
                self.help() #Help dialogue  :)
            if len(args[i]) < 2:
                print('ERROR - Invalid argument: ' + args[i])
                print('Try running flow --help')
                exit()
            argumentName = args[i][2:]
            if isinstance(self.get(argumentName), bool):
                if not (i + 1) >= len(args) and (args[i + 1].lower() != 'false' and args[i + 1].lower() != 'true') and not args[i + 1].startswith('--'):
                    print('ERROR - Expected boolean value (or no value) following argument: ' + args[i])
                    print('Try running flow --help')
                    exit()
                elif not (i + 1) >= len(args) and (args[i + 1].lower() == 'false' or args[i + 1].lower() == 'true'):
                    self[argumentName] = (args[i + 1].lower() == 'true')
                    i += 1
                else:
                    self[argumentName] = True
            elif args[i].startswith('--') and not (i + 1) >= len(args) and not args[i + 1].startswith('--') and argumentName in self:
                if isinstance(self[argumentName], float):
                    try:
                        args[i + 1] = float(args[i + 1])
                    except:
                        print('ERROR - Expected float for argument: ' + args[i])
                        print('Try running flow --help')
                        exit()
                elif isinstance(self[argumentName], int):
                    try:
                        args[i + 1] = int(args[i + 1])
                    except:
                        print('ERROR - Expected int for argument: ' + args[i])
                        print('Try running flow --help')
                        exit()
                self[argumentName] = args[i + 1]
                i += 1
            else:
                print('ERROR - Invalid argument: ' + args[i])
                print('Try running flow --help')
                exit()
            i += 1
