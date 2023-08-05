# Copyright (c) Dietmar Wolz.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory.

# See http://www.midaco-solver.com/data/pub/CEC2019_Schlueter_Munetomo.pdf for a description of the
# MINLP problem solved here. 
# Used to generate the results in https://github.com/dietmarwo/fast-cma-es/blob/master/MINLP.adoc

from fcmaes.astro import Cassini1minlp, Cassini1multi
from fcmaes.optimizer import logger, de_cma
from fcmaes import advretry, multiretry

# minlp approach, planet sequence is additional arguments
def test_optimizer(opt, problem, num_retries = 120000, num = 100, value_limit = 10.0, log = logger()):
    log.info(problem.name + ' ' + opt.name)
    for _ in range(num):
        ret = advretry.minimize(problem.fun, problem.bounds, value_limit, 
                                num_retries, log, optimizer=opt)

def sequences():
    for p1 in range(1,4):
        for p2 in range(1,4):
            for p3 in range(1,4):
                for p4 in range(3,6):
                    yield[p1,p2,p3,p4]

# simultaneous optimization 
def test_multiretry(num_retries = 128, 
             keep = 0.7, optimizer = de_cma(1500), logger = logger(), repeat = 50):
    problems = []
    ids = []
    for seq in sequences():
        problems.append(Cassini1multi(planets = seq))
        ids.append(str(seq))
    for _ in range(100):
        problem_stats = multiretry.minimize(problems, ids, num_retries, keep, optimizer, logger)
        ps = problem_stats[0]
        for _ in range(repeat):
            logger.info("problem " + ps.prob.name + ' ' + str(ps.id))
            ps.retry(optimizer)

def main():
    test_optimizer(de_cma(1500), Cassini1minlp()) 
#     test_multiretry(repeat = 50)
    
if __name__ == '__main__':
    main()
    