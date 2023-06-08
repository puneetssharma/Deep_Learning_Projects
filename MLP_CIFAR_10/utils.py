{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def grab_data(data_dir, num_cpus=1):\n",
    "    \"\"\"Downloads CIFAR10 train and test set, stores them on disk, computes mean \n",
    "        and standard deviation per channel of trainset, normalizes the train set\n",
    "        accordingly.\n",
    "\n",
    "    Args:\n",
    "        data_dir (str): Directory to store data\n",
    "        num_cpus (int, optional): Number of cpus that should be used to \n",
    "            preprocess data. Defaults to 1.\n",
    "\n",
    "    Returns:\n",
    "        CIFAR10, CIFAR10, float, float: Returns trainset and testset as\n",
    "            torchvision CIFAR10 dataset objects. Returns mean and standard\n",
    "            deviation used for normalization.\n",
    "    \"\"\"\n",
    "    trainset = torchvision.datasets.CIFAR10(data_dir, train=True, download=True, \n",
    "                                            transform=torchvision.transforms.ToTensor())\n",
    "\n",
    "    # Get normalization transform\n",
    "    num_samples = trainset.data.shape[0]\n",
    "    trainloader = torch.utils.data.DataLoader(trainset, batch_size=num_samples, \n",
    "                                              num_workers=num_cpus)\n",
    "    imgs, _ = next(iter(trainloader))\n",
    "    dataset_mean = torch.mean(imgs, dim=(0,2,3))\n",
    "    dataset_std = torch.std(imgs, dim=(0,2,3))\n",
    "\n",
    "    normalized_transform = torchvision.transforms.Compose([\n",
    "        torchvision.transforms.ToTensor(),\n",
    "        torchvision.transforms.Normalize(dataset_mean, dataset_std)\n",
    "    ])\n",
    "\n",
    "    # Load again, now normalized\n",
    "    trainset = torchvision.datasets.CIFAR10(data_dir, download=True, train=True, \n",
    "                                            transform=normalized_transform) \n",
    "    # Apply the same transform, computed from the train-set, to the test-set\n",
    "    # so both have a similar distribution. We do not normalize the test-set directly,\n",
    "    # since we are not allowed to perform any computations with it. (We only use it\n",
    "    # for reporting results in the very end)\n",
    "    testset = torchvision.datasets.CIFAR10(data_dir, download=True, train=False, \n",
    "                                           transform=normalized_transform)\n",
    "\n",
    "    return trainset, testset, dataset_mean, dataset_std\n",
    "        \n",
    "        \n",
    "def generate_train_val_data_split(trainset, split_seed=42, val_frac=0.2):\n",
    "    \"\"\"Splits train dataset into train and validation dataset.\n",
    "\n",
    "    Args:\n",
    "        trainset (CIFAR10): CIFAR10 trainset object\n",
    "        split_seed (int, optional): Seed used to randomly assign data\n",
    "            points to the validation set. Defaults to 42.\n",
    "        val_frac (float, optional): Fraction of training set that should be \n",
    "            split into validation set. Defaults to 0.2.\n",
    "\n",
    "    Returns:\n",
    "        CIFAR10, CIFAR10: CIFAR10 trainset and validation set.\n",
    "    \"\"\"\n",
    "    num_val_samples = np.ceil(val_frac * trainset.data.shape[0]).astype(int)\n",
    "    num_train_samples = trainset.data.shape[0] - num_val_samples\n",
    "    trainset, valset = torch.utils.data.random_split(trainset, \n",
    "                                  (num_train_samples, num_val_samples), \n",
    "                                  generator=torch.Generator().manual_seed(split_seed))\n",
    "    return trainset, valset\n",
    "    \n",
    "    \n",
    "def init_data_loaders(trainset, valset, testset, batch_size=1024, num_cpus=1):\n",
    "    \"\"\"Initialize train, validation and test data loader.\n",
    "\n",
    "    Args:\n",
    "        trainset (CIFAR10): Training set torchvision dataset object.\n",
    "        valset (CIFAR10): Validation set torchvision dataset object.\n",
    "        testset (CIFAR10): Test set torchvision dataset object.\n",
    "        batch_size (int, optional): Batchsize that should be generated by \n",
    "            pytorch dataloader object. Defaults to 1024.\n",
    "        num_cpus (int, optional): Number of CPUs to use when iterating over\n",
    "            the data loader. More is faster. Defaults to 1.\n",
    "\n",
    "    Returns:\n",
    "        DataLoader, DataLoader, DataLoader: Returns pytorch DataLoader objects\n",
    "            for training, validation and testing.\n",
    "    \"\"\"        \n",
    "    trainloader = torch.utils.data.DataLoader(trainset,\n",
    "                                                   batch_size=batch_size,\n",
    "                                                   shuffle=True,\n",
    "                                                   num_workers=num_cpus)\n",
    "    valloader = torch.utils.data.DataLoader(valset, \n",
    "                                                 batch_size=batch_size,\n",
    "                                                 shuffle=True,\n",
    "                                                 num_workers=num_cpus)\n",
    "    testloader = torch.utils.data.DataLoader(testset,\n",
    "                                                  batch_size=batch_size,\n",
    "                                                  shuffle=True, \n",
    "                                                  num_workers=num_cpus)\n",
    "    return trainloader, valloader, testloader"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
