# Bu dosya, görev ilerlemesini saklamak, güncellemek ve silmek için basit bir bellek içi depo sağlar.
# Her video işleme veya benzeri uzun süren görev için ilerleme durumu takip edilir.

progress_store = {}

def update_progress(task_id, update):
    progress_store[task_id] = update

def get_progress(task_id):
    return progress_store.get(task_id, None)

def delete_progress(task_id):
    if task_id in progress_store:
        del progress_store[task_id]
