from torch.optim.lr_scheduler import (MultiplicativeLR, StepLR,
                                      LambdaLR, MultiStepLR, ExponentialLR,
                                      ReduceLROnPlateau, CyclicLR,
                                      OneCycleLR, CosineAnnealingWarmRestarts)

import logging

scheduler_map = {
    'multiplicative': MultiplicativeLR,
    'step': StepLR,
    'lmbda': LambdaLR,
    'multistep': MultiStepLR,
    'exponential': ExponentialLR,
    'plateau': ReduceLROnPlateau,
    'cyclic': CyclicLR,
    'one_cycle': OneCycleLR,
    'cos_anneal': CosineAnnealingWarmRestarts
}


def get_scheduler(key, args, optimizer):
    """Creates and returns a scheduler based on scheduler type and arguments.

    Parameters
    ----------
    key : string
        type of scheduler instance
    args : dict
        dictionary of scheduler parameters.
    optimizer : torch.optim
        optimizer instance.

    Returns
    -------
    torch.optim.lr_scheduler
        scheduler instance.

    """
    logging.debug("Enter get_scheduler routine")
    scheduler = scheduler_map[key]
    args['optimizer'] = optimizer
    logging.debug("Exit get_scheduler routine")
    return scheduler(**args)

def set_scheduler(key, scheduler):
    """Allows: 

    1.Addition of a new scheduler to scheduler map
    2.Modification of existing scheduler definitions in scheduler map

    Parameters
    ----------
    key : string
        type of scheduler instance
    scheduler : torch.optim
        scheduler class
    """
    logging.debug("Enter set_scheduler routine")
    scheduler_map[key] = scheduler
    logging.debug("Exit set_scheduler routine")
