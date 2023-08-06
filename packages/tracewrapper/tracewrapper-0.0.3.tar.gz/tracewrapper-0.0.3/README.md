# Tracewrapper
Wrapper for Pythons sys.settrace

Allows you to run multiple traces at once and also allows you to queue up a class instead of the default show_trace() function.  Also allows you to filter events, modules and functions.

## To Install:
    pip3 install tracewrapper
    
    or
    
    python -m pip install tracewrapper

## Example:
    from tracewrapper import tracewrapper
    import opcode

    #Show_Trace function just like you'd feed to sys.settrace()
    def show_trace1(frame, event, arg):
        code = frame.f_code
        offset = frame.f_lasti
        print(f"Trace1| {event:10} | {str(arg):>4} |", end=' ')
        print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
        print(f"{opcode.opname[code.co_code[offset]]:<18} | {str(frame.f_locals):<35} |")
        return show_trace1

    #Another Show_Trace function just like you'd feed to sys.settrace()
    def show_trace2(frame, event, arg):
        code = frame.f_code
        offset = frame.f_lasti
        print(f"Trace2| {event:10} | {str(arg):>4} |", end=' ')
        print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
        print(f"{opcode.opname[code.co_code[offset]]:<18} | {str(frame.f_locals):<35} |")
        return show_trace2

    #Show_Trace as a class
    class TClass(tracewrapper.TracerClass):
        def trace(self, frame, event, arg):
            code = frame.f_code
            offset = frame.f_lasti
            print(f"Trace3| {event:10} | {str(arg):>4} |", end=' ')
            print(f"{frame.f_lineno:>4} | {frame.f_lasti:>6} |", end=' ')
            print(f"{opcode.opname[code.co_code[offset]]:<18} | {str(frame.f_locals):<35} |")
            return self

    #Demo fibanaci function to trace
    def fib(n):
        i, f1, f2 = 1, 1, 1
        while i < n:
            f1, f2 = f2, f1 + f2
            i += 1
        return f1

    #Instanciate the tracewrapper() class
    tracer=tracewrapper.tracewrapper()

    #Add our two demo show_trace functions
    tracer.add(show_trace1)
    tracer.add(show_trace2)

    #Instanciate TClass() our inherited TracerClass()
    tc=TClass()

    #Add TracerClass's trace method to Tracer
    tracer.add(tc.trace)

    #Activate it
    tc.start()

    #Start tracing
    tracer.start()

    #Call our demo function
    fib(6)

    #Stop Tracing
    tracer.stop()
