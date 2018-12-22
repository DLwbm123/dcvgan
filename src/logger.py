import time
from pathlib import Path

from tensorboardX import SummaryWriter

class Logger(object):
    def __init__(self, log_folder, tensorboard_dir, \
                       log_interval, epoch_iters):
        self.metrics ={
            "epoch": 0,
            "iteration": 1,
            "loss_gen": 0.,
            "loss_idis": 0.,
            "loss_vdis": 0.,
            "elapsed_time": 0,
        }
        
        self.log_interval = log_interval
        self.epoch_iters = epoch_iters
        
        self.writer = SummaryWriter(str(tensorboard_dir))
        
        self.start_time = time.time()
        self.display_metric_names()

    def update(self, name, value):
        self.metrics[name] = value

    def display_metric_names(self):
        for name in self.metrics.keys():
            print("{:>12} ".format(name), end="")
        print("")

    def print_log(self):
        self.metrics["elapsed_time"] = time.time() - self.start_time

        metric_strings = []
        for name, value in self.metrics.items():
            if name in ["epoch", "iteration"]:
                s = "{}".format(value)
            elif name in ["loss_gen", "loss_idis", "loss_vdis"]:
                s = "{:0.3f}".format(value)
            elif name in ["elapsed_time"]:
                value = int(value)
                s = "{:02d}:{:02d}:{:02d}".format(value//3600, value//60, value%60)
            else:
                raise Exception("Unsupported mertic is added")

            metric_strings.append(s)
        
        for s in metric_strings:
            print("{:>12} ".format(s), end="")
        print("")

    def log_metrics(self):
        step = self.metrics["iteration"]
        for name in ["loss_gen", "loss_idis", "loss_vdis"]:
            value = self.metrics[name]
            self.writer.add_scalar(name, value, step)

    def log_video(self, name, videos, step):
        self.writer.add_video(name, videos, fps=8, global_step=step)

    def log_histgram(self, var, tag, step):
        var = var.clone().cpu().data.numpy()
        self.writer.add_histogram(tag, var, step)

    def next_iter(self):
        # hook
        if self.metrics["iteration"] % self.log_interval == 0:
            self.print_log()
            self.log_metrics()
        
        # update iteration
        self.metrics['iteration'] += 1
        if self.metrics['iteration'] % self.epoch_iters == 0:
            self.metrics["epoch"] += 1

if __name__=="__main__":
    l = Logger(None, None, [1,2,3])
    time.sleep(3)
    l.print_log()
