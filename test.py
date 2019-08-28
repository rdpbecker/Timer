import State, commandio, userInput as user, config
from timeit import default_timer as timer

def main():
    state = State.State()
    
    commandio.sanitizeInput("Press enter to start the run")
    start = timer()
    state.startRun(timer())
    last = start
    
    for split in state.splitnames:
        if state.reset:
            break
    #    commandio.sanitizeInput("Press enter to split")
        user.waitWithInterrupt(1,last-start,state)
        end = timer()
        state.setFlags(config.skip,config.reset) 
        state.onSplitEnd(end,end-last)
        last = end
    
    state.doEnd()

if __name__ == "__main__":
    main()
