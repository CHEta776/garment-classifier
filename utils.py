import os
import shutil


def create_results_folder(results_folder='Results'):
    for folder in ['Test', 'Train']:
        if not os.path.exists(os.path.join(results_folder, folder)):
            os.makedirs(os.path.join(results_folder, folder))
    return results_folder


def create_folder(folder):
    if os.path.exists(folder):
        delete_old_logs(folder)
        os.makedirs(folder)
    return folder


def delete_old_logs(logdir):
    try:
        shutil.rmtree(logdir)
    except:
        return


def get_files(base_dir):
    files = [os.path.join(base_dir, file) for file in os.listdir(base_dir)]
    return files


label_dict = {
 0: 'T-shirt/top',
 1: 'Trouser',
 2: 'Pullover',
 3: 'Dress',
 4: 'Coat',
 5: 'Sandal',
 6: 'Shirt',
 7: 'Sneaker',
 8: 'Bag',
 9: 'Ankle boot'
}
