# /*******************************************************************************
# *  Author : Xiao Wang
# *  Email  : wang3702@purdue.edu xiaowang20140001@gmail.com
# *******************************************************************************/
from ops.os_operation import mkdir
import os
from torchvision.datasets.utils import download_url, check_integrity
import sys
import pickle
import numpy as np

class CIFAR10(object):
    """`CIFAR10 <https://www.cs.toronto.edu/~kriz/cifar.html>`_ Dataset.
    Args:
        root (string): Root directory of dataset where directory
            ``cifar-10-batches-py`` exists or will be saved to if download is set to True.

        download ():  downloads the dataset from the internet and
            puts it in root directory
    """

    def __init__(self, save_path,execute=True):
        if execute:
            self.root=save_path
            self.download_init()
            #mkdir(save_path)
            #self.download()
            
            #self.final_path=os.path.join(save_path,'cifar10')
            self.final_path=os.path.join(save_path,'Wikiart_Load')
            mkdir(self.final_path)
            #generate npy files here
            self.train_path=os.path.join(self.final_path,'trainset')
            self.test_path = os.path.join(self.final_path, 'testset')
            mkdir(self.train_path)
            mkdir(self.test_path)
            if os.path.getsize(self.train_path)<1000000:
                self.Process_Dataset(self.train_list, self.train_path)
            if os.path.getsize(self.test_path)<1000000:
                self.Process_Dataset(self.test_list, self.test_path)

    def download_init(self):
        #self.base_folder = 'cifar-10-batches-py'
        self.base_folder = 'Wikiart_Download'
        #self.url = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
        self.url = "https://drive.google.com/drive/folders/1DFvUVgJcELu7X4xp60VPsgvUZIArvTl_/"
        self.filename = "train.pickle"
        self.filename1 = "test.pickle"
        #self.filename = "cifar-10-python.tar.gz"
        #self.tgz_md5 = 'c58f30108f718f92721af3b95e74349a'
        self.train_list = ['train.pickle']

        self.test_list = ['test.pickle']

    def download(self):
        import tarfile

        """
        if self._check_integrity():
            print('Files already downloaded and verified')
            return
        """

        root = self.root
        #Removed "self.tgz_md5" param from download_url command from Torch
        download_url(self.url, root, self.filename)
        download_url(self.url, root, self.filename1)


        """
        # extract file
        cwd = os.getcwd()
        tar = tarfile.open(os.path.join(root, self.filename), "r:gz")
        os.chdir(root)
        tar.extractall()
        tar.close()
        os.chdir(cwd)
        """

    """
    def _check_integrity(self):

        root = self.root
        for fentry in (self.train_list + self.test_list):
            filename, md5 = fentry[0], fentry[1]
            fpath = os.path.join(root, self.base_folder, filename)
            if not check_integrity(fpath, md5):
                return False
        return True
    """

    def Process_Dataset(self,train_list,train_path):
        entry = []
        train_data = []
        train_labels=[]
        for fentry in train_list:
            #Previously it was 'f = fentry[0]'
            f = fentry
            file = os.path.join(self.root, self.base_folder, f)
            with open(file, "rb") as fo:
                entry = pickle.load(fo, encoding='latin1')
                #print(entry)
                train_data.append(entry['data'])
                print(len(train_data))
                #print('Data: {}{}'.format(train_list, train_data[0]))
                train_labels += entry['labels']
                #print(train_labels[0])
                #print("break")
                #print(train_labels)

                #if 'labels' in entry:
                """
                if 'labels' in entry:
                    train_labels += entry['labels']
                else:
                    train_labels += entry['fine_labels']
                """
                
                  
        train_data = np.concatenate(train_data)
        #train_data = np.array(train_data)
        train_data = train_data.reshape((len(train_data), 3, 384, 384)) #need to change the dimensions later
        train_labels=np.array(train_labels)
        #following Channel,height,width format
        #self.train_data = self.train_data.transpose((0, 2, 3, 1))  # convert to HWC
        tmp_train_path=os.path.join(train_path,'trainset', '.npy')
        np.save(tmp_train_path,train_data)
        for i in range(len(train_data)):
            tmp_train_path=os.path.join(train_path,'trainset'+str(i)+'.npy')
            tmp_aim_path = os.path.join(train_path, 'aimset' + str(i) + '.npy')
            np.save(tmp_train_path,train_data[i])
            np.save(tmp_aim_path,train_labels[i])
            
class CIFAR100(CIFAR10):
    """`CIFAR100 <https://www.cs.toronto.edu/~kriz/cifar.html>`_ Dataset.

    This is a subclass of the `CIFAR10` Dataset.
    """

    def __init__(self, save_path):
        super(CIFAR10, self).__init__()
        self.root=save_path
        self.download_init()
        if not self._check_integrity():
            mkdir(save_path)
            self.download()
        self.final_path=os.path.join(save_path,'cifar100')
        mkdir(self.final_path)
        #generate npy files here
        self.train_path=os.path.join(self.final_path,'trainset')
        self.test_path = os.path.join(self.final_path, 'testset')
        mkdir(self.train_path)
        mkdir(self.test_path)
        if os.path.getsize(self.train_path)<10000:
            self.Process_Dataset(self.train_list,self.train_path)
        if os.path.getsize(self.test_path)<10000:
            self.Process_Dataset(self.test_list,self.test_path)
    def download_init(self):
        self.base_folder = 'cifar-100-python'
        self.url = "https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz"
        self.filename = "cifar-100-python.tar.gz"
        self.tgz_md5 = 'eb9058c3a382ffc7106e4002c42a8d85'
        self.train_list = [
            ['train', '16019d7e3df5f24257cddd939b257f8d'],
        ]

        self.test_list = [
            ['test', 'f0ef6b0ae62326f3e7ffdfab6717acfc'],
        ]
        self.meta = {
            'filename': 'meta',
            'key': 'fine_label_names',
            'md5': '7973b15100ade9c7d40fb424638fde48',
        }