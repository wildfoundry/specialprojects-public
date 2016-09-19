import subprocess
import shlex
from nbstreamreader import NonBlockingStreamReader as NBSR


class Terminal():

    def __init__(self):
        self.term_started = False
        self.proc = None
        self.nbsr = None

    def start_terminal(self):
        """
        Starts /bin/sh
        """
        self.proc = subprocess.Popen(["/bin/sh"],
                                     shell=False,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        self.nbsr = NBSR(self.proc.stdout)
        self.nbsr_err = NBSR(self.proc.stderr)
        self.term_started = True

    def execute_command(self, input_cmd):
        """
        Executes anything passed to /bin/sh
        """
        output_collector = []
        err_collector = None

        # Format the command
        try:
            args_list = shlex.split(input_cmd)
        except:
            args_list = ["echo","There was an error... your command was not executed..."]
        args_str = " ".join(i for i in args_list)
        args_str += "\n"

        # If command is "exit" shut down the terminal
        if args_str == "exit\n":
            self.term_started = False
            self.proc.terminate()
            return "<<< Term mode: Finished >>>"

        # Write the command
        self.proc.stdin.write(args_str)

        # Parse output
        while True:
            output = self.nbsr.readline(0.1)
            err_collector = self.nbsr_err.readline(0.1)

            if err_collector:
                print("ERROR executing command: " + err_collector)
                return err_collector

            if not output:
                break
            output_collector.append(output)

        # Format output
        response = "".join(i for i in output_collector)

        return response
