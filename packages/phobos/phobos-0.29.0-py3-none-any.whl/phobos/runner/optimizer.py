from torch.optim import (Adadelta, Adagrad, Adam, AdamW,
                         SparseAdam, Adamax, ASGD, LBFGS,
                         RMSprop, Rprop, SGD)
import logging

optimizer_map = {
    'adadelta': Adadelta,
    'adagrad': Adagrad,
    'adam': Adam,
    'adamw': AdamW,
    'sparseadam': SparseAdam,
    'adamax': Adamax,
    'asgd': ASGD,
    'lbfgs': LBFGS,
    'rmsprop': RMSprop,
    'rprop': Rprop,
    'sgd': SGD
}


def get_optimizer(key, args, model):
    """Creates and returns a optimizer based on optimizer type and arguments.

    Parameters
    ----------
    key : string
        type of optimizer instance
    args : dict
        dictionary of optimizer parameters.
    model : torch.nn.Module
        model to train or validate.

    Returns
    -------
    torch.optim
        optimizer instance.

    """
    logging.debug("Enter get_optimizer routine")
    optimizer = optimizer_map[key]
    args['params'] = model.parameters()
    logging.debug("Exit get_optimizer routine")
    return optimizer(**args)

def set_optimizer(key, optimizer):
    """Allows: 

    1.Addition of a new optimizer to optimizer map
    2.Modification of existing optimizer definitions in optimizer map

    Parameters
    ----------
    key : string
        type of optimizer instance
    optimizer : torch.optim
        optimizer class
    """
    logging.debug("Enter set_optimizer routine")
    optimizer_map[key] = optimizer
    logging.debug("Exit set_optimizer routine")
